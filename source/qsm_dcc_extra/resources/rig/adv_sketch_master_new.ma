//Maya ASCII 2020 scene
//Name: adv_sketch_master_new.ma
//Last modified: Thu, Jul 18, 2024 07:12:50 PM
//Codeset: 936
requires maya "2020";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "202011110415-b1e20b88e2";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 19045)\n";
fileInfo "UUID" "3903A91E-405D-5BBE-B96E-F9BC38E5D261";
createNode transform -s -n "persp";
	rename -uid "C6B49449-4465-CD0B-F950-6AA68939DCFD";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -8.1638248545168679 12.795758344446893 18.327933714493422 ;
	setAttr ".r" -type "double3" -18.938352729603412 -25.400000000000002 -8.8022540096438517e-16 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "1A0AC5FB-4CAF-0C53-9CC6-1FA2A6B4E5B1";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 22.476759562395571;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "F1C42A29-4295-01D6-49CD-9A9F5ECCD134";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "4F6AADC9-4FCB-75C6-A124-658398EE6C90";
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
	rename -uid "57CCB228-4EF2-0269-0032-6FA3F05C3482";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 2.0111639134067221 5.1666808626969427 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "FA81FF30-4C93-9430-FC9B-2A975393A153";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 53.392464202931102;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "ED8BEE58-49EF-E55E-02B4-27BCD9E38C53";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "B8E9DC71-4DDA-B2C7-BF27-CB977E57D0D8";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode dagContainer -n "LAYER";
	rename -uid "E419FEC4-4E84-C3C1-099C-EFBCCBF23159";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "out_timeEditorLayer.png";
	setAttr ".ctor" -type "string" "nothings";
	setAttr ".cdat" -type "string" "2024/07/16 13:55:06";
createNode transform -n "LAYER_OFFSET" -p "LAYER";
	rename -uid "2BA262CD-4EB2-24DA-F46D-49A70A3C274E";
createNode transform -n "OFFSET" -p "LAYER_OFFSET";
	rename -uid "05990FF9-48B5-1E9E-038F-F291043E63D5";
createNode joint -n "Root_M" -p "OFFSET";
	rename -uid "364D19E9-4914-FFDC-CBAD-4CA6C1D8B3EE";
	addAttr -ci true -sn "fat" -ln "fat" -dv 1.1110763381902267 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 0.64999999999999991 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.6597575736796981e-07 8.3725490425459217 -1.7450406099424539e-16 ;
	setAttr ".r" -type "double3" 0 0 1.1198709655450322e-13 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 90.000002504478161 0 90.000002504478161 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 4.4408920985006262e-16 1 -1.9428902930940239e-15 0
		 -6.106226635438361e-16 1.8873791418627661e-15 1 0 1 -4.4408920985006262e-16 5.5511151231257827e-16 0
		 1.5316312041853076e-16 8.3627805915218154 0.28793993198261336 1;
createNode joint -n "Hip_R" -p "Root_M";
	rename -uid "C2092294-488D-FD50-E3EF-2B8F94276E2C";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.55608024366205711 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -k true -sn "twistAmount" -ln "twistAmount" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "twistAddition" -ln "twistAddition" -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.52882916166556804 -0.041596145865366058 -0.63698151849080897 ;
	setAttr ".r" -type "double3" -1.218242606159776e-06 1.1035610010232429e-16 3.5163275573808946e-06 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.45021576190533 0.29305660345666978 -179.38658571959749 ;
	setAttr ".bps" -type "matrix" -0.0051147797346149495 -0.99992961110611422 -0.010705692945416843 0
		 0.0095952939418561568 -0.010754415762693518 0.99989613104350616 0 -0.99994088293380434 0.0050115241971186893 0.0096496250075297826 0
		 -0.63698151849080908 7.8339514298562474 0.24634378611724797 1;
createNode joint -n "Knee_R" -p "Hip_R";
	rename -uid "E247AF5B-4D47-7474-7244-A7B5F1448AC4";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.41626223700831527 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.5331840515136723 -1.1102230246251565e-16 2.886579864025407e-15 ;
	setAttr ".r" -type "double3" 0 0 -1.9295923281396557e-06 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -9.9392333795734924e-17 -5.5908187760100887e-17 -3.4260508487653136 ;
	setAttr ".bps" -type "matrix" -0.0056790557774453691 -0.99749980779574332 -0.070440625869817322 0
		 0.0092724841893051298 -0.070491262385324147 0.99746929925902095 0 -0.99994088293380434 0.0050115241971186893 0.0096496250075297826 0
		 -0.6550529766761588 4.3010160752598567 0.20851860254209867 1;
createNode joint -n "Ankle_R" -p "Knee_R";
	rename -uid "49055B3C-4604-74DF-413E-EFBE44E98CF6";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.37752837948846102 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.559377193450926 -1.8915424782051105e-14 -2.2204460492503131e-16 ;
	setAttr ".r" -type "double3" -1.5643429783092405e-14 1.1217639225746935e-07 -1.2373401603105654e-07 ;
	setAttr ".ro" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.0169722652891755 0.28714040565539589 4.0422532267675244 ;
	setAttr ".bps" -type "matrix" 1.5512205235601595e-11 -0.99999999999999944 -3.1463363301572332e-08 0
		 0.027395982105753242 -3.145112891330586e-08 0.99962465964203784 0 -0.99962465964203873 -8.7747611867555753e-10 0.027395982105753273 0
		 -0.67526687829073351 0.7505380089200071 -0.042206154671357271 1;
createNode joint -n "Toes_R" -p "Ankle_R";
	rename -uid "7FBB9524-45A9-1F51-BDAD-EDB823728848";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.23313111850415758 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1.6 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.45736554094383813 1.024308098529672 -8.6772833363113477e-10 ;
	setAttr ".r" -type "double3" 1.4138559632876281e-14 -5.5659703104344817e-15 3.0970970618203368e-06 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.1228236478136107 -1.0785970067453798 59.98037853616664 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.0048998279758237749 -0.50020788371578062 0.86589148555369633 0
		 -0.023341153144323432 0.86560875751689825 0.50017663827886305 0 -0.99971555067214046 -0.022661685255766801 -0.0074340948116085499 0
		 -0.64720495107813913 0.29317243576052315 0.98171746527591863 1;
createNode joint -n "ToesEnd_R" -p "Toes_R";
	rename -uid "FFFEBDBF-4407-0B77-B3EC-68B83EB9F120";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.23313111850415758 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" 0.60368670875957775 1.2212453270876722e-15 2.3314683517128287e-15 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "Spine1_M" -p "Root_M";
	rename -uid "FBA1ACD7-43E6-FDEF-B852-E487BD1D9E04";
	addAttr -ci true -sn "fat" -ln "fat" -dv 1.0110763381902266 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 0.74333333333333329 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.56152814085142566 5.551115123125755e-17 -3.9011935763210889e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.791516639546772e-22 -5.1817813007657502e-22 -2.0127412719108724e-29 ;
	setAttr ".bps" -type "matrix" 4.4408920985006262e-16 1 -1.9428902930940239e-15 0
		 -6.106226635438361e-16 1.8873791418627661e-15 1 0 1 -4.4408920985006262e-16 5.5511151231257827e-16 0
		 1.241235178829182e-17 8.9243087323732411 0.28793993198261231 1;
createNode joint -n "Spine2_M" -p "Spine1_M";
	rename -uid "9D5B7007-42F1-99D6-718B-1D8AA59399D2";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.96440967152355994 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 0.79 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.59962425599902502 5.5511151231257938e-17 -7.5946554363953729e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.791516639546772e-22 -5.1817813007657502e-22 -2.0127412719108724e-29 ;
	setAttr ".bps" -type "matrix" 4.4408920985006262e-16 1 -1.9428902930940239e-15 0
		 -6.106226635438361e-16 1.8873791418627661e-15 1 0 1 -4.4408920985006262e-16 5.5511151231257827e-16 0
		 -4.807665391265629e-16 9.5239329883722661 0.2879399319826112 1;
createNode joint -n "Chest_M" -p "Spine2_M";
	rename -uid "DFB3DE87-4191-3DFD-2D8F-5AB616E5BA84";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.97107633819022654 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 0.78999999999999992 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.63772037114661706 -1.6653345369377417e-16 -6.9714607688025038e-16 ;
	setAttr ".r" -type "double3" 0 0 5.5659706925611543e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.791516639546772e-22 -9.4787915988669299e-23 -4.8991021656929163 ;
	setAttr ".bps" -type "matrix" 4.9461476520504664e-16 0.99634663456583983 -0.085401310231897801 0
		 -5.7046603543048761e-16 0.085401310231897759 0.99634663456583983 0 1 -4.4408920985006262e-16 5.5511151231257827e-16 0
		 -8.9470787321520091e-16 10.161653359518883 0.28793993198260981 1;
createNode joint -n "Neck_M" -p "Chest_M";
	rename -uid "E38C17DE-4B51-8587-3892-508713799458";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.43867319307110153 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.5849514155166684 -2.2204460492503131e-16 1.978345154726677e-15 ;
	setAttr ".r" -type "double3" 0 0 1.113194138512231e-14 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 11.793716668165006 ;
	setAttr ".bps" -type "matrix" 3.6757653973919305e-16 0.9927686297656918 0.12004352441156778 0
		 -6.5951705889384174e-16 -0.12004352441156782 0.9927686297656918 0 1 -4.4408920985006262e-16 5.5511151231257827e-16 0
		 1.8675776537586594e-15 11.740814368319279 0.15258300444358502 1;
createNode joint -n "Head_M" -p "Neck_M";
	rename -uid "5D34AA5F-45F3-4782-01C2-C4A56B934399";
	addAttr -ci true -sn "fat" -ln "fat" -dv 1.2486731930711015 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.0169299053850334 -2.2204460492503131e-15 3.7801001732114054e-15 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.5830332790935439e-22 7.7311393978258399e-22 -7.1369572981869469 ;
	setAttr ".bps" -type "matrix" 4.466679680214047e-16 0.99999105491813767 -0.0042296670920964341 0
		 -6.0873885195726657e-16 0.0042296670920963925 0.99999105491813767 0 1 -4.4408920985006262e-16 5.5511151231257827e-16 0
		 6.0587306754969433e-15 12.750390477056072 0.27465885436552495 1;
createNode joint -n "HeadEnd_M" -p "Head_M";
	rename -uid "CEE4BC3B-4BF6-0114-DC28-1EB73267A64A";
	addAttr -ci true -sn "fat" -ln "fat" -dv 1.249 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4461326387374598 -2.8310687127941492e-15 1.4643878777056214e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "Scapula_R" -p "Chest_M";
	rename -uid "823D95CA-4069-E4CF-FC7C-49BD12DEA731";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.4451174234256749 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.1963593845272431 -0.16669359158877284 -0.33923371315041151 ;
	setAttr ".r" -type "double3" -2.2556460832502148e-06 3.7210004925649057e-15 1.987845943464573e-16 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 57.95465371135073 90.021230732418573 54.919461078185513 ;
	setAttr ".bps" -type "matrix" -0.99999993134776388 -0.00023808161281032225 -0.00028393945362714115 0
		 -0.00031408546475769844 0.13803732152772852 0.99042697823502934 0 -0.00019660821069447987 0.99042699942125778 -0.13803738682913178 0
		 -0.33923371315041173 11.33940615489492 0.019684674052589834 1;
createNode joint -n "Shoulder_R" -p "Scapula_R";
	rename -uid "F315A6BE-47CA-8D02-82B9-84AABF0C336A";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.41511742342567487 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -k true -sn "twistAmount" -ln "twistAmount" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "twistAddition" -ln "twistAddition" -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.69760793046178393 -6.4392935428259079e-15 -8.1712414612411521e-14 ;
	setAttr ".r" -type "double3" -4.6116489876005424e-15 -1.2970699560343405e-14 3.683728371304424e-15 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -7.9457955567758374 0.29736421166712645 -1.6286531647825455 ;
	setAttr ".bps" -type "matrix" -0.9995725484721053 -0.0093014393529667772 -0.027716485472434372 0
		 -0.027715285579239909 -0.00025789960227404207 0.99961582442109054 0 -0.0093050140376983916 0.99995670741975551 -2.6852704781976655e-09 0
		 -1.0368415957198507 11.339240067273643 0.019486595637975366 1;
createNode joint -n "Elbow_R" -p "Shoulder_R";
	rename -uid "8D95E6DB-451F-0AED-C5CC-CDBF6690EEA5";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.2196966777562363 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -k true -sn "twistAmount" -ln "twistAmount" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "twistAddition" -ln "twistAddition" -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0315295518981626 4.9960036108132044e-16 -1.7763568394002505e-15 ;
	setAttr ".r" -type "double3" 0 0 4.3732626870123352e-15 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.7462428959817215e-19 1.9868632290703983e-16 3.3711672905765 ;
	setAttr ".bps" -type "matrix" -0.99947260455435483 -0.0093005091752102666 0.031112911699423932 0
		 0.031111564716236099 0.00028950876257698079 0.99951587617485282 0 -0.0093050140376989901 0.99995670741975529 -2.6838756495006777e-09 0
		 -3.0675027672070927 11.320343918352982 -0.036820263674058051 1;
createNode joint -n "Wrist_R" -p "Elbow_R";
	rename -uid "A1859BE5-415D-1A36-5AA4-75806B75209E";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.19210763381902257 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1.4100000000000006 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.88294356609389 -5.7398530373120593e-14 3.5971225997855072e-14 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.761171992749937e-19 -9.9587313279454181e-17 -1.987846675914698e-16 ;
	setAttr ".bps" -type "matrix" -0.99947260455435483 -0.0093005091752102666 0.031112911699423932 0
		 0.031111564716236099 0.00028950876257698079 0.99951587617485282 0 -0.0093050140376989901 0.99995670741975529 -2.6838756495006777e-09 0
		 -4.9494532774398188 11.302831584440151 0.021763593232762137 1;
createNode joint -n "MiddleFinger1_R" -p "Wrist_R";
	rename -uid "20BAA7A8-492A-E9F8-83B1-01A758232B23";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.083252447401662988 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.62782141712601458 0.028269968418709657 0.084808257193524028 ;
	setAttr ".r" -type "double3" -4.6714396883995402e-15 -9.6410563781862853e-15 -5.466578358765416e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.0421285448297084 4.6279031013952077 -0.37484035476347732 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.99564481223973045 -0.089952730275273327 0.024493145492884519 0
		 0.011749064153193533 0.13956043978715837 0.99014384971979652 0 -0.092484416804323621 0.98611935888230007 -0.13789576746922041 0
		 -5.5768532034814751 11.381805295618596 0.069553227572658166 1;
createNode joint -n "MiddleFinger2_R" -p "MiddleFinger1_R";
	rename -uid "1AE4EF83-4C38-7470-ECDE-3097ACC1AD50";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.25054061666085392 1.1102230246251565e-15 -7.0876637892069994e-12 ;
	setAttr ".r" -type "double3" 0 8.3489560388417288e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 3.3063643767221156 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98865344659422993 -0.14667735327776663 0.032405502199153391 0
		 0.011749064153193533 0.13956043978715837 0.99014384971979652 0 -0.14975420537959622 0.97928986397381024 -0.13625358817029951 0
		 -5.8263026687145416 11.359268483098113 0.075689755349387933 1;
createNode joint -n "MiddleFinger3_R" -p "MiddleFinger2_R";
	rename -uid "A989D2A0-417C-7D4C-F513-6385FAFE4194";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.18688778786226923 -2.2204460492503131e-16 3.907985046680551e-14 ;
	setAttr ".r" -type "double3" 0 1.5455507905236776e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0.31504276895152905 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.9878150768399061 -0.1520597670620156 0.033154203486373823 0
		 0.011749064153193533 0.13956043978715837 0.99014384971979652 0 -0.1551880583656311 0.97846855385723064 -0.13607334659383166 0
		 -6.0110699243109513 11.331856277014577 0.081745947969948288 1;
createNode joint -n "MiddleFinger4_R" -p "MiddleFinger3_R";
	rename -uid "1DA19E94-41DE-6C17-0469-40BE17A68802";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.053252447401662968 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" 0.18115391430840155 -6.6613381477509392e-16 -1.0658141036401503e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "ThumbFinger1_R" -p "Wrist_R";
	rename -uid "D596B947-46C9-78D6-6AE5-D797C66A3A33";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.11325244740166299 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.14374345962256729 0.1884101501828184 -0.028185664678991529 ;
	setAttr ".r" -type "double3" -2.1235695370375725e-06 6.3611096244772548e-15 1.4113711281112565e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -65.498105876026443 15.002501974196528 27.02196834726151 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.84395224403898295 -0.26672575807802512 0.46540517805377679 0
		 0.41439086847912709 -0.8751135520529173 0.24991294311107776 0 0.34062415930564838 0.403774245081368 0.84908276457969145 0
		 -5.0869969248303315 11.273364799015651 0.2145548072152309 1;
createNode joint -n "ThumbFinger2_R" -p "ThumbFinger1_R";
	rename -uid "AC3916C6-42A7-5C36-4BB7-5EBBCF5C36E5";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.10325244740166298 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.27267209710481244 -1.5987211554602254e-14 5.3290705182007514e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.84395224403898295 -0.26672575807802512 0.46540517805377679 0
		 0.41439086847912709 -0.8751135520529173 0.24991294311107776 0 0.34062415930564838 0.403774245081368 0.84908276457969145 0
		 -5.3171191530687576 11.200636127208659 0.34145781311859402 1;
createNode joint -n "ThumbFinger3_R" -p "ThumbFinger2_R";
	rename -uid "C599E4A8-4124-3543-48A8-C9BFF51D5AAB";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.073252447401662979 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.17963884026204258 -1.7763568394002505e-15 2.3536728122053319e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.84395224403898295 -0.26672575807802512 0.46540517805377679 0
		 0.41439086847912709 -0.8751135520529173 0.24991294311107776 0 0.34062415930564838 0.403774245081368 0.84908276457969145 0
		 -5.4687257554244626 11.152721821359522 0.42506265955614175 1;
createNode joint -n "ThumbFinger4_R" -p "ThumbFinger3_R";
	rename -uid "91AA4408-4FD0-C159-6B3F-5A9F8C76DF64";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" 0.20724412934139047 -2.8691447795381464e-07 -1.8335008089565008e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "IndexFinger1_R" -p "Wrist_R";
	rename -uid "34C9D66E-4B7B-BB67-EA3A-23B6A0C16EC1";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.093252447401662983 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.61026106187090523 0.17207985322355862 0.05669800259183333 ;
	setAttr ".r" -type "double3" 7.5165452433024493e-16 1.6660639952510062e-14 -1.6151254241806921e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 3.051447202745257 2.6966607102717637 2.3141549622688302 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.99585895398792657 -0.056317153198857627 0.071367513741543001 0
		 0.068349467766634614 0.053812003805787115 0.99620912388033456 0 -0.05994409076873819 0.99696170764076109 -0.049739918374751571 0
		 -5.5545663926261399 11.353901212449323 0.21274713687896318 1;
createNode joint -n "IndexFinger2_R" -p "IndexFinger1_R";
	rename -uid "B64A9575-4BB7-3E96-E01A-FA9213ED9AA6";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.24678135317476713 1.3322676295501878e-15 5.1514348342607263e-14 ;
	setAttr ".r" -type "double3" 0 9.5416640443905487e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 6.4227790581920612 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98290288244757928 -0.16748781962050638 0.076483684240556321 0
		 0.068349467766634614 0.053812003805787115 0.99620912388033456 0 -0.17096863435220577 0.98440443849323167 -0.041444270322532575 0
		 -5.800325812862491 11.340003189176009 0.23035930849281872 1;
createNode joint -n "IndexFinger3_R" -p "IndexFinger2_R";
	rename -uid "C10D438A-4C74-6871-8B5A-23952956A78B";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.15062951415164649 -3.5527136788005009e-15 -1.9539925233402755e-14 ;
	setAttr ".r" -type "double3" 0 1.9679682091555511e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -0.36182308142249014 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98396294423231312 -0.16126800325737811 0.076220440191961211 0
		 0.068349467766634614 0.053812003805787115 0.99620912388033456 0 -0.16475823085265232 0.9854424891244461 -0.041926435509353065 0
		 -5.9483799965038209 11.314774580280238 0.24188000869049864 1;
createNode joint -n "IndexFinger4_R" -p "IndexFinger3_R";
	rename -uid "2971A892-4A47-08B2-D2B6-A2B61D9477D6";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.04325244740166298 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" 0.17039479669862789 -5.3290705182007514e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "Cup_R" -p "Wrist_R";
	rename -uid "DD35FD56-40F1-D2F9-29C4-59BB1B771E47";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.093252447401663052 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.15341432108665298 -0.08657177004601424 -0.012137618108589265 ;
	setAttr ".r" -type "double3" -1.4411888400381559e-14 1.4908850069360234e-14 4.9696166897867428e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 20.021096164984744 -10.054865764922001 5.8310251288805066 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.97754206142477451 0.1655022610007249 0.13046271401841303 0
		 0.18059279214815782 0.33880280629564868 0.92336282244322865 0 0.10861750121198013 0.92618662268996355 -0.3610825091037011 0
		 -5.105367131031735 11.289242597213473 -0.0599930990988157 1;
createNode joint -n "PinkyFinger1_R" -p "Cup_R";
	rename -uid "C3B965C8-4D8B-DF7C-F530-638075618E47";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.40420147142822938 -0.18356061944482827 0.021732731646169512 ;
	setAttr ".r" -type "double3" 3.4588532160915748e-14 6.361109362927032e-15 5.2180975242760842e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -8.8837615298315953 5.0552069929472063 -16.764489289479329 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.99381240480976685 -0.021103337197337591 -0.10904839845391209 0
		 -0.11099825551053422 0.22437446618713303 0.968160878261902 0 0.0040362507164267564 0.97427447266279865 -0.22532856143369748 0
		 -5.5312802404306849 11.31407656696658 -0.18460023905853312 1;
createNode joint -n "PinkyFinger2_R" -p "PinkyFinger1_R";
	rename -uid "770FB24D-467E-5E57-11DE-CF96B4E8F764";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.053252447401662975 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.16890317859353843 1.3322676295501878e-15 1.4210854715202004e-14 ;
	setAttr ".r" -type "double3" 0 7.9513867036587888e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 8.250591894714006 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98410556488941447 -0.16069607485165771 -0.075584447348356842 0
		 -0.11099825551053422 0.22437446618713303 0.968160878261902 0 -0.13862043293578435 0.96116224980515619 -0.23864514476977366 0
		 -5.6991383145287422 11.310512146235036 -0.20301886017793663 1;
createNode joint -n "PinkyFinger3_R" -p "PinkyFinger2_R";
	rename -uid "908876B7-44E8-075B-0388-9E8C8EEB8D24";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.053252447401662975 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.11865603280626225 -7.9936057773011271e-15 -6.9277916736609768e-14 ;
	setAttr ".r" -type "double3" 0 1.987846675914698e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -1.145915564648438 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.9866809741190633 -0.1414419736669365 -0.080341915565024069 0
		 -0.11099825551053422 0.22437446618713303 0.968160878261902 0 -0.11891191103112418 0.96418373093951371 -0.2370858291979622 0
		 -5.8159083767210742 11.291444587505532 -0.2119874108421376 1;
createNode joint -n "PinkyFinger4_R" -p "PinkyFinger3_R";
	rename -uid "0AD332F5-4D19-AA5E-D9ED-7D8C01D71268";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.033252447401662971 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" 0.1393407709630754 -3.1086244689504383e-15 5.8619775700208265e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "RingFinger1_R" -p "Cup_R";
	rename -uid "C7CEE155-40F0-AD7D-A70E-B5972972F1C4";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.073252447401662979 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.4563956396984139 -0.065831777829516103 0.012258222186043 ;
	setAttr ".r" -type "double3" -4.1545995526617185e-14 1.3318572728628477e-14 -3.3793393490549915e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -13.90484873966683 9.3574667383968961 -13.573562366806408 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.9970745022337707 -0.070309840495513504 -0.029982717101251576 0
		 -0.039265347322753524 0.13460350109518249 0.99012127034648789 0 -0.065579489895102053 0.9884019545824535 -0.13697045916066564 0
		 -5.5620703525949633 11.353826517829035 -0.065663331084794593 1;
createNode joint -n "RingFinger2_R" -p "RingFinger1_R";
	rename -uid "167BECFC-45CB-38C6-7A71-F493E66F04DF";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.23175265222754682 3.1086244689504383e-15 3.5527136788005009e-15 ;
	setAttr ".r" -type "double3" 0 1.3517357396219947e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 6.8754933878906224 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98205351141394526 -0.18812799389174184 -0.013370064839354552 0
		 -0.039265347322753524 0.13460350109518249 0.99012127034648789 0 -0.18446987076258115 0.9728770505090496 -0.1395747519204269 0
		 -5.7931450129560975 11.337532025816508 -0.072611905293996054 1;
createNode joint -n "RingFinger3_R" -p "RingFinger2_R";
	rename -uid "AF022980-44B0-9B4C-BADA-BD8D8944A7E8";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.1623061679037443 -2.886579864025407e-15 7.2830630415410269e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98205351141394526 -0.18812799389174184 -0.013370064839354552 0
		 -0.039265347322753524 0.13460350109518249 0.99012127034648789 0 -0.18446987076258115 0.9728770505090496 -0.1395747519204269 0
		 -5.9525383550701267 11.306997692052592 -0.074781949282709578 1;
createNode joint -n "RingFinger4_R" -p "RingFinger3_R";
	rename -uid "89D9305D-4B2B-D136-838E-31A1FB44459D";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.043252447401662966 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" 0.16556611470121529 -6.2172489379008766e-15 -1.4210854715202004e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "Scapula_L" -p "Chest_M";
	rename -uid "D3414BF2-4635-A6BA-726A-5BBD4964E852";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.4451174234256749 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.1963593845272413 -0.16669359158877495 0.33923371315041567 ;
	setAttr ".r" -type "double3" 5.0751713482778153e-12 -1.9083328088779469e-14 3.6775163504421066e-14 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -122.04534881356916 89.978769446431599 54.919460596166864 ;
	setAttr ".bps" -type "matrix" -0.9999999313489204 0.0002380796095726965 0.0002839370596843008 0
		 -0.00031408281794054996 -0.13803732520717227 -0.99042697772305899 0 -0.00019660655592054443 -0.9904269989089296 0.1380373905074756 0
		 0.33923371315041545 11.339406154894917 0.019684674052588225 1;
createNode joint -n "Shoulder_L" -p "Scapula_L";
	rename -uid "787EA485-47E5-A45A-87EC-33B799C9DA78";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.41511742342567487 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -k true -sn "twistAmount" -ln "twistAmount" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "twistAddition" -ln "twistAddition" -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.69760793046178382 5.5511151231257827e-15 9.0594198809412774e-14 ;
	setAttr ".r" -type "double3" 1.1220224296108548e-11 3.071595835540049e-13 1.0851779244232573e-13 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -7.9457955567758374 0.29736421166712645 -1.6286531647825455 ;
	setAttr ".bps" -type "matrix" -0.99957254855707511 0.0093014374524606307 0.027716483045857138 0
		 -0.027715283187617561 0.0002578958345711424 -0.99961582448837227 0 -0.0093050120334945991 -0.99995670743840515 6.3764223623419269e-09 0
		 1.0368415957206607 11.33924006867111 0.019486597308006615 1;
createNode joint -n "Elbow_L" -p "Shoulder_L";
	rename -uid "90B79F33-4FD5-97C6-CF72-9A9B2E3991E4";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.2196966777562363 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -k true -sn "twistAmount" -ln "twistAmount" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "twistAddition" -ln "twistAddition" -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0315295518981635 -3.8191672047105385e-14 1.7319479184152442e-14 ;
	setAttr ".r" -type "double3" 0 0 1.0774128983457664e-13 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -5.5893590421038628e-18 -1.182106513289636e-16 3.3711672905764987 ;
	setAttr ".bps" -type "matrix" -0.9994726044985407 0.0093005070564168065 -0.031112914125764137 0
		 0.031111567108716747 -0.00028951241256909571 -0.99951587609932568 0 -0.0093050120334929112 -0.99995670743840515 6.3755943302545859e-09 0
		 3.0675027673805229 11.320343923611341 -0.036820257074346052 1;
createNode joint -n "Wrist_L" -p "Elbow_L";
	rename -uid "ED768C77-46C4-325D-B4EA-9D8D44142A58";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.19210763381902257 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1.4100000000000006 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.8829435660938896 2.1538326677728037e-14 -3.907985046680551e-14 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.4819267922473163e-18 -1.8721675328633496e-17 1.987846675914698e-16 ;
	setAttr ".bps" -type "matrix" -0.9994726044985407 0.0093005070564168065 -0.031112914125764137 0
		 0.031111567108716747 -0.00028951241256909571 -0.99951587609932568 0 -0.0093050120334929112 -0.99995670743840515 6.3755943302545859e-09 0
		 4.9494532775081561 11.302831593688083 0.021763604401140023 1;
createNode joint -n "MiddleFinger1_L" -p "Wrist_L";
	rename -uid "D3972CEE-46BB-A596-8039-01B9B6481DE2";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.083252447401662988 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.62782141712601369 -0.028269968418693253 -0.084808257193536463 ;
	setAttr ".r" -type "double3" -4.6105618839496516e-14 -1.9170296380852366e-14 2.2363275104040422e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.0421285448297084 4.6279031013952077 -0.37484035476347732 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.99564481236140856 0.089952728188738645 -0.02449314820961879 0
		 0.011749066802386103 -0.13956044344114951 -0.99014384917333231 0 -0.092484415157844321 -0.9861193585555007 0.13789577091049199 0
		 5.5768532032771647 11.381805306301539 0.069553239949104603 1;
createNode joint -n "MiddleFinger2_L" -p "MiddleFinger1_L";
	rename -uid "0D1B4B0B-4026-FA63-3196-9F8013F94CEF";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.25054061666085836 -5.9952043329758453e-15 7.0770056481705979e-12 ;
	setAttr ".r" -type "double3" 0 -1.590277340731758e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 3.3063643767221156 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98865344681066591 0.14667735117585703 -0.032405505109840499 0
		 0.011749066802386103 -0.13956044344114951 -0.99014384917333231 0 -0.1497542037428754 -0.97928986376789562 0.13625359144915536 0
		 5.8263026685407207 11.359268494303825 0.07568976840648993 1;
createNode joint -n "MiddleFinger3_L" -p "MiddleFinger2_L";
	rename -uid "800C7F65-48FC-BB1B-AC12-81B565D4D0CB";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.18688778786226923 -6.2172489379008766e-15 -4.4408920985006262e-14 ;
	setAttr ".r" -type "double3" 0 5.6653630263568893e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0.31504276895152905 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98781507706533833 0.15205976495900558 -0.033154206415045739 0
		 0.011749066802386103 -0.13956044344114951 -0.99014384917333231 0 -0.15518805673012509 -0.97846855366287644 0.1360733498566335 0
		 6.0110699241775789 11.331856288613112 0.081745961571027384 1;
createNode joint -n "MiddleFinger4_L" -p "MiddleFinger3_L";
	rename -uid "EA24B767-43EF-CC76-2042-7D8D31A39EFB";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.053252447401662968 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" -0.18115391430840244 -5.1070259132757201e-15 1.4210854715202004e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "ThumbFinger1_L" -p "Wrist_L";
	rename -uid "8C97B714-4345-D81E-F3C5-71A628B644B9";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.11325244740166299 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.14374345962256729 -0.18841015018282467 0.02818566467894712 ;
	setAttr ".r" -type "double3" -1.7791227749436549e-14 2.2263882770244617e-14 -8.9453100416161435e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -65.498107999596002 15.002501974196548 27.021968347261506 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.84395224345983744 0.26672575465791487 -0.46540518106406281 0
		 0.41439086732319963 0.87511355195526463 -0.24991294536971567 0 0.34062416214683566 -0.40377424755227503 -0.849082762264881 0
		 5.0869969244963693 11.273364809255362 0.21455481882220923 1;
createNode joint -n "ThumbFinger2_L" -p "ThumbFinger1_L";
	rename -uid "D69737A0-434F-8195-23C1-3DBF28E9C3AC";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.10325244740166298 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.27267209710481177 3.0198066269804258e-14 -2.9753977059954195e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.84395224345983744 0.26672575465791487 -0.46540518106406281 0
		 0.41439086732319963 0.87511355195526463 -0.24991294536971567 0 0.34062416214683566 -0.40377424755227503 -0.849082762264881 0
		 5.3171191525768773 11.200636138380959 0.3414578255464123 1;
createNode joint -n "ThumbFinger3_L" -p "ThumbFinger2_L";
	rename -uid "6687A154-4094-9362-EC9E-33B7C44C2645";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.073252447401662979 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.17963884026204213 1.2434497875801753e-14 -4.1300296516055823e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.84395224345983744 0.26672575465791487 -0.46540518106406281 0
		 0.41439086732319963 0.87511355195526463 -0.24991294536971567 0 0.34062416214683566 -0.40377424755227503 -0.849082762264881 0
		 5.4687257548285411 11.152721833146224 0.42506267252473601 1;
createNode joint -n "ThumbFinger4_L" -p "ThumbFinger3_L";
	rename -uid "93BCD4DE-48FB-5FA6-92D5-B7BEA5538A18";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" -0.20724412934139202 2.8691449038831252e-07 1.833500635761709e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "IndexFinger1_L" -p "Wrist_L";
	rename -uid "C0961C11-45EE-2D16-3D02-CF8780F55D40";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.093252447401662983 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.61026106187090523 -0.17207985322354824 -0.056698002591874186 ;
	setAttr ".r" -type "double3" -6.3238372377536329e-15 2.5220804700667736e-15 1.7393658414253597e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 3.051447202745257 2.6966607102717637 2.3141549622688302 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.99585895393001589 0.05631715093779547 -0.071367516333862249 0
		 0.068349470258476749 -0.053812007368861811 -0.99620912351690449 0 -0.059944088889565511 -0.99696170757616509 0.049739921934164086 0
		 5.5545663921350847 11.353901223619468 0.21274714930572197 1;
createNode joint -n "IndexFinger2_L" -p "IndexFinger1_L";
	rename -uid "4341F72B-4DA6-4951-B7FC-59A6B64764B8";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.24678135317476446 -3.6637359812630166e-15 -4.6185277824406512e-14 ;
	setAttr ".r" -type "double3" 0 2.3854160110976372e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 6.4227790581920612 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98290288260024383 0.16748781736640975 -0.076483687214775123 0
		 0.068349470258476749 -0.053812007368861811 -0.99620912351690449 0 -0.17096863247834956 -0.98440443868197269 0.041444273569617281 0
		 5.8003258123571388 11.340003200904134 0.23035932155931582 1;
createNode joint -n "IndexFinger3_L" -p "IndexFinger2_L";
	rename -uid "F5967677-4299-4DA7-A53F-ADB2751483DF";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.15062951415164472 -2.2759572004815709e-15 1.0658141036401503e-14 ;
	setAttr ".r" -type "double3" 0 7.8519943698630569e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -0.36182308142249014 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98396294437314125 0.16126800100213451 -0.076220443145615477 0
		 0.068349470258476749 -0.053812007368861811 -0.99620912351690449 0 -0.1647582289778694 -0.98544248929894884 0.041926438775155103 0
		 5.9483799960214654 11.314774592347897 0.24188002220500662 1;
createNode joint -n "IndexFinger4_L" -p "IndexFinger3_L";
	rename -uid "5F107179-41E1-21D4-3DD1-1C8115BB768E";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.04325244740166298 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" -0.170394796698627 -3.3306690738754696e-16 -1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "Cup_L" -p "Wrist_L";
	rename -uid "FE99E375-4B6E-5F15-E8DA-368D76343AA4";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.093252447401663052 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.15341432108665298 0.08657177004601202 0.012137618108605253 ;
	setAttr ".r" -type "double3" -1.5505204072134644e-14 1.2324649390671126e-14 -9.3428793767990819e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 20.021096164984744 -10.054865764922001 5.8310251288805066 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.97754206078085459 -0.16550226344456287 -0.13046271574302898 0
		 0.1805927950368795 -0.33880280936319296 -0.92336282075269593 0 0.10861750220423763 -0.92618662113114869 0.3610825128036223 0
		 5.1053671313229572 11.289242606470232 -0.059993087506853122 1;
createNode joint -n "PinkyFinger1_L" -p "Cup_L";
	rename -uid "306E09C3-4DCF-B2CC-F1EF-AFB36C84CDE7";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.40420147142822582 0.18356061944484203 -0.021732731646153525 ;
	setAttr ".r" -type "double3" -9.3428793767990803e-15 -9.9392333795734938e-16 -3.677516350442191e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -8.8837615298315953 5.0552069929472063 -16.764489289479329 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.99381240511302349 0.021103335610468524 0.1090483959972796 0
		 -0.1109982527439561 -0.22437447000549768 -0.96816087769416748 0 0.0040362521299335818 -0.97427447181780535 0.22532856506195495 0
		 5.5312802409703226 11.314076576614168 -0.18460022653958225 1;
createNode joint -n "PinkyFinger2_L" -p "PinkyFinger1_L";
	rename -uid "C015C0E1-4B3A-00B1-1370-9F81A7104FA7";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.053252447401662975 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.16890317859353843 4.4408920985006262e-16 -5.3290705182007514e-15 ;
	setAttr ".r" -type "double3" 0 -3.180554681463516e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 8.250591894714006 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98410556539237459 0.16069607315995399 0.075584444396485456 0
		 -0.1109982527439561 -0.22437447000549768 -0.96816087769416748 0 -0.13862043158042567 -0.96116224919662874 0.23864514800794456 0
		 5.6991383151196029 11.310512156150637 -0.20301884724404887 1;
createNode joint -n "PinkyFinger3_L" -p "PinkyFinger2_L";
	rename -uid "564153BA-4441-B000-09DF-078C3F640EB9";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.053252447401662975 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.11865603280625869 4.4408920985006262e-15 7.460698725481052e-14 ;
	setAttr ".r" -type "double3" 0 1.133072605271378e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -1.145915564648438 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98668097459481752 0.14144197198774086 0.080341912678502131 0
		 -0.1109982527439561 -0.22437447000549768 -0.96816087769416748 0 -0.11891190966597803 -0.96418373029727611 0.23708583249451895 0
		 5.8159083773716116 11.29144459762186 -0.21198739755798718 1;
createNode joint -n "PinkyFinger4_L" -p "PinkyFinger3_L";
	rename -uid "F4CF295F-41F3-3D67-F553-7F91AE30238B";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.033252447401662971 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" -0.13934077096307274 -4.4408920985006262e-16 -5.5067062021407764e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "RingFinger1_L" -p "Cup_L";
	rename -uid "85802480-47E8-697C-BAF2-3F9D5B243ED8";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.073252447401662979 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.45639563969841657 0.065831777829527649 -0.012258222186051881 ;
	setAttr ".r" -type "double3" -2.8426207465580184e-14 -2.6040791454482544e-14 1.1927080055488253e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -13.90484873966683 9.3574667383968961 -13.573562366806408 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.99707450244644269 0.070309838608444669 0.029982714454052525 0
		 -0.039265344683550155 -0.13460350485133757 -0.99012126994051475 0 -0.065579488241833475 -0.98840195420516541 0.13697046267480012 0
		 5.562070352770311 11.353826527980107 -0.065663318639804361 1;
createNode joint -n "RingFinger2_L" -p "RingFinger1_L";
	rename -uid "E425C04D-46C0-C471-3F10-B6A118ACBAE4";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.23175265222754415 -5.5511151231257827e-15 0 ;
	setAttr ".r" -type "double3" 0 -3.1805546814635168e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 6.8754933878906224 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98205351182300427 0.18812799197307761 0.01337006179050769 0
		 -0.039265344683550155 -0.13460350485133757 -0.99012126994051475 0 -0.18446986914666125 -0.97287705036037986 0.13957475509238793 0
		 5.7931450131807338 11.337532036404903 -0.072611892235504613 1;
createNode joint -n "RingFinger3_L" -p "RingFinger2_L";
	rename -uid "4A71B26A-47F3-8A45-3F66-62B0BE651B0F";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.06325244740166297 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.16230616790374386 -3.5527136788005009e-15 -6.9277916736609768e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.98205351182300427 0.18812799197307761 0.01337006179050769 0
		 -0.039265344683550155 -0.13460350485133757 -0.99012126994051475 0 -0.18446986914666125 -0.97287705036037986 0.13957475509238793 0
		 5.9525383553611526 11.306997702952398 -0.074781935729364132 1;
createNode joint -n "RingFinger4_L" -p "RingFinger3_L";
	rename -uid "5C28C9CB-4E36-7294-3E69-999E32FB9915";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.043252447401662966 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" -0.16556611470121263 -4.4408920985006262e-16 1.4210854715202004e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode joint -n "Hip_L" -p "Root_M";
	rename -uid "CFBF9B17-49C9-79B6-BD1E-A6B98E102A05";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.55608024366205711 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -k true -sn "twistAmount" -ln "twistAmount" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "twistAddition" -ln "twistAddition" -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.52882916166557159 -0.041596145865366613 0.63698151849080864 ;
	setAttr ".r" -type "double3" -3.8825130388958935e-19 3.3675432571793796e-37 -9.9392333795734874e-17 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.45021452567681 0.29305659555572489 0.61341076394270422 ;
	setAttr ".bps" -type "matrix" -0.0051147801855959 0.99992961110385403 0.01070569294106153 0
		 0.0095952939418574544 0.010754415762690268 -0.99989613104350616 0 -0.9999408829314973 -0.0050115246480945726 -0.0096496250123593013 0
		 0.63698151849080853 7.8339514298562438 0.24634378611724814 1;
createNode joint -n "Knee_L" -p "Hip_L";
	rename -uid "B4F335F1-42F9-9865-E10C-B1A4C2D37EE0";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.41626223700831527 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.5331840515136728 4.9543702473897611e-15 -2.4424906541753444e-15 ;
	setAttr ".r" -type "double3" 0 0 -1.9295923130320209e-06 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -6.2120208622334312e-18 -3.4260508487653136 ;
	setAttr ".bps" -type "matrix" -0.0056790562276203766 0.99749980779348757 0.070440625865468842 0
		 0.0092724841623556854 0.070491262385184883 -0.99746929925928129 0 -0.9999408829314973 -0.0050115246480945726 -0.0096496250123593013 0
		 0.65505297826955822 4.3010160752678388 0.20851860255748211 1;
createNode joint -n "Ankle_L" -p "Knee_L";
	rename -uid "41B63EE3-48D4-DA3B-56BF-5C8FA22F69CB";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.37752837948846102 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.5593771934509268 3.7789216200678766e-14 2.886579864025407e-15 ;
	setAttr ".r" -type "double3" -9.102361782540403e-15 1.3692611757468858e-07 -1.2330451683565046e-07 ;
	setAttr ".ro" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.0169722652891755 0.28714040565539589 4.0422532267675244 ;
	setAttr ".bps" -type "matrix" -4.3544854094051955e-10 0.99999999999999956 3.1459031530912387e-08 0
		 0.027395982110603029 3.1459153270892138e-08 -0.99962465964190494 0 -0.9996246596419055 4.2656596744433672e-10 -0.027395982110602967 0
		 0.67526688148647451 0.75053800893601785 -0.04220615464051497 1;
createNode joint -n "Toes_L" -p "Ankle_L";
	rename -uid "07D2727B-4491-C513-30C7-2382BC00DAC9";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.23313111850415758 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1.6 -at "double";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.45736554093793519 -1.0243080985323074 9.6422725359701644e-10 ;
	setAttr ".r" -type "double3" 1.9679682091555504e-14 3.7769086842379623e-15 2.0975199042374293e-13 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.1228235895436711 -1.0785971214673817 59.980381631686683 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.0048998277544506572 0.50020788371423996 -0.86589148555583928 0
		 -0.023341152751541191 -0.86560875752959088 -0.50017663827522707 0 -0.99971555068239581 0.022661684804966546 0.0074340948066602651 0
		 0.64720495437863235 0.2931724357742182 0.98171746530859672 1;
createNode joint -n "ToesEnd_L" -p "Toes_L";
	rename -uid "9578D532-496C-175C-2DAD-18BA17AEDF29";
	addAttr -ci true -sn "fat" -ln "fat" -dv 0.23313111850415758 -at "double";
	addAttr -ci true -sn "fatFront" -ln "fatFront" -dv 1 -at "double";
	addAttr -ci true -sn "fatWidth" -ln "fatWidth" -dv 1 -at "double";
	setAttr ".t" -type "double3" -0.60368670875957797 -7.5495165674510645e-15 -2.55351295663786e-15 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "787217F8-49B8-0CF9-A199-089C7567AEDB";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "CC2F9AF7-4F89-74AE-88FE-D1957B610AD7";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "BA1E65E5-48E3-7446-BBED-7BBBB41FDB30";
createNode displayLayerManager -n "layerManager";
	rename -uid "E9553010-47EE-DE53-8650-92BC3A251E13";
createNode displayLayer -n "defaultLayer";
	rename -uid "EBBFDF04-44F9-2CD8-8336-118BE27AFE56";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "872D6684-41D8-E8E9-3979-808B6F94F9DB";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "EB9A5688-4F41-D03B-6CCD-1F9B15608A85";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "0CFF3704-42B2-CD58-AE1C-37AF4D644FDC";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n"
		+ "            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n"
		+ "            -width 1007\n            -height 718\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n"
		+ "            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n"
		+ "            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n"
		+ "            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 893\n            -height 718\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 1\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n"
		+ "            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -autoExpandAnimatedShapes 1\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n"
		+ "            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -autoExpandAnimatedShapes 1\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n"
		+ "            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -autoExpandAnimatedShapes 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n"
		+ "                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n"
		+ "                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -valueLinesToggle 1\n                -outliner \"graphEditor1OutlineEd\" \n"
		+ "                -highlightAffectedCurves 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -autoExpandAnimatedShapes 1\n"
		+ "                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n"
		+ "                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n"
		+ "                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n"
		+ "\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n"
		+ "                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n"
		+ "                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n"
		+ "                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n"
		+ "                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n"
		+ "                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Front View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Front View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -camera \\\"persp\\\" \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1007\\n    -height 718\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Front View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -camera \\\"persp\\\" \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1007\\n    -height 718\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "DED8F773-4EA7-AC2F-1DFB-0F84EB0BFB94";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode hyperLayout -n "hyperLayout1";
	rename -uid "65EE20E6-474A-2257-75E7-00AE5D3AF897";
	setAttr ".ihi" 0;
	setAttr -s 69 ".hyp";
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "997265A3-4818-C8A3-FD06-6FB7AB1F7290";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -584.52378629692112 -353.5714145217629 ;
	setAttr ".tgi[0].vh" -type "double2" 584.52378629692112 352.38093837859196 ;
	setAttr -s 15 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -91.428573608398438;
	setAttr ".tgi[0].ni[0].y" 291.42855834960938;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 61.428569793701172;
	setAttr ".tgi[0].ni[1].y" -32.857143402099609;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 61.428569793701172;
	setAttr ".tgi[0].ni[2].y" 97.142860412597656;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" -91.428573608398438;
	setAttr ".tgi[0].ni[3].y" 31.428571701049805;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" -91.428573608398438;
	setAttr ".tgi[0].ni[4].y" 551.4285888671875;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" -245.71427917480469;
	setAttr ".tgi[0].ni[5].y" 227.14285278320313;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" -91.428573608398438;
	setAttr ".tgi[0].ni[6].y" -228.57142639160156;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" -91.428573608398438;
	setAttr ".tgi[0].ni[7].y" -358.57144165039063;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" -371.42855834960938;
	setAttr ".tgi[0].ni[8].y" -65.714286804199219;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" -91.428573608398438;
	setAttr ".tgi[0].ni[9].y" 161.42857360839844;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" -91.428573608398438;
	setAttr ".tgi[0].ni[10].y" -488.57144165039063;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" 61.428569793701172;
	setAttr ".tgi[0].ni[11].y" -162.85714721679688;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" -91.428573608398438;
	setAttr ".tgi[0].ni[12].y" -98.571426391601563;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" 61.428569793701172;
	setAttr ".tgi[0].ni[13].y" 227.14285278320313;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" -91.428573608398438;
	setAttr ".tgi[0].ni[14].y" 421.42855834960938;
	setAttr ".tgi[0].ni[14].nvs" 18304;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 89;
	setAttr -av -k on ".unw" 89;
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".ihi";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -av ".ta";
	setAttr -av ".tq";
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -av ".hfd";
	setAttr -av ".hfs";
	setAttr -av ".hfe";
	setAttr -av ".hfa";
	setAttr -av ".mbe";
	setAttr -av -k on ".mbsof";
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr -av ".btrs" 512;
	setAttr -k off -cb on ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off -cb on ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -cb on ".hwcc";
	setAttr -cb on ".hwdp";
	setAttr -cb on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
connectAttr "hyperLayout1.msg" "LAYER.hl";
connectAttr "Root_M.s" "Hip_R.is";
connectAttr "Hip_R.s" "Knee_R.is";
connectAttr "Knee_R.s" "Ankle_R.is";
connectAttr "Ankle_R.s" "Toes_R.is";
connectAttr "Toes_R.s" "ToesEnd_R.is";
connectAttr "Root_M.s" "Spine1_M.is";
connectAttr "Spine1_M.s" "Spine2_M.is";
connectAttr "Spine2_M.s" "Chest_M.is";
connectAttr "Chest_M.s" "Neck_M.is";
connectAttr "Neck_M.s" "Head_M.is";
connectAttr "Head_M.s" "HeadEnd_M.is";
connectAttr "Chest_M.s" "Scapula_R.is";
connectAttr "Scapula_R.s" "Shoulder_R.is";
connectAttr "Shoulder_R.s" "Elbow_R.is";
connectAttr "Elbow_R.s" "Wrist_R.is";
connectAttr "Wrist_R.s" "MiddleFinger1_R.is";
connectAttr "MiddleFinger1_R.s" "MiddleFinger2_R.is";
connectAttr "MiddleFinger2_R.s" "MiddleFinger3_R.is";
connectAttr "MiddleFinger3_R.s" "MiddleFinger4_R.is";
connectAttr "Wrist_R.s" "ThumbFinger1_R.is";
connectAttr "ThumbFinger1_R.s" "ThumbFinger2_R.is";
connectAttr "ThumbFinger2_R.s" "ThumbFinger3_R.is";
connectAttr "ThumbFinger3_R.s" "ThumbFinger4_R.is";
connectAttr "Wrist_R.s" "IndexFinger1_R.is";
connectAttr "IndexFinger1_R.s" "IndexFinger2_R.is";
connectAttr "IndexFinger2_R.s" "IndexFinger3_R.is";
connectAttr "IndexFinger3_R.s" "IndexFinger4_R.is";
connectAttr "Wrist_R.s" "Cup_R.is";
connectAttr "Cup_R.s" "PinkyFinger1_R.is";
connectAttr "PinkyFinger1_R.s" "PinkyFinger2_R.is";
connectAttr "PinkyFinger2_R.s" "PinkyFinger3_R.is";
connectAttr "PinkyFinger3_R.s" "PinkyFinger4_R.is";
connectAttr "Cup_R.s" "RingFinger1_R.is";
connectAttr "RingFinger1_R.s" "RingFinger2_R.is";
connectAttr "RingFinger2_R.s" "RingFinger3_R.is";
connectAttr "RingFinger3_R.s" "RingFinger4_R.is";
connectAttr "Chest_M.s" "Scapula_L.is";
connectAttr "Scapula_L.s" "Shoulder_L.is";
connectAttr "Shoulder_L.s" "Elbow_L.is";
connectAttr "Elbow_L.s" "Wrist_L.is";
connectAttr "Wrist_L.s" "MiddleFinger1_L.is";
connectAttr "MiddleFinger1_L.s" "MiddleFinger2_L.is";
connectAttr "MiddleFinger2_L.s" "MiddleFinger3_L.is";
connectAttr "MiddleFinger3_L.s" "MiddleFinger4_L.is";
connectAttr "Wrist_L.s" "ThumbFinger1_L.is";
connectAttr "ThumbFinger1_L.s" "ThumbFinger2_L.is";
connectAttr "ThumbFinger2_L.s" "ThumbFinger3_L.is";
connectAttr "ThumbFinger3_L.s" "ThumbFinger4_L.is";
connectAttr "Wrist_L.s" "IndexFinger1_L.is";
connectAttr "IndexFinger1_L.s" "IndexFinger2_L.is";
connectAttr "IndexFinger2_L.s" "IndexFinger3_L.is";
connectAttr "IndexFinger3_L.s" "IndexFinger4_L.is";
connectAttr "Wrist_L.s" "Cup_L.is";
connectAttr "Cup_L.s" "PinkyFinger1_L.is";
connectAttr "PinkyFinger1_L.s" "PinkyFinger2_L.is";
connectAttr "PinkyFinger2_L.s" "PinkyFinger3_L.is";
connectAttr "PinkyFinger3_L.s" "PinkyFinger4_L.is";
connectAttr "Cup_L.s" "RingFinger1_L.is";
connectAttr "RingFinger1_L.s" "RingFinger2_L.is";
connectAttr "RingFinger2_L.s" "RingFinger3_L.is";
connectAttr "RingFinger3_L.s" "RingFinger4_L.is";
connectAttr "Root_M.s" "Hip_L.is";
connectAttr "Hip_L.s" "Knee_L.is";
connectAttr "Knee_L.s" "Ankle_L.is";
connectAttr "Ankle_L.s" "Toes_L.is";
connectAttr "Toes_L.s" "ToesEnd_L.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "Root_M.msg" "hyperLayout1.hyp[0].dn";
connectAttr "Hip_R.msg" "hyperLayout1.hyp[1].dn";
connectAttr "Knee_R.msg" "hyperLayout1.hyp[2].dn";
connectAttr "Ankle_R.msg" "hyperLayout1.hyp[3].dn";
connectAttr "Toes_R.msg" "hyperLayout1.hyp[4].dn";
connectAttr "ToesEnd_R.msg" "hyperLayout1.hyp[5].dn";
connectAttr "Spine1_M.msg" "hyperLayout1.hyp[6].dn";
connectAttr "Spine2_M.msg" "hyperLayout1.hyp[7].dn";
connectAttr "Chest_M.msg" "hyperLayout1.hyp[8].dn";
connectAttr "Neck_M.msg" "hyperLayout1.hyp[9].dn";
connectAttr "Head_M.msg" "hyperLayout1.hyp[10].dn";
connectAttr "HeadEnd_M.msg" "hyperLayout1.hyp[11].dn";
connectAttr "Scapula_R.msg" "hyperLayout1.hyp[12].dn";
connectAttr "Shoulder_R.msg" "hyperLayout1.hyp[13].dn";
connectAttr "Elbow_R.msg" "hyperLayout1.hyp[14].dn";
connectAttr "Wrist_R.msg" "hyperLayout1.hyp[15].dn";
connectAttr "MiddleFinger1_R.msg" "hyperLayout1.hyp[16].dn";
connectAttr "MiddleFinger2_R.msg" "hyperLayout1.hyp[17].dn";
connectAttr "MiddleFinger3_R.msg" "hyperLayout1.hyp[18].dn";
connectAttr "MiddleFinger4_R.msg" "hyperLayout1.hyp[19].dn";
connectAttr "ThumbFinger1_R.msg" "hyperLayout1.hyp[20].dn";
connectAttr "ThumbFinger2_R.msg" "hyperLayout1.hyp[21].dn";
connectAttr "ThumbFinger3_R.msg" "hyperLayout1.hyp[22].dn";
connectAttr "ThumbFinger4_R.msg" "hyperLayout1.hyp[23].dn";
connectAttr "IndexFinger1_R.msg" "hyperLayout1.hyp[24].dn";
connectAttr "IndexFinger2_R.msg" "hyperLayout1.hyp[25].dn";
connectAttr "IndexFinger3_R.msg" "hyperLayout1.hyp[26].dn";
connectAttr "IndexFinger4_R.msg" "hyperLayout1.hyp[27].dn";
connectAttr "Cup_R.msg" "hyperLayout1.hyp[28].dn";
connectAttr "PinkyFinger1_R.msg" "hyperLayout1.hyp[29].dn";
connectAttr "PinkyFinger2_R.msg" "hyperLayout1.hyp[30].dn";
connectAttr "PinkyFinger3_R.msg" "hyperLayout1.hyp[31].dn";
connectAttr "PinkyFinger4_R.msg" "hyperLayout1.hyp[32].dn";
connectAttr "RingFinger1_R.msg" "hyperLayout1.hyp[33].dn";
connectAttr "RingFinger2_R.msg" "hyperLayout1.hyp[34].dn";
connectAttr "RingFinger3_R.msg" "hyperLayout1.hyp[35].dn";
connectAttr "RingFinger4_R.msg" "hyperLayout1.hyp[36].dn";
connectAttr "Scapula_L.msg" "hyperLayout1.hyp[37].dn";
connectAttr "Shoulder_L.msg" "hyperLayout1.hyp[38].dn";
connectAttr "Elbow_L.msg" "hyperLayout1.hyp[39].dn";
connectAttr "Wrist_L.msg" "hyperLayout1.hyp[40].dn";
connectAttr "MiddleFinger1_L.msg" "hyperLayout1.hyp[41].dn";
connectAttr "MiddleFinger2_L.msg" "hyperLayout1.hyp[42].dn";
connectAttr "MiddleFinger3_L.msg" "hyperLayout1.hyp[43].dn";
connectAttr "MiddleFinger4_L.msg" "hyperLayout1.hyp[44].dn";
connectAttr "ThumbFinger1_L.msg" "hyperLayout1.hyp[45].dn";
connectAttr "ThumbFinger2_L.msg" "hyperLayout1.hyp[46].dn";
connectAttr "ThumbFinger3_L.msg" "hyperLayout1.hyp[47].dn";
connectAttr "ThumbFinger4_L.msg" "hyperLayout1.hyp[48].dn";
connectAttr "IndexFinger1_L.msg" "hyperLayout1.hyp[49].dn";
connectAttr "IndexFinger2_L.msg" "hyperLayout1.hyp[50].dn";
connectAttr "IndexFinger3_L.msg" "hyperLayout1.hyp[51].dn";
connectAttr "IndexFinger4_L.msg" "hyperLayout1.hyp[52].dn";
connectAttr "Cup_L.msg" "hyperLayout1.hyp[53].dn";
connectAttr "PinkyFinger1_L.msg" "hyperLayout1.hyp[54].dn";
connectAttr "PinkyFinger2_L.msg" "hyperLayout1.hyp[55].dn";
connectAttr "PinkyFinger3_L.msg" "hyperLayout1.hyp[56].dn";
connectAttr "PinkyFinger4_L.msg" "hyperLayout1.hyp[57].dn";
connectAttr "RingFinger1_L.msg" "hyperLayout1.hyp[58].dn";
connectAttr "RingFinger2_L.msg" "hyperLayout1.hyp[59].dn";
connectAttr "RingFinger3_L.msg" "hyperLayout1.hyp[60].dn";
connectAttr "RingFinger4_L.msg" "hyperLayout1.hyp[61].dn";
connectAttr "Hip_L.msg" "hyperLayout1.hyp[62].dn";
connectAttr "Knee_L.msg" "hyperLayout1.hyp[63].dn";
connectAttr "Ankle_L.msg" "hyperLayout1.hyp[64].dn";
connectAttr "Toes_L.msg" "hyperLayout1.hyp[65].dn";
connectAttr "ToesEnd_L.msg" "hyperLayout1.hyp[66].dn";
connectAttr "OFFSET.msg" "hyperLayout1.hyp[67].dn";
connectAttr "LAYER_OFFSET.msg" "hyperLayout1.hyp[68].dn";
connectAttr ":topShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr "shapeEditorManager.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "renderLayerManager.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr ":persp.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr ":perspShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn";
connectAttr "layerManager.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn";
connectAttr ":lightLinker1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn";
connectAttr ":sideShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn";
connectAttr "OFFSET.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn";
connectAttr ":frontShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn";
connectAttr ":front.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn";
connectAttr "poseInterpolatorManager.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr ":top.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn";
connectAttr "defaultLayer.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn";
connectAttr ":side.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of adv_sketch_master_new.ma
