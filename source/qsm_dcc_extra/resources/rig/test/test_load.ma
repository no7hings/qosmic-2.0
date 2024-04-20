//Maya ASCII 2019 scene
//Name: test_load.ma
//Last modified: Wed, Apr 17, 2024 05:12:01 PM
//Codeset: 936
file -rdi 1 -ns "max" -rfn "maxRN" -op "VERS|2019|UVER|undef|MADE|undef|CHNG|Mon, Sep 11, 2023 11:15:34 AM|ICON|undef|INFO|undef|OBJN|127433|INCL|undef(|LUNI|cm|TUNI|pal|AUNI|deg|TDUR|141120000|"
		 -typ "mayaBinary" "E:/myworkspace/lynxi-root-2.0/packages/qsm_dcc_extra/resources/rig/max.mb";
file -rdi 1 -ns "sam" -rfn "samRN" -op "VERS|2019|UVER|undef|MADE|undef|CHNG|Mon, Sep 04, 2023 12:06:15 PM|ICON|undef|INFO|undef|OBJN|3850|INCL|undef(|LUNI|cm|TUNI|film|AUNI|deg|TDUR|141120000|"
		 -typ "mayaBinary" "E:/myworkspace/lynxi-root-2.0/packages/qsm_dcc_extra/resources/rig/sam.mb";
file -r -ns "max" -dr 1 -rfn "maxRN" -op "VERS|2019|UVER|undef|MADE|undef|CHNG|Mon, Sep 11, 2023 11:15:34 AM|ICON|undef|INFO|undef|OBJN|127433|INCL|undef(|LUNI|cm|TUNI|pal|AUNI|deg|TDUR|141120000|"
		 -typ "mayaBinary" "E:/myworkspace/lynxi-root-2.0/packages/qsm_dcc_extra/resources/rig/max.mb";
file -r -ns "sam" -dr 1 -rfn "samRN" -op "VERS|2019|UVER|undef|MADE|undef|CHNG|Mon, Sep 04, 2023 12:06:15 PM|ICON|undef|INFO|undef|OBJN|3850|INCL|undef(|LUNI|cm|TUNI|film|AUNI|deg|TDUR|141120000|"
		 -typ "mayaBinary" "E:/myworkspace/lynxi-root-2.0/packages/qsm_dcc_extra/resources/rig/sam.mb";
requires maya "2019";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2019";
fileInfo "version" "2019";
fileInfo "cutIdentifier" "201812112215-434d8d9c04";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 19045)\n";
createNode transform -s -n "persp";
	rename -uid "C203E03B-4033-C54F-F7FA-C18F8589B325";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1.7076712260625093 25.799200162025166 33.909136298788582 ;
	setAttr ".r" -type "double3" -29.738352729602362 -0.99999999999992761 -4.9703737017760705e-17 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "19472838-4F84-BA5D-9B52-508D5E84B604";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 46.144491277249884;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "0584CFCE-4C55-5D68-6220-228DF6C64433";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "DCF47FD4-449C-BB13-15D6-7B9642E30F95";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "59332A6A-45D5-07F6-D7A2-CE9E642369CC";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "8DA8E06D-4B5F-FAC0-97D5-F9A0704DC841";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "D6DD20D4-4C02-E383-BA45-F898A647D080";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "58F0E571-47B8-0925-CD5E-FEA6242134BB";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "E875DA02-4632-A32B-7ED4-32AD7D7FAAEE";
	setAttr -s 31 ".lnk";
	setAttr -s 25 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "C8524D97-4009-9D10-0D72-64858D626870";
	setAttr ".bsdt[0].bscd" -type "Int32Array" 1 0 ;
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "BE826FB3-4F7B-C558-315D-C7A64E2625E2";
createNode displayLayerManager -n "layerManager";
	rename -uid "A279148B-408B-2960-4EAE-F4A925BB898F";
createNode displayLayer -n "defaultLayer";
	rename -uid "58BB7DA4-4C38-5D78-6BD0-18A879407AED";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "69FB2DCF-4FF1-A362-6FA6-E081D0A73887";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "E90E29F6-4C9F-80AB-C9FA-23BA64E8C8AE";
	setAttr ".g" yes;
createNode reference -n "maxRN";
	rename -uid "52D17FC8-4D7D-BCD9-F028-D39220329BD7";
	setAttr -s 60 ".phl";
	setAttr ".phl[1]" 0;
	setAttr ".phl[2]" 0;
	setAttr ".phl[3]" 0;
	setAttr ".phl[4]" 0;
	setAttr ".phl[5]" 0;
	setAttr ".phl[6]" 0;
	setAttr ".phl[7]" 0;
	setAttr ".phl[8]" 0;
	setAttr ".phl[9]" 0;
	setAttr ".phl[10]" 0;
	setAttr ".phl[11]" 0;
	setAttr ".phl[12]" 0;
	setAttr ".phl[13]" 0;
	setAttr ".phl[14]" 0;
	setAttr ".phl[15]" 0;
	setAttr ".phl[16]" 0;
	setAttr ".phl[17]" 0;
	setAttr ".phl[18]" 0;
	setAttr ".phl[19]" 0;
	setAttr ".phl[20]" 0;
	setAttr ".phl[21]" 0;
	setAttr ".phl[22]" 0;
	setAttr ".phl[23]" 0;
	setAttr ".phl[24]" 0;
	setAttr ".phl[25]" 0;
	setAttr ".phl[26]" 0;
	setAttr ".phl[27]" 0;
	setAttr ".phl[28]" 0;
	setAttr ".phl[29]" 0;
	setAttr ".phl[30]" 0;
	setAttr ".phl[31]" 0;
	setAttr ".phl[32]" 0;
	setAttr ".phl[33]" 0;
	setAttr ".phl[34]" 0;
	setAttr ".phl[35]" 0;
	setAttr ".phl[36]" 0;
	setAttr ".phl[37]" 0;
	setAttr ".phl[38]" 0;
	setAttr ".phl[39]" 0;
	setAttr ".phl[40]" 0;
	setAttr ".phl[41]" 0;
	setAttr ".phl[42]" 0;
	setAttr ".phl[43]" 0;
	setAttr ".phl[44]" 0;
	setAttr ".phl[45]" 0;
	setAttr ".phl[46]" 0;
	setAttr ".phl[47]" 0;
	setAttr ".phl[48]" 0;
	setAttr ".phl[49]" 0;
	setAttr ".phl[50]" 0;
	setAttr ".phl[51]" 0;
	setAttr ".phl[52]" 0;
	setAttr ".phl[53]" 0;
	setAttr ".phl[54]" 0;
	setAttr ".phl[55]" 0;
	setAttr ".phl[56]" 0;
	setAttr ".phl[57]" 0;
	setAttr ".phl[58]" 0;
	setAttr ".phl[59]" 0;
	setAttr ".phl[60]" 0;
	setAttr ".ed" -type "dataReferenceEdits" 
		"maxRN"
		"maxRN" 0
		"maxRN" 87
		2 "|max:Group|max:MotionSystem|max:MainSystem|max:Main" "translate" " -type \"double3\" 0 0 0"
		
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKFollowRoot|max:FKOffsetRoot_M|max:FKExtraRoot_M|max:FKXRoot_M|max:FKOffsetRootPart1_M|max:FKInbetweenRootPart1_M|max:FKExtraRootPart1_M|max:FKRootPart1_M|max:FKXRootPart1_M|max:FKOffsetRootPart2_M|max:FKInbetweenRootPart2_M|max:FKExtraRootPart2_M|max:FKRootPart2_M|max:FKXRootPart2_M|max:HipSwingerStabilizer|max:FKOffsetSpine1_M|max:FKExtraSpine1_M|max:FKSpine1_M" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKFollowRoot|max:FKOffsetRoot_M|max:FKExtraRoot_M|max:FKXRoot_M|max:FKOffsetRootPart1_M|max:FKInbetweenRootPart1_M|max:FKExtraRootPart1_M|max:FKRootPart1_M|max:FKXRootPart1_M|max:FKOffsetRootPart2_M|max:FKInbetweenRootPart2_M|max:FKExtraRootPart2_M|max:FKRootPart2_M|max:FKXRootPart2_M|max:HipSwingerStabilizer|max:FKOffsetSpine1_M|max:FKExtraSpine1_M|max:FKXSpine1_M|max:FKOffsetSpine1Part1_M|max:FKInbetweenSpine1Part1_M|max:FKExtraSpine1Part1_M|max:FKSpine1Part1_M|max:FKXSpine1Part1_M|max:FKOffsetSpine1Part2_M|max:FKInbetweenSpine1Part2_M|max:FKExtraSpine1Part2_M|max:FKSpine1Part2_M|max:FKXSpine1Part2_M|max:FKOffsetChest_M|max:FKExtraChest_M|max:FKChest_M" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R|max:FKXKnee_R|max:FKOffsetAnkle_R|max:FKExtraAnkle_R|max:FKAnkle_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R|max:FKXKnee_R|max:FKOffsetAnkle_R|max:FKExtraAnkle_R|max:FKAnkle_R|max:FKXAnkle_R|max:FKOffsetToes_R|max:FKExtraToes_R|max:FKToes_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L|max:FKXKnee_L|max:FKOffsetAnkle_L|max:FKExtraAnkle_L|max:FKAnkle_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L|max:FKXKnee_L|max:FKOffsetAnkle_L|max:FKExtraAnkle_L|max:FKAnkle_L|max:FKXAnkle_L|max:FKOffsetToes_L|max:FKExtraToes_L|max:FKToes_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToChest_M|max:FKOffsetNeck_M|max:FKExtraNeck_M|max:FKNeck_M" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToChest_M|max:FKOffsetNeck_M|max:FKExtraNeck_M|max:FKXNeck_M|max:FKOffsetNeckPart1_M|max:FKInbetweenNeckPart1_M|max:FKExtraNeckPart1_M|max:FKNeckPart1_M|max:FKXNeckPart1_M|max:FKOffsetNeckPart2_M|max:FKInbetweenNeckPart2_M|max:FKExtraNeckPart2_M|max:FKNeckPart2_M|max:FKXNeckPart2_M|max:FKOffsetHead_M|max:FKGlobalStaticHead_M|max:FKGlobalHead_M|max:FKExtraHead_M|max:FKHead_M" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToChest_M|max:FKOffsetNeck_M|max:FKExtraNeck_M|max:FKXNeck_M|max:FKOffsetNeckPart1_M|max:FKInbetweenNeckPart1_M|max:FKExtraNeckPart1_M|max:FKNeckPart1_M|max:FKXNeckPart1_M|max:FKOffsetNeckPart2_M|max:FKInbetweenNeckPart2_M|max:FKExtraNeckPart2_M|max:FKNeckPart2_M|max:FKXNeckPart2_M|max:FKOffsetHead_M|max:FKGlobalStaticHead_M|max:FKGlobalHead_M|max:FKExtraHead_M|max:FKHead_M" 
		"Global" " -k 1 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R" 
		"Global" " -k 1 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R|max:FKXShoulder_R|max:FKOffsetElbow_R|max:FKExtraElbow_R|max:FKElbow_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R|max:FKXShoulder_R|max:FKOffsetElbow_R|max:FKExtraElbow_R|max:FKElbow_R|max:FKXElbow_R|max:FKOffsetWrist_R|max:FKExtraWrist_R|max:FKWrist_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L" 
		"Global" " -k 1 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L|max:FKXShoulder_L|max:FKOffsetElbow_L|max:FKExtraElbow_L|max:FKElbow_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L|max:FKXShoulder_L|max:FKOffsetElbow_L|max:FKExtraElbow_L|max:FKElbow_L|max:FKXElbow_L|max:FKOffsetWrist_L|max:FKExtraWrist_L|max:FKWrist_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|max:Group|max:MotionSystem|max:FKIKSystem|max:FKIKParentConstraintLeg_R|max:FKIKLeg_R" 
		"FKIKBlend" " -k 1 0"
		2 "|max:Group|max:MotionSystem|max:FKIKSystem|max:FKIKParentConstraintArm_R|max:FKIKArm_R" 
		"FKIKBlend" " -k 1 0"
		2 "|max:Group|max:MotionSystem|max:FKIKSystem|max:FKIKParentConstraintSpine_M|max:FKIKSpine_M" 
		"FKIKBlend" " -k 1 0"
		2 "|max:Group|max:MotionSystem|max:FKIKSystem|max:FKIKParentConstraintLeg_L|max:FKIKLeg_L" 
		"FKIKBlend" " -k 1 0"
		2 "|max:Group|max:MotionSystem|max:FKIKSystem|max:FKIKParentConstraintArm_L|max:FKIKArm_L" 
		"FKIKBlend" " -k 1 0"
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKFollowRoot|max:FKOffsetRoot_M|max:FKExtraRoot_M|max:FKXRoot_M|max:FKOffsetRootPart1_M|max:FKInbetweenRootPart1_M|max:FKExtraRootPart1_M|max:FKRootPart1_M|max:FKXRootPart1_M|max:FKOffsetRootPart2_M|max:FKInbetweenRootPart2_M|max:FKExtraRootPart2_M|max:FKRootPart2_M|max:FKXRootPart2_M|max:HipSwingerStabilizer|max:FKOffsetSpine1_M|max:FKExtraSpine1_M|max:FKSpine1_M.rotateX" 
		"maxRN.placeHolderList[1]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKFollowRoot|max:FKOffsetRoot_M|max:FKExtraRoot_M|max:FKXRoot_M|max:FKOffsetRootPart1_M|max:FKInbetweenRootPart1_M|max:FKExtraRootPart1_M|max:FKRootPart1_M|max:FKXRootPart1_M|max:FKOffsetRootPart2_M|max:FKInbetweenRootPart2_M|max:FKExtraRootPart2_M|max:FKRootPart2_M|max:FKXRootPart2_M|max:HipSwingerStabilizer|max:FKOffsetSpine1_M|max:FKExtraSpine1_M|max:FKSpine1_M.rotateY" 
		"maxRN.placeHolderList[2]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKFollowRoot|max:FKOffsetRoot_M|max:FKExtraRoot_M|max:FKXRoot_M|max:FKOffsetRootPart1_M|max:FKInbetweenRootPart1_M|max:FKExtraRootPart1_M|max:FKRootPart1_M|max:FKXRootPart1_M|max:FKOffsetRootPart2_M|max:FKInbetweenRootPart2_M|max:FKExtraRootPart2_M|max:FKRootPart2_M|max:FKXRootPart2_M|max:HipSwingerStabilizer|max:FKOffsetSpine1_M|max:FKExtraSpine1_M|max:FKSpine1_M.rotateZ" 
		"maxRN.placeHolderList[3]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKFollowRoot|max:FKOffsetRoot_M|max:FKExtraRoot_M|max:FKXRoot_M|max:FKOffsetRootPart1_M|max:FKInbetweenRootPart1_M|max:FKExtraRootPart1_M|max:FKRootPart1_M|max:FKXRootPart1_M|max:FKOffsetRootPart2_M|max:FKInbetweenRootPart2_M|max:FKExtraRootPart2_M|max:FKRootPart2_M|max:FKXRootPart2_M|max:HipSwingerStabilizer|max:FKOffsetSpine1_M|max:FKExtraSpine1_M|max:FKXSpine1_M|max:FKOffsetSpine1Part1_M|max:FKInbetweenSpine1Part1_M|max:FKExtraSpine1Part1_M|max:FKSpine1Part1_M|max:FKXSpine1Part1_M|max:FKOffsetSpine1Part2_M|max:FKInbetweenSpine1Part2_M|max:FKExtraSpine1Part2_M|max:FKSpine1Part2_M|max:FKXSpine1Part2_M|max:FKOffsetChest_M|max:FKExtraChest_M|max:FKChest_M.rotateX" 
		"maxRN.placeHolderList[4]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKFollowRoot|max:FKOffsetRoot_M|max:FKExtraRoot_M|max:FKXRoot_M|max:FKOffsetRootPart1_M|max:FKInbetweenRootPart1_M|max:FKExtraRootPart1_M|max:FKRootPart1_M|max:FKXRootPart1_M|max:FKOffsetRootPart2_M|max:FKInbetweenRootPart2_M|max:FKExtraRootPart2_M|max:FKRootPart2_M|max:FKXRootPart2_M|max:HipSwingerStabilizer|max:FKOffsetSpine1_M|max:FKExtraSpine1_M|max:FKXSpine1_M|max:FKOffsetSpine1Part1_M|max:FKInbetweenSpine1Part1_M|max:FKExtraSpine1Part1_M|max:FKSpine1Part1_M|max:FKXSpine1Part1_M|max:FKOffsetSpine1Part2_M|max:FKInbetweenSpine1Part2_M|max:FKExtraSpine1Part2_M|max:FKSpine1Part2_M|max:FKXSpine1Part2_M|max:FKOffsetChest_M|max:FKExtraChest_M|max:FKChest_M.rotateY" 
		"maxRN.placeHolderList[5]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKFollowRoot|max:FKOffsetRoot_M|max:FKExtraRoot_M|max:FKXRoot_M|max:FKOffsetRootPart1_M|max:FKInbetweenRootPart1_M|max:FKExtraRootPart1_M|max:FKRootPart1_M|max:FKXRootPart1_M|max:FKOffsetRootPart2_M|max:FKInbetweenRootPart2_M|max:FKExtraRootPart2_M|max:FKRootPart2_M|max:FKXRootPart2_M|max:HipSwingerStabilizer|max:FKOffsetSpine1_M|max:FKExtraSpine1_M|max:FKXSpine1_M|max:FKOffsetSpine1Part1_M|max:FKInbetweenSpine1Part1_M|max:FKExtraSpine1Part1_M|max:FKSpine1Part1_M|max:FKXSpine1Part1_M|max:FKOffsetSpine1Part2_M|max:FKInbetweenSpine1Part2_M|max:FKExtraSpine1Part2_M|max:FKSpine1Part2_M|max:FKXSpine1Part2_M|max:FKOffsetChest_M|max:FKExtraChest_M|max:FKChest_M.rotateZ" 
		"maxRN.placeHolderList[6]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R.rotateX" 
		"maxRN.placeHolderList[7]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R.rotateY" 
		"maxRN.placeHolderList[8]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R.rotateZ" 
		"maxRN.placeHolderList[9]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R.rotateX" 
		"maxRN.placeHolderList[10]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R.rotateY" 
		"maxRN.placeHolderList[11]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R.rotateZ" 
		"maxRN.placeHolderList[12]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R|max:FKXKnee_R|max:FKOffsetAnkle_R|max:FKExtraAnkle_R|max:FKAnkle_R.rotateX" 
		"maxRN.placeHolderList[13]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R|max:FKXKnee_R|max:FKOffsetAnkle_R|max:FKExtraAnkle_R|max:FKAnkle_R.rotateY" 
		"maxRN.placeHolderList[14]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R|max:FKXKnee_R|max:FKOffsetAnkle_R|max:FKExtraAnkle_R|max:FKAnkle_R.rotateZ" 
		"maxRN.placeHolderList[15]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R|max:FKXKnee_R|max:FKOffsetAnkle_R|max:FKExtraAnkle_R|max:FKAnkle_R|max:FKXAnkle_R|max:FKOffsetToes_R|max:FKExtraToes_R|max:FKToes_R.rotateX" 
		"maxRN.placeHolderList[16]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R|max:FKXKnee_R|max:FKOffsetAnkle_R|max:FKExtraAnkle_R|max:FKAnkle_R|max:FKXAnkle_R|max:FKOffsetToes_R|max:FKExtraToes_R|max:FKToes_R.rotateY" 
		"maxRN.placeHolderList[17]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_R|max:FKExtraHip_R|max:FKHip_R|max:FKXHip_R|max:FKOffsetKnee_R|max:FKExtraKnee_R|max:FKKnee_R|max:FKXKnee_R|max:FKOffsetAnkle_R|max:FKExtraAnkle_R|max:FKAnkle_R|max:FKXAnkle_R|max:FKOffsetToes_R|max:FKExtraToes_R|max:FKToes_R.rotateZ" 
		"maxRN.placeHolderList[18]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L.rotateX" 
		"maxRN.placeHolderList[19]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L.rotateY" 
		"maxRN.placeHolderList[20]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L.rotateZ" 
		"maxRN.placeHolderList[21]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L.rotateX" 
		"maxRN.placeHolderList[22]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L.rotateY" 
		"maxRN.placeHolderList[23]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L.rotateZ" 
		"maxRN.placeHolderList[24]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L|max:FKXKnee_L|max:FKOffsetAnkle_L|max:FKExtraAnkle_L|max:FKAnkle_L.rotateX" 
		"maxRN.placeHolderList[25]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L|max:FKXKnee_L|max:FKOffsetAnkle_L|max:FKExtraAnkle_L|max:FKAnkle_L.rotateY" 
		"maxRN.placeHolderList[26]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L|max:FKXKnee_L|max:FKOffsetAnkle_L|max:FKExtraAnkle_L|max:FKAnkle_L.rotateZ" 
		"maxRN.placeHolderList[27]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L|max:FKXKnee_L|max:FKOffsetAnkle_L|max:FKExtraAnkle_L|max:FKAnkle_L|max:FKXAnkle_L|max:FKOffsetToes_L|max:FKExtraToes_L|max:FKToes_L.rotateX" 
		"maxRN.placeHolderList[28]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L|max:FKXKnee_L|max:FKOffsetAnkle_L|max:FKExtraAnkle_L|max:FKAnkle_L|max:FKXAnkle_L|max:FKOffsetToes_L|max:FKExtraToes_L|max:FKToes_L.rotateY" 
		"maxRN.placeHolderList[29]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToRoot_M|max:FKOffsetHip_L|max:FKExtraHip_L|max:FKHip_L|max:FKXHip_L|max:FKOffsetKnee_L|max:FKExtraKnee_L|max:FKKnee_L|max:FKXKnee_L|max:FKOffsetAnkle_L|max:FKExtraAnkle_L|max:FKAnkle_L|max:FKXAnkle_L|max:FKOffsetToes_L|max:FKExtraToes_L|max:FKToes_L.rotateZ" 
		"maxRN.placeHolderList[30]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToChest_M|max:FKOffsetNeck_M|max:FKExtraNeck_M|max:FKNeck_M.rotateX" 
		"maxRN.placeHolderList[31]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToChest_M|max:FKOffsetNeck_M|max:FKExtraNeck_M|max:FKNeck_M.rotateY" 
		"maxRN.placeHolderList[32]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToChest_M|max:FKOffsetNeck_M|max:FKExtraNeck_M|max:FKNeck_M.rotateZ" 
		"maxRN.placeHolderList[33]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToChest_M|max:FKOffsetNeck_M|max:FKExtraNeck_M|max:FKXNeck_M|max:FKOffsetNeckPart1_M|max:FKInbetweenNeckPart1_M|max:FKExtraNeckPart1_M|max:FKNeckPart1_M|max:FKXNeckPart1_M|max:FKOffsetNeckPart2_M|max:FKInbetweenNeckPart2_M|max:FKExtraNeckPart2_M|max:FKNeckPart2_M|max:FKXNeckPart2_M|max:FKOffsetHead_M|max:FKGlobalStaticHead_M|max:FKGlobalHead_M|max:FKExtraHead_M|max:FKHead_M.rotateX" 
		"maxRN.placeHolderList[34]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToChest_M|max:FKOffsetNeck_M|max:FKExtraNeck_M|max:FKXNeck_M|max:FKOffsetNeckPart1_M|max:FKInbetweenNeckPart1_M|max:FKExtraNeckPart1_M|max:FKNeckPart1_M|max:FKXNeckPart1_M|max:FKOffsetNeckPart2_M|max:FKInbetweenNeckPart2_M|max:FKExtraNeckPart2_M|max:FKNeckPart2_M|max:FKXNeckPart2_M|max:FKOffsetHead_M|max:FKGlobalStaticHead_M|max:FKGlobalHead_M|max:FKExtraHead_M|max:FKHead_M.rotateY" 
		"maxRN.placeHolderList[35]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToChest_M|max:FKOffsetNeck_M|max:FKExtraNeck_M|max:FKXNeck_M|max:FKOffsetNeckPart1_M|max:FKInbetweenNeckPart1_M|max:FKExtraNeckPart1_M|max:FKNeckPart1_M|max:FKXNeckPart1_M|max:FKOffsetNeckPart2_M|max:FKInbetweenNeckPart2_M|max:FKExtraNeckPart2_M|max:FKNeckPart2_M|max:FKXNeckPart2_M|max:FKOffsetHead_M|max:FKGlobalStaticHead_M|max:FKGlobalHead_M|max:FKExtraHead_M|max:FKHead_M.rotateZ" 
		"maxRN.placeHolderList[36]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R.rotateX" 
		"maxRN.placeHolderList[37]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R.rotateY" 
		"maxRN.placeHolderList[38]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R.rotateZ" 
		"maxRN.placeHolderList[39]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R|max:FKXShoulder_R|max:FKOffsetElbow_R|max:FKExtraElbow_R|max:FKElbow_R.rotateX" 
		"maxRN.placeHolderList[40]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R|max:FKXShoulder_R|max:FKOffsetElbow_R|max:FKExtraElbow_R|max:FKElbow_R.rotateY" 
		"maxRN.placeHolderList[41]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R|max:FKXShoulder_R|max:FKOffsetElbow_R|max:FKExtraElbow_R|max:FKElbow_R.rotateZ" 
		"maxRN.placeHolderList[42]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R|max:FKXShoulder_R|max:FKOffsetElbow_R|max:FKExtraElbow_R|max:FKElbow_R|max:FKXElbow_R|max:FKOffsetWrist_R|max:FKExtraWrist_R|max:FKWrist_R.rotateX" 
		"maxRN.placeHolderList[43]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R|max:FKXShoulder_R|max:FKOffsetElbow_R|max:FKExtraElbow_R|max:FKElbow_R|max:FKXElbow_R|max:FKOffsetWrist_R|max:FKExtraWrist_R|max:FKWrist_R.rotateY" 
		"maxRN.placeHolderList[44]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_R|max:FKOffsetShoulder_R|max:FKGlobalStaticShoulder_R|max:FKGlobalShoulder_R|max:FKExtraShoulder_R|max:FKShoulder_R|max:FKXShoulder_R|max:FKOffsetElbow_R|max:FKExtraElbow_R|max:FKElbow_R|max:FKXElbow_R|max:FKOffsetWrist_R|max:FKExtraWrist_R|max:FKWrist_R.rotateZ" 
		"maxRN.placeHolderList[45]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L.rotateX" 
		"maxRN.placeHolderList[46]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L.rotateY" 
		"maxRN.placeHolderList[47]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L.rotateZ" 
		"maxRN.placeHolderList[48]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L|max:FKXShoulder_L|max:FKOffsetElbow_L|max:FKExtraElbow_L|max:FKElbow_L.rotateX" 
		"maxRN.placeHolderList[49]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L|max:FKXShoulder_L|max:FKOffsetElbow_L|max:FKExtraElbow_L|max:FKElbow_L.rotateY" 
		"maxRN.placeHolderList[50]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L|max:FKXShoulder_L|max:FKOffsetElbow_L|max:FKExtraElbow_L|max:FKElbow_L.rotateZ" 
		"maxRN.placeHolderList[51]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L|max:FKXShoulder_L|max:FKOffsetElbow_L|max:FKExtraElbow_L|max:FKElbow_L|max:FKXElbow_L|max:FKOffsetWrist_L|max:FKExtraWrist_L|max:FKWrist_L.rotateX" 
		"maxRN.placeHolderList[52]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L|max:FKXShoulder_L|max:FKOffsetElbow_L|max:FKExtraElbow_L|max:FKElbow_L|max:FKXElbow_L|max:FKOffsetWrist_L|max:FKExtraWrist_L|max:FKWrist_L.rotateY" 
		"maxRN.placeHolderList[53]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:FKSystem|max:FKParentConstraintToScapula_L|max:FKOffsetShoulder_L|max:FKGlobalStaticShoulder_L|max:FKGlobalShoulder_L|max:FKExtraShoulder_L|max:FKShoulder_L|max:FKXShoulder_L|max:FKOffsetElbow_L|max:FKExtraElbow_L|max:FKElbow_L|max:FKXElbow_L|max:FKOffsetWrist_L|max:FKExtraWrist_L|max:FKWrist_L.rotateZ" 
		"maxRN.placeHolderList[54]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:RootSystem|max:RootCenterBtwLegsBlended_M|max:RootOffsetX_M|max:RootExtraX_M|max:RootX_M.translateX" 
		"maxRN.placeHolderList[55]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:RootSystem|max:RootCenterBtwLegsBlended_M|max:RootOffsetX_M|max:RootExtraX_M|max:RootX_M.translateY" 
		"maxRN.placeHolderList[56]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:RootSystem|max:RootCenterBtwLegsBlended_M|max:RootOffsetX_M|max:RootExtraX_M|max:RootX_M.translateZ" 
		"maxRN.placeHolderList[57]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:RootSystem|max:RootCenterBtwLegsBlended_M|max:RootOffsetX_M|max:RootExtraX_M|max:RootX_M.rotateX" 
		"maxRN.placeHolderList[58]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:RootSystem|max:RootCenterBtwLegsBlended_M|max:RootOffsetX_M|max:RootExtraX_M|max:RootX_M.rotateY" 
		"maxRN.placeHolderList[59]" ""
		5 4 "maxRN" "|max:Group|max:MotionSystem|max:RootSystem|max:RootCenterBtwLegsBlended_M|max:RootOffsetX_M|max:RootExtraX_M|max:RootX_M.rotateZ" 
		"maxRN.placeHolderList[60]" "";
	setAttr ".ptag" -type "string" "";
lockNode -l 1 ;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "B9C2BA2B-46A6-344A-5B6E-C1B931CDD0E1";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n"
		+ "            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n"
		+ "            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n"
		+ "            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n"
		+ "            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n"
		+ "            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n"
		+ "            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n"
		+ "            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n"
		+ "            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n"
		+ "            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 839\n            -height 716\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n"
		+ "            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n"
		+ "            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n"
		+ "            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n"
		+ "                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n"
		+ "                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n"
		+ "                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n"
		+ "            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n"
		+ "                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n"
		+ "                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n"
		+ "                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n"
		+ "\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n"
		+ "                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n"
		+ "                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n"
		+ "                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n"
		+ "                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n"
		+ "                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n"
		+ "\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 839\\n    -height 716\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 839\\n    -height 716\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "B082D01C-4F6C-242A-BD55-4EA52ABB5654";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 32 -ast 0 -aet 32 ";
	setAttr ".st" 6;
createNode reference -n "samRN";
	rename -uid "13D4BA10-4AEE-3338-0A33-9FB6DDE43365";
	setAttr -s 60 ".phl";
	setAttr ".phl[1]" 0;
	setAttr ".phl[2]" 0;
	setAttr ".phl[3]" 0;
	setAttr ".phl[4]" 0;
	setAttr ".phl[5]" 0;
	setAttr ".phl[6]" 0;
	setAttr ".phl[7]" 0;
	setAttr ".phl[8]" 0;
	setAttr ".phl[9]" 0;
	setAttr ".phl[10]" 0;
	setAttr ".phl[11]" 0;
	setAttr ".phl[12]" 0;
	setAttr ".phl[13]" 0;
	setAttr ".phl[14]" 0;
	setAttr ".phl[15]" 0;
	setAttr ".phl[16]" 0;
	setAttr ".phl[17]" 0;
	setAttr ".phl[18]" 0;
	setAttr ".phl[19]" 0;
	setAttr ".phl[20]" 0;
	setAttr ".phl[21]" 0;
	setAttr ".phl[22]" 0;
	setAttr ".phl[23]" 0;
	setAttr ".phl[24]" 0;
	setAttr ".phl[25]" 0;
	setAttr ".phl[26]" 0;
	setAttr ".phl[27]" 0;
	setAttr ".phl[28]" 0;
	setAttr ".phl[29]" 0;
	setAttr ".phl[30]" 0;
	setAttr ".phl[31]" 0;
	setAttr ".phl[32]" 0;
	setAttr ".phl[33]" 0;
	setAttr ".phl[34]" 0;
	setAttr ".phl[35]" 0;
	setAttr ".phl[36]" 0;
	setAttr ".phl[37]" 0;
	setAttr ".phl[38]" 0;
	setAttr ".phl[39]" 0;
	setAttr ".phl[40]" 0;
	setAttr ".phl[41]" 0;
	setAttr ".phl[42]" 0;
	setAttr ".phl[43]" 0;
	setAttr ".phl[44]" 0;
	setAttr ".phl[45]" 0;
	setAttr ".phl[46]" 0;
	setAttr ".phl[47]" 0;
	setAttr ".phl[48]" 0;
	setAttr ".phl[49]" 0;
	setAttr ".phl[50]" 0;
	setAttr ".phl[51]" 0;
	setAttr ".phl[52]" 0;
	setAttr ".phl[53]" 0;
	setAttr ".phl[54]" 0;
	setAttr ".phl[55]" 0;
	setAttr ".phl[56]" 0;
	setAttr ".phl[57]" 0;
	setAttr ".phl[58]" 0;
	setAttr ".phl[59]" 0;
	setAttr ".phl[60]" 0;
	setAttr ".ed" -type "dataReferenceEdits" 
		"samRN"
		"samRN" 0
		"samRN" 85
		2 "|sam:Group|sam:MotionSystem|sam:MainSystem|sam:Main" "translate" " -type \"double3\" 10 0 0"
		
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKFollowRoot|sam:FKOffsetRoot_M|sam:FKExtraRoot_M|sam:FKXRoot_M|sam:FKOffsetRootPart1_M|sam:FKInbetweenRootPart1_M|sam:FKExtraRootPart1_M|sam:FKRootPart1_M|sam:FKXRootPart1_M|sam:FKOffsetRootPart2_M|sam:FKInbetweenRootPart2_M|sam:FKExtraRootPart2_M|sam:FKRootPart2_M|sam:FKXRootPart2_M|sam:HipSwingerStabilizer|sam:FKOffsetSpine1_M|sam:FKExtraSpine1_M|sam:FKSpine1_M" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKFollowRoot|sam:FKOffsetRoot_M|sam:FKExtraRoot_M|sam:FKXRoot_M|sam:FKOffsetRootPart1_M|sam:FKInbetweenRootPart1_M|sam:FKExtraRootPart1_M|sam:FKRootPart1_M|sam:FKXRootPart1_M|sam:FKOffsetRootPart2_M|sam:FKInbetweenRootPart2_M|sam:FKExtraRootPart2_M|sam:FKRootPart2_M|sam:FKXRootPart2_M|sam:HipSwingerStabilizer|sam:FKOffsetSpine1_M|sam:FKExtraSpine1_M|sam:FKXSpine1_M|sam:FKOffsetSpine1Part1_M|sam:FKInbetweenSpine1Part1_M|sam:FKExtraSpine1Part1_M|sam:FKSpine1Part1_M|sam:FKXSpine1Part1_M|sam:FKOffsetSpine1Part2_M|sam:FKInbetweenSpine1Part2_M|sam:FKExtraSpine1Part2_M|sam:FKSpine1Part2_M|sam:FKXSpine1Part2_M|sam:FKOffsetChest_M|sam:FKExtraChest_M|sam:FKChest_M" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R|sam:FKXKnee_R|sam:FKOffsetAnkle_R|sam:FKExtraAnkle_R|sam:FKAnkle_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R|sam:FKXKnee_R|sam:FKOffsetAnkle_R|sam:FKExtraAnkle_R|sam:FKAnkle_R|sam:FKXAnkle_R|sam:FKOffsetToes_R|sam:FKExtraToes_R|sam:FKToes_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L|sam:FKXKnee_L|sam:FKOffsetAnkle_L|sam:FKExtraAnkle_L|sam:FKAnkle_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L|sam:FKXKnee_L|sam:FKOffsetAnkle_L|sam:FKExtraAnkle_L|sam:FKAnkle_L|sam:FKXAnkle_L|sam:FKOffsetToes_L|sam:FKExtraToes_L|sam:FKToes_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToChest_M|sam:FKOffsetNeck_M|sam:FKExtraNeck_M|sam:FKNeck_M" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToChest_M|sam:FKOffsetNeck_M|sam:FKExtraNeck_M|sam:FKXNeck_M|sam:FKOffsetNeckPart1_M|sam:FKInbetweenNeckPart1_M|sam:FKExtraNeckPart1_M|sam:FKNeckPart1_M|sam:FKXNeckPart1_M|sam:FKOffsetNeckPart2_M|sam:FKInbetweenNeckPart2_M|sam:FKExtraNeckPart2_M|sam:FKNeckPart2_M|sam:FKXNeckPart2_M|sam:FKOffsetHead_M|sam:FKGlobalStaticHead_M|sam:FKGlobalHead_M|sam:FKExtraHead_M|sam:FKHead_M" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToChest_M|sam:FKOffsetNeck_M|sam:FKExtraNeck_M|sam:FKXNeck_M|sam:FKOffsetNeckPart1_M|sam:FKInbetweenNeckPart1_M|sam:FKExtraNeckPart1_M|sam:FKNeckPart1_M|sam:FKXNeckPart1_M|sam:FKOffsetNeckPart2_M|sam:FKInbetweenNeckPart2_M|sam:FKExtraNeckPart2_M|sam:FKNeckPart2_M|sam:FKXNeckPart2_M|sam:FKOffsetHead_M|sam:FKGlobalStaticHead_M|sam:FKGlobalHead_M|sam:FKExtraHead_M|sam:FKHead_M" 
		"Global" " -k 1 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R|sam:FKXShoulder_R|sam:FKOffsetElbow_R|sam:FKExtraElbow_R|sam:FKElbow_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R|sam:FKXShoulder_R|sam:FKOffsetElbow_R|sam:FKExtraElbow_R|sam:FKElbow_R|sam:FKXElbow_R|sam:FKOffsetWrist_R|sam:FKExtraWrist_R|sam:FKWrist_R" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L|sam:FKXShoulder_L|sam:FKOffsetElbow_L|sam:FKExtraElbow_L|sam:FKElbow_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L|sam:FKXShoulder_L|sam:FKOffsetElbow_L|sam:FKExtraElbow_L|sam:FKElbow_L|sam:FKXElbow_L|sam:FKOffsetWrist_L|sam:FKExtraWrist_L|sam:FKWrist_L" 
		"translate" " -type \"double3\" 0 0 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKIKSystem|sam:FKIKParentConstraintLeg_R|sam:FKIKLeg_R" 
		"FKIKBlend" " -k 1 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKIKSystem|sam:FKIKParentConstraintArm_R|sam:FKIKArm_R" 
		"FKIKBlend" " -k 1 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKIKSystem|sam:FKIKParentConstraintSpine_M|sam:FKIKSpine_M" 
		"FKIKBlend" " -k 1 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKIKSystem|sam:FKIKParentConstraintLeg_L|sam:FKIKLeg_L" 
		"FKIKBlend" " -k 1 0"
		2 "|sam:Group|sam:MotionSystem|sam:FKIKSystem|sam:FKIKParentConstraintArm_L|sam:FKIKArm_L" 
		"FKIKBlend" " -k 1 0"
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKFollowRoot|sam:FKOffsetRoot_M|sam:FKExtraRoot_M|sam:FKXRoot_M|sam:FKOffsetRootPart1_M|sam:FKInbetweenRootPart1_M|sam:FKExtraRootPart1_M|sam:FKRootPart1_M|sam:FKXRootPart1_M|sam:FKOffsetRootPart2_M|sam:FKInbetweenRootPart2_M|sam:FKExtraRootPart2_M|sam:FKRootPart2_M|sam:FKXRootPart2_M|sam:HipSwingerStabilizer|sam:FKOffsetSpine1_M|sam:FKExtraSpine1_M|sam:FKSpine1_M.rotateX" 
		"samRN.placeHolderList[1]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKFollowRoot|sam:FKOffsetRoot_M|sam:FKExtraRoot_M|sam:FKXRoot_M|sam:FKOffsetRootPart1_M|sam:FKInbetweenRootPart1_M|sam:FKExtraRootPart1_M|sam:FKRootPart1_M|sam:FKXRootPart1_M|sam:FKOffsetRootPart2_M|sam:FKInbetweenRootPart2_M|sam:FKExtraRootPart2_M|sam:FKRootPart2_M|sam:FKXRootPart2_M|sam:HipSwingerStabilizer|sam:FKOffsetSpine1_M|sam:FKExtraSpine1_M|sam:FKSpine1_M.rotateY" 
		"samRN.placeHolderList[2]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKFollowRoot|sam:FKOffsetRoot_M|sam:FKExtraRoot_M|sam:FKXRoot_M|sam:FKOffsetRootPart1_M|sam:FKInbetweenRootPart1_M|sam:FKExtraRootPart1_M|sam:FKRootPart1_M|sam:FKXRootPart1_M|sam:FKOffsetRootPart2_M|sam:FKInbetweenRootPart2_M|sam:FKExtraRootPart2_M|sam:FKRootPart2_M|sam:FKXRootPart2_M|sam:HipSwingerStabilizer|sam:FKOffsetSpine1_M|sam:FKExtraSpine1_M|sam:FKSpine1_M.rotateZ" 
		"samRN.placeHolderList[3]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKFollowRoot|sam:FKOffsetRoot_M|sam:FKExtraRoot_M|sam:FKXRoot_M|sam:FKOffsetRootPart1_M|sam:FKInbetweenRootPart1_M|sam:FKExtraRootPart1_M|sam:FKRootPart1_M|sam:FKXRootPart1_M|sam:FKOffsetRootPart2_M|sam:FKInbetweenRootPart2_M|sam:FKExtraRootPart2_M|sam:FKRootPart2_M|sam:FKXRootPart2_M|sam:HipSwingerStabilizer|sam:FKOffsetSpine1_M|sam:FKExtraSpine1_M|sam:FKXSpine1_M|sam:FKOffsetSpine1Part1_M|sam:FKInbetweenSpine1Part1_M|sam:FKExtraSpine1Part1_M|sam:FKSpine1Part1_M|sam:FKXSpine1Part1_M|sam:FKOffsetSpine1Part2_M|sam:FKInbetweenSpine1Part2_M|sam:FKExtraSpine1Part2_M|sam:FKSpine1Part2_M|sam:FKXSpine1Part2_M|sam:FKOffsetChest_M|sam:FKExtraChest_M|sam:FKChest_M.rotateX" 
		"samRN.placeHolderList[4]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKFollowRoot|sam:FKOffsetRoot_M|sam:FKExtraRoot_M|sam:FKXRoot_M|sam:FKOffsetRootPart1_M|sam:FKInbetweenRootPart1_M|sam:FKExtraRootPart1_M|sam:FKRootPart1_M|sam:FKXRootPart1_M|sam:FKOffsetRootPart2_M|sam:FKInbetweenRootPart2_M|sam:FKExtraRootPart2_M|sam:FKRootPart2_M|sam:FKXRootPart2_M|sam:HipSwingerStabilizer|sam:FKOffsetSpine1_M|sam:FKExtraSpine1_M|sam:FKXSpine1_M|sam:FKOffsetSpine1Part1_M|sam:FKInbetweenSpine1Part1_M|sam:FKExtraSpine1Part1_M|sam:FKSpine1Part1_M|sam:FKXSpine1Part1_M|sam:FKOffsetSpine1Part2_M|sam:FKInbetweenSpine1Part2_M|sam:FKExtraSpine1Part2_M|sam:FKSpine1Part2_M|sam:FKXSpine1Part2_M|sam:FKOffsetChest_M|sam:FKExtraChest_M|sam:FKChest_M.rotateY" 
		"samRN.placeHolderList[5]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKFollowRoot|sam:FKOffsetRoot_M|sam:FKExtraRoot_M|sam:FKXRoot_M|sam:FKOffsetRootPart1_M|sam:FKInbetweenRootPart1_M|sam:FKExtraRootPart1_M|sam:FKRootPart1_M|sam:FKXRootPart1_M|sam:FKOffsetRootPart2_M|sam:FKInbetweenRootPart2_M|sam:FKExtraRootPart2_M|sam:FKRootPart2_M|sam:FKXRootPart2_M|sam:HipSwingerStabilizer|sam:FKOffsetSpine1_M|sam:FKExtraSpine1_M|sam:FKXSpine1_M|sam:FKOffsetSpine1Part1_M|sam:FKInbetweenSpine1Part1_M|sam:FKExtraSpine1Part1_M|sam:FKSpine1Part1_M|sam:FKXSpine1Part1_M|sam:FKOffsetSpine1Part2_M|sam:FKInbetweenSpine1Part2_M|sam:FKExtraSpine1Part2_M|sam:FKSpine1Part2_M|sam:FKXSpine1Part2_M|sam:FKOffsetChest_M|sam:FKExtraChest_M|sam:FKChest_M.rotateZ" 
		"samRN.placeHolderList[6]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R.rotateX" 
		"samRN.placeHolderList[7]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R.rotateY" 
		"samRN.placeHolderList[8]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R.rotateZ" 
		"samRN.placeHolderList[9]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R.rotateX" 
		"samRN.placeHolderList[10]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R.rotateY" 
		"samRN.placeHolderList[11]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R.rotateZ" 
		"samRN.placeHolderList[12]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R|sam:FKXKnee_R|sam:FKOffsetAnkle_R|sam:FKExtraAnkle_R|sam:FKAnkle_R.rotateX" 
		"samRN.placeHolderList[13]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R|sam:FKXKnee_R|sam:FKOffsetAnkle_R|sam:FKExtraAnkle_R|sam:FKAnkle_R.rotateY" 
		"samRN.placeHolderList[14]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R|sam:FKXKnee_R|sam:FKOffsetAnkle_R|sam:FKExtraAnkle_R|sam:FKAnkle_R.rotateZ" 
		"samRN.placeHolderList[15]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R|sam:FKXKnee_R|sam:FKOffsetAnkle_R|sam:FKExtraAnkle_R|sam:FKAnkle_R|sam:FKXAnkle_R|sam:FKOffsetToes_R|sam:FKExtraToes_R|sam:FKToes_R.rotateX" 
		"samRN.placeHolderList[16]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R|sam:FKXKnee_R|sam:FKOffsetAnkle_R|sam:FKExtraAnkle_R|sam:FKAnkle_R|sam:FKXAnkle_R|sam:FKOffsetToes_R|sam:FKExtraToes_R|sam:FKToes_R.rotateY" 
		"samRN.placeHolderList[17]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_R|sam:FKExtraHip_R|sam:FKHip_R|sam:FKXHip_R|sam:FKOffsetKnee_R|sam:FKExtraKnee_R|sam:FKKnee_R|sam:FKXKnee_R|sam:FKOffsetAnkle_R|sam:FKExtraAnkle_R|sam:FKAnkle_R|sam:FKXAnkle_R|sam:FKOffsetToes_R|sam:FKExtraToes_R|sam:FKToes_R.rotateZ" 
		"samRN.placeHolderList[18]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L.rotateX" 
		"samRN.placeHolderList[19]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L.rotateY" 
		"samRN.placeHolderList[20]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L.rotateZ" 
		"samRN.placeHolderList[21]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L.rotateX" 
		"samRN.placeHolderList[22]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L.rotateY" 
		"samRN.placeHolderList[23]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L.rotateZ" 
		"samRN.placeHolderList[24]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L|sam:FKXKnee_L|sam:FKOffsetAnkle_L|sam:FKExtraAnkle_L|sam:FKAnkle_L.rotateX" 
		"samRN.placeHolderList[25]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L|sam:FKXKnee_L|sam:FKOffsetAnkle_L|sam:FKExtraAnkle_L|sam:FKAnkle_L.rotateY" 
		"samRN.placeHolderList[26]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L|sam:FKXKnee_L|sam:FKOffsetAnkle_L|sam:FKExtraAnkle_L|sam:FKAnkle_L.rotateZ" 
		"samRN.placeHolderList[27]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L|sam:FKXKnee_L|sam:FKOffsetAnkle_L|sam:FKExtraAnkle_L|sam:FKAnkle_L|sam:FKXAnkle_L|sam:FKOffsetToes_L|sam:FKExtraToes_L|sam:FKToes_L.rotateX" 
		"samRN.placeHolderList[28]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L|sam:FKXKnee_L|sam:FKOffsetAnkle_L|sam:FKExtraAnkle_L|sam:FKAnkle_L|sam:FKXAnkle_L|sam:FKOffsetToes_L|sam:FKExtraToes_L|sam:FKToes_L.rotateY" 
		"samRN.placeHolderList[29]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToRoot_M|sam:FKOffsetHip_L|sam:FKExtraHip_L|sam:FKHip_L|sam:FKXHip_L|sam:FKOffsetKnee_L|sam:FKExtraKnee_L|sam:FKKnee_L|sam:FKXKnee_L|sam:FKOffsetAnkle_L|sam:FKExtraAnkle_L|sam:FKAnkle_L|sam:FKXAnkle_L|sam:FKOffsetToes_L|sam:FKExtraToes_L|sam:FKToes_L.rotateZ" 
		"samRN.placeHolderList[30]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToChest_M|sam:FKOffsetNeck_M|sam:FKExtraNeck_M|sam:FKNeck_M.rotateX" 
		"samRN.placeHolderList[31]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToChest_M|sam:FKOffsetNeck_M|sam:FKExtraNeck_M|sam:FKNeck_M.rotateY" 
		"samRN.placeHolderList[32]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToChest_M|sam:FKOffsetNeck_M|sam:FKExtraNeck_M|sam:FKNeck_M.rotateZ" 
		"samRN.placeHolderList[33]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToChest_M|sam:FKOffsetNeck_M|sam:FKExtraNeck_M|sam:FKXNeck_M|sam:FKOffsetNeckPart1_M|sam:FKInbetweenNeckPart1_M|sam:FKExtraNeckPart1_M|sam:FKNeckPart1_M|sam:FKXNeckPart1_M|sam:FKOffsetNeckPart2_M|sam:FKInbetweenNeckPart2_M|sam:FKExtraNeckPart2_M|sam:FKNeckPart2_M|sam:FKXNeckPart2_M|sam:FKOffsetHead_M|sam:FKGlobalStaticHead_M|sam:FKGlobalHead_M|sam:FKExtraHead_M|sam:FKHead_M.rotateX" 
		"samRN.placeHolderList[34]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToChest_M|sam:FKOffsetNeck_M|sam:FKExtraNeck_M|sam:FKXNeck_M|sam:FKOffsetNeckPart1_M|sam:FKInbetweenNeckPart1_M|sam:FKExtraNeckPart1_M|sam:FKNeckPart1_M|sam:FKXNeckPart1_M|sam:FKOffsetNeckPart2_M|sam:FKInbetweenNeckPart2_M|sam:FKExtraNeckPart2_M|sam:FKNeckPart2_M|sam:FKXNeckPart2_M|sam:FKOffsetHead_M|sam:FKGlobalStaticHead_M|sam:FKGlobalHead_M|sam:FKExtraHead_M|sam:FKHead_M.rotateY" 
		"samRN.placeHolderList[35]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToChest_M|sam:FKOffsetNeck_M|sam:FKExtraNeck_M|sam:FKXNeck_M|sam:FKOffsetNeckPart1_M|sam:FKInbetweenNeckPart1_M|sam:FKExtraNeckPart1_M|sam:FKNeckPart1_M|sam:FKXNeckPart1_M|sam:FKOffsetNeckPart2_M|sam:FKInbetweenNeckPart2_M|sam:FKExtraNeckPart2_M|sam:FKNeckPart2_M|sam:FKXNeckPart2_M|sam:FKOffsetHead_M|sam:FKGlobalStaticHead_M|sam:FKGlobalHead_M|sam:FKExtraHead_M|sam:FKHead_M.rotateZ" 
		"samRN.placeHolderList[36]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R.rotateX" 
		"samRN.placeHolderList[37]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R.rotateY" 
		"samRN.placeHolderList[38]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R.rotateZ" 
		"samRN.placeHolderList[39]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R|sam:FKXShoulder_R|sam:FKOffsetElbow_R|sam:FKExtraElbow_R|sam:FKElbow_R.rotateX" 
		"samRN.placeHolderList[40]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R|sam:FKXShoulder_R|sam:FKOffsetElbow_R|sam:FKExtraElbow_R|sam:FKElbow_R.rotateY" 
		"samRN.placeHolderList[41]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R|sam:FKXShoulder_R|sam:FKOffsetElbow_R|sam:FKExtraElbow_R|sam:FKElbow_R.rotateZ" 
		"samRN.placeHolderList[42]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R|sam:FKXShoulder_R|sam:FKOffsetElbow_R|sam:FKExtraElbow_R|sam:FKElbow_R|sam:FKXElbow_R|sam:FKOffsetWrist_R|sam:FKExtraWrist_R|sam:FKWrist_R.rotateX" 
		"samRN.placeHolderList[43]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R|sam:FKXShoulder_R|sam:FKOffsetElbow_R|sam:FKExtraElbow_R|sam:FKElbow_R|sam:FKXElbow_R|sam:FKOffsetWrist_R|sam:FKExtraWrist_R|sam:FKWrist_R.rotateY" 
		"samRN.placeHolderList[44]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_R|sam:FKOffsetShoulder_R|sam:FKFollowShoulder_R|sam:FKFollowReOffsetShoulder_R|sam:FKExtraShoulder_R|sam:FKShoulder_R|sam:FKXShoulder_R|sam:FKOffsetElbow_R|sam:FKExtraElbow_R|sam:FKElbow_R|sam:FKXElbow_R|sam:FKOffsetWrist_R|sam:FKExtraWrist_R|sam:FKWrist_R.rotateZ" 
		"samRN.placeHolderList[45]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L.rotateX" 
		"samRN.placeHolderList[46]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L.rotateY" 
		"samRN.placeHolderList[47]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L.rotateZ" 
		"samRN.placeHolderList[48]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L|sam:FKXShoulder_L|sam:FKOffsetElbow_L|sam:FKExtraElbow_L|sam:FKElbow_L.rotateX" 
		"samRN.placeHolderList[49]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L|sam:FKXShoulder_L|sam:FKOffsetElbow_L|sam:FKExtraElbow_L|sam:FKElbow_L.rotateY" 
		"samRN.placeHolderList[50]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L|sam:FKXShoulder_L|sam:FKOffsetElbow_L|sam:FKExtraElbow_L|sam:FKElbow_L.rotateZ" 
		"samRN.placeHolderList[51]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L|sam:FKXShoulder_L|sam:FKOffsetElbow_L|sam:FKExtraElbow_L|sam:FKElbow_L|sam:FKXElbow_L|sam:FKOffsetWrist_L|sam:FKExtraWrist_L|sam:FKWrist_L.rotateX" 
		"samRN.placeHolderList[52]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L|sam:FKXShoulder_L|sam:FKOffsetElbow_L|sam:FKExtraElbow_L|sam:FKElbow_L|sam:FKXElbow_L|sam:FKOffsetWrist_L|sam:FKExtraWrist_L|sam:FKWrist_L.rotateY" 
		"samRN.placeHolderList[53]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:FKSystem|sam:FKParentConstraintToScapula_L|sam:FKOffsetShoulder_L|sam:FKFollowShoulder_L|sam:FKFollowReOffsetShoulder_L|sam:FKExtraShoulder_L|sam:FKShoulder_L|sam:FKXShoulder_L|sam:FKOffsetElbow_L|sam:FKExtraElbow_L|sam:FKElbow_L|sam:FKXElbow_L|sam:FKOffsetWrist_L|sam:FKExtraWrist_L|sam:FKWrist_L.rotateZ" 
		"samRN.placeHolderList[54]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:RootSystem|sam:RootCenterBtwLegsBlended_M|sam:RootOffsetX_M|sam:RootExtraX_M|sam:RootX_M.translateX" 
		"samRN.placeHolderList[55]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:RootSystem|sam:RootCenterBtwLegsBlended_M|sam:RootOffsetX_M|sam:RootExtraX_M|sam:RootX_M.translateY" 
		"samRN.placeHolderList[56]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:RootSystem|sam:RootCenterBtwLegsBlended_M|sam:RootOffsetX_M|sam:RootExtraX_M|sam:RootX_M.translateZ" 
		"samRN.placeHolderList[57]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:RootSystem|sam:RootCenterBtwLegsBlended_M|sam:RootOffsetX_M|sam:RootExtraX_M|sam:RootX_M.rotateX" 
		"samRN.placeHolderList[58]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:RootSystem|sam:RootCenterBtwLegsBlended_M|sam:RootOffsetX_M|sam:RootExtraX_M|sam:RootX_M.rotateY" 
		"samRN.placeHolderList[59]" ""
		5 4 "samRN" "|sam:Group|sam:MotionSystem|sam:RootSystem|sam:RootCenterBtwLegsBlended_M|sam:RootOffsetX_M|sam:RootExtraX_M|sam:RootX_M.rotateZ" 
		"samRN.placeHolderList[60]" "";
	setAttr ".ptag" -type "string" "";
lockNode -l 1 ;
createNode animCurveTA -n "RootX_M_rotateX";
	rename -uid "CA7D4B14-4C1D-EA65-9016-16B5C995AF5A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.86093500964872949 1 -1.0167784806401046
		 2 -1.1203692513260006 3 -1.1419909778124384 4 -1.0634717147596051 5 -0.91443135657246399
		 6 -0.61841506297567261 7 -0.32613562862683482 8 -0.034671228010459298 9 0.23715952816829669
		 10 0.4176029212700928 11 0.59734973600934993 12 0.70711630692972027 13 0.82891965180876837
		 14 0.92027709716273132 15 1.0140616964480653 16 1.0737228393554792 17 1.0440912697207312
		 18 1.0175870799269768 19 0.96094973219514157 20 0.90376301576293749 21 0.94752800746500143
		 22 1.0067327651549713 23 1.0678717987673825 24 1.1275264681891632 25 1.1088408852844178
		 26 1.0829003103742123 27 0.80108583670944766 28 0.41752867196273552 29 0.049302130936609699
		 30 -0.32917207043046548 31 -0.6245931914998758 32 -0.86093500964872949;
	setAttr ".pst" 3;
createNode animCurveTA -n "RootX_M_rotateY";
	rename -uid "078A4F92-4F73-3945-485F-FCB6BB9EEA09";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 5.2073850300217641 1 4.5560504798272632
		 2 3.4619628656116528 3 2.4593787717744404 4 1.4787602033647527 5 0.60212491892252074
		 6 -0.13230101228853991 7 -0.8661447391300926 8 -1.4813881244502261 9 -2.1741607041209994
		 10 -3.1257885933095921 11 -4.0150504156299451 12 -4.5997803123243077 13 -5.1319392958381433
		 14 -5.0972780186670379 15 -5.1015277555411176 16 -4.012301921844756 17 -3.6138358442583218
		 18 -3.2348231564740377 19 -2.6736079156853325 20 -2.1426889930267032 21 -1.3439532173756965
		 22 -0.5835098633192306 23 0.70305349562120567 24 2.1010498074088306 25 3.2634602524642871
		 26 4.3940954500690106 27 4.9431018692143915 28 5.2718970901406861 29 5.4450595419184786
		 30 5.5355370296449671 31 5.4540915145598854 32 5.2073850300217641;
	setAttr ".pst" 3;
createNode animCurveTA -n "RootX_M_rotateZ";
	rename -uid "D9B70ECC-43CD-C98B-0402-3191F04BCA1C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -5.7812927983303668 1 -5.2856490398773008
		 2 -4.3871837991233686 3 -3.6741849612220099 4 -3.1230454125821696 5 -2.865908375366788
		 6 -2.9578435417498632 7 -3.1693835798357881 8 -3.676860762003666 9 -4.0059282390860123
		 10 -3.8214166121303772 11 -3.5780044245949414 12 -2.7496508151580987 13 -1.9407199401677091
		 14 -1.1340812496560722 15 -0.10121281424760616 16 0.79093474149699872 17 0.37354010700626006
		 18 -0.030720733206484052 19 -0.89611725534263831 20 -1.7309572826124777 21 -2.1673165095366751
		 22 -2.510253524506787 23 -2.4416793037570446 24 -2.2958688837068384 25 -2.5326499111743002
		 26 -2.8972986704744721 27 -3.5617594100785266 28 -4.4269259819238265 29 -5.062038559172569
		 30 -5.7585996821822647 31 -5.9173381084583392 32 -5.7812927983303668;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKSpine1_M_rotateX";
	rename -uid "C280FE96-40A5-D011-3FBD-0FB3E2912EC7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -9.0590956739125481 1 -7.1899902073397968
		 2 -4.8986282108277353 3 -2.9321258131181041 4 -1.3043385152902707 5 0.081880814247663206
		 6 1.044788633699657 7 1.9600996894323868 8 2.5249046606696601 9 3.1307996274675336
		 10 3.737951872731093 11 4.2956479881047427 12 4.4940337190770077 13 4.681557346640175
		 14 3.9650928656080437 15 3.3511872719159719 16 0.1082051914573393 17 -1.580173767051444
		 18 -3.233060659382426 19 -4.9092586981569761 20 -6.5495553410358553 21 -8.024294104170739
		 22 -9.4018790780443489 23 -10.765969663103393 24 -12.176703662475253 25 -12.915308581021316
		 26 -13.534859292854097 27 -13.41464967206047 28 -13.086511788052475 29 -12.468172256257379
		 30 -11.741749676802202 31 -10.57032057150079 32 -9.0590956739125481;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKSpine1_M_rotateY";
	rename -uid "960D5F2E-4CA0-3A60-F4EE-1BB002AD207B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 6.5535423094468781 1 5.8846869489481035
		 2 4.9872046660236107 3 4.2654303845422739 4 3.7347261074075306 5 3.477456943386366
		 6 3.50160080747639 7 3.6453206560961107 8 4.1493790787592246 9 4.4484385975505303
		 10 4.0788968434659783 11 3.6847906628653324 12 2.809828522274231 13 1.9689667473685262
		 14 1.3924268816046443 15 0.58154746549972891 16 -0.058824570528947483 17 1.0248549676055101
		 18 2.0923302558951686 19 3.1893630050253892 20 4.2314192617266801 21 4.8235274846457914
		 22 5.3223447735133655 23 5.2391138232970622 24 5.0424071853818715 25 5.2727490304188764
		 26 5.6361987973604712 27 6.1468626391902648 28 6.8379292694263611 29 7.048192160168095
		 30 7.2007888475169901 31 7.0661626444919037 32 6.5535423094468781;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKSpine1_M_rotateZ";
	rename -uid "3B0B5FBC-4AE8-F2F7-4EFB-A5B16DEDAB55";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -8.8601102641377025 1 -8.2996589767513349
		 2 -7.8620552678947799 3 -7.5325119742444127 4 -7.3356701979616705 5 -7.2535275606993119
		 6 -7.33930741359619 7 -7.472239460819897 8 -7.7668935480345374 9 -8.0344241305865491
		 10 -8.2450054143278191 11 -8.4516448959128958 12 -8.5874779152939773 13 -8.723087239469363
		 14 -8.7867040518872486 15 -8.8446811850297404 16 -8.4003392374443351 17 -8.4689435178379444
		 18 -8.5682119356626565 19 -8.6177955688396395 20 -8.6818024790251105 21 -8.8455110934774908
		 22 -9.0079056564428264 23 -9.3740725328877197 24 -9.7764977993373332 25 -10.137461089393371
		 26 -10.501679051452633 27 -10.660538664649172 28 -10.741322707185727 29 -10.5470240473375
		 30 -10.111632323393119 31 -9.5518497912521543 32 -8.8601102641377025;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKChest_M_rotateX";
	rename -uid "9E2EC65E-4C3D-457A-51AE-F6BA3C285E50";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -6.1099049968378074e-05 1 6.5355757936888788e-05
		 2 -5.5247937516262947e-05 3 5.6319294185432715e-05 4 -0.00072199640879850875 5 0.001185704681924039
		 6 0.00057001528371486768 7 -0.0012568332430845741 8 -4.5201650372622819e-05 9 8.238077560128107e-05
		 10 -7.7848807459563101e-06 11 1.2553930083376832e-05 12 0.00058884764392211364 13 -0.003274214281915567
		 14 1.3608305316021062e-06 15 -6.2649971702733602e-06 16 2.8904438428152446e-13 17 -2.9688606984187461e-07
		 18 -3.6499009528399954e-06 19 9.2920971325166663e-07 20 9.1992954618064308e-05 21 -2.2357780534196798e-05
		 22 -1.0058974260055151e-05 23 1.1809085064227711e-05 24 3.9958128038026558e-05 25 -2.1337426425010858e-05
		 26 -0.0059502596580059547 27 0.0031216475328747538 28 0.0011558303808900548 29 -0.00079895242533717858
		 30 0.00010753641539602954 31 -0.00010815273938674649 32 -6.1099049968378074e-05;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKChest_M_rotateY";
	rename -uid "C7CC56FF-4868-436F-EC6B-119142CFA7CB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -3.3004726747620672e-05 1 5.9992680234069055e-05
		 2 -0.00012391625370137126 3 0.00014028013582492575 4 -0.0039679967613814099 5 0.00663819723974861
		 6 -0.0015205953133524527 7 0.0033046351021212722 8 0.0027579541864910526 9 -0.007822859885501094
		 10 1.6186555662307457e-05 11 -3.4929347244681567e-05 12 0.00027553386397082409 13 -0.0015297331522944671
		 14 -0.00029484500171554504 15 0.0025839590247633882 16 1.085464755035763e-13 17 -5.0023320679637758e-07
		 18 -1.0093686460800504e-05 19 2.5693528835416723e-06 20 0.00013282682250424698 21 -4.1043304357469132e-05
		 22 0.0067335301915603255 23 -0.0020522649339361873 24 0.0071590090306074029 25 -0.0029032148752937748
		 26 0.0028345062486093064 27 -0.0015165403951416974 28 0.0066622535343967655 29 -0.0045329705384332761
		 30 -0.0042081460104609909 31 0.0035364314041289903 32 -3.3004726747620672e-05;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKChest_M_rotateZ";
	rename -uid "0C77D53E-4C2C-171C-FC8A-4280E6B4BDE1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 1.6087968668946873 1 1.6081121626617962
		 2 1.6081841340518621 3 1.6088399553033998 4 1.6092070144761046 5 1.6070125985201023
		 6 1.6083862236790121 7 1.6086705404059336 8 1.608502592052157 9 1.6085643415055846
		 10 1.6084967146746236 11 1.6084930945215685 12 1.6084700304155723 13 1.6085450594345774
		 14 1.60849564195926 15 1.6084267934068672 16 1.6084872447027618 17 1.6084704855065983
		 18 1.6073446947000305 19 1.6086523407178848 20 1.604929125216308 21 1.6092574231378853
		 22 1.611448192749632 23 1.6076005279279968 24 1.6092150948700639 25 1.6081794023572604
		 26 1.6051727520094989 27 1.610242764834753 28 1.6176818204476937 29 1.6022941213570681
		 30 1.608469566548312 31 1.6083645919684835 32 1.6087968668946873;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKNeck_M_rotateX";
	rename -uid "70FECA1D-4C2E-533A-F32F-8D9EAFDB8962";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.33937670948234849 1 0.19892164680564364
		 2 0.097698661577558868 3 0.016806515574850713 4 -0.027434742500356542 5 -0.067100186544882603
		 6 -0.094112467515155077 7 -0.12008682496562667 8 -0.13694930310388326 9 -0.1464380642450174
		 10 -0.11111082828133539 11 -0.080344333987626901 12 -0.053771560836793568 13 -0.024542860491810359
		 14 0.035189920131162351 15 0.09465218403691944 16 0.32330720434141419 17 0.47953970935601586
		 18 0.63539434612215784 19 0.7297276471906704 20 0.8204061979175844 21 0.89701459105481185
		 22 0.97018033714349761 23 1.0174180086276927 24 1.0659506398835914 25 1.0510715210542048
		 26 1.0236103324069135 27 0.9734956804726147 28 0.92055290426221514 29 0.81355464187794579
		 30 0.67651871254933482 31 0.51923419417005556 32 0.33937670948234849;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKNeck_M_rotateY";
	rename -uid "771C8A2B-42DF-3C5B-9A43-20BB630799B7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.027502301970704836 1 0.026524629857257277
		 2 0.023637237305722397 3 0.038169177835940225 4 0.097536082344441055 5 0.15695728211790094
		 6 0.23377236047098024 7 0.30653615018486502 8 0.36368140847914121 9 0.42557647382445585
		 10 0.49787321534369045 11 0.55195991321058635 12 0.50670303619082913 13 0.46034289178604954
		 14 0.33715317318743809 15 0.2187687625168846 16 0.13748970542847222 17 -0.13723408602013903
		 18 -0.41117974388908596 19 -0.50827110211157567 20 -0.59387220471590207 21 -0.66864549093492487
		 22 -0.73941175701324491 23 -0.79974545721110635 24 -0.86554252748623306 25 -0.87476659413134772
		 26 -0.87588363941196679 27 -0.81629278037317932 28 -0.71748868715212766 29 -0.55525209182714252
		 30 -0.3468978624681508 31 -0.18084218509307323 32 -0.027502301970704836;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKNeck_M_rotateZ";
	rename -uid "85B699A2-4141-A8E0-1900-D09896DE108A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 21.367025535549441 1 21.407217492121742
		 2 21.474797527639346 3 21.493449481595725 4 21.459491052254204 5 21.413983516996076
		 6 21.334822094364775 7 21.272157920007452 8 21.255667458009398 9 21.231022633664729
		 10 21.192585094225851 11 21.155043360273279 12 21.117536914289733 13 21.077196998371655
		 14 21.001895069589693 15 20.928031328920834 16 20.79168882900041 17 20.983557474922648
		 18 21.17123864220185 19 21.395839254712708 20 21.634968665687161 21 21.668943118793777
		 22 21.683498048117858 23 21.615326290959327 24 21.522051872248834 25 21.437437375218423
		 26 21.344779869450363 27 21.329020626898096 28 21.328620004339978 29 21.330134171199386
		 30 21.332593169391721 31 21.34550843556687 32 21.367025535549441;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHead_M_rotateX";
	rename -uid "F211850A-47B3-8D1C-9C40-59AA032F4700";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.98231056939409189 1 0.60569985821730365
		 2 0.29248023931435913 3 0.062984806901200965 4 -0.036964830358059864 5 -0.12074283920719237
		 6 -0.15646364230344828 7 -0.19157154755850175 8 -0.20628547057813956 9 -0.20689516965152352
		 10 -0.052458687478402127 11 0.072943455921425079 12 0.12431019041021818 13 0.18423628915470844
		 14 0.29012854921263914 15 0.39830278840820982 16 1.0344942963371178 17 1.3422746433529533
		 18 1.6479625107722657 19 1.8727858701264024 20 2.0930023510431983 21 2.2778955109837522
		 22 2.4548907529105408 23 2.56089621353828 24 2.6670813827843483 25 2.6183921014678995
		 26 2.5305089862476007 27 2.423717197450423 28 2.3208753709534902 29 2.0963660820807393
		 30 1.8091891449712583 31 1.4362817177558591 32 0.98231056939409189;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHead_M_rotateY";
	rename -uid "5E172C3F-4553-A34B-6654-F1912139F9D5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.25826897806517796 1 -0.14679730809377883
		 2 -0.12612534406186671 3 -0.080636737306736941 4 -0.013609647985206058 5 0.055360564269715966
		 6 0.13693639016540232 7 0.21416361798879463 8 0.27318718111606927 9 0.33431782260215459
		 10 0.39295729302060028 11 0.43695054293114882 12 0.38422362260341453 13 0.33077545220898669
		 14 0.19385974969233605 15 0.061511935242394955 16 -0.093241183794545143 17 -0.40582748548831932
		 18 -0.71688217115819397 19 -0.83786257880592963 20 -0.94592887488446564 21 -1.0414894055075914
		 22 -1.1323563527569229 23 -1.2063214968681029 24 -1.2874651141986322 25 -1.2912140116475821
		 26 -1.2863581049976613 27 -1.2118378063154134 28 -1.1006751434173148 29 -0.91076362120881449
		 30 -0.66701713224821635 31 -0.45690439549025735 32 -0.25826897806517796;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHead_M_rotateZ";
	rename -uid "F6A2CDFC-4796-E867-D32A-9DA9CDB02F90";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -12.72644852939375 1 -12.687711123345792
		 2 -12.620873209009023 3 -12.602608774806919 4 -12.637057145621579 5 -12.682426754281305
		 6 -12.760446323446937 7 -12.822312954986753 8 -12.838517655427658 9 -12.863010848552314
		 10 -12.902122173599755 11 -12.940237871620736 12 -12.977705032220999 13 -13.01798781752775
		 14 -13.093047193654185 15 -13.16656332997983 16 -13.302200953287921 17 -13.107595458582411
		 18 -12.916345713123267 19 -12.689520145489166 20 -12.448443631224366 21 -12.411533117095859
		 22 -12.394380499405697 23 -12.461086073637825 24 -12.552374228829605 25 -12.637272223183107
		 26 -12.729999612662576 27 -12.748833859669999 28 -12.751142920192075 29 -12.752905005220487
		 30 -12.753899018558974 31 -12.745924730769605 32 -12.72644852939375;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_R_rotateX";
	rename -uid "B265B958-4376-8D21-3361-5CB5C6FCD7A8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 14.150768274773863 1 6.6266629559137051
		 2 -0.85564752548312806 3 -6.9723208790083477 4 -11.433229224498644 5 -14.821378752434496
		 6 -17.17257259326459 7 -18.942066058877767 8 -19.594266610339364 9 -20.168738697436627
		 10 -19.606759049822184 11 -18.973646996956802 12 -17.223976262672746 13 -15.117280871642981
		 14 -11.860328871586635 15 -8.0742621380726209 16 2.8339480425161279 17 9.0131956860022342
		 18 14.464184054247749 19 19.436373505582527 20 23.759908544301531 21 26.858140516205054
		 22 29.483428559414637 23 31.311144438456811 24 33.039011382628622 25 33.883852370751555
		 26 34.584556442462009 27 34.060369985781143 28 32.956326185587635 29 30.413980761701687
		 30 26.502084693179945 31 21.098212589534231 32 14.150768274773863;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_R_rotateY";
	rename -uid "825DCF5E-46CA-3423-24BF-908BA2CDD245";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 73.884013323429215 1 74.095851865613128
		 2 73.691950340160645 3 72.961231205624742 4 72.006028037280785 5 71.028931953733434
		 6 70.254515776436847 7 69.591285417630573 8 69.76610219521271 9 69.914253626961582
		 10 70.406652805387992 11 70.944657973822558 12 72.000784502420814 13 72.95677858553708
		 14 73.855096189084833 15 74.616153639997336 16 74.702907183630245 17 74.097137912436679
		 18 73.293113283909392 19 72.326568938132809 20 71.194965869514945 21 70.317595971428204
		 22 69.432284730949092 23 68.9859759045967 24 68.56783241415377 25 68.50545612543057
		 26 68.54650286379497 27 69.017754843744783 28 69.799159336793338 29 70.899273229033469
		 30 72.100992507392789 31 73.141296648247732 32 73.884013323429215;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_R_rotateZ";
	rename -uid "03A8CF52-494E-5821-D145-CE9E6ACC6554";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -28.82406918977459 1 -18.346964408121625
		 2 -7.7977447397618942 3 1.225929208646563 4 8.4302666423178145 5 14.323863984315629
		 6 18.882453224698988 7 22.51482754680298 8 23.723741246223124 9 24.723226522892087
		 10 23.406456534597059 11 21.944293862795625 12 18.276059638922749 13 14.279534715289129
		 14 8.6733402406125357 15 2.5482318716670234 16 -13.106842609059367 17 -21.638616030807274
		 18 -29.382379132206143 19 -36.525684817925175 20 -43.019785927595606 21 -47.779533428377349
		 22 -51.967567448541111 23 -54.752595268947253 24 -57.376183577584925 25 -58.578782267701044
		 26 -59.507005884896586 27 -58.538573453895715 28 -56.666150117349829 29 -52.528217631787776
		 30 -46.547511123985153 31 -38.645327855030693 32 -28.82406918977459;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_R_rotateX";
	rename -uid "75C56FF9-4A25-B1E3-FCAD-5BBA229F486F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -32.394446670078089 1 -30.777274662571457
		 2 -28.740181596873853 3 -26.53550777000271 4 -23.966078165245236 5 -21.545415945442169
		 6 -19.136782315750796 7 -17.089528034840345 8 -16.299760443827836 9 -15.706028933885483
		 10 -16.469778364681112 11 -17.332739556945057 12 -19.47526692445571 13 -21.594682507354733
		 14 -24.329943599323414 15 -27.05909785831571 16 -30.869507155749698 17 -31.680571147541404
		 18 -32.446060796461786 19 -32.737672845161477 20 -32.990285532140661 21 -33.113038035878233
		 22 -33.222513627471365 23 -33.250488924153764 24 -33.275890221168133 25 -33.398821337956541
		 26 -33.533493702654475 27 -33.92157147023223 28 -34.447142827433794 29 -34.506312827922159
		 30 -34.345729989907149 31 -33.588971998908498 32 -32.394446670078089;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_R_rotateY";
	rename -uid "B3EDF662-4392-D1E0-BD15-C3933B57F61B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.86743038183742915 1 -0.54449058033050202
		 2 -0.39168632363960892 3 -0.24773310736534382 4 -0.14791712436002269 5 -0.035814209876873573
		 6 0.061615470672265173 7 0.12377127830697145 8 -0.042310684911187349 9 -0.14269407364326891
		 10 -0.17833309430717534 11 -0.22882747079827101 12 -0.41116413854697809 13 -0.56718475108926147
		 14 -1.0067318682761595 15 -1.3425575609633962 16 -2.5695235213671994 17 -3.1845589866074482
		 18 -3.8135793686829711 19 -3.8943781892175005 20 -3.9494934230100887 21 -4.1289530400303462
		 22 -4.3191752145007918 23 -4.4868702401652101 24 -4.6715582237800941 25 -4.6257530199505119
		 26 -4.5494149154927834 27 -4.1531646641505748 28 -3.6502978681187601 29 -2.9582299359399582
		 30 -2.1026928656355595 31 -1.4446358005999249 32 -0.86743038183742915;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_R_rotateZ";
	rename -uid "E1A3BA1C-4CDB-4ED3-6938-7E90AAAC2497";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 20.444526613972382 1 21.757474542852467
		 2 23.004135246293703 3 24.463644969736631 4 26.2229192982049 5 28.06812156905843
		 6 30.286804695607131 7 32.227084421401436 8 33.275574127481093 9 34.032653120342495
		 10 33.387480944336581 11 32.590268927432106 12 30.22212775696936 13 27.938227682020756
		 14 25.409742511672256 15 22.895954593563175 16 19.768597942352656 17 19.866180663005714
		 18 19.94188927616926 19 20.343023376865009 20 20.798820579239099 21 20.53726597604707
		 22 20.232974456043674 23 19.328877391414281 24 18.289628088657828 25 17.577550413441223
		 26 16.935806317769192 27 16.622831470563753 28 16.427344937053075 29 16.875054237548131
		 30 17.902224322972071 31 19.078075395176668 32 20.444526613972382;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_R_rotateX";
	rename -uid "141FB618-4847-7F17-E089-2EBF821B9F97";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 8.7983879196947079 1 9.8081037180117256
		 2 10.800239537890658 3 11.676424351583995 4 12.378719442152564 5 12.987533025774091
		 6 13.443615182863047 7 13.743084080932835 8 13.746186517540906 9 13.747216606647916
		 10 13.700512458288301 11 13.621041160532645 12 13.161875702947667 13 12.681929475493284
		 14 11.527713462915797 15 10.402427436782444 16 7.5345243399873914 17 6.529504053319056
		 18 5.5276364272429142 19 5.1441605751072128 20 4.7947166250145949 21 4.6102688616357179
		 22 4.4361108906817535 23 4.4758500187974422 24 4.5449976148988247 25 4.6425308373776977
		 26 4.7425442703953422 27 5.0460671808867623 28 5.4151067336352607 29 6.0595240477943095
		 30 6.8512736944401533 31 7.7677330927615635 32 8.7983879196947079;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_R_rotateY";
	rename -uid "1C820F5D-4CCC-FA89-F048-A59741D7569E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 4.0801535606578616 1 3.0568986433979788
		 2 2.4583296141563458 3 2.1468618527985561 4 2.0946297175502382 5 2.0229110295081441
		 6 1.7807853268047318 7 1.6499741021358982 8 1.6493065365283515 9 1.6698820515583788
		 10 1.9633874929836697 11 2.1994042994093839 12 2.2833822960631269 13 2.4119357457480692
		 14 2.8822714132771035 15 3.3743856919042403 16 5.5079984300307876 17 5.8174311494365023
		 18 6.1191008507199633 19 6.6144507609545649 20 7.1123915274514253 21 7.7377485704240803
		 22 8.369768420430205 23 8.7861465662590561 24 9.1784437980979021 25 9.4080916433165473
		 26 9.6132633478275125 27 9.4481816512031749 28 9.1788558877434916 29 8.2431546719162103
		 30 6.9241986194799958 31 5.5594059100172748 32 4.0801535606578616;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_R_rotateZ";
	rename -uid "6CAB0BA9-4EC4-1A7F-43D7-11B5EE21D1D1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -3.7665334564744892 1 -3.1615749856880275
		 2 -2.5930537571202588 3 -1.9195689628792656 4 -1.1089104165935557 5 -0.29677322884331137
		 6 0.63862918007430314 7 1.2731777744204518 8 1.3222564146003233 9 1.3289428003248409
		 10 0.74251793124848553 11 0.16696076973126259 12 -0.80998194269452872 13 -1.760642616462361
		 14 -2.7229739210621271 15 -3.6706694955494985 16 -5.0063387761345961 17 -5.1092109735024511
		 18 -5.2072502338925002 19 -5.1552054039972699 20 -5.0927063489237687 21 -4.990952324165991
		 22 -4.871656922711348 23 -5.0988684743514021 24 -5.4213197553668735 25 -5.6358202238580608
		 26 -5.8291128660462981 27 -5.9215764625725082 28 -5.9755492205472978 29 -5.6724809323253256
		 30 -4.9821540482386366 31 -4.3731034946847736 32 -3.7665334564744892;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_R_rotateX";
	rename -uid "571204EC-4363-BD22-9415-9FBADB5261E7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 359.36140793146848 1 359.67517750012684
		 2 360.06429395856242 3 360.37335531110438 4 360.51914444700753 5 360.66634570436196
		 6 360.86721400425006 7 361.08848688395659 8 361.34746318010826 9 361.56944823507928
		 10 361.60936568572197 11 361.60393821653656 12 361.0997735133268 13 360.76141828619592
		 14 360.57807299855949 15 0.63637662440650189 16 1.6549486141928149 17 1.9219888438168884
		 18 2.1230452087964178 19 1.5884323154968132 20 0.96948274095683162 21 360.30576665710629
		 22 359.7124769362091 23 359.5741928811222 24 359.50409943190522 25 359.52821270593734
		 26 359.58031829497924 27 359.41757457046504 28 359.14046668270078 29 359.02815578748584
		 30 359.01061149585013 31 359.09493647906567 32 359.36140793146848;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_R_rotateY";
	rename -uid "EB36E867-4C8A-EBC8-B64E-D18F7DBB5A86";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 9.5584031347753804 1 9.6945387698317713
		 2 9.136107239922973 3 8.7088862394801083 4 8.3608198763366772 5 8.2038337720716239
		 6 8.5118417577621202 7 8.8677253955975903 8 9.4175457655101873 9 9.6992149847039322
		 10 8.6072736278198736 11 7.4205403553318732 12 4.864692570542104 13 2.4044272355066427
		 14 0.2510777978115265 15 -2.0485193500354577 16 -4.0404130112194014 17 -3.2078718960024668
		 18 -2.3215382955941224 19 -1.1588498056306187 20 -0.041619116161505931 21 0.41876905232136002
		 22 0.78608379707950238 23 0.77891409680555601 24 0.77694310889745799 25 0.9872611698832684
		 26 1.2226017217395877 27 2.4574226766243914 28 4.1563608936735301 29 5.8082131367165761
		 30 7.6311424271840078 31 8.8105798181671204 32 9.5584031347753804;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_R_rotateZ";
	rename -uid "2FAF31E0-448A-1A7A-DA69-50A80851C7AC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 9.7006584170730203 1 6.9528828928507282
		 2 2.7070223109069707 3 -1.5711836787315652 4 -4.7351741333778197 5 -7.1792936605177644
		 6 -8.939756519924364 7 -10.750245553962319 8 -12.421425190145648 9 -14.056338353351801
		 10 -15.869575523768459 11 -17.159003523115427 12 -14.57161811614362 13 -12.09328811843112
		 14 -5.5209327136739104 15 1.0937561413785308 16 14.450318849818006 17 18.878683374342387
		 18 23.274089918265108 19 25.004535861146643 20 26.691225272076924 21 25.829769075753024
		 22 24.727056521687402 23 23.846737538643463 24 23.00392677478434 25 22.399041230159472
		 26 21.993265721327582 27 20.165180100238864 28 17.968181391169303 29 15.314272786063258
		 30 12.870510508550028 31 11.282284851876341 32 9.7006584170730203;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_R_rotateX";
	rename -uid "27CBD2AD-4BD0-12BC-0659-BBB86F7D15FA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.5136123692093737 1 0.82017736726291102
		 2 0.90343938058693407 3 0.87234788250083861 4 0.63731818465314916 5 0.57915802768738323
		 6 0.74832243543306043 7 0.92637784599804784 8 1.1597331987060868 9 1.3599583826805011
		 10 1.4572169767538337 11 1.5372445202850571 12 1.4327735369835155 13 1.4314645253639464
		 14 1.5976586294928936 15 1.8246932690261977 16 3.2016491472590589 17 4.1984689645732498
		 18 5.2465308022775163 19 4.8047052042806273 20 4.1533005313698954 21 2.1854297635581892
		 22 0.20070121133469029 23 -0.58212603699921306 24 -0.99264088493081359 25 -0.82276960779917219
		 26 -0.46878864272418747 27 -0.46371200503005272 28 -0.55988163367432942 29 -0.52656661860244247
		 30 -0.38494316853105842 31 -0.014875086073532898 32 0.5136123692093737;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_R_rotateY";
	rename -uid "36C1B06A-4EFB-6E40-F35A-FDB5701C8663";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -1.2403683685139779 1 -1.272654742813133
		 2 -0.9854976011321317 3 -0.75431567829973967 4 -0.65770108806309957 5 -0.67387707311616452
		 6 -0.971189511879473 7 -1.3329026030683244 8 -1.9689464480277765 9 -2.4725398096951148
		 10 -2.5420073998647981 11 -2.5787268075156007 12 -1.7770508565735312 13 -1.0755631059229742
		 14 -0.39669693809008638 15 -0.012925709461533328 16 -0.2916670003768092 17 0.25188808949607627
		 18 0.70876069492233973 19 1.9671463383048864 20 3.4189140818535617 21 3.431077086205732
		 22 2.8567569404249329 23 1.6940997382693583 24 0.19138198028270698 25 -0.20640954279006291
		 26 -0.3976719542039111 27 -0.3922101231841662 28 -0.33268947488933232 29 -0.39128991269045271
		 30 -0.59881212196119038 31 -0.90035738660477271 32 -1.2403683685139779;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_R_rotateZ";
	rename -uid "7481F2D5-4DEF-7C6B-DC42-C2B9E28364F4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -13.580912475852312 1 -12.908759071282095
		 2 -8.3141221171398083 3 -3.4526907217005181 4 -0.19310359293932708 5 1.4007632421615339
		 6 1.539945761146599 7 1.5840948340602206 8 1.3966685438452535 9 0.99940309351568057
		 10 0.68471711406950853 11 -0.11488491484453754 12 -8.12876351793801 13 -15.3022291686671
		 14 -26.398946026419306 15 -37.666743707156556 16 -55.079119909266723 17 -56.572118057429456
		 18 -58.070012366536062 19 -52.634483097017693 20 -46.83271826075184 21 -36.154977610654115
		 22 -25.034408085036805 23 -17.237330873093246 24 -9.2496589785137839 25 -7.9876935271621781
		 26 -7.6083542254178846 27 -7.9772653239278277 28 -9.1309581263251083 29 -9.3670718183266928
		 30 -10.025817972006225 31 -12.040005473721592 32 -13.580912475852312;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_R_rotateX";
	rename -uid "711ED5EC-4B7B-C175-2F18-79A95FEBFDAB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 370.36366833724321 1 369.31275004702775
		 2 368.0724931365117 3 367.11201844785046 4 366.48860208674023 5 365.90666908361703
		 6 365.45012204598527 7 364.95536593507109 8 364.44443236543731 9 363.91441030872176
		 10 363.34900704814555 11 362.93504613333641 12 363.23478389914868 13 363.60709576045281
		 14 365.03339066273662 15 366.47433746841688 16 370.1155116084372 17 370.26300979833343
		 18 370.66362523846453 19 371.51966647244353 20 372.21840259512925 21 373.33601537902791
		 22 374.29204747929259 23 373.74553547422119 24 372.63836548185776 25 372.1419811676962
		 26 371.76968892891205 27 371.89963481771076 28 372.33062724125989 29 372.25952790465379
		 30 371.97476800448209 31 371.31163318857324 32 370.36366833724321;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_R_rotateY";
	rename -uid "5ED0CBA9-4A71-7647-C1F9-898C4C4CE1FD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -2.583462592745648 1 -3.2241359816440065
		 2 -3.6751615432846103 3 -4.4654113757804295 4 -4.9964155740511877 5 -4.9730146767507
		 6 -4.6841335373152564 7 -4.2699828992979336 8 -3.4763330350718933 9 -2.5534573766735345
		 10 -1.0421597525879041 11 0.5592451395762299 12 3.1717435297103567 13 5.5677665235149068
		 14 6.1369499386081836 15 7.0830773156341458 16 7.3947820591633517 17 4.2565427072884399
		 18 1.0544171114500167 19 2.7280850626426409 20 4.509891855155435 21 6.7931024909360689
		 22 9.3146048352268647 23 5.8309887253831283 24 0.64594006146443017 25 -1.2503882076093615
		 26 -2.4046590035845599 27 -2.3546211240445603 28 -1.7955328965066177 29 -1.9649302744480257
		 30 -2.1457269545634996 31 -2.1213490354477402 32 -2.583462592745648;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_R_rotateZ";
	rename -uid "C6F7AE3E-4984-7681-6962-E88786EA66DD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 3.3565566232009796 1 4.8728488665372574
		 2 4.7327967698073161 3 4.1589432411735601 4 4.0192161788848102 5 4.2527480380466152
		 6 5.7131334418637563 7 6.9540043193361161 8 7.8792181670715529 9 8.5428600752408155
		 10 7.4239092122644177 11 6.3379523802558575 12 4.7365390323855747 13 2.4342652962001932
		 14 -7.0993097175028055 15 -15.978438302227268 16 -21.949483280420178 17 -17.110967388720766
		 18 -12.406733906493306 19 -6.2544871069451382 20 0.086170641065148754 21 2.7779399206638766
		 22 5.0753683644980123 23 3.7055745231941497 24 1.7684011395416976 25 0.46662635771747174
		 26 -0.63420081508546455 27 -2.0900429154520155 28 -3.789724341130511 29 -3.6742278640173516
		 30 -2.3709115010207227 31 0.10655629596071121 32 3.3565566232009796;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_R_rotateX";
	rename -uid "C111D8FF-47B1-450F-3DF7-66B75864A463";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 359.50655509576586 1 359.50655509576586
		 2 359.50655509576586 3 359.50655509576586 4 359.50655509576586 5 359.50655509576586
		 6 359.50655509576586 7 359.50655509576586 8 359.50655509576586 9 359.50655509576586
		 10 359.50655509576586 11 359.50655509576586 12 359.50655509576586 13 359.50655509576586
		 14 359.50655509576586 15 359.50655509576586 16 359.50655509576586 17 359.50655509576586
		 18 359.50655509576586 19 359.50655509576586 20 359.50655509576586 21 359.50655509576586
		 22 359.50655509576586 23 359.50655509576586 24 359.50655509576586 25 359.50655509576586
		 26 359.50655509576586 27 359.50655509576586 28 359.50655509576586 29 359.50655509576586
		 30 359.50655509576586 31 359.50655509576586 32 359.50655509576586;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_R_rotateY";
	rename -uid "7B1515AE-416B-CA87-8D52-47B6F7C56C1A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.077235056997522783 1 -0.077235056997522991
		 2 -0.07723505699754793 3 -0.077235056997523158 4 -0.077235056997497803 5 -0.077235056997548651
		 6 -0.077235056997548332 7 -0.077235056997548707 8 -0.077235056997497636 9 -0.077235056997523796
		 10 -0.077235056997524004 11 -0.07723505699752492 12 -0.077235056997551135 13 -0.077235056997552606
		 14 -0.077235056997528764 15 -0.077235056997529708 16 -0.077235056997528473 17 -0.077235056997527002
		 18 -0.077235056997551843 19 -0.077235056997551052 20 -0.077235056997549859 21 -0.077235056997523061
		 22 -0.077235056997523255 23 -0.077235056997523019 24 -0.077235056997548263 25 -0.077235056997548221
		 26 -0.077235056997523324 27 -0.077235056997522575 28 -0.077235056997522838 29 -0.07723505699754793
		 30 -0.077235056997522741 31 -0.077235056997497553 32 -0.077235056997522783;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_R_rotateZ";
	rename -uid "A7948D58-4407-4674-A12C-9DA52595D247";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -7.9956234268828705 1 -8.0040460228339008
		 2 -7.9793793467141052 3 -7.9811797871374637 4 -7.5629548291949522 5 -7.0967587953186255
		 6 -6.4240074824276796 7 -5.5877880373015616 8 -4.354775178843779 9 -2.6851346347873988
		 10 0.90033049085183026 11 4.992827419550002 12 13.414136549662848 13 21.959515816981465
		 14 37.156698982710793 15 47.349885754233007 16 34.490529986320681 17 26.092958788027246
		 18 17.788189643820328 19 9.3154416231266417 20 0.37145255241223002 21 -3.9502359628096353
		 22 -7.8520845761518787 23 -8.0715126350601416 24 -8.071919688790997 25 -8.0728536094605499
		 26 -8.0738135646943725 27 -8.0752870166644577 28 -8.0769350491112402 29 -8.0786747847060258
		 30 -8.0801164073935112 31 -7.9859495063355705 32 -7.9956234268828705;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_L_rotateX";
	rename -uid "47999D5F-42B7-2724-0014-54B81172C84F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 11.724572882481176 1 17.681736831112531
		 2 22.035787850481157 3 24.799060935640476 4 26.352844407283445 5 27.335991527613757
		 6 27.77156811403734 7 28.011589692510125 8 27.949388293066296 9 27.977621435549302
		 10 28.909776832549149 11 29.564448465398154 12 29.012883696242564 13 28.104419785082133
		 14 24.167394184000695 15 19.026796134164091 16 -3.9300144137999946 17 -9.968548559097135
		 18 -16.107565501312333 19 -19.677276754245334 20 -22.756874355816485 21 -23.879480143908363
		 22 -24.511394035856441 23 -24.972832275422682 24 -25.351549799332432 25 -25.524116387924831
		 26 -25.706370023947212 27 -23.949342704628695 28 -20.866198642533199 29 -13.781237746669749
		 30 -4.8804226759342457 31 4.0768846751364967 32 11.724572882481176;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_L_rotateY";
	rename -uid "153589F7-48CA-90D9-55BF-7A86ED59B1D8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 78.700159483277488 1 77.289593075759058
		 2 75.563107622648914 3 73.86353547280531 4 72.239811810861724 5 70.745829595307043
		 6 69.452673773930428 7 68.293204744193375 8 67.723236351785943 9 67.365187169598215
		 10 68.517227863115281 11 69.606672973847637 12 71.206338529344464 13 72.788063529112307
		 14 74.576347923981302 15 76.222587074476692 16 77.929013708514148 17 78.049979611222852
		 18 78.043527139095886 19 77.525184744428657 20 76.914952298628251 21 76.295772976164386
		 22 75.624983321884798 23 75.506741164814414 24 75.420214800041606 25 75.991475957921381
		 26 76.756739046209589 27 78.032670711784959 28 79.563689602694325 29 80.175438772025046
		 30 80.279138967981922 31 79.751850827336639 32 78.700159483277488;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_L_rotateZ";
	rename -uid "8DF1D51C-4392-FCDD-92BF-E9924EF3C015";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -23.392047505979651 1 -31.552203751238579
		 2 -38.092606746605007 3 -42.858851534901497 4 -46.178766038418082 5 -48.786725826213029
		 6 -50.642969589380009 7 -52.153588081609314 8 -52.716488349884024 9 -53.148772057922095
		 10 -52.963348728392049 11 -52.531438130849672 12 -50.262919015506959 13 -47.627483542252101
		 14 -41.259646086281229 15 -33.70057935555824 16 -3.8547254526249364 17 3.2759764216097005
		 18 10.527212086867495 19 15.409581803995623 20 19.80943363613147 21 22.112676177927941
		 22 23.881985909626515 23 24.925270248062191 24 25.855532214875428 25 25.76038414639396
		 26 25.529480707081557 27 22.503352893808415 28 17.83648880039523 29 8.7832012655685983
		 30 -2.3469706738983356 31 -13.51816286470515 32 -23.392047505979651;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_L_rotateX";
	rename -uid "C4A5B1D6-4B76-9CB4-EC1B-79B9BDB35885";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -34.443658353063505 1 -35.038180877124645
		 2 -35.346494689597698 3 -35.657072594079132 4 -35.926339501505417 5 -36.244258035296205
		 6 -36.69187878216087 7 -37.082145126106369 8 -37.339650870702535 9 -37.445833922453851
		 10 -36.478782123458224 11 -35.659902230362661 12 -35.136897689509979 13 -34.613008285431121
		 14 -34.324520011326747 15 -34.001757492630546 16 -32.028751060877454 17 -32.92125762118534
		 18 -33.791409970599361 19 -32.779990944889107 20 -31.648453489852322 21 -29.908887209242589
		 22 -28.057539936759746 23 -27.128265870004338 24 -26.205405390624392 25 -26.521553302688215
		 26 -27.056761633611575 27 -28.19552816036876 28 -29.56390369768426 29 -30.982363053028536
		 30 -32.466401064992318 31 -33.576435780656929 32 -34.443658353063505;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_L_rotateY";
	rename -uid "8914DBBE-4A28-C001-A3D4-74B5840C26AE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.40893261469702746 1 0.42334970142944883
		 2 0.25806129052742405 3 0.19218027543215124 4 0.22885742121274194 5 0.35765807149191386
		 6 0.69892300642388361 7 1.0351312062222655 8 1.396494930589999 9 1.6350494500524755
		 10 1.40908376299937 11 1.1941471322116999 12 0.88980564390667538 13 0.58173504884485105
		 14 0.19403598577950207 15 -0.19850424485151044 16 -1.8180212546773209 17 -2.0940656195632856
		 18 -2.3534693151441339 19 -3.2459011233151478 20 -4.1695095590370999 21 -4.7722620747878111
		 22 -5.3892255733596937 23 -5.2182213799896608 24 -4.9890319735528319 25 -4.4774853679120925
		 26 -3.8265773910196543 27 -2.8827324408231876 28 -1.7882072583727662 29 -0.96654540233057828
		 30 -0.24194244390153888 31 0.19221420001935563 32 0.40893261469702746;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_L_rotateZ";
	rename -uid "8A554A22-4FFD-CBD3-96C9-B485C3C6917E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 19.404188444339642 1 19.022403430610087
		 2 19.076207953890442 3 19.056939649485212 4 18.930027498448187 5 18.58217493654108
		 6 17.618764581561891 7 16.711933055993928 8 15.855111288293974 9 14.963056402552239
		 10 14.022585079709421 11 13.100536286682626 12 12.295265823491304 13 11.532620008102739
		 14 11.384370769523688 15 11.214692239736317 16 11.515588114608462 17 13.315568998384201
		 18 15.069801847101004 19 17.433739877682097 20 19.811014558960338 21 22.64955956794827
		 22 25.514440616616795 23 27.309674381405252 24 29.149284832042174 25 29.258601814278176
		 26 29.171605928363338 27 28.105955006560304 28 26.426334639399652 29 24.414648717911525
		 30 22.056910064879073 31 20.495136557013353 32 19.404188444339642;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_L_rotateX";
	rename -uid "E0CE433C-4CB1-9758-A27B-27B3B464EDD5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 3.5910110794208872 1 3.4260804034907122
		 2 3.2393316115224007 3 3.0825577536274156 4 2.9692275833571116 5 2.9133880129314278
		 6 2.9566412329900249 7 3.0357593341349225 8 3.2323732564229526 9 3.4060243909804102
		 10 3.5208295312745834 11 3.6377321273157657 12 3.7408672498478146 13 3.8423818620701087
		 14 3.9051541856925467 15 3.9684392488179139 16 3.8496862574792798 17 3.7947532898156102
		 18 3.7377696929083495 19 3.7316915977856349 20 3.7290192923990308 21 3.5027657020898797
		 22 3.2216464663325635 23 3.1242087888597592 24 3.0497722487616552 25 3.1587692535282832
		 26 3.3296254063303969 27 3.5523002314299208 28 3.83165009954191 29 3.8787202307417985
		 30 3.8680691993395384 31 3.77015322671943 32 3.5910110794208872;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_L_rotateY";
	rename -uid "251FBA6A-4F58-A0B9-5039-189899E4476D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.63991496186001795 1 2.1899933052334566
		 2 4.7580194037888877 3 6.9300964328137526 4 8.8879327346986923 5 9.828597436188204
		 6 9.553047940868991 7 9.3040667556428591 8 9.0367065511938005 9 8.7475243009490296
		 10 8.381171547407904 11 8.0567612312341605 12 7.9911356489511434 13 7.8814429205578298
		 14 7.3569272716426255 15 6.8300385659986604 16 3.4332840053333338 17 2.0348956094052406
		 18 0.64310119354634865 19 0.029145900709572004 20 -0.54895440624740488 21 -0.68800442762374237
		 22 -0.76767719270690837 23 -0.73072294540185279 24 -0.67859907250820461 25 -0.63549019091289261
		 26 -0.59014149390691595 27 -0.70705193829266066 28 -0.94894569950231955 29 -0.83457450712373316
		 30 -0.51233535143181486 31 0.020098834536061316 32 0.63991496186001795;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_L_rotateZ";
	rename -uid "B866E99C-4C49-1F34-FC88-34BB396A2881";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -3.3624865884024873 1 -3.2613701831545252
		 2 -2.8488696534122866 3 -2.5137771427783284 4 -2.1961001944653904 5 -2.0540354569631747
		 6 -2.1626323933253779 7 -2.3251258791591285 8 -2.6817135266468042 9 -2.9768146588637148
		 10 -3.0612077818572798 11 -3.1566334244106455 12 -3.2216390910416206 13 -3.2764910102555294
		 14 -3.1376733830610379 15 -3.0047076011153964 16 -2.3235554634895523 17 -2.4274095052673328
		 18 -2.5366070901025717 19 -2.5159174908669621 20 -2.4882376397271231 21 -2.5070486342373579
		 22 -2.5257003963140621 23 -2.6740281246760156 24 -2.862035338473444 25 -2.9317918173020914
		 26 -2.9664284780086008 27 -3.032885156273629 28 -3.1100875844540807 29 -3.1729541573570152
		 30 -3.2281897548000953 31 -3.2909065522278329 32 -3.3624865884024873;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_L_rotateX";
	rename -uid "29C3DF93-4518-98BD-6540-168D70FC0414";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 1.5332592731336376 1 1.8873145869568122
		 2 1.9177185650323763 3 1.7255927382317227 4 0.90245299246114385 5 0.4009055293177487
		 6 0.31963128166961458 7 0.30311038952356401 8 0.65327007192655406 9 0.85341822685258162
		 10 0.57231095586333458 11 0.26421079989621044 12 -0.40200467849048965 13 -0.99439442716819759
		 14 358.5853489962098 15 358.16185531151143 16 357.71551396376043 17 357.95320873194254
		 18 358.24884950871819 19 358.44183423109581 20 358.55614911272244 21 358.68765590780913
		 22 358.72370479542104 23 359.02549251418475 24 359.41192996732599 25 -0.33608765150182074
		 26 -0.16583179780758106 27 0.031422474109737621 28 0.2614073845664393 29 0.4273354422959188
		 30 0.57661839296905815 31 0.95456104222502969 32 1.5332592731336376;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_L_rotateY";
	rename -uid "E1AF7C8F-4AE6-7C6B-2AE9-CCBF8532406C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -9.4076271253693058 1 -8.380287512901571
		 2 -6.637908839935708 3 -5.321726917480496 4 -4.4617743623378185 5 -4.0390270553320837
		 6 -4.043473376490728 7 -4.14498568572193 8 -4.5749236530874899 9 -4.8010765738011623
		 10 -4.0549656771469795 11 -3.3108381070981374 12 -1.9137767251474911 13 -0.48661228975561543
		 14 1.2919602231475724 15 3.3046655486159082 16 6.654037412414155 17 6.7471554063310357
		 18 6.7040469851434121 19 5.4108432965393423 20 4.077173399275047 21 2.5774290681326009
		 22 1.1191557304356539 23 0.71289068516021448 24 0.53362745753961993 25 -0.85192330377461667
		 26 -2.5873747184113127 27 -4.5090341923247514 28 -6.5769833408365859 29 -8.0754107427841184
		 30 -9.4852614634958066 31 -9.7562325712744045 32 -9.4076271253693058;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_L_rotateZ";
	rename -uid "9AEEC514-42C5-060C-06A4-65B739537734";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 9.1827768656741391 1 13.459470544118167
		 2 16.237815654853456 3 17.959086705166687 4 18.233005605306769 5 18.580443837920551
		 6 18.888994696928531 7 19.654470762765676 8 21.432761651675953 9 22.924882313232747
		 10 23.318242300924481 11 23.581140167277116 12 21.044779091012316 13 18.854960638124272
		 14 17.136559264264005 15 16.079351438164636 16 14.850957629767521 17 12.065265287423259
		 18 8.9094440551685743 19 4.9657495104896174 20 0.60278158753337563 21 -3.6415137716236901
		 22 -7.6970989560127858 23 -11.730270149556176 24 -15.327685908821991 25 -17.505404820642447
		 26 -19.532333375920185 27 -17.342332910128135 28 -13.433659290156628 29 -8.5042802419678054
		 30 -2.4490683282743908 31 3.379558206214571 32 9.1827768656741391;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_L_rotateX";
	rename -uid "C6157AB2-4990-4697-A219-0986641A9E46";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 358.33588843962553 1 358.39217622793524
		 2 358.87081089714371 3 359.04215962309905 4 359.00816808887151 5 358.97765376846604
		 6 359.2307847358565 7 359.41075630113306 8 359.63733585583509 9 359.76794860802522
		 10 359.5455099811623 11 359.31718519910078 12 358.98882797325376 13 358.66470470033232
		 14 358.45505066134353 15 358.17907872811645 16 357.51903751205236 17 357.56658428423384
		 18 357.72089733053758 19 357.91805811462473 20 358.11938668435118 21 358.41162105209656
		 22 358.60264752490798 23 359.03780214149594 24 359.53923993347354 25 359.98575715488471
		 26 360.49105594455671 27 360.55464473379334 28 360.44915253609025 29 359.92818853583577
		 30 359.09690328978968 31 358.57580118748047 32 358.33588843962553;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_L_rotateY";
	rename -uid "CD611812-40F6-98BB-9668-129FAC957520";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -5.1860580356394772 1 -5.0986166867916811
		 2 -4.7566323153163443 3 -4.3359216228870121 4 -3.7794245787798628 5 -3.2567197748250272
		 6 -2.8385475982318078 7 -2.4592842788569551 8 -2.1926853218257443 9 -2.0385758478684122
		 10 -2.6062370012380698 11 -3.0666316378352527 12 -3.2794224748557981 13 -3.520551339200864
		 14 -3.8815428923952515 15 -4.3180968707016651 16 -6.5070344137750764 17 -6.9807557763939876
		 18 -7.3197598057760089 19 -6.5638287818917052 20 -5.7841527002023438 21 -4.4753231290751341
		 22 -2.9529459033320675 23 -3.4169724928206149 24 -4.2894356497528374 25 -4.0164833243631612
		 26 -3.3993243082912832 27 -3.796094113908326 28 -4.6339474959062068 29 -5.0269635599524438
		 30 -5.1915921395664162 31 -5.2010958690305955 32 -5.1860580356394772;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_L_rotateZ";
	rename -uid "1BE95E7C-4FDD-8FFA-E65A-8D957ACA3F8E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -54.036841632034466 1 -55.426015672585962
		 2 -52.546169362268195 3 -47.508422856300626 4 -38.692151413619804 5 -29.944767934071905
		 6 -20.023377802005037 7 -12.357948915581165 8 -10.997718171651341 9 -9.8255303482899041
		 10 -11.896937591653625 11 -13.305237082808139 12 -12.883991189893255 13 -12.637382364194739
		 14 -14.014029581070568 15 -16.521170850869861 16 -23.326430037079056 17 -22.61340789959613
		 18 -20.996701963650111 19 -17.805755037567152 20 -13.622312559086881 21 -9.3978538705937282
		 22 -5.3028762756807337 23 -1.5706874836043041 24 1.3329826034317336 25 1.1878425506126837
		 26 0.76331266265245701 27 -6.7975620099940519 28 -18.209092996834013 29 -28.30203433681422
		 30 -39.109318247751908 31 -47.309895659576334 32 -54.036841632034466;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_L_rotateX";
	rename -uid "9DFEB668-4036-3D81-AC5E-EE8A0C8492D6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 369.68416764904629 1 371.680912178288
		 2 373.30432089647957 3 374.52356335138978 4 374.97765879826562 5 374.92171443964469
		 6 373.01327432422897 7 371.30224362236572 8 369.84007071611109 9 368.83112843852263
		 10 369.50746373651259 11 370.17030305242884 12 371.23689542439502 13 372.16013181761855
		 14 372.15696073088299 15 372.23694932877652 16 371.42259533978319 17 371.61883913446019
		 18 371.77863511443758 19 371.05787343403529 20 370.40235865072117 21 369.03822982189769
		 22 367.75947969079954 23 366.75598506696741 24 365.78604971706073 25 364.98755642430865
		 26 364.22098084426199 27 363.69253750172317 28 363.28915195859287 29 363.76220669552811
		 30 365.0696779333939 31 367.1040204461604 32 369.68416764904629;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_L_rotateY";
	rename -uid "5970089A-4C84-B7F8-6E3D-4F81BACDFD69";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 8.9761261317333556 1 8.6506931786536985
		 2 7.1689815745676624 3 6.6745976679741634 4 6.9068844770105935 5 6.5532274546635438
		 6 3.7036874548248617 7 1.7902018834869098 8 1.4870233820968457 9 1.1786620586532108
		 10 1.4466980365903996 11 1.690161005462907 12 1.9531630778009346 13 2.2050721026293485
		 14 1.5225262345637842 15 1.2374719874596423 16 1.2983490101855792 17 1.2649777537680265
		 18 1.1839644591024887 19 0.78043917520987516 20 0.048119900803680157 21 -0.16016381299602214
		 22 -0.86901275253044763 23 0.0080810981399954598 24 1.4407525034018687 25 1.3281704146905413
		 26 0.92371699167500065 27 2.0855746738278684 28 4.1552064788101006 29 5.9265376109777304
		 30 8.0618303118237762 31 8.8709829520604035 32 8.9761261317333556;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_L_rotateZ";
	rename -uid "4995523D-44FE-BF39-0226-0CBB61E6ABDF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -9.784521562670804 1 -6.7372159091771655
		 2 -1.6801968960832174 3 2.0778471278257671 4 4.582682069496899 5 5.5494065491888582
		 6 3.8268494908986899 7 2.5978253256079005 8 1.8360117969551208 9 1.0343628096946615
		 10 0.14947286728693573 11 -0.86828898227350704 12 -2.8405690568254776 13 -4.4259788000887159
		 14 -1.7928580021308234 15 1.3574612811298636 16 9.3796448221851403 17 11.423931050123967
		 18 12.94273493971637 19 13.638454357951465 20 13.887858850914233 21 13.913389933043238
		 22 14.074566211062963 23 13.192720357944689 24 12.548895967546562 25 11.663612339989168
		 26 10.826082510110821 27 8.1027691987970183 28 3.2645113563603605 29 -2.8243995695159749
		 30 -9.9378530277445165 31 -11.185754930297003 32 -9.784521562670804;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_L_rotateX";
	rename -uid "848F69F5-43B7-5048-65D1-35A3ECE5140B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 359.50655509576563 1 359.50655509576563
		 2 359.50655509576563 3 359.50655509576563 4 359.50655509576563 5 359.50655509576563
		 6 359.50655509576563 7 359.50655509576563 8 359.50655509576563 9 359.50655509576563
		 10 359.50655509576563 11 359.50655509576563 12 359.50655509576563 13 359.50655509576563
		 14 359.50655509576563 15 359.50655509576563 16 359.50655509576563 17 359.50655509576563
		 18 359.50655509576563 19 359.50655509576563 20 359.50655509576563 21 359.50655509576563
		 22 359.50655509576563 23 359.50655509576563 24 359.50655509576563 25 359.50655509576563
		 26 359.50655509576563 27 359.50655509576563 28 359.50655509576563 29 359.50655509576563
		 30 359.50655509576563 31 359.50655509576563 32 359.50655509576563;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_L_rotateY";
	rename -uid "296B7106-4678-BCF7-3BCF-5B88A3290F27";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.077235056997568871 1 -0.077235056997543322
		 2 -0.077235056997567969 3 -0.077235056997568927 4 -0.077235056997542698 5 -0.077235056997543183
		 6 -0.077235056997542406 7 -0.077235056997542365 8 -0.077235056997567358 9 -0.07723505699754217
		 10 -0.077235056997542351 11 -0.077235056997592574 12 -0.077235056997567442 13 -0.077235056997592283
		 14 -0.077235056997567678 15 -0.077235056997542115 16 -0.077235056997542656 17 -0.077235056997567261
		 18 -0.077235056997567803 19 -0.077235056997567372 20 -0.077235056997567608 21 -0.077235056997567789
		 22 -0.077235056997542212 23 -0.077235056997542462 24 -0.077235056997542531 25 -0.077235056997593504
		 26 -0.077235056997543156 27 -0.077235056997569801 28 -0.077235056997571064 29 -0.077235056997571452
		 30 -0.077235056997572618 31 -0.077235056997547291 32 -0.077235056997568871;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_L_rotateZ";
	rename -uid "4CD79281-412C-BA5F-5A8A-69886FD02D7C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 12.267092796042386 1 5.3788476245758199
		 2 3.5780627577292958 3 0.44160142301993233 4 -3.9275335818271593 5 -6.9509815534421895
		 6 -7.5544092043328988 7 -8.0800146669103707 8 -8.0748430862278511 9 -8.0749271383787882
		 10 -8.0749316799340711 11 -8.0748622512464614 12 -8.0747185077704682 13 -8.0745334970784324
		 14 -8.072074673835365 15 -7.9080081127680417 16 -7.9080459172925339 17 -7.907770409141432
		 18 -7.9078170711997089 19 -7.9078407964656998 20 -8.0687042034360204 21 -8.0746840796289803
		 22 -8.0744926576741882 23 -6.826616267497883 24 -5.1746909211465395 25 -3.2008394854289706
		 26 -1.7462052643448014 27 7.4006086805567826 28 20.746189346251686 29 26.802306261896909
		 30 29.243190423512953 31 25.225230448051789 32 12.267092796042386;
	setAttr ".pst" 3;
createNode animCurveTL -n "RootX_M_translateX";
	rename -uid "9810CF76-412E-77C9-7BA1-C8A82056C759";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.42367453764788759 1 -0.47525408541831332
		 2 -0.5114808893933448 3 -0.53863413697924434 4 -0.55087047762076236 5 -0.55618423547477314
		 6 -0.55050963148565657 7 -0.53798244023824915 8 -0.50287071095303171 9 -0.45964863048398924
		 10 -0.37493197774534481 11 -0.28767226599681384 12 -0.16363698661061038 13 -0.041023311387923603
		 14 0.083353677921673572 15 0.20582053114706136 16 0.38715855855445563 17 0.42625380089956388
		 18 0.46471519887965246 19 0.47413719090210205 20 0.48027169384307145 21 0.46568977232753417
		 22 0.4477714870215207 23 0.41278769438010404 24 0.37480779649137214 25 0.30294828725382539
		 26 0.22486399730977472 27 0.10197883790781943 28 -0.03956513956706021 29 -0.16155995884143301
		 30 -0.2750550664536644 31 -0.35973291485111863 32 -0.42367453764788759;
	setAttr ".pst" 3;
createNode animCurveTL -n "RootX_M_translateY";
	rename -uid "7AD75D51-44DA-F57F-7008-7D9159CC445A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.17686132139737154 1 -0.15188738745948527
		 2 -0.10662654969505425 3 -0.077082481074409515 4 -0.067027827968789921 5 -0.068132892062497064
		 6 -0.10119103289042997 7 -0.13715807513010603 8 -0.18693686183364733 9 -0.22793058998571425
		 10 -0.23535697995921723 11 -0.24224673349839065 12 -0.20324615171076843 13 -0.17453630647154128
		 14 -0.14646944264401185 15 -0.15099270528925857 16 -0.23446565720243484 17 -0.21635821500418118
		 18 -0.19854467156658373 19 -0.15956681005342332 20 -0.12314718202096842 21 -0.13022968926271261
		 22 -0.14558855042410102 23 -0.18599802036487034 24 -0.23372695796394893 25 -0.25456818333008613
		 26 -0.27063376604876055 27 -0.2518281500119457 28 -0.22373711247953665 29 -0.19741434906584132
		 30 -0.18750601753539087 31 -0.18304106078300464 32 -0.17686132139737154;
	setAttr ".pst" 3;
createNode animCurveTL -n "RootX_M_translateZ";
	rename -uid "B335EBF7-4067-8E2A-FADE-37AF7D407C55";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.32469742629856202 1 0.28216067295678332
		 2 0.2246159723028911 3 0.16049507957384096 4 0.086220575469097144 5 0.012576803193832002
		 6 -0.060575704086734336 7 -0.12106964994611612 8 -0.13790269451677631 9 -0.14960517291797124
		 10 -0.10842989726886512 11 -0.069783901109065502 12 -0.0023169117999984443 13 0.056525046903801529
		 14 0.080842926093310202 15 0.089981039245144195 16 0 17 -0.0073548716526998393 18 -0.017577566057314076
		 19 -0.038338016956619814 20 -0.068506372326139375 21 -0.10614860903613277 22 -0.1509208913779711
		 23 -0.14162851619419198 24 -0.13078987876569922 25 -0.064762872313888206 26 0.012318977375608437
		 27 0.12613156773030884 28 0.25660370849079545 29 0.32906442542267234 30 0.36612729102019048
		 31 0.36015035774037013 32 0.32469742629856202;
	setAttr ".pst" 3;
createNode animCurveTA -n "RootX_M_rotateX1";
	rename -uid "D7C5A693-42AA-BB23-EBF8-8BBAE1E3DF43";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 5.9184436910315608 1 5.2036159399870616
		 2 4.0762710571289151 3 4.6398851220276924 4 5.538649246036349 5 6.278230570855758
		 6 6.9524267705847036 7 7.5690078682066613 8 7.903225803674272 9 8.0381983007362248
		 10 8.027743046763927 11 7.8143704226086603 12 7.5326516650316018 13 7.1439608350983086
		 14 6.7225716164214777 15 6.3579385568920497 16 6.2796330471089483 17 6.2487806285889116
		 18 6.4775019088019956 19 6.8791098542316336 20 7.2695361184546021 21 7.7120996808018747
		 22 8.1956180990763148 23 8.6222501368571614 24 9.0410587383250114 25 9.133146948539423
		 26 9.050102052811642 27 8.8804635525861819 28 8.5242242471416532 29 7.814899883187957
		 30 6.8848364414655725 31 6.3239929131651227 32 5.9184436910315608;
	setAttr ".pst" 3;
createNode animCurveTA -n "RootX_M_rotateY1";
	rename -uid "41196B6E-46CE-928F-0737-01971470BDEA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 4.5737798190816807 1 4.5709986359608941
		 2 4.1609601974487003 3 3.7053857415754146 4 3.0598114444485196 5 2.6447556855528425
		 6 2.3129398796573684 7 2.0344657176315049 8 2.0050044128487579 9 2.3866579514752781
		 10 2.7251922074291164 11 2.9879048768412511 12 3.1681470726281331 13 3.2818656875729566
		 14 3.4243277591455166 15 3.5913043095327168 16 3.7691092816805951 17 4.059563011733796
		 18 4.6650654857136802 19 5.4732659043015888 20 6.4945826531366784 21 7.4838125516147107
		 22 8.4288391364652497 23 8.7232862823662991 24 8.6788682547458667 25 8.4631508042409962
		 26 7.7788300376489374 27 7.0454905771861966 28 6.274887317168762 29 5.4118282653657044
		 30 4.6329546400206256 31 4.5749167364906267 32 4.5737798190816807;
	setAttr ".pst" 3;
createNode animCurveTA -n "RootX_M_rotateZ1";
	rename -uid "11DD74C1-4F5B-B002-524A-95B81A12C237";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.58476935787212592 1 -1.4538805061841589
		 2 -1.9634118080139471 3 -0.88043562041166046 4 0.53011409484475303 5 1.1670298737616627
		 6 1.5463754971544799 7 1.7295611800235766 8 1.5623489915666173 9 0.039997465779630974
		 10 -0.33855643382864525 11 -0.30799573715635448 12 0.069332645920638994 13 1.4616096313606382
		 14 2.5497236631790332 15 3.5088785287509889 16 4.4610800996222713 17 5.0819604973067847
		 18 4.9653790453487909 19 4.3851349116926901 20 3.169460021593459 21 1.7994903337622423
		 22 0.35722747321645343 23 -0.37631075775257689 24 -0.48408462843225031 25 -0.4649619366625683
		 26 -0.24546809040787257 27 -0.10061451452575956 28 -0.028755403443025875 29 0.22059520378259578
		 30 0.53905294108040569 31 0.21805729633229179 32 -0.58476935787212592;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKSpine1_M_rotateX1";
	rename -uid "A4769AC1-434B-00AE-008C-FCAF25F7E97A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -16.843377094570748 1 -14.304427271200588
		 2 -9.8108414543052636 3 -7.727775739291836 4 -4.6088155825921282 5 -2.3221295758291567
		 6 -0.14259066872430987 7 2.0419819680644515 8 3.827237577795974 9 5.1555247795746313
		 10 5.778027856835009 11 5.9211030285982895 12 5.7957299606493722 13 5.1332795777952294
		 14 4.160287609566768 15 2.8093014914069201 16 0.98654950848279954 17 -1.3322469621331052
		 18 -4.3419661835062424 19 -7.6479192145232364 20 -10.852851352383755 21 -14.175941346889784
		 22 -17.874182604756026 23 -20.943714124374459 24 -23.110993011702902 25 -24.263472018415353
		 26 -24.562997487720935 27 -24.498414042548983 28 -23.90098426609983 29 -22.536131848095188
		 30 -20.565579352097142 31 -18.724199286566879 32 -16.843377094570748;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKSpine1_M_rotateY1";
	rename -uid "38F4804E-4F9B-6401-4042-7696A91BB956";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 5.2429637250482459 1 7.0770432733938877
		 2 8.5106393688395823 3 7.4603278378589017 4 5.8614980003435697 5 4.6882513162974702
		 6 3.3356154289874378 7 1.3330939510856183 8 0.81477547924876315 9 1.5454332602666274
		 10 1.4926088733943343 11 -0.1159115467899923 12 -2.2178888637130281 13 -4.705530211232924
		 14 -6.4988531452176934 15 -7.7448517357366997 16 -8.4580274714567256 17 -8.6824435670603215
		 18 -7.9123355936379269 19 -6.1573390725215056 20 -3.7588818306484408 21 -1.290280815093346
		 22 1.1132563272372358 23 2.1965754623323464 24 2.3717078320284082 25 2.3253322916558807
		 26 1.9984899378738403 27 1.934890678741513 28 1.9797168698175638 29 2.0276212695270925
		 30 2.1212240431209102 31 3.1396713547575259 32 5.2429637250482459;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKSpine1_M_rotateZ1";
	rename -uid "42E40186-42DF-821C-E50A-BB8FBF871B25";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 5.5191228082458315 1 6.5596018277680566
		 2 8.3224660475994217 3 8.193397790869934 4 8.0894905536537554 5 8.2917392375784083
		 6 8.5058431544619442 7 8.6219212069603355 8 8.5624932222201053 9 7.8587462546774232
		 10 7.5226649805893659 11 7.4682531068105975 12 7.583849696583381 13 8.1102412628393861
		 14 8.8534139936067024 15 9.5851783356196201 16 9.6490653045248305 17 9.655779064472247
		 18 9.6335469392672159 19 9.4603587282971446 20 8.9016055407487631 21 8.0762067333628558
		 22 7.0281870399518347 23 6.0262150930588447 24 5.149082696605328 25 4.4985043835040726
		 26 4.0980029537681535 27 3.8430759133818206 28 3.7315170951646657 29 3.8237557580062531
		 30 4.2402316665688993 31 4.8019350404046408 32 5.5191228082458315;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKChest_M_rotateX1";
	rename -uid "E5632A01-45CF-890B-FCB8-A98CA147B6A1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 3.3369373205150423e-05 1 0.00054721197934475116
		 2 4.8520207722783164e-16 3 0.00076022713053987604 4 -0.00020026162132459778 5 -0.00040250172357564806
		 6 -2.4681851411231207e-05 7 -0.0001038713471331778 8 -0.0047688366595590621 9 -0.024502534001109261
		 10 0.022813260927695669 11 0.0035521224544375713 12 0.0025244951215633413 13 5.0006747163736326e-05
		 14 0.0019039079397148071 15 0.0015213766665825267 16 -0.0026277590887102162 17 1.2290119688802095e-05
		 18 0.00050815028352152664 19 -0.00012177388208459233 20 -0.00056131301247668995 21 -0.00014034400168123974
		 22 -0.00097759146474058595 23 0.00063290808885010572 24 0.0014787412848839515 25 -0.0015222507563246728
		 26 -0.0021403774323497161 27 0.0016504614903404551 28 -3.2635364070069619e-05 29 0.00031099887293233356
		 30 -0.00016722479864632737 31 0.00052053648783125385 32 3.3369373205150423e-05;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKChest_M_rotateY1";
	rename -uid "CA48F569-4A5D-A6F4-0F67-81B3E66CAAF9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 6.5360211276132668e-05 1 -0.002438859019488422
		 2 -6.7225297597033047e-15 3 0.0025241220093498197 4 -0.00040418864842773966 5 -0.00092110840805722529
		 6 -0.00010843602598979036 7 -0.0012045078539656944 8 -0.00016458818880025737 9 -0.006676421632693919
		 10 0.0084688574918562187 11 0.0050860887612531325 12 -0.0036026691491780911 13 -0.00078417471567511477
		 14 -0.012402861256080739 15 -0.011616399498355259 16 0.021429309029646168 17 0.0001927849634471128
		 18 0.00074743927635102108 19 -0.00015611204436067762 20 -5.5936130467809754e-05 21 -0.00043310034058518924
		 22 -0.001555405280288829 23 -0.0015101876030501583 24 -0.013449502915324315 25 0.013511688104676085
		 26 0.0089460384209882459 27 -0.0055792210870902912 28 -0.0027854137068814553 29 0.0024005018753998305
		 30 0.00058652888987260443 31 -0.00068366286973840632 32 6.5360211276132668e-05;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKChest_M_rotateZ1";
	rename -uid "37007BBB-465A-1F71-3F31-838C5D62B23D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 2.7446061353992488 1 2.745220535832428
		 2 2.7444344684213386 3 2.7548908021935161 4 2.7396040630374476 5 2.7356983810665376
		 6 2.7440104996355665 7 2.7409744607232898 8 2.7459930344148638 9 2.7432935464322088
		 10 2.7502153373080769 11 2.7555646890338696 12 2.7331850394125441 13 2.743168900731372
		 14 2.750432990520649 15 2.7498387914456792 16 2.7361367842746143 17 2.7447585996971093
		 18 2.7439610156900835 19 2.7440837813772321 20 2.7423109333155335 21 2.7440701544207813
		 22 2.7391210628167397 23 2.7477503472979907 24 2.7492713246200342 25 2.7420333283801326
		 26 2.744111307090809 27 2.7431403490657869 28 2.7428041861831596 29 2.745755095527691
		 30 2.7440957205780556 31 2.7458709849616985 32 2.7446061353992488;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKNeck_M_rotateX1";
	rename -uid "4963BFD9-4ABA-1BDD-7A4E-C989706D87AD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.075166028312774996 1 -0.31927536463803929
		 2 -0.79243207096322898 3 -1.6304639405109067 4 -2.6117420954735264 5 -2.8694602726624892
		 6 -3.0036684523407593 7 -3.0284699338263321 8 -3.0932167311736092 9 -3.2879759450514174
		 10 -3.2113892587736217 11 -2.3466821708210097 12 -2.0296472209364707 13 -1.858466546256468
		 14 -1.7266559982442433 15 -1.8359016280300267 16 -1.8397249840941112 17 -1.7949873124278224
		 18 -1.6574788421503388 19 -1.4460989637638721 20 -1.1329456592646834 21 -0.83659295723179228
		 22 0.065982483211255091 23 1.1055255835918902 24 1.9017945880099458 25 2.4312189998154645
		 26 2.6983124296223995 27 2.4919804454170436 28 2.2255612337256419 29 1.7489981936742873
		 30 1.1273890271978988 31 0.57003231950521316 32 0.075166028312774996;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKNeck_M_rotateY1";
	rename -uid "966D085E-4A35-DED4-F42F-DCA5C52BFD6D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.95365017793150286 1 -1.1371550408388651
		 2 -1.8927008526763323 3 -4.4770092524195446 4 -7.250012696484049 5 -7.7696695140771386
		 6 -7.7078919212142987 7 -6.7414757933313796 8 -6.3968092843586684 9 -6.8119589237738207
		 10 -6.3923926140329002 11 -3.9163567926683793 12 -3.154474937541738 13 -3.1103410423952327
		 14 -3.6760577208897161 15 -5.2402233015860968 16 -6.9947746386814185 17 -8.716423283181209
		 18 -9.5768825617976265 19 -10.073772310337974 20 -10.541639553859152 21 -10.706249837440135
		 22 -8.9501956733251351 23 -6.5802978203713476 24 -4.0110026718435465 25 -1.7684091277258633
		 26 0.078755203531790302 27 0.44484409889893251 28 0.30562714421997617 29 -0.11969077413843378
		 30 -0.72121952950368606 31 -0.9283786923698587 32 -0.95365017793150286;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKNeck_M_rotateZ1";
	rename -uid "42B0775C-465C-04B6-7820-B995E621A0BF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -6.8702804113736136 1 -6.3200562037985124
		 2 -7.2098208749250716 3 -7.3144251067130801 4 -7.7438750042462754 5 -9.1197231217053449
		 6 -10.370416989428902 7 -10.918718420291622 8 -10.851846339516477 9 -9.5626493108639519
		 10 -9.2751836095509077 11 -9.5779080498571574 12 -9.2515519612753252 13 -8.1143392322189065
		 14 -8.0244037495948124 15 -8.081165238629362 16 -7.9480195357184966 17 -7.7378938974232918
		 18 -9.319503774962417 19 -11.593774178196478 20 -12.575905606616516 21 -12.988744989291394
		 22 -12.937197906246711 23 -12.881744357603232 24 -12.976244419135293 25 -12.878056931802378
		 26 -12.03250622718509 27 -11.031644798106132 28 -9.8966284683300358 29 -8.9532324592408372
		 30 -8.1622685768672394 31 -7.4651981075129692 32 -6.8702804113736136;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHead_M_rotateX1";
	rename -uid "C30BF01B-4F78-3C2C-09EA-3290A3AC5F29";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 1.0983598261123728 1 0.04207513839488497
		 2 -0.7178109629823054 3 -1.211240280801636 4 -1.7971989023865402 5 -1.9148159438644035
		 6 -1.9890634303774926 7 -2.7338136673217104 8 -3.4248207409738676 9 -3.8486580086278681
		 10 -3.9464064375157437 11 -3.506852419323268 12 -3.1568862767768819 13 -2.7835822616351464
		 14 -2.0812130185964648 15 -1.0584885638887711 16 0.21971449403852467 17 1.7493739938498223
		 18 3.2783185949345581 19 4.7514979886009145 20 6.1443998180289201 21 7.4260124639654093
		 22 8.528449216475753 23 8.9549976336865829 24 8.9231155007725071 25 8.4878003538263229
		 26 7.6131965066362399 27 6.7940787956856878 28 6.1464168499477063 29 5.1540412119676509
		 30 3.86920561347018 31 2.4447344666563029 32 1.0983598261123728;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHead_M_rotateY1";
	rename -uid "478745B8-4785-3207-BBB0-D88B214F6576";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -3.6703265553060378 1 -3.864902943007722
		 2 -3.0753369567746645 3 0.030539753140209843 4 4.0890562752501749 5 6.0546063915565371
		 6 6.7362497465638649 7 6.7008660003557408 8 6.5754024941402278 9 6.3656717567943595
		 10 5.477942890653102 11 2.9892140463254364 12 1.2915165934652573 13 0.25605070144042469
		 14 -0.52357508192090574 15 -0.88542561802659281 16 -0.65953910223602064 17 -0.36568684562397147
		 18 0.17056546798544298 19 1.2180106891382965 20 3.2739451215132349 21 4.449793833272385
		 22 4.5557782354499787 23 4.0486542366941745 24 2.3570237309495488 25 0.73439593138907533
		 26 -0.67876524984813102 27 -0.93706646770253788 28 -0.68559553296598852 29 -0.74092115931973757
		 30 -0.95847200597431426 31 -2.0274528239881908 32 -3.6703265553060378;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHead_M_rotateZ1";
	rename -uid "AD7EEF19-4010-DCA2-7C55-0A857E2E5EF2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -6.8348608391298074 1 -7.272141755281341
		 2 -7.5620927242195508 3 -8.4267288678624741 4 -9.4822633379401164 5 -9.8984240066614131
		 6 -9.9838995442251797 7 -9.8857267453334163 8 -9.7960527497590242 9 -9.7539434240938636
		 10 -9.5936303689768376 11 -9.3109456131616799 12 -9.4762682765728279 13 -10.091493898446938
		 14 -9.8704239524936881 15 -9.2838977890556613 16 -9.247446464021829 17 -9.2415736378833593
		 18 -8.7584714521730955 19 -8.2893745243625307 20 -8.7070611206163431 21 -9.3344049647625145
		 22 -10.055802330806667 23 -10.216812810213918 24 -8.9747482762191257 25 -7.8833089020449352
		 26 -7.1516994011687602 27 -7.1217600026880605 28 -7.4779296500259145 29 -7.5380175333992412
		 30 -7.5263911548514724 31 -7.2687002991618002 32 -6.8348608391298074;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_R_rotateX1";
	rename -uid "E35228CB-4638-CB6B-412E-86A2232CDBE6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 21.477314412567512 1 19.098038283884826
		 2 13.448219234567667 3 10.518276087607312 4 5.4814313795354135 5 1.4843408416894415
		 6 -1.9504110432847224 7 -4.5045547330475149 8 -6.1646743356242366 9 -6.9164954483541834
		 10 -6.8163653284848014 11 -6.7838850353798152 12 -6.4554856316200331 13 -5.7209404679912783
		 14 -4.2499509658364483 15 -1.9913174535620182 16 0.97893547756393795 17 4.3891662911653491
		 18 7.7604402597121167 19 10.999375678236694 20 13.993416288202152 21 16.593870098201208
		 22 18.708169786048774 23 20.289572815967205 24 21.351712324354121 25 -157.92263173851811
		 26 -157.33974756726869 27 -156.97845326360437 28 -156.98553894038358 29 -156.9121219647017
		 30 -156.86211720971704 31 22.510817587877614 32 21.477314412567512;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_R_rotateY1";
	rename -uid "B4654904-4518-25F9-87B9-128B83761DE7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -27.855955056789149 1 -22.551364589539396
		 2 -15.491917886871837 3 -12.611485170119943 4 -9.6354843822165677 5 -8.7714711222160506
		 6 -9.128832326768233 7 -10.359351323321077 8 -12.077846441321256 9 -14.177680046124356
		 10 -15.004408161886479 11 -14.936431674013759 12 -13.877644043914643 13 -11.952808480604501
		 14 -9.7933158822143138 15 -7.7409108377171965 16 -6.4773010756586391 17 -6.0925669316492002
		 18 -7.0471967027992033 19 -9.4548512197518253 20 -13.131160721915908 21 -18.067417489346912
		 22 -24.579178022804822 23 -30.417640501217708 24 -34.997436515052698 25 -141.75682054395452
		 26 -139.86192242916641 27 -139.3603603412339 28 -139.33636644987456 29 -140.43310846699322
		 30 -143.90805308248849 31 -32.273651652138469 32 -27.855955056789149;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_R_rotateZ1";
	rename -uid "78177915-4268-C89E-6F6F-AFA0A65B1440";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -20.684994327741741 1 -15.796659395539544
		 2 -5.6762396320876443 3 -0.57556757146015991 4 7.2073839656064811 5 13.414609308117926
		 6 18.891399116008177 7 23.581209337805578 8 26.758834939891535 9 28.382046229497551
		 10 28.547814927920644 11 27.524899193832091 12 25.481003821170738 13 22.441706029376235
		 14 18.616346283501581 15 14.031101197665778 16 8.9011007889526752 17 3.4458250407534798
		 18 -1.8534663809593204 19 -6.8016557270593365 20 -11.129269330588839 21 -14.930580369756559
		 22 -18.499170299000376 23 -21.161595738439761 24 -22.989624068772347 25 -204.62108570793654
		 26 -205.96131055945256 27 -206.57643308342597 28 -206.85642615908523 29 -206.6881290140409
		 30 -205.51414108162137 31 -23.657514521877321 32 -20.684994327741741;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_R_rotateX1";
	rename -uid "F0016484-4241-EC67-58DA-5C86BB31D6BF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 141.85826093719652 1 145.51032316124787
		 2 150.92503880404129 3 153.83674060215333 4 158.07305642451198 5 -18.952676941905811
		 6 -16.349638548304561 7 -14.005788515422699 8 -12.542652661466478 9 -192.07905144649911
		 10 -192.39640857645972 11 -193.52009808432607 12 -197.27857441503008 13 -199.76733062171391
		 14 -21.281873362192748 15 -25.076682593128758 16 -26.562757804848165 17 -29.179662017890134
		 18 -30.679002237860221 19 -32.13499589235834 20 -32.184267954414295 21 144.2019442686389
		 22 141.40989444984277 23 141.00490584188856 24 138.85756228985807 25 137.25228114151886
		 26 136.74696377177023 27 136.01183266612117 28 135.36047550017327 29 135.91480917062074
		 30 137.47323116736464 31 139.22339210726349 32 141.85826093719652;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_R_rotateY1";
	rename -uid "4673D4B8-4C96-60D8-C6BF-89A75966A101";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 156.70910924009726 1 159.3635849649462
		 2 162.55448702039604 3 164.42473036479424 4 167.08911761761385 5 10.829573692083118
		 6 9.2091370083384518 7 8.2510868048850572 8 7.5827728063291211 9 172.81336021529259
		 10 172.90610510582431 11 172.6815622543163 12 172.27812033086715 13 171.61220571603414
		 14 10.523326367548437 15 10.853082234509731 16 11.130434008413637 17 12.280270293607023
		 18 12.897715016996214 19 12.959799974688021 20 14.843428348005556 21 163.17947682064278
		 22 160.69115861359359 23 158.48473728408729 24 156.20884498570462 25 154.70074792080402
		 26 154.159812374403 27 153.71992010061408 28 153.28941211232376 29 153.21708437739065
		 30 154.005973019164 31 155.10809081541137 32 156.70910924009726;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_R_rotateZ1";
	rename -uid "7D4E63B0-4EFF-5377-63CC-2480EA655181";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -89.161617303710315 1 -91.522553084732323
		 2 -94.844753957303695 3 -96.064859214483917 4 -97.642425815640863 5 81.851477015377867
		 6 81.573443685890737 7 81.502766872427728 8 81.400067549833295 9 261.15495942282115
		 10 260.6985775615646 11 260.03539062874358 12 258.84065445931168 13 257.0089977081488
		 14 77.464209111125442 15 74.50736712343884 16 74.457344587260962 17 74.9340715010606
		 18 76.370371756213629 19 77.741756896605224 20 79.165809427812263 21 -96.18473691881519
		 22 -91.637221020446205 23 -88.164689020966676 24 -85.032797411659089 25 -82.95474119947923
		 26 -82.132293514779462 27 -81.67134499938237 28 -81.604621920946997 29 -82.436257018637022
		 30 -84.604575325450114 31 -86.780421428483209 32 -89.161617303710315;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_R_rotateX1";
	rename -uid "CAFA2DA0-473E-1F8A-315A-5FBDE7832962";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 37.530036819156969 1 37.672264182828805
		 2 37.965748566489786 3 37.742374697956734 4 37.491183339705913 5 37.43822318312192
		 6 37.530695990349244 7 37.739987508568277 8 38.10517163682691 9 38.661963295283158
		 10 39.295017858224426 11 39.990120598209586 12 40.535521053140947 13 40.884273560640736
		 14 40.787530656076456 15 40.531571252463856 16 39.93829790454042 17 39.017712410724663
		 18 38.418784499611029 19 37.973141121323536 20 37.670259091732255 21 37.495050620185459
		 22 37.435537187813331 23 37.502506191134252 24 37.628273595958056 25 37.775409490989581
		 26 37.647438794605897 27 37.667835728165727 28 37.880200653722078 29 37.884981901074596
		 30 37.76215260198277 31 37.687959224446352 32 37.530036819156969;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_R_rotateY1";
	rename -uid "5E6CA171-4777-E1B2-7F9F-F194F31ECFBC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -18.750153976517442 1 -19.97053605957257
		 2 -21.770299151373383 3 -21.094845302784108 4 -20.182340793054792 5 -19.64050220329527
		 6 -19.464273342321341 7 -19.567453802289965 8 -20.131392556436666 9 -21.26977119377462
		 10 -22.595933608623994 11 -24.079962384428999 12 -25.356626762220333 13 -26.391205414476971
		 14 -26.841038130544923 15 -27.042448180232654 16 -26.084877005161989 17 -23.983509908544896
		 18 -22.80705303859979 19 -21.886693794905359 20 -21.102689920602774 21 -20.493588646341575
		 22 -20.014571070793853 23 -19.890247278489664 24 -20.04061750496847 25 -19.9084737748544
		 26 -18.942222958034929 27 -18.836962881535651 28 -19.188452703763467 29 -19.135931237362623
		 30 -18.857301299554784 31 -18.761234274517875 32 -18.750153976517442;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_R_rotateZ1";
	rename -uid "31C52A17-4AC9-B5ED-6D1E-1382D7D655E4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 28.237376861561589 1 26.13974511199541
		 2 24.003869294924723 3 23.82678827673578 4 23.671600729241533 5 24.574138494051809
		 6 26.055104604012481 7 27.835340672160363 8 29.53637526013754 9 31.071644557777901
		 10 32.411813619930705 11 33.546898240753009 12 33.886788971453477 13 33.709112321200799
		 14 32.452610896307682 15 30.572738514533413 16 28.962735102777664 17 27.30325406601585
		 18 25.460313541936546 19 23.872645102744762 20 22.968912047160174 21 22.696754071674516
		 22 23.284257468432696 23 24.231828570303897 24 25.346134072678595 25 26.774385517169431
		 26 28.456201145428963 27 29.883754278888677 28 31.00241247976815 29 31.093903410078489
		 30 30.851103746804284 31 29.930279425053016 32 28.237376861561589;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_R_rotateX1";
	rename -uid "EEBAB96C-494B-3D58-DC60-A79D6628412B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -2.2820374806665407 1 -2.6039111779423494
		 2 -2.4370818356761217 3 -2.0128442512273077 4 -1.5742880291768444 5 -1.5507341612034695
		 6 -1.5090259969932294 7 -1.3763208808888108 8 -1.2645823335163471 9 -1.1369491851044429
		 10 -1.1571122941982133 11 -1.3984218018074597 12 -1.4428811409778621 13 -1.1960516602180242
		 14 -0.78625107454244292 15 359.76578919751995 16 360.36370271098093 17 360.95942276696184
		 18 361.50153861184259 19 361.77461981532883 20 361.67537731075322 21 361.15415264423518
		 22 359.92472951213307 23 -1.1331705559182319 24 -1.7957507427302311 25 -1.8706885191676978
		 26 -1.5260460339794626 27 -1.4655832664088064 28 -1.5526253578963451 29 -1.6780938263578882
		 30 -1.8464426002771674 31 -2.0693007581226404 32 -2.2820374806665407;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_R_rotateY1";
	rename -uid "05C9D0E3-4C35-3F9C-DD9F-EBA76615131A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 8.5338618162643751 1 11.044741273881016
		 2 13.354122574188102 3 12.498162011458309 4 11.297369125090468 5 10.430444316647133
		 6 10.124321930455283 7 10.128753709618605 8 10.353488060294762 9 11.765936394258524
		 10 12.078225166669757 11 11.435289597673499 12 9.8431677501833637 13 7.4272885718509958
		 14 5.0570958405917255 15 2.716432355502882 16 0.61784149105845498 17 -1.0618708028958679
		 18 -1.8477482631994915 19 -2.0147966015950112 20 -0.99230063989211093 21 0.66142729249513055
		 22 2.5788908067769571 23 3.9668726632214 24 4.4872138129184487 25 4.536043067345263
		 26 4.4576949282196328 27 4.5361120425517667 28 4.8933517258762826 29 4.9482959546359773
		 30 4.9581878126538586 31 5.974114822880372 32 8.5338618162643751;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_R_rotateZ1";
	rename -uid "E225135B-4724-F09B-F218-52A9CEB9A1C0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 27.299293545947162 1 23.333155907872094
		 2 14.982301096612781 3 11.987049085018896 4 7.8833442681280994 5 5.6684492557097821
		 6 3.8571268858429488 7 2.1729157185099663 8 0.99056885294914077 9 0.37112314122692291
		 10 0.37526964882243991 11 1.2055125352408818 12 2.898886332551923 13 5.4963440587741186
		 14 9.3919739717340214 15 14.304500911867274 16 19.556043158626888 17 24.957574982914704
		 18 30.127931581802208 19 34.506626547202657 20 37.66352484328732 21 38.749048812696849
		 22 38.725243829918199 23 38.585980501469642 24 37.984477581143878 25 36.914642945025413
		 26 35.369891337281068 27 33.917231432952164 28 32.559378213613016 29 31.19920406460627
		 30 29.843318874069986 31 28.715695284495517 32 27.299293545947162;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_R_rotateX1";
	rename -uid "23E7E4D9-497F-0FEB-0ED5-BDBCF09274E3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -6.1022668547248902 1 -5.4520378096939615
		 2 -4.7394613952026869 3 -4.5551281819561416 4 -4.4565073563255879 5 -4.8696859997619999
		 6 -5.0196380852445266 7 -4.8046990822285185 8 -4.3890350163223593 9 -3.833911842366633
		 10 -3.2214181154115256 11 -2.5486048132965515 12 -1.1091681853873281 13 0.96291484535773553
		 14 2.890723381149721 15 4.6402847686140918 16 5.7966003645469257 17 6.5364230963796244
		 18 7.0764141279524608 19 7.208050301576117 20 6.912490908591554 21 365.90217280304108
		 22 362.33996384847273 23 358.33198142192998 24 354.50890928824447 25 -7.8328936557324731
		 26 -8.4281628471102241 27 -8.5389143710669533 28 -8.5468583986545106 29 -8.5523418199124652
		 30 -8.331494270219844 31 -7.3443224872912722 32 -6.1022668547248902;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_R_rotateY1";
	rename -uid "DAF75E47-4B24-CAD7-E43C-C0897164F4CA";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 8.3657822608502457 1 8.8448091623957854
		 2 8.0128926376804515 3 6.1813153010684934 4 3.7227692208937557 5 2.4632459057497731
		 6 1.6392999430482595 7 1.1291372891678706 8 1.1654262998443627 9 2.3467072111846248
		 10 4.4703826591482683 11 7.4888920892612161 12 9.7673189814357055 13 11.361161807282686
		 14 12.212622289051348 15 12.581675445308361 16 12.916431661169355 17 13.32147518980314
		 18 14.213023161604958 19 15.316055474211922 20 16.528247074071594 21 17.661925129437844
		 22 18.58517253979538 23 18.439523789898644 24 16.862423965046567 25 13.989726229538171
		 26 9.7272287179562156 27 7.2756466076476132 28 6.5662439284759504 29 7.1576253402365424
		 30 8.7566542855124094 31 8.6997458206518896 32 8.3657822608502457;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_R_rotateZ1";
	rename -uid "280C6C94-41C9-9D79-D1E0-ABA2E4478C8F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -38.006632377862609 1 -40.38419255276424
		 2 -40.439270665937329 3 -38.69771402965803 4 -36.048521597505108 5 -33.51606828438009
		 6 -32.558468758932293 7 -32.875203561270645 8 -34.40803888694019 9 -38.055076825540979
		 10 -42.866975023013829 11 -48.771669194634235 12 -55.218219407801485 13 -62.159781070204154
		 14 -69.429215329987414 15 -76.62416587295138 16 -83.003077336537842 17 -86.979594377192257
		 18 -87.234986293014956 19 -87.244239715802237 20 -83.718597711572627 21 -76.425616363592809
		 22 -65.868814336513793 23 -54.990083734203971 24 -44.759535727320696 25 -35.338344418433415
		 26 -26.764272144064662 27 -22.204863168293315 28 -21.169980743369294 29 -22.755250077357001
		 30 -28.300795583297919 31 -33.372806220240612 32 -38.006632377862609;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_R_rotateX1";
	rename -uid "8E32D7C6-4194-FEA9-575B-3C8285E793DF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 22.848487616284942 1 385.71223193014032
		 2 387.97541502815926 3 22.810334328914085 4 16.712370774580084 5 15.79225775592646
		 6 15.708835914289256 7 15.45770175173168 8 15.232199909391488 9 14.943665909823645
		 10 15.289198544929395 11 17.176705627732208 12 17.980037283951468 13 18.125025101195138
		 14 18.178482029563099 15 18.165849879194536 16 17.405037957477596 17 16.130531116624077
		 18 15.090520474514893 19 14.525693019019013 20 15.150599625505194 21 17.588460742068918
		 22 22.540587238392991 23 27.812927537847568 24 32.901645187388972 25 37.096685707824655
		 26 40.450156508605041 27 39.80490600566025 28 34.281181573240978 29 29.108189302700421
		 30 24.510455671333037 31 23.139651133007956 32 22.848487616284942;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_R_rotateY1";
	rename -uid "AAEFCFAA-4AA2-C630-8A66-3EB9A5B50DAE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -15.406125239403993 1 -20.518669070417349
		 2 -22.860461912751358 3 -19.705880859249309 4 -13.3816392617587 5 -4.4985618072188478
		 6 2.5827307197223077 7 5.0351922342044499 8 6.5201320449633178 9 7.6190042783838381
		 10 8.3258392058343897 11 8.6895131981924347 12 8.7241129401529136 13 8.7383450677771037
		 14 9.5034467040911466 15 11.05675204161996 16 11.07136515564649 17 10.8591711525851
		 18 10.665352129521073 19 10.190666473821901 20 6.6810540020610683 21 2.0161590254791935
		 22 -2.0970405054216212 23 -6.2918886966509158 24 -11.093917676160466 25 -10.981862684984174
		 26 -3.35744493870616 27 -2.0685702686448133 28 -4.0368799472029222 29 -7.5908644481347531
		 30 -12.081559414850116 31 -14.071290125529019 32 -15.406125239403993;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_R_rotateZ1";
	rename -uid "C7630A0C-4E67-F474-9514-819F25B53C40";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 15.817974976093351 1 18.666850403841064
		 2 20.325876352924325 3 18.691308228092943 4 14.222309167925582 5 6.1244240293541132
		 6 -1.0562611617577513 7 -5.3624698495061223 8 -8.0512166659921895 9 -9.1882641584743983
		 10 -9.2140965939946522 11 -8.8533319413821747 12 -9.1030659248736452 13 -10.429426516370421
		 14 -11.795280194618014 15 -13.271816688487394 16 -15.080144767840361 17 -16.372377156819645
		 18 -14.569607907390495 19 -11.650911478524163 20 -9.5014602148462792 21 -8.7263072561063169
		 22 -8.8921274819424525 23 -9.6390071382214213 24 -14.21988683570285 25 -15.262927491731016
		 26 -12.205006846962382 27 -9.6780634559732324 28 -7.5251413968384231 29 -2.8799398918338626
		 30 3.602704759814384 31 10.037413508594511 32 15.817974976093351;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_R_rotateX1";
	rename -uid "1834C406-4BBD-F9C6-304B-F5A2EC7F0375";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 359.74404027862363 1 359.74404027862363
		 2 359.74404027862363 3 359.74404027862363 4 359.74404027862363 5 359.74404027862363
		 6 359.74404027862363 7 359.74404027862363 8 359.74404027862363 9 359.74404027862363
		 10 359.74404027862363 11 359.74404027862363 12 359.74404027862363 13 359.74404027862363
		 14 359.74404027862363 15 359.74404027862363 16 359.74404027862363 17 359.74404027862363
		 18 359.74404027862363 19 359.74404027862363 20 359.74404027862363 21 359.74404027862363
		 22 359.74404027862363 23 359.74404027862363 24 359.74404027862363 25 359.74404027862363
		 26 359.74404027862363 27 359.74404027862363 28 359.74404027862363 29 359.74404027862363
		 30 359.74404027862363 31 359.74404027862363 32 359.74404027862363;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_R_rotateY1";
	rename -uid "07C502FD-402E-FDE5-8913-CA92F1CA3AB6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.61857828420965466 1 0.6185782842096309
		 2 0.61857828420958394 3 0.61857828420963024 4 0.61857828420962913 5 0.61857828420965144
		 6 0.61857828420962746 7 0.61857828420962901 8 0.61857828420965422 9 0.61857828420965444
		 10 0.61857828420965477 11 0.61857828420963124 12 0.6185782842096309 13 0.61857828420965466
		 14 0.61857828420965433 15 0.61857828420963101 16 0.61857828420963101 17 0.61857828420963101
		 18 0.61857828420965477 19 0.61857828420965455 20 0.61857828420965444 21 0.61857828420965466
		 22 0.61857828420965444 23 0.61857828420963112 24 0.61857828420963035 25 0.61857828420963035
		 26 0.61857828420965433 27 0.61857828420965399 28 0.61857828420963046 29 0.61857828420965433
		 30 0.61857828420965466 31 0.6185782842096077 32 0.61857828420965466;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_R_rotateZ1";
	rename -uid "FF62700D-426E-A509-1A99-2CA2430E9127";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 5.3866111654362356 1 5.9093472523209973
		 2 8.3306533431517789 3 13.548544822399029 4 22.513245128152686 5 33.709899546154546
		 6 37.486065151652511 7 22.528572924798631 8 10.450228656154392 9 5.9046884747180242
		 10 5.3290012410700589 11 5.3731259379571972 12 5.38063866176876 13 5.3806068427286862
		 14 5.380635489438605 15 5.3807015450583489 16 5.3807005901600498 17 5.3806956730966107
		 18 5.3806763961750663 19 5.3806572816566396 20 5.3814863469283063 21 5.386915760682653
		 22 5.5423161421928926 23 6.6190178909247637 24 10.590841090033351 25 11.450251379043776
		 26 9.4106186643682204 27 9.1113056500103582 28 9.6415722359647287 29 8.7548739319683726
		 30 6.1248008542802115 31 5.479574982333598 32 5.3866111654362356;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_L_rotateX1";
	rename -uid "F5256222-4F00-F8B3-1AB3-39A9EB708EB6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 13.914235330962171 1 12.677478797665922
		 2 12.075257434068886 3 13.241755711836367 4 15.135758332731248 5 16.410993859681074
		 6 17.602217139756174 7 18.896972881371532 8 -160.07679251412441 9 -159.33447359516896
		 10 -158.89144443990409 11 -158.66383010704715 12 -157.63270728146605 13 -155.98370719738497
		 14 -155.67369811575603 15 -157.20770185577669 16 21.00826170048985 17 18.991659721928212
		 18 17.476734505870649 19 15.792371023899031 20 13.84073819131096 21 12.325880661839507
		 22 11.584613753978191 23 12.050315005134086 24 13.042994937995156 25 14.39234274999356
		 26 16.124369655925936 27 17.732195870660735 28 19.085004863105709 29 19.061535669818994
		 30 17.997096747882825 31 16.190488417863921 32 13.914235330962171;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_L_rotateY1";
	rename -uid "57FE9D20-44D6-AE51-0705-229323B3F059";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -14.659593988498148 1 -12.619319608981218
		 2 -9.6967321998331482 3 -10.073954486662743 4 -11.291610098769246 5 -13.792802248840566
		 6 -17.274287185668353 7 -21.570244702843699 8 -154.25325668503677 9 -150.38645557007911
		 10 -147.20211656109979 11 -144.73088057250791 12 -143.61176546258815 13 -143.72773283922385
		 14 -145.20103859944018 15 -149.20705385835242 16 -26.320527417252961 17 -21.305058184057458
		 18 -16.238388093983399 19 -12.003923545480296 20 -9.6313745036509211 21 -8.6431464577247823
		 22 -8.6255652713364324 23 -9.5946956366538192 24 -11.536587508359801 25 -13.767650852992661
		 26 -16.231534839986665 27 -18.207586109029283 28 -19.638121871498612 29 -19.567374885512184
		 30 -18.595262911429533 31 -16.880759040852027 32 -14.659593988498148;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_L_rotateZ1";
	rename -uid "0D534520-49C6-EE4A-975F-90828FC82B75";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -4.4769202728715012 1 -8.1876212807091022
		 2 -14.485507193025969 3 -17.040779570510956 4 -20.861099694473889 5 -24.024944192834393
		 6 -26.424651969490043 7 -27.947930803144221 8 -209.13621673084756 9 -210.08661141116414
		 10 -210.7214976096264 11 -210.96186763049317 12 -210.10589587265159 13 -208.32564655138447
		 14 -206.73125292367035 15 -204.64383076663441 16 -22.751254176913935 17 -20.579766663623538
		 18 -17.162912903597775 19 -13.416506147886428 20 -9.8630037005744615 21 -6.5395379511380076
		 22 -3.5661742830489107 23 -1.2147302817323566 24 0.68911916189169664 25 1.9836268740831713
		 26 2.5894998617230187 27 2.7721508346490329 28 2.5618131198423963 29 2.0346877573398725
		 30 0.21016113020125962 31 -1.9471531821199308 32 -4.4769202728715012;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_L_rotateX1";
	rename -uid "7905A4DD-47C1-0EDD-16F1-BFA973F80D32";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 142.60738623835394 1 144.0656707841122
		 2 -216.41783711796248 3 -215.78118146404617 4 -215.10267236591648 5 -214.92813688271789
		 6 -215.14954683781457 7 -35.642384543669216 8 143.0395307026823 9 140.78677498843246
		 10 138.53491084582981 11 137.2261485227819 12 134.84979891672018 13 132.9904040189349
		 14 133.24291801712511 15 134.64771324689227 16 136.45573797687649 17 138.98759189269754
		 18 141.48365979517078 19 143.65727838715188 20 145.5948021547502 21 146.2909791493143
		 22 146.64201165584177 23 146.36459037895017 24 145.17656007279575 25 143.03809616378655
		 26 139.84544539054701 27 137.19292729897546 28 135.35618613662038 29 136.00864472707676
		 30 138.67395884859633 31 140.07971715674236 32 142.60738623835394;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_L_rotateY1";
	rename -uid "1D6FC624-4746-5267-E71E-FD8BD69C3C6D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 154.77604896739876 1 166.54812701453977
		 2 177.76457246072587 3 176.53755082648721 4 175.03069307677328 5 174.75351160563775
		 6 174.13660106477352 7 10.369678421677175 8 164.50487311380576 9 159.64591002132306
		 10 157.08598188614846 11 156.17733165792939 12 153.65959429644735 13 149.35382613619228
		 14 149.52336604323779 15 151.86511526739619 16 156.20322493207792 17 160.22270672003225
		 18 161.43580549275813 19 161.92714283507152 20 162.15552432746134 21 161.75745267710181
		 22 159.58110588485442 23 156.18068552050107 24 151.68703410711436 25 147.27605824117791
		 26 143.41004821517078 27 140.11088488251571 28 137.54565952071027 29 137.25501493967857
		 30 140.8143783578891 31 146.94622121351529 32 154.77604896739876;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_L_rotateZ1";
	rename -uid "A9745EF5-440C-5EE2-1841-CEA693885C7B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -90.427147052084123 1 -93.083083028737775
		 2 257.21675162484337 3 256.5127988738509 4 256.24643367626362 5 257.7735730998096
		 6 261.29139964002547 7 85.806339929883549 8 -93.056624010132282 9 -89.600251016371686
		 10 -86.519945600389619 11 -84.607800634528331 12 -81.811802526793699 13 -79.870601313436367
		 14 -80.220950634359681 15 -81.4113799988816 16 -82.462888216255465 17 -83.882432647087072
		 18 -84.327716812980327 19 -84.809227416024527 20 -84.825824768066283 21 -83.566910389441148
		 22 -81.412279944611711 23 -79.017633350255053 24 -76.493624042705903 25 -74.203286727990573
		 26 -71.797424187992519 27 -70.628047204902799 28 -70.767816476987932 29 -73.134945194165141
		 30 -78.55557492745244 31 -84.267854269386021 32 -90.427147052084123;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_L_rotateX1";
	rename -uid "4E779B5A-42B4-2B33-8AE6-9F9AA98A7F94";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 25.085658287217438 1 28.603230087507384
		 2 38.215486601093765 3 45.434508208447035 4 55.339042156661819 5 59.173188769947956
		 6 61.723981049488202 7 64.58926687958548 8 66.733888591337148 9 68.20427349447823
		 10 68.347280124800321 11 62.656794533277029 12 56.017617660170941 13 48.720243890879289
		 14 44.437510888667916 15 42.219137930048795 16 41.344487974921599 17 41.102601700199472
		 18 42.402572702301001 19 43.991612122158593 20 44.904708705899431 21 45.831615247423422
		 22 44.065550337704693 23 41.705964720927099 24 39.928822976240184 25 36.688837173745412
		 26 31.787756704258413 27 27.79120458000056 28 24.792316575112107 29 21.998035095762866
		 30 20.372647672752588 31 21.437177713628362 32 25.085658287217438;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_L_rotateY1";
	rename -uid "F9211ED4-42BF-7D89-5A25-18987418AC62";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -36.491437520824505 1 -36.867859925968403
		 2 -33.801336068094507 3 -18.581336552171699 4 -2.1474506824203248 5 0.9503859964154957
		 6 1.4938998218169022 7 -2.5050515380683183 8 -7.3111293818227736 9 -11.927245850203706
		 10 -15.227064644717737 11 -18.156613917783179 12 -20.677612540527772 13 -22.715934652262668
		 14 -24.6407949513152 15 -26.456441447227284 16 -28.283037355462024 17 -29.314673958545203
		 18 -28.244375162515389 19 -27.176553373688922 20 -28.174958004948905 21 -28.947087056919081
		 22 -29.268477913592271 23 -29.548291812332931 24 -29.721654437874097 25 -30.383294346976253
		 26 -31.70431922780007 27 -34.186307515725886 28 -37.558023793955236 29 -37.432414789727758
		 30 -35.934949813774324 31 -36.062065933953335 32 -36.491437520824505;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_L_rotateZ1";
	rename -uid "EFF82D3B-4376-F25B-67A7-3A91EF1B1C15";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 11.68485836314902 1 6.5669070485787087
		 2 9.1555230951884337 3 8.2320400831084832 4 8.2349703662116358 5 8.7577881740060217
		 6 9.4871831291797584 7 11.248989545314419 8 14.384990957460108 9 19.48574289859739
		 10 20.333715943202328 11 17.027770004191819 12 13.026085072848637 13 8.0490570248279152
		 14 0.9043582363013194 15 -7.6502334005593147 16 -16.897956465238416 17 -23.39519282944072
		 18 -19.229309261129096 19 -11.871992035739567 20 -5.2619286616469232 21 1.5066749788432761
		 22 7.3657298472369854 23 12.232398189206295 24 16.225398256403583 25 18.978645135007636
		 26 20.541231197092259 27 19.646151100518722 28 17.830562074960987 29 15.140192392084327
		 30 12.360741117357481 31 11.718980096310089 32 11.68485836314902;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_L_rotateX1";
	rename -uid "513A6D55-419C-BBB3-5928-6FB4B9983168";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 361.89089442745967 1 361.88902899047309
		 2 362.24545199677033 3 2.1400261838403565 4 1.6117706179902771 5 0.41631696300512816
		 6 -0.92032019139594512 7 -2.3906862147423178 8 -2.8927941518018221 9 -2.8659257712163373
		 10 -3.0378689671055428 11 -3.6833335615097265 12 -4.3191008293141024 13 -4.9633492781706599
		 14 -5.6130254726853925 15 -6.2853988295352865 16 -7.1852148626022965 17 -7.8652677140067979
		 18 -7.8726082696969923 19 -7.8941814666767449 20 -8.3315910672313489 21 -8.6243402159807125
		 22 -6.5781724034417817 23 -4.7396780824086662 24 -4.1572057372991758 25 -3.605390088338706
		 26 -2.984684098221829 27 -2.1000895220401317 28 -0.99419820345697718 29 -0.43800847987688363
		 30 -0.20398773709342219 31 0.85083044612734438 32 361.89089442745967;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_L_rotateY1";
	rename -uid "334020C5-4477-3C77-E7AA-08AE973D00FB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 1.4267450792574299 1 0.7157646352264605
		 2 1.2893811488503808 3 3.1367308998057148 4 5.6188929243069241 5 6.7994621726542883
		 6 7.8528722369838935 7 9.0593448186762213 8 10.102052416993775 9 10.942108589871872
		 10 12.027048230178163 11 13.397341425383896 12 14.894505234734284 13 16.508260505319004
		 14 18.196472437132559 15 19.833695026197994 16 20.966904875726126 17 21.709824273703234
		 18 22.108671571610238 19 22.21227448603932 20 20.959950748254197 21 18.45217955900171
		 22 14.558691033578413 23 11.773086029897234 24 11.159202495390515 25 10.550925392836008
		 26 9.7153230520095875 27 8.3579235713005406 28 6.5862823553050855 29 6.0279748620111162
		 30 5.928531023818139 31 4.186827356773243 32 1.4267450792574299;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_L_rotateZ1";
	rename -uid "D577687E-42D2-11C5-8115-18B23BB9FA9C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 1.3937473365350983 1 7.6644119461168954
		 2 17.959975754872879 3 22.228290306605015 4 27.677649249551163 5 29.99016567000357
		 6 30.513621510123794 7 29.736904842261939 8 28.53349915729347 9 26.981190218995412
		 10 25.586089958199317 11 24.395674706871667 12 23.890703840679986 13 23.829885094572628
		 14 23.250136200828678 15 22.226069577015412 16 20.804785522647357 17 18.539174192665183
		 18 14.188404945142976 19 9.2847683930905109 20 5.2132225862931705 21 1.2224410372899261
		 22 -3.0591198409548568 23 -6.5923395780180378 24 -9.1138350297770572 25 -10.525387975738692
		 26 -10.90577582144086 27 -10.768623911948374 28 -9.8539080802452705 29 -8.6103767955422281
		 30 -6.7927168780255158 31 -3.2850063891821843 32 1.3937473365350983;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_L_rotateX1";
	rename -uid "C21F217F-4A1B-6E03-B08B-C9BDF5B5D072";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 363.10661205057869 1 363.10629918956278
		 2 362.93331730649976 3 362.59849080184 4 361.81682510786402 5 360.74825901437714
		 6 359.35068125390171 7 357.61002104271887 8 356.57130129820581 9 356.52441000113851
		 10 356.37754522692353 11 356.06229213818938 12 355.74256125415781 13 355.35723672981436
		 14 354.93085283800428 15 354.47175686610876 16 354.04188874717858 17 353.58634280736254
		 18 352.95299646224572 19 352.16228378060322 20 350.97292475793711 21 350.56177290264799
		 22 352.50430770191753 23 354.23900710951006 24 354.87511014496806 25 355.57052835945905
		 26 356.2685940026717 27 357.46332021154586 28 359.09773376293691 29 360.11992696047696
		 30 360.7794682052384 31 362.10134864103259 32 363.24231782731022;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_L_rotateY1";
	rename -uid "7ABCDB21-46A1-489F-29B2-858EA9E796E4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 3.6807879647352992 1 3.6831477147216094
		 2 3.402144564886183 3 2.9231206657573439 4 2.4598571180590865 5 2.4135337433646695
		 6 2.2093979559949211 7 0.43261427869201602 8 -2.1229684050237383 9 -5.3377796856800774
		 10 -7.366265689320203 11 -8.0748571338007942 12 -7.7202508931287559 13 -6.0824629694429282
		 14 -5.0757509481980811 15 -4.2443841642291549 16 -2.4389702880519928 17 -0.95524979380177211
		 18 -1.6813455941231288 19 -2.8788659742260703 20 -3.7146832742544338 21 -4.7591508386556329
		 22 -6.2907722170499705 23 -7.5323404667643405 24 -8.3270177470278455 25 -8.071978617058793
		 26 -5.5067509458409187 27 -2.6370067454644661 28 0.41161131900677184 29 2.4307780253736295
		 30 3.4797808109757336 31 3.6770198096530438 32 3.7741773917544958;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKKnee_L_rotateZ1";
	rename -uid "E04C4989-44CE-FC32-B91C-6AB1324640AF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -69.855660239687452 1 -70.149194914263461
		 2 -78.008307006203552 3 -76.51164790189911 4 -72.188169140755605 5 -64.734428247322825
		 6 -55.721713921591274 7 -45.291330772161267 8 -36.299386082687505 9 -29.380579028612981
		 10 -25.027150755384231 11 -23.274092637243054 12 -23.998050076964422 13 -27.76359100023528
		 14 -31.986461058016868 15 -36.648412686570282 16 -41.205467599744395 17 -44.167316903328917
		 18 -42.923491782005122 19 -40.283464542266145 20 -37.468972443467656 21 -33.4046515876556
		 22 -26.903937126679178 23 -21.958874123729412 24 -19.79166735664791 25 -19.795898625507601
		 26 -22.592270049864247 27 -26.88929297650375 28 -32.614060700638163 29 -39.097235759095192
		 30 -46.348317983138237 31 -54.482601003263888 32 -62.732760179778566;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_L_rotateX1";
	rename -uid "A9AC2DCD-48DA-465A-3F15-C99EF4FCE060";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 16.033232443736871 1 14.854302414029071
		 2 14.334966955723621 3 13.824913215277972 4 13.160739465505923 5 13.039395728441017
		 6 12.972631754423146 7 12.973194248728962 8 11.723677142717868 9 7.7402668235756407
		 10 6.4179224929718917 11 5.9580007463492572 12 6.1588304705599901 13 7.9535605699873004
		 14 10.436806005543 15 13.542297368892688 16 17.249321711722018 17 19.927722327675511
		 18 19.924851040556025 19 19.543964313987086 20 18.606302217880838 21 16.761661984925425
		 22 12.883300572343215 23 11.921863664000391 24 14.679377443106183 25 17.22028986388834
		 26 19.452557222813397 27 19.754646330404125 28 19.561023629978401 29 19.888592538487647
		 30 20.848860331518296 31 19.33474686369874 32 16.033232443736896;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_L_rotateY1";
	rename -uid "C6C63175-425A-B650-257D-F7BAE94856AB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 25.843350279452995 1 22.954887423294327
		 2 17.381986639050037 3 17.191507904331424 4 17.068673518382909 5 19.397600844744616
		 6 22.559039582537402 7 26.044393620142607 8 26.45729622577106 9 21.095787373947029
		 10 14.327472723985455 11 6.4995221613902414 12 0.20056621383039253 13 -4.7168289696174179
		 14 -8.5760313634232759 15 -11.392343292708055 16 -13.39182516941165 17 -14.312829313744738
		 18 -13.527079096204808 19 -10.029537629325251 20 -2.3382411741452205 21 6.5575303608950302
		 22 15.382825106404621 23 23.550996808398757 24 31.266018562660186 25 33.135694485986001
		 26 32.335342204291244 27 31.0238612407144 28 29.317482796597275 29 28.272025867864773
		 30 27.626471086280848 31 26.894800133236611 32 25.843350279453002;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_L_rotateZ1";
	rename -uid "007D5A5D-42EC-C65D-54C2-A2ABF2706F1B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -12.231927708284198 1 -11.066912872001947
		 2 -8.5252485098337853 3 -8.6137861486725669 4 -8.6670046026133711 5 -7.3489790030968347
		 6 -5.7212066172101821 7 -4.6703308366726013 8 -2.5975721564862164 9 0.85080198422069775
		 10 3.5208162640764042 11 5.3247586219529541 12 7.8586761139264585 13 11.039063707398689
		 14 15.103366006460906 15 19.450211613150017 16 22.149079982111665 17 23.764244097223614
		 18 24.56802795289979 19 24.746723993044224 20 23.529620479162617 21 18.212898323563294
		 22 6.1905360964588887 23 -3.553443667465066 24 -7.9575134617087029 25 -11.553429925686794
		 26 -14.587105395594683 27 -16.022436613272365 28 -16.426292816585061 29 -15.958444479049531
		 30 -14.252365750147522 31 -13.145749351186595 32 -12.231927708284221;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_L_rotateX1";
	rename -uid "46ADB4AF-4B21-63E2-5E8B-0FBB0EB3A775";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 359.74399289899941 1 359.74399289899941
		 2 359.74399289899941 3 359.74399289899941 4 359.74399289899941 5 359.74399289899941
		 6 359.74399289899941 7 359.74399289899941 8 359.74399289899941 9 359.74399289899941
		 10 359.74399289899941 11 359.74399289899941 12 359.74399289899941 13 359.74399289899941
		 14 359.74399289899941 15 359.74399289899941 16 359.74399289899941 17 359.74399289899941
		 18 359.74399289899941 19 359.74399289899941 20 359.74399289899941 21 359.74399289899941
		 22 359.74399289899941 23 359.74399289899941 24 359.74399289899941 25 359.74399289899941
		 26 359.74399289899941 27 359.74399289899941 28 359.74399289899941 29 359.74399289899941
		 30 359.74399289899941 31 359.74399289899941 32 359.74399289899941;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_L_rotateY1";
	rename -uid "E759FBAA-473A-3573-7293-1A9C3482D8D8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.61869281221964367 1 0.61869281221964401
		 2 0.61869281221962058 3 0.6186928122196439 4 0.61869281221962047 5 0.61869281221962003
		 6 0.61869281221961958 7 0.61869281221964245 8 0.61869281221964245 9 0.61869281221961947
		 10 0.61869281221961969 11 0.61869281221962003 12 0.61869281221962014 13 0.6186928122196439
		 14 0.61869281221964367 15 0.61869281221964367 16 0.61869281221964356 17 0.61869281221961947
		 18 0.61869281221964267 19 0.61869281221964245 20 0.61869281221959527 21 0.61869281221964167
		 22 0.61869281221961747 23 0.61869281221961747 24 0.6186928122196178 25 0.6186928122196188
		 26 0.61869281221962025 27 0.61869281221962025 28 0.61869281221962036 29 0.61869281221964367
		 30 0.6186928122196439 31 0.61869281221962036 32 0.61869281221964378;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKToes_L_rotateZ1";
	rename -uid "44C8C108-4699-B158-CCA3-37930A4D877E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 5.3805247741266955 1 5.3804971105800989
		 2 5.3804413380609857 3 5.3860447760975489 4 5.4506095072357974 5 7.3746488652986821
		 6 10.818564968206529 7 16.244228722465266 8 17.447384162502548 9 12.814302066668986
		 10 9.0839508941993596 11 6.6772197473732726 12 5.6081468317416237 13 5.3847571668949481
		 14 5.4137278420348895 15 5.8308449983427915 16 8.1630020351125694 17 11.928453981532227
		 18 14.248697832857296 19 16.5681185395614 20 19.534718243776432 21 23.374221578341139
		 22 29.653435770205064 23 31.408290374734079 24 24.536111836288352 25 16.202799727711653
		 26 6.9571273110885707 27 5.337017702848228 28 5.3754948236191602 29 5.3805247741266955
		 30 5.380532840430444 31 5.3805299230373773 32 5.3805247741266893;
	setAttr ".pst" 3;
createNode animCurveTL -n "RootX_M_translateX1";
	rename -uid "74C9E0C0-43C7-F122-5602-7496BC251F71";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.10804262120973333 1 0.084180396984171721
		 2 0.06824348821400314 3 0.070137888958936703 4 0.073647260304798234 5 0.076256574914288389
		 6 0.083896006965178821 7 0.10062659977142339 8 0.11499562819329476 9 0.12428746907276481
		 10 0.1345617123059259 11 0.14626304714363275 12 0.16699115678112125 13 0.19522726218833494
		 14 0.22224256864065564 15 0.24812163624781464 16 0.27295657242049326 17 0.28858007675497299
		 18 0.28815479303042318 19 0.28435532674430991 20 0.27387068403675796 21 0.26214374687657277
		 22 0.25139291591562862 23 0.24476775980846077 24 0.24409671215239762 25 0.23977484945028688
		 26 0.23037633366239063 27 0.2240524851616667 28 0.21990087400205485 29 0.20290973063850537
		 30 0.17562390102155875 31 0.1423959109877114 32 0.10804262120973333;
	setAttr ".pst" 3;
createNode animCurveTL -n "RootX_M_translateY1";
	rename -uid "812650E7-4101-9EFF-ECD4-AC8BAB8580E9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.5723391203547088 1 -0.63739632921442002
		 2 -0.63506386083290067 3 -0.56305435587915831 4 -0.4243725350059826 5 -0.24796261336356196
		 6 -0.088088017443118005 7 0.038044311137403142 8 0.070322427185729453 9 0.066502171214224859
		 10 0.041519761385480081 11 -0.044555863361479098 12 -0.15195150913456246 13 -0.28124567813645918
		 14 -0.4307441977882025 15 -0.58905464390416817 16 -0.73388317631177991 17 -0.82360357341238633
		 18 -0.82210387898646431 19 -0.80745790863070077 20 -0.71864063283880775 21 -0.56565725738675177
		 22 -0.34944445907776611 23 -0.18104308923561163 24 -0.10360829229245105 25 -0.051923618694919682
		 26 -0.019094071733075424 27 -0.02897750153003642 28 -0.10639202834318695 29 -0.20835785485661518
		 30 -0.33273854377956802 31 -0.45801732893537483 32 -0.5723391203547088;
	setAttr ".pst" 3;
createNode animCurveTL -n "RootX_M_translateZ1";
	rename -uid "3F42D6F2-4500-38D1-38D2-E4B4A4A4A25B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.4891238151986077 1 0.43451889422344225
		 2 0.38129088872623118 3 0.35971292061103127 4 0.3323015125146439 5 0.32299577014207159
		 6 0.31607925518377755 7 0.30755285300530427 8 0.3011943074119719 9 0.29739561625282218
		 10 0.29702407459731067 11 0.2981308980311867 12 0.29104310897386221 13 0.25430325688019728
		 14 0.19501100470848065 15 0.12364655440712724 16 0.0772379062357616 17 0.055037411767632188
		 18 0.074671998969292649 19 0.11634181358942586 20 0.16604323855984687 21 0.22051340317082124
		 22 0.27862528726122698 23 0.32315778353463287 24 0.34498417864163616 25 0.37376833659426745
		 26 0.41344539601360458 27 0.45573629702135443 28 0.49995468200348547 29 0.54176149510488258
		 30 0.57468724929924442 31 0.55126174031365116 32 0.4891238151986077;
	setAttr ".pst" 3;
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 31 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 33 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -s 6 ".r";
select -ne :initialShadingGroup;
	setAttr -s 6 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 2 ".gn";
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :ikSystem;
	setAttr -s 6 ".sol";
connectAttr "FKSpine1_M_rotateX.o" "maxRN.phl[1]";
connectAttr "FKSpine1_M_rotateY.o" "maxRN.phl[2]";
connectAttr "FKSpine1_M_rotateZ.o" "maxRN.phl[3]";
connectAttr "FKChest_M_rotateX.o" "maxRN.phl[4]";
connectAttr "FKChest_M_rotateY.o" "maxRN.phl[5]";
connectAttr "FKChest_M_rotateZ.o" "maxRN.phl[6]";
connectAttr "FKHip_R_rotateX.o" "maxRN.phl[7]";
connectAttr "FKHip_R_rotateY.o" "maxRN.phl[8]";
connectAttr "FKHip_R_rotateZ.o" "maxRN.phl[9]";
connectAttr "FKKnee_R_rotateX.o" "maxRN.phl[10]";
connectAttr "FKKnee_R_rotateY.o" "maxRN.phl[11]";
connectAttr "FKKnee_R_rotateZ.o" "maxRN.phl[12]";
connectAttr "FKAnkle_R_rotateX.o" "maxRN.phl[13]";
connectAttr "FKAnkle_R_rotateY.o" "maxRN.phl[14]";
connectAttr "FKAnkle_R_rotateZ.o" "maxRN.phl[15]";
connectAttr "FKToes_R_rotateX.o" "maxRN.phl[16]";
connectAttr "FKToes_R_rotateY.o" "maxRN.phl[17]";
connectAttr "FKToes_R_rotateZ.o" "maxRN.phl[18]";
connectAttr "FKHip_L_rotateX.o" "maxRN.phl[19]";
connectAttr "FKHip_L_rotateY.o" "maxRN.phl[20]";
connectAttr "FKHip_L_rotateZ.o" "maxRN.phl[21]";
connectAttr "FKKnee_L_rotateX.o" "maxRN.phl[22]";
connectAttr "FKKnee_L_rotateY.o" "maxRN.phl[23]";
connectAttr "FKKnee_L_rotateZ.o" "maxRN.phl[24]";
connectAttr "FKAnkle_L_rotateX.o" "maxRN.phl[25]";
connectAttr "FKAnkle_L_rotateY.o" "maxRN.phl[26]";
connectAttr "FKAnkle_L_rotateZ.o" "maxRN.phl[27]";
connectAttr "FKToes_L_rotateX.o" "maxRN.phl[28]";
connectAttr "FKToes_L_rotateY.o" "maxRN.phl[29]";
connectAttr "FKToes_L_rotateZ.o" "maxRN.phl[30]";
connectAttr "FKNeck_M_rotateX.o" "maxRN.phl[31]";
connectAttr "FKNeck_M_rotateY.o" "maxRN.phl[32]";
connectAttr "FKNeck_M_rotateZ.o" "maxRN.phl[33]";
connectAttr "FKHead_M_rotateX.o" "maxRN.phl[34]";
connectAttr "FKHead_M_rotateY.o" "maxRN.phl[35]";
connectAttr "FKHead_M_rotateZ.o" "maxRN.phl[36]";
connectAttr "FKShoulder_R_rotateX.o" "maxRN.phl[37]";
connectAttr "FKShoulder_R_rotateY.o" "maxRN.phl[38]";
connectAttr "FKShoulder_R_rotateZ.o" "maxRN.phl[39]";
connectAttr "FKElbow_R_rotateX.o" "maxRN.phl[40]";
connectAttr "FKElbow_R_rotateY.o" "maxRN.phl[41]";
connectAttr "FKElbow_R_rotateZ.o" "maxRN.phl[42]";
connectAttr "FKWrist_R_rotateX.o" "maxRN.phl[43]";
connectAttr "FKWrist_R_rotateY.o" "maxRN.phl[44]";
connectAttr "FKWrist_R_rotateZ.o" "maxRN.phl[45]";
connectAttr "FKShoulder_L_rotateX.o" "maxRN.phl[46]";
connectAttr "FKShoulder_L_rotateY.o" "maxRN.phl[47]";
connectAttr "FKShoulder_L_rotateZ.o" "maxRN.phl[48]";
connectAttr "FKElbow_L_rotateX.o" "maxRN.phl[49]";
connectAttr "FKElbow_L_rotateY.o" "maxRN.phl[50]";
connectAttr "FKElbow_L_rotateZ.o" "maxRN.phl[51]";
connectAttr "FKWrist_L_rotateX.o" "maxRN.phl[52]";
connectAttr "FKWrist_L_rotateY.o" "maxRN.phl[53]";
connectAttr "FKWrist_L_rotateZ.o" "maxRN.phl[54]";
connectAttr "RootX_M_translateX.o" "maxRN.phl[55]";
connectAttr "RootX_M_translateY.o" "maxRN.phl[56]";
connectAttr "RootX_M_translateZ.o" "maxRN.phl[57]";
connectAttr "RootX_M_rotateX.o" "maxRN.phl[58]";
connectAttr "RootX_M_rotateY.o" "maxRN.phl[59]";
connectAttr "RootX_M_rotateZ.o" "maxRN.phl[60]";
connectAttr "FKSpine1_M_rotateX1.o" "samRN.phl[1]";
connectAttr "FKSpine1_M_rotateY1.o" "samRN.phl[2]";
connectAttr "FKSpine1_M_rotateZ1.o" "samRN.phl[3]";
connectAttr "FKChest_M_rotateX1.o" "samRN.phl[4]";
connectAttr "FKChest_M_rotateY1.o" "samRN.phl[5]";
connectAttr "FKChest_M_rotateZ1.o" "samRN.phl[6]";
connectAttr "FKHip_R_rotateX1.o" "samRN.phl[7]";
connectAttr "FKHip_R_rotateY1.o" "samRN.phl[8]";
connectAttr "FKHip_R_rotateZ1.o" "samRN.phl[9]";
connectAttr "FKKnee_R_rotateX1.o" "samRN.phl[10]";
connectAttr "FKKnee_R_rotateY1.o" "samRN.phl[11]";
connectAttr "FKKnee_R_rotateZ1.o" "samRN.phl[12]";
connectAttr "FKAnkle_R_rotateX1.o" "samRN.phl[13]";
connectAttr "FKAnkle_R_rotateY1.o" "samRN.phl[14]";
connectAttr "FKAnkle_R_rotateZ1.o" "samRN.phl[15]";
connectAttr "FKToes_R_rotateX1.o" "samRN.phl[16]";
connectAttr "FKToes_R_rotateY1.o" "samRN.phl[17]";
connectAttr "FKToes_R_rotateZ1.o" "samRN.phl[18]";
connectAttr "FKHip_L_rotateX1.o" "samRN.phl[19]";
connectAttr "FKHip_L_rotateY1.o" "samRN.phl[20]";
connectAttr "FKHip_L_rotateZ1.o" "samRN.phl[21]";
connectAttr "FKKnee_L_rotateX1.o" "samRN.phl[22]";
connectAttr "FKKnee_L_rotateY1.o" "samRN.phl[23]";
connectAttr "FKKnee_L_rotateZ1.o" "samRN.phl[24]";
connectAttr "FKAnkle_L_rotateX1.o" "samRN.phl[25]";
connectAttr "FKAnkle_L_rotateY1.o" "samRN.phl[26]";
connectAttr "FKAnkle_L_rotateZ1.o" "samRN.phl[27]";
connectAttr "FKToes_L_rotateX1.o" "samRN.phl[28]";
connectAttr "FKToes_L_rotateY1.o" "samRN.phl[29]";
connectAttr "FKToes_L_rotateZ1.o" "samRN.phl[30]";
connectAttr "FKNeck_M_rotateX1.o" "samRN.phl[31]";
connectAttr "FKNeck_M_rotateY1.o" "samRN.phl[32]";
connectAttr "FKNeck_M_rotateZ1.o" "samRN.phl[33]";
connectAttr "FKHead_M_rotateX1.o" "samRN.phl[34]";
connectAttr "FKHead_M_rotateY1.o" "samRN.phl[35]";
connectAttr "FKHead_M_rotateZ1.o" "samRN.phl[36]";
connectAttr "FKShoulder_R_rotateX1.o" "samRN.phl[37]";
connectAttr "FKShoulder_R_rotateY1.o" "samRN.phl[38]";
connectAttr "FKShoulder_R_rotateZ1.o" "samRN.phl[39]";
connectAttr "FKElbow_R_rotateX1.o" "samRN.phl[40]";
connectAttr "FKElbow_R_rotateY1.o" "samRN.phl[41]";
connectAttr "FKElbow_R_rotateZ1.o" "samRN.phl[42]";
connectAttr "FKWrist_R_rotateX1.o" "samRN.phl[43]";
connectAttr "FKWrist_R_rotateY1.o" "samRN.phl[44]";
connectAttr "FKWrist_R_rotateZ1.o" "samRN.phl[45]";
connectAttr "FKShoulder_L_rotateX1.o" "samRN.phl[46]";
connectAttr "FKShoulder_L_rotateY1.o" "samRN.phl[47]";
connectAttr "FKShoulder_L_rotateZ1.o" "samRN.phl[48]";
connectAttr "FKElbow_L_rotateX1.o" "samRN.phl[49]";
connectAttr "FKElbow_L_rotateY1.o" "samRN.phl[50]";
connectAttr "FKElbow_L_rotateZ1.o" "samRN.phl[51]";
connectAttr "FKWrist_L_rotateX1.o" "samRN.phl[52]";
connectAttr "FKWrist_L_rotateY1.o" "samRN.phl[53]";
connectAttr "FKWrist_L_rotateZ1.o" "samRN.phl[54]";
connectAttr "RootX_M_translateX1.o" "samRN.phl[55]";
connectAttr "RootX_M_translateY1.o" "samRN.phl[56]";
connectAttr "RootX_M_translateZ1.o" "samRN.phl[57]";
connectAttr "RootX_M_rotateX1.o" "samRN.phl[58]";
connectAttr "RootX_M_rotateY1.o" "samRN.phl[59]";
connectAttr "RootX_M_rotateZ1.o" "samRN.phl[60]";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of test_load.ma
