import os
import re

from System.IO import *
from System.Text.RegularExpressions import *

from Deadline.Scripting import *
from Deadline.Plugins import *

from FranticX.Processes import *

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlinePlugin class.
######################################################################
def GetDeadlinePlugin():
    return LazyMachine()

def CleanupDeadlinePlugin( deadlinePlugin ):
    deadlinePlugin.Cleanup()

######################################################################
## This is the main DeadlinePlugin class for the CommandLine plugin.
######################################################################
class LazyMachine( DeadlinePlugin ):

    def __init__( self ):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderTasksCallback += self.RenderTasks
        self.ShProcess = None
    
    def Cleanup( self ):
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback

        del self.InitializeProcessCallback
        del self.RenderTasksCallback

        if self.ShProcess:
            self.ShProcess.Cleanup()
            del self.ShProcess
    
    def InitializeProcess( self ):
        self.SingleFramesOnly = self.GetBooleanPluginInfoEntryWithDefault( "SingleFramesOnly", False )
        self.LogInfo( "Single Frames Only: %s" % self.SingleFramesOnly )

        self.PluginType = PluginType.Advanced
        self.StdoutHandling = True

        self.AddStdoutHandlerCallback( ".*Progress: (\d+)%.*" ).HandleCallback += self.HandleProgress

    def RenderTasks( self ):
        executable = self.GetRenderExecutable()
        arguments = self.GetRenderArguments()
        startupDir = self.GetStartupDirectory()

        shellExecute = self.GetBooleanPluginInfoEntryWithDefault( "ShellExecute", False )
        self.LogInfo( "Execute in Shell: %s" % shellExecute )

        if not shellExecute:
            self.LogInfo( "Invoking: Run Process" )
            # StdOut/Err will NOT be captured here as unmanaged process
            exitCode = self.RunProcess( executable, arguments, startupDir, -1 )
        else:
            self.LogInfo( "Invoking: Managed Shell Process" )
            self.ShProcess = ShellManagedProcess( self, arguments, startupDir )
            self.RunManagedProcess( self.ShProcess )
            exitCode = self.ShProcess.ExitCode

        self.LogInfo( "Process returned: %s" % exitCode )

        if exitCode != 0:
            self.FailRender( "Process returned non-zero exit code '{}'".format( exitCode ) )

    def GetRenderExecutable( self ):
        executable = RepositoryUtils.CheckPathMapping( self.GetPluginInfoEntryWithDefault( "Executable", "" ).strip() )
        if executable != "":
            self.LogInfo( "Executable: %s" % executable )
        return executable
    
    def GetRenderArguments( self ):
        arguments = RepositoryUtils.CheckPathMapping( self.GetPluginInfoEntryWithDefault( "Arguments", "" ).strip() )

        arguments = re.sub( r"<(?i)STARTFRAME>", str( self.GetStartFrame() ), arguments )
        arguments = re.sub( r"<(?i)ENDFRAME>", str( self.GetEndFrame() ), arguments )
        arguments = re.sub( r"<(?i)QUOTE>", "\"", arguments)

        arguments = self.ReplacePaddedFrame( arguments, "<(?i)STARTFRAME%([0-9]+)>", self.GetStartFrame() )
        arguments = self.ReplacePaddedFrame( arguments, "<(?i)ENDFRAME%([0-9]+)>", self.GetEndFrame() )

        count = 0
        for filename in self.GetAuxiliaryFilenames():
            localAuxFile = Path.Combine( self.GetJobsDataDirectory(), filename )
            arguments = re.sub( r"<(?i)AUXFILE" + str( count ) + r">", localAuxFile.replace( "\\", "/" ), arguments )
            count += 1

        arguments = arguments.replace(u'\u201c', '"').replace(u'\u201d', '"')

        if arguments != "":
            self.LogInfo( "Arguments: %s" % arguments )
        
        return arguments

    def GetStartupDirectory( self ):
        startupDir = self.GetPluginInfoEntryWithDefault( "StartupDirectory", "" ).strip()
        if startupDir != "":
            self.LogInfo( "Startup Directory: %s" % startupDir )
        return startupDir
    
    def ReplacePaddedFrame( self, arguments, pattern, frame ):
        frameRegex = Regex( pattern )
        while True:
            frameMatch = frameRegex.Match( arguments )
            if frameMatch.Success:
                paddingSize = int( frameMatch.Groups[ 1 ].Value )
                if paddingSize > 0:
                    padding = StringUtils.ToZeroPaddedString( frame, paddingSize, False )
                else:
                    padding = str(frame)
                arguments = arguments.replace( frameMatch.Groups[ 0 ].Value, padding )
            else:
                break
        
        return arguments

    def HandleProgress( self ):
        progress = float( self.GetRegexMatch(1) )
        self.SetProgress( progress )

#################################################################################
## This is the shell managed process for running SHELL commands.
#################################################################################
class ShellManagedProcess( ManagedProcess ):
    '''
    This class provides a Deadline Managed Process using a pre-selected shell executable and provided command/arguments
    '''
    deadlinePlugin = None
    
    def __init__( self, deadlinePlugin, argument, directory ):
        self.deadlinePlugin = deadlinePlugin
        self.Argument = argument
        self.Directory = directory
        self.ExitCode = -1
        
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument
        self.StartupDirectoryCallback += self.StartupDirectory
        self.CheckExitCodeCallback += self.CheckExitCode

    def Cleanup( self ):
        for stdoutHandler in self.StdoutHandlers:
            del stdoutHandler.HandleCallback

        del self.InitializeProcessCallback
        del self.RenderExecutableCallback
        del self.RenderArgumentCallback
        del self.StartupDirectoryCallback
        del self.CheckExitCodeCallback
    
    def InitializeProcess( self ):
        self.PopupHandling = True
        self.StdoutHandling = True
        self.HideDosWindow = True
        # Ensure child processes are killed and the parent process is terminated on exit
        self.UseProcessTree = True
        self.TerminateOnExit = True

        self.ShellString = self.deadlinePlugin.GetPluginInfoEntryWithDefault( "Shell", "default" )
    
    def RenderExecutable( self ):
        shellExecutable = ""
        if self.ShellString == "default":
            # Grab the default shell executable from the User's environment.
            shellExecutable = os.environ.get( "SHELL", "/bin/sh" )
        else:
            # Search the list of potential paths for the shell executable.
            shellExeList = self.deadlinePlugin.GetConfigEntry( "ShellExecutable_" + self.ShellString )
            shellExecutable = FileUtils.SearchFileList( shellExeList )
        
        if( shellExecutable == "" ):
            self.deadlinePlugin.FailRender( self.ShellString + " shell executable was not found in the semicolon separated list \"" + shellExeList + "\". The path to the shell executable can be configured from the Plugin Configuration in the Deadline Monitor." )
        
        return shellExecutable

    def RenderArgument( self ):
        if self.ShellString == "cmd":
            return '/c "{}"'.format( self.Argument )
        else:
            escapedQuotes = self.Argument.replace( "'", "'\\''" )
            return "-c '{}'".format( escapedQuotes )

    def StartupDirectory( self ):
        return self.Directory

    def CheckExitCode( self, exitCode ):
        self.ExitCode = exitCode
