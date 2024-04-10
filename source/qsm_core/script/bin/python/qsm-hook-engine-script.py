# coding:utf-8
import sys


def main(argv):
    # run error in katana --script, no "__file__" argument
    # sys.stdout.write('execute qsm-hook-engine-script from: "{}"\n'.format(__file__))
    import lxsession.commands as ssn_commands; ssn_commands.execute_option_hook(argv[1])


if __name__ == '__main__':
    main(sys.argv)
