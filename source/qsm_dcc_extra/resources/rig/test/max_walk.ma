//Maya ASCII 2019 scene
//Name: max_walk.ma
//Last modified: Wed, Apr 17, 2024 05:21:26 PM
//Codeset: 936
file -rdi 1 -ns "max" -rfn "maxRN" -op "VERS|2019|UVER|undef|MADE|undef|CHNG|Mon, Sep 11, 2023 11:15:34 AM|ICON|undef|INFO|undef|OBJN|127433|INCL|undef(|LUNI|cm|TUNI|pal|AUNI|deg|TDUR|141120000|"
		 -typ "mayaBinary" "E:/myworkspace/lynxi-root-2.0/packages/qsm_dcc_extra/resources/rig/max.mb";
file -r -ns "max" -dr 1 -rfn "maxRN" -op "VERS|2019|UVER|undef|MADE|undef|CHNG|Mon, Sep 11, 2023 11:15:34 AM|ICON|undef|INFO|undef|OBJN|127433|INCL|undef(|LUNI|cm|TUNI|pal|AUNI|deg|TDUR|141120000|"
		 -typ "mayaBinary" "E:/myworkspace/lynxi-root-2.0/packages/qsm_dcc_extra/resources/rig/max.mb";
requires maya "2019";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2019";
fileInfo "version" "2019";
fileInfo "cutIdentifier" "201812112215-434d8d9c04";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 19045)\n";
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
		"maxRN" 407
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
		2 "|max:Group|max:Geometry" "overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry" "overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry" "overrideShading" " 1"
		2 "|max:Group|max:Geometry" "overrideTexturing" " 1"
		2 "|max:Group|max:Geometry" "overridePlayback" " 1"
		2 "|max:Group|max:Geometry" "overrideEnabled" " 1"
		2 "|max:Group|max:Geometry" "overrideVisibility" " 1"
		2 "|max:Group|max:Geometry" "hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry" "overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry" "overrideColor" " 0"
		2 "|max:Group|max:Geometry" "overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo" "overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo" "overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo" "overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo" "overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo" "overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo" "overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo" "overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo" "hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo" "overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo" "overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo" "overrideColorRGB" " -type \"float3\" 0 0 0"
		
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:model:bodySkinShape" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:bodySkin|max:bodySkinShapeDeformed" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShape" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:head|max:headShapeOrig" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:model:lowerTeethShape" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:lowerTeeth|max:lowerTeethShapeOrig" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:model:upperTeethShape" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:upperTeeth|max:upperTeethShapeOrig" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformed" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browL|max:browLShapeDeformedOrig" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformed" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:browR|max:browRShapeDeformedOrig" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:model:eyeRShape" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeR|max:eyeRShapeOrig" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:model:eyeLShape" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:eyeL|max:eyeLShapeOrig" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overrideDisplayType" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overrideLevelOfDetail" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overrideShading" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overrideTexturing" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overridePlayback" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overrideEnabled" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overrideVisibility" 
		" 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "hideOnPlayback" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overrideRGBColors" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overrideColor" 
		" 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue" "overrideColorRGB" 
		" -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:model:tongueShape" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overrideDisplayType" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overrideLevelOfDetail" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overrideShading" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overrideTexturing" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overridePlayback" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overrideEnabled" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overrideVisibility" " 1"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"hideOnPlayback" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overrideRGBColors" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overrideColor" " 0"
		2 "|max:Group|max:Geometry|max:model:geo|max:model:tongue|max:tongueShapeOrig" 
		"overrideColorRGB" " -type \"float3\" 0 0 0"
		3 "max:Hi.drawInfo" "|max:Group|max:Geometry|max:model:geo.drawOverride" 
		""
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
createNode animCurveTA -n "FKSpine1_M_rotateX";
	rename -uid "C280FE96-40A5-D011-3FBD-0FB3E2912EC7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -9.0590956739125481 1 -7.1899902073397968
		 2 -4.8986282108277353 3 -2.9321258131181041 4 -1.3043385152902707 5 0.081880814247663206
		 6 1.044788633699657 7 1.9600996894323868 8 2.5249046606696601 9 3.1307996274675336
		 10 3.737951872731093 11 4.2956479881047427 12 4.4940337190770077 13 4.681557346640175
		 14 3.9650928656080437 15 3.3511872719159719 16 0.1082051914573393 17 -1.580173767051444
		 18 -3.233060659382426 19 -4.9092586981569761 20 -6.5495553410358553 21 -8.0242941041707407
		 22 -9.4018790780443489 23 -10.765969663103393 24 -12.176703662475253 25 -12.915308581021316
		 26 -13.534859292854097 27 -13.41464967206047 28 -13.086511788052475 29 -12.468172256257379
		 30 -11.741749676802202 31 -10.57032057150079 32 -9.0590956739125481;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKSpine1_M_rotateY";
	rename -uid "960D5F2E-4CA0-3A60-F4EE-1BB002AD207B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 6.5535423094468781 1 5.8846869489481035
		 2 4.9872046660236107 3 4.2654303845422747 4 3.7347261074075306 5 3.477456943386366
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
		 26 -10.501679051452635 27 -10.660538664649172 28 -10.741322707185727 29 -10.5470240473375
		 30 -10.111632323393119 31 -9.5518497912521543 32 -8.8601102641377025;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKChest_M_rotateX";
	rename -uid "9E2EC65E-4C3D-457A-51AE-F6BA3C285E50";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -6.1099049968378074e-05 1 6.5355757936888788e-05
		 2 -5.5247937516262947e-05 3 5.6319294185432715e-05 4 -0.00072199640879850875 5 0.001185704681924039
		 6 0.00057001528371486768 7 -0.0012568332430845741 8 -4.5201650372622819e-05 9 8.2380775601281056e-05
		 10 -7.7848807459563101e-06 11 1.2553930083376832e-05 12 0.00058884764392211364 13 -0.003274214281915567
		 14 1.3608305316021062e-06 15 -6.2649971702733602e-06 16 2.8904438428152446e-13 17 -2.9688606984187461e-07
		 18 -3.6499009528399954e-06 19 9.2920971325166663e-07 20 9.1992954618064308e-05 21 -2.2357780534196798e-05
		 22 -1.0058974260055153e-05 23 1.1809085064227711e-05 24 3.9958128038026558e-05 25 -2.1337426425010858e-05
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
		 10 1.6186555662307461e-05 11 -3.4929347244681567e-05 12 0.00027553386397082409 13 -0.0015297331522944671
		 14 -0.00029484500171554504 15 0.0025839590247633882 16 1.085464755035763e-13 17 -5.0023320679637758e-07
		 18 -1.0093686460800504e-05 19 2.5693528835416723e-06 20 0.00013282682250424701 21 -4.1043304357469132e-05
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
createNode animCurveTA -n "FKHip_R_rotateX";
	rename -uid "571204EC-4363-BD22-9415-9FBADB5261E7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 359.36140793146848 1 359.67517750012684
		 2 360.06429395856242 3 360.37335531110438 4 360.51914444700759 5 360.66634570436196
		 6 360.86721400425006 7 361.08848688395659 8 361.34746318010826 9 361.56944823507928
		 10 361.60936568572203 11 361.60393821653656 12 361.0997735133268 13 360.76141828619592
		 14 360.57807299855949 15 0.63637662440650189 16 1.6549486141928149 17 1.9219888438168884
		 18 2.1230452087964178 19 1.5884323154968132 20 0.96948274095683162 21 360.30576665710629
		 22 359.71247693620916 23 359.5741928811222 24 359.50409943190522 25 359.52821270593734
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
		 22 24.727056521687402 23 23.846737538643463 24 23.003926774784343 25 22.399041230159476
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
		 26 -0.3976719542039111 27 -0.3922101231841662 28 -0.33268947488933232 29 -0.39128991269045277
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
		 2 368.0724931365117 3 367.11201844785046 4 366.48860208674029 5 365.90666908361703
		 6 365.45012204598527 7 364.95536593507109 8 364.44443236543731 9 363.91441030872176
		 10 363.34900704814555 11 362.93504613333641 12 363.23478389914868 13 363.60709576045281
		 14 365.03339066273662 15 366.47433746841688 16 370.1155116084372 17 370.26300979833348
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
		 14 6.1369499386081836 15 7.0830773156341467 16 7.3947820591633517 17 4.2565427072884399
		 18 1.0544171114500167 19 2.7280850626426409 20 4.509891855155435 21 6.7931024909360698
		 22 9.3146048352268647 23 5.8309887253831283 24 0.64594006146443017 25 -1.2503882076093615
		 26 -2.4046590035845599 27 -2.3546211240445603 28 -1.7955328965066177 29 -1.9649302744480257
		 30 -2.1457269545634996 31 -2.1213490354477402 32 -2.583462592745648;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_R_rotateZ";
	rename -uid "C6F7AE3E-4984-7681-6962-E88786EA66DD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 3.35655662320098 1 4.8728488665372574
		 2 4.7327967698073161 3 4.158943241173561 4 4.0192161788848102 5 4.2527480380466152
		 6 5.7131334418637563 7 6.9540043193361161 8 7.8792181670715529 9 8.5428600752408155
		 10 7.4239092122644177 11 6.3379523802558575 12 4.7365390323855747 13 2.4342652962001932
		 14 -7.0993097175028055 15 -15.978438302227268 16 -21.949483280420178 17 -17.110967388720766
		 18 -12.406733906493306 19 -6.2544871069451391 20 0.086170641065148754 21 2.7779399206638766
		 22 5.0753683644980123 23 3.7055745231941497 24 1.7684011395416976 25 0.46662635771747174
		 26 -0.63420081508546455 27 -2.0900429154520155 28 -3.789724341130511 29 -3.6742278640173516
		 30 -2.3709115010207227 31 0.10655629596071121 32 3.35655662320098;
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
		 6 -6.4240074824276796 7 -5.5877880373015625 8 -4.354775178843779 9 -2.6851346347873988
		 10 0.90033049085183026 11 4.992827419550002 12 13.414136549662848 13 21.959515816981465
		 14 37.156698982710793 15 47.349885754233007 16 34.490529986320681 17 26.092958788027246
		 18 17.788189643820328 19 9.3154416231266417 20 0.37145255241223002 21 -3.9502359628096353
		 22 -7.8520845761518787 23 -8.0715126350601416 24 -8.071919688790997 25 -8.0728536094605499
		 26 -8.0738135646943725 27 -8.0752870166644595 28 -8.0769350491112402 29 -8.0786747847060258
		 30 -8.0801164073935112 31 -7.9859495063355705 32 -7.9956234268828705;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHip_L_rotateX";
	rename -uid "29C3DF93-4518-98BD-6540-168D70FC0414";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 1.5332592731336376 1 1.8873145869568122
		 2 1.9177185650323763 3 1.7255927382317227 4 0.90245299246114385 5 0.4009055293177487
		 6 0.31963128166961458 7 0.30311038952356406 8 0.65327007192655406 9 0.85341822685258162
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
		 2 -6.6379088399357089 3 -5.321726917480496 4 -4.4617743623378185 5 -4.0390270553320837
		 6 -4.043473376490728 7 -4.14498568572193 8 -4.5749236530874899 9 -4.8010765738011623
		 10 -4.0549656771469795 11 -3.3108381070981374 12 -1.9137767251474911 13 -0.48661228975561543
		 14 1.2919602231475724 15 3.3046655486159082 16 6.654037412414155 17 6.7471554063310366
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
		 6 18.888994696928531 7 19.654470762765676 8 21.432761651675953 9 22.92488231323275
		 10 23.318242300924481 11 23.581140167277116 12 21.044779091012316 13 18.854960638124275
		 14 17.136559264264008 15 16.079351438164636 16 14.850957629767521 17 12.065265287423259
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
		 6 359.23078473585656 7 359.41075630113306 8 359.63733585583509 9 359.76794860802522
		 10 359.5455099811623 11 359.31718519910078 12 358.98882797325376 13 358.66470470033232
		 14 358.45505066134353 15 358.17907872811645 16 357.51903751205236 17 357.56658428423384
		 18 357.72089733053758 19 357.91805811462473 20 358.11938668435118 21 358.41162105209656
		 22 358.60264752490798 23 359.037802141496 24 359.53923993347354 25 359.98575715488471
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
	setAttr -s 33 ".ktv[0:32]"  0 -54.036841632034474 1 -55.426015672585962
		 2 -52.546169362268202 3 -47.508422856300626 4 -38.692151413619804 5 -29.944767934071905
		 6 -20.02337780200504 7 -12.357948915581165 8 -10.997718171651341 9 -9.8255303482899041
		 10 -11.896937591653625 11 -13.305237082808139 12 -12.883991189893255 13 -12.637382364194739
		 14 -14.014029581070568 15 -16.521170850869861 16 -23.326430037079056 17 -22.61340789959613
		 18 -20.996701963650114 19 -17.805755037567152 20 -13.622312559086883 21 -9.3978538705937282
		 22 -5.3028762756807337 23 -1.5706874836043041 24 1.3329826034317336 25 1.1878425506126837
		 26 0.76331266265245701 27 -6.7975620099940519 28 -18.209092996834013 29 -28.30203433681422
		 30 -39.109318247751908 31 -47.309895659576341 32 -54.036841632034474;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKAnkle_L_rotateX";
	rename -uid "9DFEB668-4036-3D81-AC5E-EE8A0C8492D6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 369.68416764904629 1 371.680912178288
		 2 373.30432089647957 3 374.52356335138978 4 374.97765879826562 5 374.92171443964469
		 6 373.01327432422897 7 371.30224362236572 8 369.84007071611114 9 368.83112843852268
		 10 369.50746373651259 11 370.17030305242884 12 371.23689542439502 13 372.16013181761855
		 14 372.15696073088299 15 372.23694932877652 16 371.42259533978319 17 371.61883913446025
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
		 2 7.1689815745676624 3 6.6745976679741643 4 6.9068844770105935 5 6.5532274546635447
		 6 3.7036874548248617 7 1.7902018834869098 8 1.4870233820968459 9 1.1786620586532108
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
		 14 -1.7928580021308234 15 1.3574612811298636 16 9.3796448221851403 17 11.423931050123969
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
		 2 -0.077235056997567969 3 -0.077235056997568927 4 -0.077235056997542711 5 -0.077235056997543183
		 6 -0.077235056997542406 7 -0.077235056997542365 8 -0.077235056997567358 9 -0.07723505699754217
		 10 -0.077235056997542351 11 -0.077235056997592574 12 -0.077235056997567442 13 -0.077235056997592283
		 14 -0.077235056997567678 15 -0.077235056997542115 16 -0.077235056997542656 17 -0.077235056997567261
		 18 -0.077235056997567803 19 -0.077235056997567372 20 -0.077235056997567608 21 -0.077235056997567789
		 22 -0.077235056997542212 23 -0.077235056997542476 24 -0.077235056997542531 25 -0.077235056997593504
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
		 22 -8.07449265767419 23 -6.826616267497883 24 -5.1746909211465395 25 -3.2008394854289706
		 26 -1.7462052643448014 27 7.4006086805567826 28 20.746189346251686 29 26.802306261896909
		 30 29.243190423512953 31 25.225230448051793 32 12.267092796042386;
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
		 18 0.63539434612215795 19 0.7297276471906704 20 0.8204061979175844 21 0.89701459105481185
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
		 10 0.49787321534369045 11 0.55195991321058646 12 0.50670303619082913 13 0.46034289178604954
		 14 0.33715317318743809 15 0.2187687625168846 16 0.13748970542847222 17 -0.13723408602013903
		 18 -0.41117974388908596 19 -0.50827110211157567 20 -0.59387220471590207 21 -0.66864549093492487
		 22 -0.73941175701324491 23 -0.79974545721110646 24 -0.86554252748623317 25 -0.87476659413134772
		 26 -0.87588363941196679 27 -0.81629278037317932 28 -0.71748868715212766 29 -0.55525209182714252
		 30 -0.3468978624681508 31 -0.18084218509307323 32 -0.027502301970704836;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKNeck_M_rotateZ";
	rename -uid "85B699A2-4141-A8E0-1900-D09896DE108A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 21.367025535549441 1 21.407217492121742
		 2 21.474797527639346 3 21.493449481595729 4 21.459491052254204 5 21.413983516996076
		 6 21.334822094364775 7 21.272157920007452 8 21.255667458009398 9 21.231022633664729
		 10 21.192585094225851 11 21.155043360273279 12 21.117536914289737 13 21.077196998371655
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
		 2 0.29248023931435913 3 0.062984806901200979 4 -0.036964830358059864 5 -0.12074283920719237
		 6 -0.15646364230344828 7 -0.19157154755850175 8 -0.20628547057813956 9 -0.20689516965152352
		 10 -0.052458687478402127 11 0.072943455921425079 12 0.12431019041021818 13 0.18423628915470844
		 14 0.29012854921263914 15 0.39830278840820982 16 1.0344942963371178 17 1.3422746433529533
		 18 1.6479625107722657 19 1.8727858701264024 20 2.0930023510431983 21 2.2778955109837522
		 22 2.4548907529105408 23 2.56089621353828 24 2.6670813827843483 25 2.6183921014678999
		 26 2.5305089862476007 27 2.423717197450423 28 2.3208753709534902 29 2.0963660820807393
		 30 1.8091891449712583 31 1.4362817177558591 32 0.98231056939409189;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKHead_M_rotateY";
	rename -uid "5E172C3F-4553-A34B-6654-F1912139F9D5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -0.25826897806517796 1 -0.14679730809377883
		 2 -0.12612534406186671 3 -0.080636737306736941 4 -0.013609647985206058 5 0.055360564269715973
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
		 10 -12.902122173599757 11 -12.940237871620736 12 -12.977705032220999 13 -13.01798781752775
		 14 -13.093047193654185 15 -13.16656332997983 16 -13.302200953287921 17 -13.107595458582411
		 18 -12.916345713123267 19 -12.689520145489166 20 -12.448443631224366 21 -12.41153311709586
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
		 10 70.406652805387992 11 70.944657973822558 12 72.000784502420814 13 72.956778585537094
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
		 30 -46.54751112398516 31 -38.645327855030693 32 -28.82406918977459;
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
		 26 -33.533493702654475 27 -33.92157147023223 28 -34.447142827433801 29 -34.506312827922159
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
	setAttr -s 33 ".ktv[0:32]"  0 8.7983879196947097 1 9.8081037180117256
		 2 10.800239537890658 3 11.676424351583995 4 12.378719442152564 5 12.987533025774091
		 6 13.443615182863047 7 13.743084080932835 8 13.746186517540906 9 13.747216606647916
		 10 13.700512458288301 11 13.621041160532645 12 13.161875702947667 13 12.681929475493284
		 14 11.527713462915797 15 10.402427436782444 16 7.5345243399873914 17 6.529504053319056
		 18 5.5276364272429142 19 5.1441605751072128 20 4.7947166250145949 21 4.6102688616357179
		 22 4.4361108906817535 23 4.4758500187974422 24 4.5449976148988247 25 4.6425308373776977
		 26 4.7425442703953422 27 5.0460671808867623 28 5.4151067336352607 29 6.0595240477943095
		 30 6.8512736944401533 31 7.7677330927615635 32 8.7983879196947097;
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
		 6 0.63862918007430314 7 1.273177774420452 8 1.3222564146003233 9 1.3289428003248409
		 10 0.74251793124848553 11 0.16696076973126259 12 -0.80998194269452872 13 -1.760642616462361
		 14 -2.7229739210621271 15 -3.6706694955494985 16 -5.0063387761345961 17 -5.1092109735024511
		 18 -5.2072502338925002 19 -5.1552054039972699 20 -5.0927063489237687 21 -4.990952324165991
		 22 -4.871656922711348 23 -5.0988684743514021 24 -5.4213197553668735 25 -5.6358202238580608
		 26 -5.8291128660462981 27 -5.9215764625725082 28 -5.9755492205472978 29 -5.6724809323253256
		 30 -4.9821540482386366 31 -4.3731034946847736 32 -3.7665334564744892;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_L_rotateX";
	rename -uid "47999D5F-42B7-2724-0014-54B81172C84F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 11.724572882481178 1 17.681736831112534
		 2 22.035787850481157 3 24.799060935640476 4 26.352844407283445 5 27.335991527613757
		 6 27.771568114037343 7 28.011589692510125 8 27.949388293066296 9 27.977621435549302
		 10 28.909776832549149 11 29.564448465398154 12 29.012883696242564 13 28.104419785082133
		 14 24.167394184000695 15 19.026796134164091 16 -3.9300144137999946 17 -9.968548559097135
		 18 -16.107565501312333 19 -19.677276754245334 20 -22.756874355816485 21 -23.879480143908363
		 22 -24.511394035856441 23 -24.972832275422682 24 -25.351549799332432 25 -25.524116387924831
		 26 -25.706370023947212 27 -23.949342704628695 28 -20.866198642533199 29 -13.781237746669751
		 30 -4.8804226759342466 31 4.0768846751364967 32 11.724572882481178;
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
		 22 75.624983321884798 23 75.506741164814429 24 75.420214800041606 25 75.991475957921381
		 26 76.756739046209589 27 78.032670711784959 28 79.563689602694325 29 80.175438772025046
		 30 80.279138967981922 31 79.751850827336639 32 78.700159483277488;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKShoulder_L_rotateZ";
	rename -uid "8DF1D51C-4392-FCDD-92BF-E9924EF3C015";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -23.392047505979651 1 -31.552203751238579
		 2 -38.092606746605007 3 -42.858851534901497 4 -46.178766038418082 5 -48.786725826213029
		 6 -50.642969589380009 7 -52.153588081609314 8 -52.716488349884024 9 -53.148772057922102
		 10 -52.963348728392049 11 -52.531438130849672 12 -50.262919015506959 13 -47.627483542252101
		 14 -41.259646086281229 15 -33.70057935555824 16 -3.8547254526249364 17 3.2759764216097005
		 18 10.527212086867495 19 15.409581803995623 20 19.80943363613147 21 22.112676177927941
		 22 23.881985909626515 23 24.925270248062191 24 25.855532214875428 25 25.760384146393964
		 26 25.529480707081557 27 22.503352893808415 28 17.83648880039523 29 8.7832012655685983
		 30 -2.3469706738983356 31 -13.51816286470515 32 -23.392047505979651;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_L_rotateX";
	rename -uid "C4A5B1D6-4B76-9CB4-EC1B-79B9BDB35885";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 -34.443658353063505 1 -35.038180877124645
		 2 -35.346494689597698 3 -35.657072594079132 4 -35.926339501505417 5 -36.244258035296205
		 6 -36.69187878216087 7 -37.082145126106369 8 -37.339650870702542 9 -37.445833922453851
		 10 -36.478782123458224 11 -35.659902230362661 12 -35.136897689509979 13 -34.613008285431121
		 14 -34.324520011326747 15 -34.001757492630546 16 -32.028751060877454 17 -32.92125762118534
		 18 -33.791409970599361 19 -32.779990944889107 20 -31.648453489852322 21 -29.908887209242589
		 22 -28.057539936759746 23 -27.128265870004341 24 -26.205405390624392 25 -26.521553302688215
		 26 -27.056761633611579 27 -28.19552816036876 28 -29.56390369768426 29 -30.982363053028536
		 30 -32.466401064992318 31 -33.576435780656929 32 -34.443658353063505;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKElbow_L_rotateY";
	rename -uid "8914DBBE-4A28-C001-A3D4-74B5840C26AE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.40893261469702746 1 0.42334970142944889
		 2 0.25806129052742405 3 0.19218027543215124 4 0.22885742121274194 5 0.35765807149191386
		 6 0.69892300642388372 7 1.0351312062222655 8 1.3964949305899992 9 1.6350494500524755
		 10 1.40908376299937 11 1.1941471322116999 12 0.88980564390667538 13 0.58173504884485105
		 14 0.1940359857795021 15 -0.19850424485151044 16 -1.8180212546773209 17 -2.0940656195632856
		 18 -2.3534693151441339 19 -3.2459011233151478 20 -4.1695095590371007 21 -4.7722620747878111
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
		 10 14.022585079709422 11 13.100536286682626 12 12.295265823491304 13 11.532620008102739
		 14 11.384370769523688 15 11.214692239736317 16 11.515588114608462 17 13.315568998384201
		 18 15.069801847101004 19 17.433739877682097 20 19.811014558960341 21 22.64955956794827
		 22 25.514440616616795 23 27.309674381405252 24 29.149284832042174 25 29.258601814278176
		 26 29.171605928363338 27 28.105955006560304 28 26.426334639399656 29 24.414648717911525
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
		 18 3.7377696929083495 19 3.7316915977856349 20 3.7290192923990308 21 3.5027657020898801
		 22 3.2216464663325635 23 3.1242087888597592 24 3.0497722487616552 25 3.1587692535282832
		 26 3.3296254063303969 27 3.5523002314299212 28 3.83165009954191 29 3.8787202307417985
		 30 3.8680691993395384 31 3.77015322671943 32 3.5910110794208872;
	setAttr ".pst" 3;
createNode animCurveTA -n "FKWrist_L_rotateY";
	rename -uid "251FBA6A-4F58-A0B9-5039-189899E4476D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 33 ".ktv[0:32]"  0 0.63991496186001795 1 2.1899933052334566
		 2 4.7580194037888885 3 6.9300964328137526 4 8.8879327346986923 5 9.828597436188204
		 6 9.553047940868991 7 9.3040667556428609 8 9.0367065511938005 9 8.7475243009490296
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
	setAttr -s 33 ".ktv[0:32]"  0 -3.3624865884024873 1 -3.2613701831545256
		 2 -2.8488696534122866 3 -2.5137771427783284 4 -2.1961001944653904 5 -2.0540354569631747
		 6 -2.1626323933253779 7 -2.3251258791591285 8 -2.6817135266468042 9 -2.9768146588637148
		 10 -3.0612077818572803 11 -3.1566334244106455 12 -3.2216390910416206 13 -3.2764910102555294
		 14 -3.1376733830610379 15 -3.0047076011153964 16 -2.3235554634895523 17 -2.4274095052673328
		 18 -2.5366070901025717 19 -2.5159174908669621 20 -2.4882376397271231 21 -2.5070486342373579
		 22 -2.5257003963140621 23 -2.6740281246760156 24 -2.862035338473444 25 -2.9317918173020914
		 26 -2.9664284780086008 27 -3.032885156273629 28 -3.1100875844540807 29 -3.1729541573570152
		 30 -3.2281897548000953 31 -3.2909065522278329 32 -3.3624865884024873;
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
		 6 -2.9578435417498632 7 -3.1693835798357886 8 -3.676860762003666 9 -4.0059282390860123
		 10 -3.8214166121303772 11 -3.5780044245949414 12 -2.7496508151580987 13 -1.9407199401677091
		 14 -1.1340812496560722 15 -0.10121281424760616 16 0.79093474149699872 17 0.37354010700626006
		 18 -0.030720733206484052 19 -0.89611725534263831 20 -1.7309572826124777 21 -2.1673165095366751
		 22 -2.510253524506787 23 -2.4416793037570446 24 -2.2958688837068384 25 -2.5326499111743002
		 26 -2.8972986704744721 27 -3.5617594100785266 28 -4.4269259819238265 29 -5.062038559172569
		 30 -5.7585996821822647 31 -5.9173381084583392 32 -5.7812927983303668;
	setAttr ".pst" 3;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "9CD97EAB-4780-DF1D-AA79-5188CF5F0878";
	setAttr -s 31 ".lnk";
	setAttr -s 25 ".slnk";
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
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
// End of max_walk.ma
