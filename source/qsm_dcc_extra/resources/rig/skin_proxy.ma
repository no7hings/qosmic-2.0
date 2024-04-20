//Maya ASCII 2019 scene
//Name: skin_proxy.ma
//Last modified: Fri, Apr 19, 2024 01:59:50 PM
//Codeset: 936
requires maya "2019";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2019";
fileInfo "version" "2019";
fileInfo "cutIdentifier" "201812112215-434d8d9c04";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 19045)\n";
createNode dagContainer -n "skin_proxy_dgc";
	rename -uid "9A10A9FB-4A7D-3141-3610-A18AB015B58F";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_locator_visibility" -ln "qsm_locator_visibility" 
		-at "long";
	addAttr -ci true -sn "qsm_cache" -ln "qsm_cache" -dt "string";
	addAttr -ci true -k true -sn "qsm_height" -ln "qsm_height" -at "double";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "fileNew.png";
	setAttr ".ctor" -type "string" "nothings";
	setAttr ".cdat" -type "string" "2024/04/19 13:59:21";
	setAttr -k on ".qsm_scale_weight";
	setAttr -k on ".qsm_locator_visibility";
	setAttr -k on ".qsm_height" 17.276973483903447;
createNode transform -n "root_M_grp" -p "skin_proxy_dgc";
	rename -uid "92AA760F-4182-8AAD-04A9-E984360A3EE6";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 1.9709482123356969e-16 8.4764785019111475 0.04798655039699995 ;
	setAttr ".r" -type "double3" 89.999999999999986 -5.7558320031945414 89.999999999999986 ;
	setAttr -k on ".qsm_distance" 0.66065640264072389;
createNode transform -n "root_M_ctl" -p "root_M_grp";
	rename -uid "8A91997B-4FE7-CB93-3F4C-E1870A47FA29";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "root_M_ctl_x_Shape" -p "root_M_ctl";
	rename -uid "50B47187-4551-CDB8-03E2-47893EEBCFBF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "root_M_ctl_y_Shape" -p "root_M_ctl";
	rename -uid "BEF97CF9-4059-7718-865B-C5AD211C0A52";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "root_M_ctl_z_Shape" -p "root_M_ctl";
	rename -uid "6A4D76EE-4F12-E74B-F0EF-E5B71E82A9D6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.33032820132036195 ;
	setAttr ".los" -type "double3" 0 0 0.33032820132036195 ;
createNode transform -n "root_M_geo_copy" -p "root_M_ctl";
	rename -uid "7215D2A8-4C75-9D23-D3EE-F49177302B3B";
createNode mesh -n "root_M_geo_copyShape" -p "root_M_geo_copy";
	rename -uid "AA7EC70E-4308-915B-CA59-778B2CE02A4C";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.375 0.125 0.125 0.125 0.375 0.625 0.625 0.625 0.875
		 0.125 0.625 0.125 0.5 0.125 0.5 0 0.5 1 0.5 0.75 0.5 0.625 0.5 0.5 0.5 0.25 0.25
		 0.25 0.375 0.375 0.25 0.125 0.25 0 0.375 0.875 0.5 0.875 0.625 0.875 0.75 0 0.75
		 0.125 0.625 0.375 0.75 0.25 0.5 0.375;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -2.3007545 -10.133883 1.4507539 
		2.3007545 -10.133883 1.4507539 -2.3007545 -8.3465414 -0.16548479 2.3007545 -8.3465414 
		-0.16548479 -1 -7.4288545 -0.99532127 1 -7.4288545 -0.99532127 -1 -8.5291443 -0.00036245101 
		1 -8.5291443 -0.00036245101 -2.5875418 -9.1504097 0.56142932 -1 -7.9789991 -0.4978421 
		1 -7.9789991 -0.4978421 2.5875418 -9.1504097 0.56142932 -2.3801522e-15 -9.1504097 
		0.56142932 -2.3699988e-15 -10.41616 1.706008 -9.3432785e-16 -8.2833433 -0.22263293 
		-8.7489742e-16 -7.616323 -0.82579917 -1.184747e-15 -6.9004416 -1.4731488 -2.3903054e-15 
		-7.8846631 -0.58314729 -1.6503773 -7.8876977 -0.58040321 -1.7937709 -8.5647049 0.03179412 
		-1.6503773 -9.3315134 0.72519523 -1.6521633e-15 -9.3497505 0.74168676 1.6503773 -9.3315134 
		0.72519523 1.7937709 -8.5647049 0.03179412 1.6503773 -7.8876977 -0.58040321 -1.8439736e-15 
		-7.3265209 -1.0878583;
	setAttr -s 26 ".vt[0:25]"  1.15037727 9.22396946 -0.79119223 -1.15037727 9.22396946 -0.79119223
		 1.15037727 9.061056137 0.82504594 -1.15037727 9.061056137 0.82504594 0.5 7.92885447 0.49532104
		 -0.5 7.92885447 0.49532104 0.5 8.029144287 -0.49963728 -0.5 8.029144287 -0.49963728
		 1.29377091 9.13432693 0.098131418 0.5 7.97899914 -0.0021581054 -0.5 7.97899914 -0.0021581054
		 -1.29377091 9.13432693 0.098131418 2.4598162e-16 9.13432693 0.098131418 3.1134528e-16 9.24969864 -1.046446085
		 -4.4867102e-16 7.80574751 -0.49963728 -5.096547e-16 7.64938021 -0.0021581054 -4.0199879e-16 7.70545816 0.77936518
		 1.8061798e-16 9.018957138 1.2427088 0.82518864 8.49495506 0.66018343 0.89688545 8.55666351 0.047986634
		 0.82518864 8.6265564 -0.64541471 -6.8662873e-17 8.52772236 -0.77304161 -0.82518864 8.6265564 -0.64541471
		 -0.89688545 8.55666351 0.047986634 -0.82518864 8.49495506 0.66018343 -8.6509963e-17 8.36220741 1.07740283;
	setAttr -s 48 ".ed[0:47]"  0 13 1 2 17 1 4 16 1 6 14 1 0 8 1 1 11 1
		 2 18 1 3 24 1 4 9 1 5 10 1 6 20 1 7 22 1 8 2 1 9 6 1 8 19 1 10 7 1 9 15 1 11 3 1
		 10 23 1 11 12 1 12 8 1 13 1 1 12 13 1 14 7 1 13 21 1 15 10 1 14 15 1 16 5 1 15 16 1
		 17 3 1 16 25 1 17 12 1 18 4 1 19 9 1 18 19 1 20 0 1 19 20 1 21 14 1 20 21 1 22 1 1
		 21 22 1 23 11 1 22 23 1 24 5 1 23 24 1 25 17 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 21 5 19 22
		mu 0 4 21 1 19 20
		f 4 29 7 46 45
		mu 0 4 26 3 36 38
		f 4 25 15 -24 26
		mu 0 4 24 17 7 23
		f 4 40 39 -22 24
		mu 0 4 32 33 9 22
		f 4 -40 42 41 -6
		mu 0 4 1 34 35 19
		f 4 35 4 14 36
		mu 0 4 30 0 14 29
		f 4 -15 12 6 34
		mu 0 4 29 14 2 27
		f 4 27 9 -26 28
		mu 0 4 25 5 17 24
		f 4 -42 44 -8 -18
		mu 0 4 19 35 37 3
		f 4 31 -20 17 -30
		mu 0 4 26 20 19 3
		f 4 0 -23 20 -5
		mu 0 4 0 21 20 14
		f 4 38 -25 -1 -36
		mu 0 4 31 32 22 8
		f 4 16 -27 -4 -14
		mu 0 4 16 24 23 6
		f 4 2 -29 -17 -9
		mu 0 4 4 25 24 16
		f 4 1 -46 47 -7
		mu 0 4 2 26 38 28
		f 4 -21 -32 -2 -13
		mu 0 4 14 20 26 2
		f 4 -34 -35 32 8
		mu 0 4 15 29 27 13
		f 4 10 -37 33 13
		mu 0 4 12 30 29 15
		f 4 3 -38 -39 -11
		mu 0 4 6 23 32 31
		f 4 23 11 -41 37
		mu 0 4 23 7 33 32
		f 4 -43 -12 -16 18
		mu 0 4 35 34 10 18
		f 4 -45 -19 -10 -44
		mu 0 4 37 35 18 11
		f 4 -47 43 -28 30
		mu 0 4 38 36 5 25
		f 4 -48 -31 -3 -33
		mu 0 4 28 38 25 4;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "spine_a_M_grp" -p "skin_proxy_dgc";
	rename -uid "4FE25F8E-4713-3DE8-637F-A5BBFAC907D8";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -8.1997581557992738e-17 9.1338040832010616 0.11424334274358698 ;
	setAttr ".r" -type "double3" 89.999999999999986 -5.7558320031945405 89.999999999999986 ;
	setAttr -k on ".qsm_distance" 1.3213128052814263;
createNode transform -n "spine_a_M_ctl" -p "spine_a_M_grp";
	rename -uid "BD5E39EE-4660-D5EE-D6B5-FBAC36FD524D";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "spine_a_M_ctl_x_Shape" -p "spine_a_M_ctl";
	rename -uid "C610E0B8-43F2-0086-CF76-84A291C791A5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "spine_a_M_ctl_y_Shape" -p "spine_a_M_ctl";
	rename -uid "2C9958D5-4B37-258E-A4B2-CDB5C50E87B0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "spine_a_M_ctl_z_Shape" -p "spine_a_M_ctl";
	rename -uid "0CEF2F71-4F0A-FB0D-145D-A5A1FC75363B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.66065640264071313 ;
	setAttr ".los" -type "double3" 0 0 0.66065640264071313 ;
createNode transform -n "spine_a_M_geo_copy" -p "spine_a_M_ctl";
	rename -uid "E11A4786-4B99-42B4-D38E-B891BD1E8DAA";
createNode mesh -n "spine_a_M_geo_copyShape" -p "spine_a_M_geo_copy";
	rename -uid "1C448C1B-4ED0-66AB-03D5-A5A834858764";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.375 0.125 0.125 0.125 0.375 0.625 0.625 0.625 0.875
		 0.125 0.625 0.125 0.5 0.25 0.5 0.5 0.5 0.625 0.5 0.75 0.5 0 0.5 1 0.5 0.125 0.25
		 0.25 0.375 0.375 0.25 0.125 0.25 0 0.375 0.875 0.5 0.875 0.625 0.875 0.75 0 0.75
		 0.125 0.625 0.375 0.75 0.25 0.5 0.375;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -1.7687728 -11.183534 1.7392652 
		1.7687728 -11.183534 1.7392652 -1.7687728 -9.5016899 0.21842501 1.7687728 -9.5016899 
		0.21842501 -1.7612665 -8.3710918 -0.80394125 1.7612665 -8.3710918 -0.80394125 -1.7612665 
		-10.308993 0.9484449 1.7612665 -10.308993 0.9484449 -2.4342716 -10.342612 0.97884506 
		-2.4159105 -9.3400421 0.072251797 2.4159105 -9.3400421 0.072251797 2.4342716 -10.342612 
		0.97884506 -3.6483547e-15 -9.1498451 -0.099737719 -2.3783777e-15 -8.0109415 -1.1296136 
		-2.3051051e-15 -9.3400421 0.072251797 -2.3570547e-15 -10.669143 1.2741171 -3.2321526e-15 
		-11.535378 2.0574279 -3.4402537e-15 -10.342612 0.97884506 -1.5486177 -8.9363899 -0.29275864 
		-2.1277604 -9.8413267 0.52554798 -1.5486177 -10.746264 1.3438555 -2.7123717e-15 -11.102261 
		1.6657724 1.5486177 -10.746264 1.3438555 2.1277604 -9.8413267 0.52554798 1.5486177 
		-8.9363899 -0.29275864 -3.1550709e-15 -8.5803938 -0.61467558;
	setAttr -s 26 ".vt[0:25]"  0.88438642 10.24294567 -0.71931225 -0.88438642 10.24294567 -0.71931225
		 0.88438642 10.31260586 1.048088312 -0.88438642 10.31260586 1.048088312 0.88063323 9.18758202 0.94029194
		 -0.88063323 9.18758202 0.94029194 0.88063323 9.36421776 -0.81209475 -0.88063323 9.36421776 -0.81209475
		 1.21713579 10.27777576 0.16438803 1.20795524 9.27589989 0.064098626 -1.20795524 9.27589989 0.064098626
		 -1.21713579 10.27777576 0.16438803 5.9411336e-16 10.32717896 1.41783202 -3.8822541e-17 9.15475464 1.26596379
		 -1.4928691e-18 9.27589989 0.064098626 9.8447834e-17 9.39704514 -1.13776648 5.3813433e-16 10.22837257 -1.089055896
		 5.6612389e-16 10.27777576 0.16438803 0.77430886 9.75009346 0.99419016 1.063880205 9.77683735 0.11424333
		 0.77430886 9.80358219 -0.7657035 2.7717507e-16 9.81270885 -1.11341119 -0.77430886 9.80358219 -0.7657035
		 -1.063880205 9.77683735 0.11424333 -0.77430886 9.75009346 0.99419016 3.4849781e-16 9.7409668 1.34189785;
	setAttr -s 48 ".ed[0:47]"  0 16 1 2 12 1 4 13 1 6 15 1 0 8 1 1 11 1
		 2 18 1 3 24 1 4 9 1 5 10 1 6 20 1 7 22 1 8 2 1 9 6 1 8 19 1 10 7 1 9 14 1 11 3 1
		 10 23 1 11 17 1 12 3 1 13 5 1 12 25 1 14 10 1 13 14 1 15 7 1 14 15 1 16 1 1 15 21 1
		 17 8 1 16 17 1 17 12 1 18 4 1 19 9 1 18 19 1 20 0 1 19 20 1 21 16 1 20 21 1 22 1 1
		 21 22 1 23 11 1 22 23 1 24 5 1 23 24 1 25 13 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 0 30 29 -5
		mu 0 4 0 24 26 14
		f 4 1 22 47 -7
		mu 0 4 2 20 38 28
		f 4 16 26 -4 -14
		mu 0 4 16 22 23 6
		f 4 38 37 -1 -36
		mu 0 4 31 32 25 8
		f 4 -40 42 41 -6
		mu 0 4 1 34 35 19
		f 4 35 4 14 36
		mu 0 4 30 0 14 29
		f 4 -15 12 6 34
		mu 0 4 29 14 2 27
		f 4 2 24 -17 -9
		mu 0 4 4 21 22 16
		f 4 -42 44 -8 -18
		mu 0 4 19 35 37 3
		f 4 -30 31 -2 -13
		mu 0 4 14 26 20 2
		f 4 20 7 46 -23
		mu 0 4 20 3 36 38
		f 4 -25 21 9 -24
		mu 0 4 22 21 5 17
		f 4 -27 23 15 -26
		mu 0 4 23 22 17 7
		f 4 -38 40 39 -28
		mu 0 4 25 32 33 9
		f 4 -31 27 5 19
		mu 0 4 26 24 1 19
		f 4 -32 -20 17 -21
		mu 0 4 20 26 19 3
		f 4 -34 -35 32 8
		mu 0 4 15 29 27 13
		f 4 10 -37 33 13
		mu 0 4 12 30 29 15
		f 4 3 28 -39 -11
		mu 0 4 6 23 32 31
		f 4 -41 -29 25 11
		mu 0 4 33 32 23 7
		f 4 -43 -12 -16 18
		mu 0 4 35 34 10 18
		f 4 -45 -19 -10 -44
		mu 0 4 37 35 18 11
		f 4 -47 43 -22 -46
		mu 0 4 38 36 5 21
		f 4 -48 45 -3 -33
		mu 0 4 28 38 21 4;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "spine_b_M_grp" -p "skin_proxy_dgc";
	rename -uid "2EAE2D12-443E-9D84-8FD0-4A909BCB9C7D";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -1.9318431423020035e-15 10.448455245780869 0.24675692743675889 ;
	setAttr ".r" -type "double3" 89.999999999999986 9.960272767559319 89.999999999999972 ;
	setAttr -k on ".qsm_distance" 1.384807147363738;
createNode transform -n "spine_b_M_ctl" -p "spine_b_M_grp";
	rename -uid "880EFBA0-4882-E468-C3F9-84A3D77CA56F";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "spine_b_M_ctl_x_Shape" -p "spine_b_M_ctl";
	rename -uid "29CC50A0-4AD4-E577-6C1D-E1882ABF48CD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "spine_b_M_ctl_y_Shape" -p "spine_b_M_ctl";
	rename -uid "A7D9A33A-4BE3-E45C-E800-22ACBF7E5DC8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "spine_b_M_ctl_z_Shape" -p "spine_b_M_ctl";
	rename -uid "A78DFDD1-4153-BB3F-7CC5-C2AD85C9A183";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.692403573681869 ;
	setAttr ".los" -type "double3" 0 0 0.692403573681869 ;
createNode transform -n "spine_b_M_geo_copy" -p "spine_b_M_ctl";
	rename -uid "2D899CA1-4F0C-1C47-2090-70A771BCDA5F";
createNode mesh -n "spine_b_M_geo_copyShape" -p "spine_b_M_geo_copy";
	rename -uid "DC0138EA-4B67-7AE1-DBCA-198DB33BA8C7";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.25 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.5 0.25 0.5 0.5 0.5 0.75 0.5 0 0.5 1 0.375 0.125 0.5
		 0.125 0.625 0.125 0.625 0.625 0.875 0.125 0.5 0.625 0.125 0.125 0.375 0.625 0.25
		 0.125 0.25 0.25 0.375 0.375 0.5 0.375 0.625 0.375 0.75 0.25 0.75 0.125 0.625 0.875
		 0.75 0 0.5 0.875 0.25 0 0.375 0.875;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -2.917011 -12.694385 2.4279542 
		2.917011 -12.694385 2.4279542 -2.5880296 -10.945246 0.34487814 2.5880296 -10.945246 
		0.34487814 -1.782087 -9.6991873 -1.1390709 1.782087 -9.6991873 -1.1390709 -2.0378389 
		-11.132536 0.56792468 2.0378389 -11.132536 0.56792468 -2.3527524e-15 -10.671297 0.018628919 
		-8.0068324e-17 -9.3836288 -1.5148746 3.4123712e-16 -11.132536 0.56792468 -1.3396318e-15 
		-12.694385 2.4279542 -3.2994771 -11.628396 1.1584523 -1.8075632e-15 -11.628396 1.1584523 
		3.2994771 -11.628396 1.1584523 2.3351707 -10.385042 -0.32227623 1.6116786e-16 -10.385042 
		-0.32227623 -2.3351707 -10.385042 -0.32227623 -2.9130919 -11.011312 0.42355785 -2.2593341 
		-10.201186 -0.54123336 -1.2050446e-15 -9.8539581 -0.95475286 2.2593341 -10.201186 
		-0.54123336 2.9130919 -11.011312 0.42355785 2.5616391 -11.948875 1.5401156 -4.4600578e-16 
		-11.948875 1.5401156 -2.5616391 -11.948875 1.5401156;
	setAttr -s 26 ".vt[0:25]"  1.45850551 11.49924469 -1.15120363 -1.45850551 11.49924469 -1.15120363
		 1.29401481 12.019147873 1.061260104 -1.29401481 12.019147873 1.061260104 0.89104348 10.50757217 1.057130337
		 -0.89104348 10.50757217 1.057130337 1.018919468 10.37237167 -0.51167852 -1.018919468 10.37237167 -0.51167852
		 -1.4821698e-15 12.10881805 1.41469586 -2.6011334e-15 10.5373373 1.4025116 -2.6945952e-15 10.37237167 -0.51167852
		 -1.8275261e-15 11.49924469 -1.15120363 1.64973855 11.76795483 0.15673107 -1.6752872e-15 11.76795483 0.15673107
		 -1.64973855 11.76795483 0.15673107 -1.16758537 10.44287968 0.30645841 -2.6546487e-15 10.44287968 0.30645841
		 1.16758537 10.44287968 0.30645841 1.45654595 11.10460091 0.226246 1.12966704 11.26791191 1.18589997
		 -2.0583616e-15 11.32965946 1.59029078 -1.12966704 11.26791191 1.18589997 -1.45654595 11.10460091 0.226246
		 -1.28081954 10.92922592 -0.87292504 -2.2850848e-15 10.92922592 -0.87292504 1.28081954 10.92922592 -0.87292504;
	setAttr -s 48 ".ed[0:47]"  0 11 1 2 8 1 4 9 1 6 10 1 0 12 1 1 14 1 2 19 1
		 3 21 1 4 17 1 5 15 1 7 23 1 8 3 1 9 5 1 10 7 1 9 16 1 11 1 1 10 24 1 11 13 1 6 25 1
		 8 20 1 12 2 1 13 8 1 12 13 1 14 3 1 13 14 1 15 7 1 14 22 1 16 10 1 15 16 1 17 6 1
		 16 17 1 17 18 1 18 12 1 19 4 1 18 19 1 20 9 1 19 20 1 21 5 1 20 21 1 22 15 1 21 22 1
		 23 1 1 22 23 1 24 11 1 23 24 1 25 0 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 22 21 -2 -21
		mu 0 4 19 20 14 2
		f 4 -34 36 35 -3
		mu 0 4 4 29 30 15
		f 4 2 14 30 -9
		mu 0 4 4 15 24 26
		f 4 46 -19 3 16
		mu 0 4 36 38 6 16
		f 4 -38 40 39 -10
		mu 0 4 11 32 33 23
		f 4 34 33 8 31
		mu 0 4 27 28 13 25
		f 4 38 37 -13 -36
		mu 0 4 30 31 5 15
		f 4 -15 12 9 28
		mu 0 4 24 15 5 22
		f 4 44 -17 13 10
		mu 0 4 34 36 16 7
		f 4 -22 24 23 -12
		mu 0 4 14 20 21 3
		f 4 18 47 -32 29
		mu 0 4 12 37 27 25
		f 4 0 17 -23 -5
		mu 0 4 0 17 20 19
		f 4 -25 -18 15 5
		mu 0 4 21 20 17 1
		f 4 42 -11 -26 -40
		mu 0 4 33 35 10 23
		f 4 -28 -29 25 -14
		mu 0 4 16 24 22 7
		f 4 -31 27 -4 -30
		mu 0 4 26 24 16 6
		f 4 20 6 -35 32
		mu 0 4 19 2 28 27
		f 4 -37 -7 1 19
		mu 0 4 30 29 2 14
		f 4 11 7 -39 -20
		mu 0 4 14 3 31 30
		f 4 -41 -8 -24 26
		mu 0 4 33 32 3 21
		f 4 -6 -42 -43 -27
		mu 0 4 21 1 35 33
		f 4 -16 -44 -45 41
		mu 0 4 9 18 36 34
		f 4 -1 -46 -47 43
		mu 0 4 18 8 38 36
		f 4 -48 45 4 -33
		mu 0 4 27 37 0 19;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "chest_M_grp" -p "skin_proxy_dgc";
	rename -uid "64D4214F-4871-CA64-6D22-0BB6574A33E3";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 6.7827560489097947e-16 11.812390467490841 0.0072333453646353657 ;
	setAttr ".r" -type "double3" 89.999999999999986 12.704707235980711 89.999999999999972 ;
	setAttr -k on ".qsm_distance" 2.3706035457537875;
createNode transform -n "chest_M_ctl" -p "chest_M_grp";
	rename -uid "84425A41-4FEC-7FD2-24AF-B49546849347";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "chest_M_ctl_x_Shape" -p "chest_M_ctl";
	rename -uid "108F0FA1-4453-43CB-4EA0-048174869B6D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "chest_M_ctl_y_Shape" -p "chest_M_ctl";
	rename -uid "13C2326A-4009-A6AC-89CB-4ABAC28AD911";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "chest_M_ctl_z_Shape" -p "chest_M_ctl";
	rename -uid "1E0485C2-4A74-BD94-9AC2-5E90B2BA1CA3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 1.1853017728768938 ;
	setAttr ".los" -type "double3" 0 0 1.1853017728768938 ;
createNode transform -n "chest_M_geo_copy" -p "chest_M_ctl";
	rename -uid "717D417A-4FFF-708E-09DD-4F9E823FC348";
createNode mesh -n "chest_M_geo_copyShape" -p "chest_M_geo_copy";
	rename -uid "34FDE3D3-445E-1AA3-FE13-E6BA4B618325";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.375 0.125 0.125 0.125 0.375 0.625 0.625 0.625 0.875
		 0.125 0.625 0.125 0.5 0.25 0.5 0.5 0.5 0.625 0.5 0.75 0.5 0 0.5 1 0.5 0.125 0.25
		 0.25 0.375 0.375 0.25 0.125 0.25 0 0.375 0.875 0.5 0.875 0.625 0.875 0.75 0 0.75
		 0.125 0.625 0.375 0.75 0.25 0.5 0.375;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -3.790266 -14.598848 3.4773545 
		3.9347203 -14.598848 3.4773545 -3.7902648 -12.558722 0.92608601 3.7877192 -12.558722 
		0.92608601 -2.5546103 -10.87985 -1.1734154 2.5546103 -10.87985 -1.1734154 -2.5546103 
		-12.71132 1.1169181 2.5546103 -12.71132 1.1169181 -3.7902672 -13.569556 2.1901796 
		-3.0248666 -11.756564 -0.077046067 3.0248666 -11.756564 -0.077046067 4.0285668 -13.569556 
		2.1901796 -1.9579449e-14 -12.307891 0.61241144 -1.7225272e-14 -10.666421 -1.4403193 
		-1.6705873e-14 -11.756564 -0.077046067 -1.6186474e-14 -12.846709 1.2862283 -1.9215554e-14 
		-14.728143 3.6390436 -1.9317848e-14 -13.569556 2.1901796 -3.1724377 -11.719286 -0.12366419 
		-3.407567 -12.66306 1.0565672 -3.1724381 -13.655085 2.2971368 -1.7701015e-14 -13.787427 
		2.4626365 3.2446651 -13.655085 2.2971368 3.5267167 -12.66306 1.0565672 3.1711648 
		-11.719286 -0.12366419 -1.840236e-14 -11.487156 -0.4139539;
	setAttr -s 26 ".vt[0:25]"  1.89513302 13.47838497 -1.51694298 -1.96736014 13.47838497 -1.51694298
		 1.89513242 13.42497635 0.53167874 -1.89385962 13.42497635 0.53167874 1.27730513 12.066130638 1.16608179
		 -1.27730513 12.066130638 1.16608179 1.27730513 11.54978371 -1.12425184 -1.27730513 11.54978371 -1.12425184
		 1.89513361 13.41040039 -0.51618183 1.51243329 11.81895924 0.069713071 -1.51243329 11.81895924 0.069713071
		 -2.014283419 13.41040039 -0.51618183 6.9156441e-15 13.49569321 0.84535342 5.7218952e-15 12.12630463 1.43298697
		 5.5477676e-15 11.81895924 0.069713071 5.3736401e-15 11.5116148 -1.29356098 6.8851861e-15 13.44193268 -1.67863202
		 6.8673213e-15 13.41040039 -0.51618183 1.58621883 12.74555397 0.84888023 1.70378351 12.61468029 -0.22323436
		 1.58621907 12.51408482 -1.32059741 6.1294133e-15 12.47677422 -1.48609662 -1.62233257 12.51408482 -1.32059741
		 -1.76335835 12.61468029 -0.22323436 -1.58558238 12.74555397 0.84888023 6.3187696e-15 12.81099892 1.13917017;
	setAttr -s 48 ".ed[0:47]"  0 16 1 2 12 1 4 13 1 6 15 1 0 8 1 1 11 1
		 2 18 1 3 24 1 4 9 1 5 10 1 6 20 1 7 22 1 8 2 1 9 6 1 8 19 1 10 7 1 9 14 1 11 3 1
		 10 23 1 11 17 1 12 3 1 13 5 1 12 25 1 14 10 1 13 14 1 15 7 1 14 15 1 16 1 1 15 21 1
		 17 8 1 16 17 1 17 12 1 18 4 1 19 9 1 18 19 1 20 0 1 19 20 1 21 16 1 20 21 1 22 1 1
		 21 22 1 23 11 1 22 23 1 24 5 1 23 24 1 25 13 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 0 30 29 -5
		mu 0 4 0 24 26 14
		f 4 47 -7 1 22
		mu 0 4 38 28 2 20
		f 4 16 26 -4 -14
		mu 0 4 16 22 23 6
		f 4 37 -1 -36 38
		mu 0 4 32 25 8 31
		f 4 41 -6 -40 42
		mu 0 4 35 19 1 34
		f 4 35 4 14 36
		mu 0 4 30 0 14 29
		f 4 12 6 34 -15
		mu 0 4 14 2 27 29
		f 4 2 24 -17 -9
		mu 0 4 4 21 22 16
		f 4 -8 -18 -42 44
		mu 0 4 37 3 19 35
		f 4 -30 31 -2 -13
		mu 0 4 14 26 20 2
		f 4 20 7 46 -23
		mu 0 4 20 3 36 38
		f 4 -25 21 9 -24
		mu 0 4 22 21 5 17
		f 4 -27 23 15 -26
		mu 0 4 23 22 17 7
		f 4 39 -28 -38 40
		mu 0 4 33 9 25 32
		f 4 -31 27 5 19
		mu 0 4 26 24 1 19
		f 4 -32 -20 17 -21
		mu 0 4 20 26 19 3
		f 4 -35 32 8 -34
		mu 0 4 29 27 13 15
		f 4 10 -37 33 13
		mu 0 4 12 30 29 15
		f 4 28 -39 -11 3
		mu 0 4 23 32 31 6
		f 4 11 -41 -29 25
		mu 0 4 7 33 32 23
		f 4 18 -43 -12 -16
		mu 0 4 18 35 34 10
		f 4 -44 -45 -19 -10
		mu 0 4 11 37 35 18
		f 4 -47 43 -22 -46
		mu 0 4 38 36 5 21
		f 4 -33 -48 45 -3
		mu 0 4 4 28 38 21;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "neck_M_grp" -p "skin_proxy_dgc";
	rename -uid "95A3161F-44AA-97AB-1E97-39A7ADFAF75E";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 4.4227832541972014e-15 14.124953291076064 -0.51412484063801167 ;
	setAttr ".r" -type "double3" 89.999999999999972 -10.933677604010247 89.999999999999972 ;
	setAttr -k on ".qsm_distance" 1.6808343962180303;
createNode transform -n "neck_M_ctl" -p "neck_M_grp";
	rename -uid "97A41C3F-43F7-53B3-D324-33BEF853C852";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "neck_M_ctl_x_Shape" -p "neck_M_ctl";
	rename -uid "364A4597-49F4-0BD4-F75C-AABDE16B7146";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "neck_M_ctl_y_Shape" -p "neck_M_ctl";
	rename -uid "1111219A-460F-1D40-C8F9-5CBA9BC8F420";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "neck_M_ctl_z_Shape" -p "neck_M_ctl";
	rename -uid "780EAF1A-4BEF-C03D-DA63-CF9A2C105578";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.84041719810901516 ;
	setAttr ".los" -type "double3" 0 0 0.84041719810901516 ;
createNode transform -n "neck_M_geo_copy" -p "neck_M_ctl";
	rename -uid "5B0CE46B-415A-D1D4-BBA7-9E819578825D";
createNode mesh -n "neck_M_geo_copyShape" -p "neck_M_geo_copy";
	rename -uid "0C9C9C91-42B7-8B44-5B3E-D1B0BBF24E60";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.75 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.5 0 0.5 1 0.5 0.25 0.5 0.5 0.5 0.75 0.375 0.125 0.125
		 0.125 0.375 0.625 0.5 0.625 0.625 0.625 0.875 0.125 0.625 0.125 0.5 0.125 0.625 0.875
		 0.75 0 0.5 0.875 0.25 0 0.375 0.875 0.25 0.125 0.25 0.25 0.375 0.375 0.5 0.375 0.625
		 0.375 0.75 0.25 0.75 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -1 -15.911102 1.9882495 1 
		-15.911102 1.9882495 -1 -14.344783 0.69555211 1 -14.344783 0.69555211 -1 -13.674558 
		0.14240927 1 -13.674558 0.14240927 -1 -14.864231 1.1242576 1 -14.864231 1.1242576 
		-1.1792933e-14 -16.014311 2.0734286 -1.1697256e-14 -13.854397 0.29083249 -1.0336208e-14 
		-12.72527 -0.64104629 -9.1249623e-15 -14.614329 0.91801107 -1 -15.179546 1.3844898 
		-1 -14.269394 0.63333291 -9.9178749e-15 -13.609517 0.088730715 1 -14.269394 0.63333291 
		1 -15.179546 1.3844898 -1.1696887e-14 -15.179546 1.3844898 1 -15.2037 1.4044245 -1.0828504e-14 
		-15.417998 1.5812861 -1 -15.2037 1.4044245 -1 -14.72447 1.0089114 -1 -14.00967 0.41898072 
		-1.1009334e-14 -13.524273 0.018377969 1 -14.00967 0.41898072 1 -14.72447 1.0089114;
	setAttr -s 26 ".vt[0:25]"  0.5 15.51431084 -0.64985716 -0.5 15.51431084 -0.64985716
		 0.5 14.84478283 0.13417542 -0.5 14.84478283 0.13417542 0.5 14.17455769 0.0047018826
		 -0.5 14.17455769 0.0047018826 0.5 14.36423111 -0.97714555 -0.5 14.36423111 -0.97714555
		 5.209929e-15 15.51431084 -0.75497389 4.7898701e-15 14.66837692 0.41988209 4.1032144e-15 13.56089592 0.22798616
		 3.9920798e-15 13.70435333 -1.52217567 0.5 15.17954636 -0.31039917 0.5 14.26939392 -0.48622179
		 4.1307611e-15 13.6095171 -0.6136964 -0.5 14.26939392 -0.48622179 -0.5 15.17954636 -0.31039917
		 5.0202673e-15 15.17954636 -0.31039917 -0.5 14.85589409 -0.7271589 4.7292704e-15 14.9125042 -0.87682563
		 0.5 14.85589409 -0.7271589 0.5 14.72447014 -0.39831048 0.5 14.50967026 0.069438636
		 4.4528052e-15 14.31390858 0.32661203 -0.5 14.50967026 0.069438636 -0.5 14.72447014 -0.39831048;
	setAttr -s 48 ".ed[0:47]"  0 8 1 2 9 1 4 10 1 6 11 1 0 12 1 1 16 1 2 22 1
		 3 24 1 4 13 1 5 15 1 6 20 1 7 18 1 8 1 1 9 3 1 8 17 1 10 5 1 9 23 1 11 7 1 10 14 1
		 11 19 1 12 2 1 13 6 1 12 21 1 14 11 1 13 14 1 15 7 1 14 15 1 16 3 1 15 25 1 17 9 1
		 16 17 1 17 12 1 18 1 1 19 8 1 18 19 1 20 0 1 19 20 1 21 13 1 20 21 1 22 4 1 21 22 1
		 23 10 1 22 23 1 24 5 1 23 24 1 25 16 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 0 14 31 -5
		mu 0 4 0 14 26 19
		f 4 42 41 -3 -40
		mu 0 4 34 35 17 4
		f 4 24 23 -4 -22
		mu 0 4 21 22 18 6
		f 4 3 19 36 -11
		mu 0 4 6 18 29 31
		f 4 47 -12 -26 28
		mu 0 4 38 28 10 24
		f 4 10 38 37 21
		mu 0 4 12 30 32 20
		f 4 12 5 30 -15
		mu 0 4 14 1 25 26
		f 4 -42 44 43 -16
		mu 0 4 17 35 36 5
		f 4 -24 26 25 -18
		mu 0 4 18 22 23 7
		f 4 -20 17 11 34
		mu 0 4 29 18 7 27
		f 4 -38 40 39 8
		mu 0 4 20 32 33 13
		f 4 2 18 -25 -9
		mu 0 4 4 17 22 21
		f 4 -27 -19 15 9
		mu 0 4 23 22 17 5
		f 4 -29 -10 -44 46
		mu 0 4 38 24 11 37
		f 4 -31 27 -14 -30
		mu 0 4 26 25 3 16
		f 4 -32 29 -2 -21
		mu 0 4 19 26 16 2
		f 4 -34 -35 32 -13
		mu 0 4 15 29 27 9
		f 4 -37 33 -1 -36
		mu 0 4 31 29 15 8
		f 4 -39 35 4 22
		mu 0 4 32 30 0 19
		f 4 -41 -23 20 6
		mu 0 4 33 32 19 2
		f 4 1 16 -43 -7
		mu 0 4 2 16 35 34
		f 4 -45 -17 13 7
		mu 0 4 36 35 16 3
		f 4 -46 -47 -8 -28
		mu 0 4 25 38 37 3
		f 4 -33 -48 45 -6
		mu 0 4 1 28 38 25;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "head_M_grp" -p "skin_proxy_dgc";
	rename -uid "007B307C-4E9C-6272-8EE6-3197601960F5";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 8.867870785812063e-15 15.775276165428851 -0.19531662572254516 ;
	setAttr ".r" -type "double3" 89.999999999999972 4.2688694398687465e-07 89.999999999999972 ;
	setAttr -k on ".qsm_distance" 1.5016973184745961;
createNode transform -n "head_M_ctl" -p "head_M_grp";
	rename -uid "4480D551-41B4-17BE-D685-838963514452";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "head_M_ctl_x_Shape" -p "head_M_ctl";
	rename -uid "AEAA6594-4777-ED72-C2C2-0DB975382D36";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "head_M_ctl_y_Shape" -p "head_M_ctl";
	rename -uid "8FBDB544-4AA2-2183-3A82-9C816D56C0D7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "head_M_ctl_z_Shape" -p "head_M_ctl";
	rename -uid "821AD9D1-4D9F-4665-E717-11A764AA5701";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.75084865923729804 ;
	setAttr ".los" -type "double3" 0 0 0.75084865923729804 ;
createNode transform -n "head_M_geo_copy" -p "head_M_ctl";
	rename -uid "D7D457F2-4AC7-B62F-FBED-F9B037803F78";
createNode mesh -n "head_M_geo_copyShape" -p "head_M_geo_copy";
	rename -uid "2F670357-418E-C62C-CC29-9188FA365C40";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.4375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.25 0 0.375 0.875 0.25 0.25 0.375 0.375 0.625 0.375
		 0.75 0.25 0.625 0.875 0.75 0 0.625 0.125 0.375 0.125 0.25 0.125 0.125 0.125 0.375
		 0.625 0.625 0.625 0.875 0.125 0.75 0.125 0.5 0.25 0.5 0.375 0.5 0.5 0.5 0.625 0.5
		 0.75 0.5 0.875 0.5 0 0.5 1 0.5 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -1 -17.318674 1.7387151 1 
		-17.318674 1.7387151 -1 -16.203457 0.62349737 1 -16.203457 0.62349737 -1 -13.523763 
		-2.0561965 1 -13.523763 -2.0561965 -1 -15.829657 0.24969704 1 -15.829657 0.24969704 
		-1.1841385 -16.615807 1.0358474 -1.1960133 -14.779387 -0.8005724 1.1960133 -14.779387 
		-0.8005724 1.1841385 -16.615807 1.0358474 1 -17.018461 1.438501 -1 -17.018461 1.438501 
		-1.7672861 -15.718042 0.13808307 -1.3025823 -14.65754 -0.92241889 1.3025823 -14.65754 
		-0.92241889 1.7672861 -15.718042 0.13808307 -1.7823435e-14 -16.26741 0.68745124 -1.6659298e-14 
		-14.675255 -0.90470469 -1.5018612e-14 -13.294564 -2.2853956 -1.5016956e-14 -14.554759 
		-1.0252 -1.4959527e-14 -15.853294 0.27333507 -1.5430201e-14 -16.703571 1.1236118 
		-1.666291e-14 -17.50984 1.9298797 -1.7533811e-14 -17.170317 1.5903579;
	setAttr -s 26 ".vt[0:25]"  0.5 16.69612694 -0.8178643 -0.5 16.69612694 -0.8178643
		 0.5 16.97520256 0.57642901 -0.5 16.97520256 0.57642901 0.5 14.6092453 0.89016557
		 -0.5 14.6092453 0.89016557 0.5 15.3296566 -0.69531661 -0.5 15.3296566 -0.69531661
		 0.59206927 15.966856 -0.84426761 0.59800667 16.022031784 1.047327995 -0.59800667 16.022031784 1.047327995
		 -0.59206927 15.966856 -0.84426761 -0.5 17.09305954 -0.12071764 0.5 17.09305954 -0.12071764
		 0.88364303 15.95869446 0.045335218 0.65129113 14.96945095 0.11659366 -0.65129113 14.96945095 0.11659366
		 -0.88364303 15.95869446 0.045335218 9.6199531e-15 17.096437454 0.63371003 8.8935368e-15 16.013847351 1.14327586
		 8.1179113e-15 14.47529984 0.98541939 8.3610241e-15 14.87435532 0.1242792 8.5871108e-15 15.27341175 -0.77519947
		 8.8691931e-15 15.95867252 -0.94021547 9.4772619e-15 16.79419136 -0.91096449 9.693927e-15 17.22700691 -0.13862717;
	setAttr -s 48 ".ed[0:47]"  0 24 1 2 18 1 4 20 1 6 22 1 0 13 1 1 12 1
		 2 9 1 3 10 1 4 15 1 5 16 1 6 8 1 7 11 1 8 0 1 9 4 1 8 14 1 10 5 1 9 19 1 11 1 1 10 17 1
		 11 23 1 12 3 1 13 2 1 12 25 1 14 9 1 13 14 1 15 6 1 14 15 1 16 7 1 15 21 1 17 11 1
		 16 17 1 17 12 1 18 3 1 19 10 1 18 19 1 20 5 1 19 20 1 21 16 1 20 21 1 22 7 1 21 22 1
		 23 8 1 22 23 1 24 1 1 23 24 1 25 13 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 0 46 45 -5
		mu 0 4 0 36 38 23
		f 4 16 36 -3 -14
		mu 0 4 17 31 32 4
		f 4 28 40 -4 -26
		mu 0 4 26 33 34 6
		f 4 3 42 41 -11
		mu 0 4 6 34 35 15
		f 4 -12 -28 30 29
		mu 0 4 21 10 28 29
		f 4 10 14 26 25
		mu 0 4 12 14 24 25
		f 4 12 4 24 -15
		mu 0 4 14 0 23 24
		f 4 1 34 -17 -7
		mu 0 4 2 30 31 17
		f 4 -18 -30 31 -6
		mu 0 4 1 21 29 22
		f 4 -42 44 -1 -13
		mu 0 4 15 35 37 8
		f 4 -46 47 -2 -22
		mu 0 4 23 38 30 2
		f 4 -25 21 6 -24
		mu 0 4 24 23 2 16
		f 4 -27 23 13 8
		mu 0 4 25 24 16 13
		f 4 2 38 -29 -9
		mu 0 4 4 32 33 26
		f 4 -31 -10 -16 18
		mu 0 4 29 28 11 19
		f 4 -32 -19 -8 -21
		mu 0 4 22 29 19 3
		f 4 32 7 -34 -35
		mu 0 4 30 3 18 31
		f 4 -37 33 15 -36
		mu 0 4 32 31 18 5
		f 4 -39 35 9 -38
		mu 0 4 33 32 5 27
		f 4 -41 37 27 -40
		mu 0 4 34 33 27 7
		f 4 -43 39 11 19
		mu 0 4 35 34 7 20
		f 4 -45 -20 17 -44
		mu 0 4 37 35 20 9
		f 4 -47 43 5 22
		mu 0 4 38 36 1 22
		f 4 -48 -23 20 -33
		mu 0 4 30 38 22 3;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "head_end_M_grp" -p "skin_proxy_dgc";
	rename -uid "C6F79FB5-4D6A-78B8-7110-128651BE8F82";
	setAttr ".t" -type "double3" 1.4527148839507679e-14 17.276973483903447 -0.19531663691106471 ;
	setAttr ".r" -type "double3" 89.999999999999972 -6.3611093629270304e-15 89.999999999999972 ;
createNode transform -n "head_end_M_ctl" -p "head_end_M_grp";
	rename -uid "4922F75E-46FF-571E-BA5A-DFAD045D2D57";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "head_end_M_ctl_x_Shape" -p "head_end_M_ctl";
	rename -uid "9746BCB0-4620-6E09-14F6-86A04567BD6F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "head_end_M_ctl_y_Shape" -p "head_end_M_ctl";
	rename -uid "301DD609-47F9-DB79-E146-5B9805BD7F9C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "head_end_M_ctl_z_Shape" -p "head_end_M_ctl";
	rename -uid "984A8E8A-4C2C-31D6-4FCE-B2AF720F716E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "scapula_L_grp" -p "skin_proxy_dgc";
	rename -uid "C7B4B293-441E-5A59-59BE-4EBD6F2F2DD5";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 0.40427470940584542 13.277207530751266 -0.5592115895429971 ;
	setAttr ".r" -type "double3" -89.993146533943502 -0.010713070142130845 179.99329215118746 ;
	setAttr -k on ".qsm_distance" 1.8350927434492401;
createNode transform -n "scapula_L_ctl" -p "scapula_L_grp";
	rename -uid "6D9EB00A-4D37-248D-9575-76A27DEB681F";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "scapula_L_ctl_x_Shape" -p "scapula_L_ctl";
	rename -uid "5986EB94-425C-5CC1-4693-69A35BC16F50";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "scapula_L_ctl_y_Shape" -p "scapula_L_ctl";
	rename -uid "9544312F-43E6-4BFC-C4CF-8E9ABAFEC8A7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "scapula_L_ctl_z_Shape" -p "scapula_L_ctl";
	rename -uid "12C2B567-4592-2052-A99A-778697DD442B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.91754637172462006 ;
	setAttr ".los" -type "double3" 0 0 0.91754637172462006 ;
createNode transform -n "scapula_L_geo_copy" -p "scapula_L_ctl";
	rename -uid "B46BE534-4174-C176-9A3C-29BD0B640F2F";
createNode mesh -n "scapula_R_geoShape" -p "scapula_L_geo_copy";
	rename -uid "9D71EB52-45FF-A236-3270-D3A4ABB9F78B";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.875 0.75 0 0.25 0 0.375 0.875 0.25 0.25 0.375
		 0.375 0.625 0.375 0.75 0.25 0.625 0.625 0.875 0.125 0.125 0.125 0.375 0.625 0.25
		 0.125 0.375 0.125 0.625 0.125 0.75 0.125 0.5 0.25 0.5 0.375 0.5 0.5 0.5 0.625 0.5
		 0.75 0.5 0.875 0.5 0 0.5 1 0.5 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -1.7836848 -14.291794 2.9539387 
		-1.3166703 -14.578636 2.7737129 -1.9510864 -12.346916 1.1759174 -1.316885 -13.433517 
		1.6284572 -0.051027671 -12.147038 -0.92465961 0.52029002 -13.857623 0.21495925 0.12308765 
		-14.271142 1.0259279 0.52049351 -14.947567 1.3050338 -0.39350331 -14.806554 2.0782526 
		-0.77607369 -14.271018 1.925239 -0.95019323 -12.225292 0.053058613 -0.39371812 -13.661435 
		0.93299723 0.51200515 -14.480918 0.84673256 -0.22557282 -13.166335 0.26954889 -0.95001727 
		-13.16625 0.99412876 -1.9509289 -13.187008 2.0161088 -1.3167908 -13.933458 2.1284573 
		-0.33630243 -14.218704 1.4330041 -1.6339855 -12.889107 1.4010763 -0.65686637 -12.969706 
		0.5042842 0.25174865 -13.088349 -0.28592703 0.077145688 -13.797525 0.59812218 0.25204042 
		-14.65259 1.2785013 -0.65657556 -14.533945 2.0687125 -1.6337007 -14.415277 2.9274309 
		-1.63386 -13.560233 2.072283;
	setAttr -s 26 ".vt[0:25]"  1.97161114 13.46485138 -1.38646972 1.97310472 13.93338108 -1.20483899
		 1.97196329 13.29801464 0.39159095 1.97331882 13.93351746 -0.059583426 0.05102738 13.2773838 0.57120091
		 0.56008399 14.3576231 -0.059369922 0.043961108 13.44419956 -1.38610649 0.5598802 14.35749245 -1.14944446
		 1.27777398 14.16129875 -1.20473611 0.9431228 13.44409466 -1.38625574 0.95019317 13.27726936 0.49266315
		 1.2779882 14.16143513 -0.059480727 0.6917389 14.48091793 -0.55940926 0.22557281 13.27724171 -0.44827154
		 0.95001721 13.27715683 -0.44840699 1.97180617 13.29791451 -0.44860053 1.97322536 13.93345833 -0.55958343
		 1.27790141 14.21870422 -0.55948758 1.97264123 13.61576653 0.16711473 1.11409032 13.73443985 0.2053349
		 0.32402655 13.85308361 0.20546848 0.4986299 13.85297871 -0.50384474 0.32373402 13.85289574 -1.35895979
		 1.11379778 13.73425102 -1.35909343 1.97235584 13.61558342 -1.3592397 1.97251582 13.61568642 -0.50409186;
	setAttr -s 48 ".ed[0:47]"  0 24 1 2 18 1 4 20 1 6 22 1 0 15 1 1 16 1
		 2 10 1 3 11 1 4 13 1 5 12 1 6 9 1 7 8 1 8 1 1 9 0 1 8 23 1 10 4 1 9 14 1 11 5 1 10 19 1
		 11 17 1 12 7 1 13 6 1 12 21 1 14 10 1 13 14 1 15 2 1 14 15 1 16 3 1 15 25 1 17 8 1
		 16 17 1 17 12 1 18 3 1 19 11 1 18 19 1 20 5 1 19 20 1 21 13 1 20 21 1 22 7 1 21 22 1
		 23 9 1 22 23 1 24 1 1 23 24 1 25 16 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 28 47 -2 -26
		mu 0 4 27 38 30 2
		f 4 18 36 -3 -16
		mu 0 4 19 31 32 4
		f 4 2 38 37 -9
		mu 0 4 4 32 33 25
		f 4 3 42 41 -11
		mu 0 4 6 34 35 17
		f 4 19 31 -10 -18
		mu 0 4 21 29 23 11
		f 4 24 23 15 8
		mu 0 4 24 26 18 13
		f 4 -42 44 -1 -14
		mu 0 4 17 35 37 8
		f 4 -24 26 25 6
		mu 0 4 18 26 27 2
		f 4 1 34 -19 -7
		mu 0 4 2 30 31 19
		f 4 30 -20 -8 -28
		mu 0 4 28 29 21 3
		f 4 -38 40 -4 -22
		mu 0 4 25 33 34 6
		f 4 10 16 -25 21
		mu 0 4 12 16 26 24
		f 4 -27 -17 13 4
		mu 0 4 27 26 16 0
		f 4 0 46 -29 -5
		mu 0 4 0 36 38 27
		f 4 -13 -30 -31 -6
		mu 0 4 1 15 29 28
		f 4 -32 29 -12 -21
		mu 0 4 23 29 15 10
		f 4 32 7 -34 -35
		mu 0 4 30 3 20 31
		f 4 -37 33 17 -36
		mu 0 4 32 31 20 5
		f 4 -39 35 9 22
		mu 0 4 33 32 5 22
		f 4 -41 -23 20 -40
		mu 0 4 34 33 22 7
		f 4 -43 39 11 14
		mu 0 4 35 34 7 14
		f 4 -45 -15 12 -44
		mu 0 4 37 35 14 9
		f 4 -47 43 5 -46
		mu 0 4 38 36 1 28
		f 4 -48 45 27 -33
		mu 0 4 30 38 28 3;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "scapula_R_grp" -p "skin_proxy_dgc";
	rename -uid "FC422D7F-41F8-80DE-7609-30B2C36AE17A";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -0.40427470940584964 13.277207530751268 -0.55921158954299632 ;
	setAttr ".r" -type "double3" 90.006853441183225 0.010713070273765279 -179.99329293053475 ;
	setAttr -k on ".qsm_distance" 1.8350927434492381;
createNode transform -n "scapula_R_ctl" -p "scapula_R_grp";
	rename -uid "6BBC9542-4FA0-1D2A-197E-1086125F3B13";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "scapula_R_ctl_x_Shape" -p "scapula_R_ctl";
	rename -uid "AE237CE8-41AE-C090-B557-3B88998C773B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "scapula_R_ctl_y_Shape" -p "scapula_R_ctl";
	rename -uid "0808D069-4892-1627-52F2-27B4AF04F141";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "scapula_R_ctl_z_Shape" -p "scapula_R_ctl";
	rename -uid "A0394803-4E0E-646D-8D8B-EDBFFABB147E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.91754637172461906 ;
	setAttr ".los" -type "double3" 0 0 0.91754637172461906 ;
createNode transform -n "scapula_R_geo_copy" -p "scapula_R_ctl";
	rename -uid "2449055D-4FB6-4A67-EE5E-FD82B9BAA13A";
createNode mesh -n "scapula_R_geo_copyShape" -p "scapula_R_geo_copy";
	rename -uid "F093D72B-4109-A1B6-F680-4395D3B2A7D9";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.875 0.75 0 0.25 0 0.375 0.875 0.25 0.25 0.375
		 0.375 0.625 0.375 0.75 0.25 0.625 0.625 0.875 0.125 0.125 0.125 0.375 0.625 0.25
		 0.125 0.375 0.125 0.625 0.125 0.75 0.125 0.5 0.25 0.5 0.375 0.5 0.5 0.5 0.625 0.5
		 0.75 0.5 0.875 0.5 0 0.5 1 0.5 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".vt[0:25]"  -0.18792617 -0.82694244 1.567469 -0.6564343 -0.64525509 1.56887388
		 -0.020876884 0.95109844 1.56750834 -0.65643382 0.5 1.56887376 2.8312206e-07 1.1303463 -0.3534587
		 -1.080374002 0.5 0.15558934 -0.16704877 -0.82694244 -0.36017847 -1.080373764 -0.59007454 0.15558934
		 -0.88427055 -0.64525509 0.87351644 -0.16704911 -0.82692337 0.53898323 1.1920929e-07 1.051977158 0.54572177
		 -0.88426995 0.5 0.8735165 -1.20374393 0 0.2873233 1.4901161e-08 0.1109066 -0.17872265
		 5.9604645e-08 0.1109066 0.54572177 -0.020877242 0.1109066 1.56750822 -0.65643454 0 1.56887388
		 -0.94159889 0 0.87351656 -0.33865571 0.72665977 1.56819105 -0.45722389 0.76473427 0.7096191
		 -0.57577527 0.76473427 -0.080458552 -0.5757755 0.0554533 0.094277442 -0.57577443 -0.79969406 -0.080458522
		 -0.45722222 -0.79969406 0.70961905 -0.33865499 -0.79969406 1.56819117 -0.33865595 0.0554533 1.56819117;
	setAttr -s 48 ".ed[0:47]"  0 24 1 2 18 1 4 20 1 6 22 1 0 15 1 1 16 1
		 2 10 1 3 11 1 4 13 1 5 12 1 6 9 1 7 8 1 8 1 1 9 0 1 8 23 1 10 4 1 9 14 1 11 5 1 10 19 1
		 11 17 1 12 7 1 13 6 1 12 21 1 14 10 1 13 14 1 15 2 1 14 15 1 16 3 1 15 25 1 17 8 1
		 16 17 1 17 12 1 18 3 1 19 11 1 18 19 1 20 5 1 19 20 1 21 13 1 20 21 1 22 7 1 21 22 1
		 23 9 1 22 23 1 24 1 1 23 24 1 25 16 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 25 1 -48 -29
		mu 0 4 27 2 30 38
		f 4 15 2 -37 -19
		mu 0 4 19 4 32 31
		f 4 8 -38 -39 -3
		mu 0 4 4 25 33 32
		f 4 10 -42 -43 -4
		mu 0 4 6 17 35 34
		f 4 17 9 -32 -20
		mu 0 4 21 11 23 29
		f 4 -9 -16 -24 -25
		mu 0 4 24 13 18 26
		f 4 13 0 -45 41
		mu 0 4 17 8 37 35
		f 4 -7 -26 -27 23
		mu 0 4 18 2 27 26
		f 4 6 18 -35 -2
		mu 0 4 2 19 31 30
		f 4 27 7 19 -31
		mu 0 4 28 3 21 29
		f 4 21 3 -41 37
		mu 0 4 25 6 34 33
		f 4 -22 24 -17 -11
		mu 0 4 12 24 26 16
		f 4 -5 -14 16 26
		mu 0 4 27 0 16 26
		f 4 4 28 -47 -1
		mu 0 4 0 27 38 36
		f 4 5 30 29 12
		mu 0 4 1 28 29 15
		f 4 20 11 -30 31
		mu 0 4 23 10 15 29
		f 4 34 33 -8 -33
		mu 0 4 30 31 20 3
		f 4 35 -18 -34 36
		mu 0 4 32 5 20 31
		f 4 -23 -10 -36 38
		mu 0 4 33 22 5 32
		f 4 39 -21 22 40
		mu 0 4 34 7 22 33
		f 4 -15 -12 -40 42
		mu 0 4 35 14 7 34
		f 4 43 -13 14 44
		mu 0 4 37 9 14 35
		f 4 45 -6 -44 46
		mu 0 4 38 28 1 36
		f 4 32 -28 -46 47
		mu 0 4 30 3 28 38;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "shoulder_L_grp" -p "skin_proxy_dgc";
	rename -uid "A4E51626-46F5-57AE-925E-8D9DE9F3A049";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 2.2393674082006418 13.276992689020442 -0.55955471214433239 ;
	setAttr ".r" -type "double3" -89.590602550651539 0.92997648099639263 104.22551210822394 ;
	setAttr -k on ".qsm_distance" 3.1664084826285808;
createNode transform -n "shoulder_L_ctl" -p "shoulder_L_grp";
	rename -uid "A49C7E14-48E3-7199-24B4-D2B14841C44D";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "shoulder_L_ctl_x_Shape" -p "shoulder_L_ctl";
	rename -uid "BF599EB3-4DFC-2355-808F-47B8EEE0E36A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "shoulder_L_ctl_y_Shape" -p "shoulder_L_ctl";
	rename -uid "80ACD75F-4151-97C2-B52C-9584DB8C2789";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "shoulder_L_ctl_z_Shape" -p "shoulder_L_ctl";
	rename -uid "33435E8A-499F-A278-C34A-DE81F753FE85";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 1.5832042413142904 ;
	setAttr ".los" -type "double3" 0 0 1.5832042413142904 ;
createNode transform -n "shoulder_L_geo_copy" -p "shoulder_L_ctl";
	rename -uid "7179C919-4F57-DD62-3514-C988E5BEF443";
createNode mesh -n "shoulder_R_geoShape" -p "shoulder_L_geo_copy";
	rename -uid "63CC7492-47D1-8B64-6CF2-ECA0B312E543";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.25 0.375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.125 0.125 0.375 0.625 0.375 0.125 0.625 0.125 0.625
		 0.625 0.875 0.125 0.625 0.875 0.75 0 0.25 0 0.375 0.875 0.25 0.125 0.25 0.25 0.375
		 0.375 0.625 0.375 0.75 0.25 0.75 0.125 0.5 0.5 0.5 0.625 0.5 0.75 0.5 0.875 0.5 0
		 0.5 1 0.5 0.125 0.5 0.25 0.5 0.375;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -3.0509102 -10.485157 4.2353497 
		-3.0202506 -10.730776 4.2424955 -2.9960392 -9.7578545 3.0323648 -2.965379 -10.003474 
		3.0395093 -2.4379709 -11.640383 0.46577767 -2.2171683 -12.889036 -0.02477275 -2.434109 
		-12.931942 1.7801198 -2.2136211 -14.075447 1.182567 -2.4355779 -12.440686 1.2801982 
		-3.0234749 -10.121506 3.6338575 -2.9880838 -10.405025 3.6421046 -2.2107112 -13.504321 
		0.56390011 -2.6213455 -12.434434 2.7809443 -2.6520071 -12.188808 2.7738066 -2.6538281 
		-11.579782 2.154037 -2.6565351 -10.674472 1.232758 -2.6253338 -11.10054 1.4235208 
		-2.6184354 -11.863308 2.1622777 -2.0980253 -13.070229 -0.802679 -2.0468411 -14.048487 
		-0.19872394 -2.0938694 -14.460072 0.61167991 -2.6363101 -12.434135 2.9020514 -3.0404465 
		-10.672458 4.3455973 -3.0081446 -10.244315 3.6374292 -2.9707363 -9.7484789 2.817297 
		-2.6412044 -10.797285 1.2363272;
	setAttr -s 26 ".vt[0:25]"  2.55091047 9.99933529 -0.98903918 3.52025056 10.24495411 -0.9961834
		 2.49603915 10.24404144 -0.020996094 3.46537924 10.48966122 -0.028140068 1.93797088 12.45493126 0.27038631
		 2.9795537 13.47669888 0.022532072 1.93410897 12.43194199 -1.043955684 2.97600651 13.45558071 -1.18480694
		 1.93557787 12.44068623 -0.54403424 2.52347469 10.12168789 -0.50501752 3.64238691 10.40520763 -0.51326394
		 3.12739968 13.5043211 -0.56614017 3.12134528 11.81456757 -1.1565311 2.1520071 11.56894112 -1.14938688
		 2.15382814 11.57978153 -0.52961755 2.15653515 11.59589577 0.39166129 3.12533379 11.83831024 0.20089245
		 3.27273846 11.86330795 -0.53786445 2.15664458 13.8649435 0.22524422 2.14356852 14.04848671 -0.57276738
		 2.15248895 13.84020519 -1.18911481 2.63630986 11.68957329 -1.27763462 3.040446281 10.10044384 -1.078451157
		 3.0081448555 10.24449825 -0.50858951 2.9707365 10.41132641 0.15137148 2.64120436 11.71870899 0.38808906;
	setAttr -s 48 ".ed[0:47]"  0 22 1 2 24 1 4 18 1 6 20 1 0 9 1 1 10 1
		 2 15 1 3 16 1 4 8 1 5 11 1 6 13 1 7 12 1 8 6 1 9 2 1 8 14 1 10 3 1 9 23 1 11 7 1
		 10 17 1 11 19 1 12 1 1 13 0 1 12 21 1 14 9 1 13 14 1 15 4 1 14 15 1 16 5 1 15 25 1
		 17 11 1 16 17 1 17 12 1 18 5 1 19 8 1 18 19 1 20 7 1 19 20 1 21 13 1 20 21 1 22 1 1
		 21 22 1 23 10 1 22 23 1 24 3 1 23 24 1 25 16 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 16 44 -2 -14
		mu 0 4 16 36 37 2
		f 4 28 47 -3 -26
		mu 0 4 26 38 30 4
		f 4 2 34 33 -9
		mu 0 4 4 30 31 15
		f 4 3 38 37 -11
		mu 0 4 6 32 33 23
		f 4 29 -10 -28 30
		mu 0 4 29 19 11 28
		f 4 14 26 25 8
		mu 0 4 14 24 25 13
		f 4 10 24 -15 12
		mu 0 4 12 22 24 14
		f 4 0 42 -17 -5
		mu 0 4 0 34 36 16
		f 4 31 -12 -18 -30
		mu 0 4 29 21 10 19
		f 4 -34 36 -4 -13
		mu 0 4 15 31 32 6
		f 4 -38 40 -1 -22
		mu 0 4 23 33 35 8
		f 4 -25 21 4 -24
		mu 0 4 24 22 0 16
		f 4 -27 23 13 6
		mu 0 4 25 24 16 2
		f 4 1 46 -29 -7
		mu 0 4 2 37 38 26
		f 4 18 -31 -8 -16
		mu 0 4 17 29 28 3
		f 4 -21 -32 -19 -6
		mu 0 4 1 21 29 17
		f 4 32 9 19 -35
		mu 0 4 30 5 18 31
		f 4 -37 -20 17 -36
		mu 0 4 32 31 18 7
		f 4 -39 35 11 22
		mu 0 4 33 32 7 20
		f 4 -41 -23 20 -40
		mu 0 4 35 33 20 9
		f 4 -43 39 5 -42
		mu 0 4 36 34 1 17
		f 4 -45 41 15 -44
		mu 0 4 37 36 17 3
		f 4 -47 43 7 -46
		mu 0 4 38 37 3 27
		f 4 -48 45 27 -33
		mu 0 4 30 38 27 5;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "shoulder_R_grp" -p "skin_proxy_dgc";
	rename -uid "BBA05D79-40E5-9249-FBBB-E28294FB5348";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -2.2393674082035653 13.2769927139817 -0.55955471214945351 ;
	setAttr ".r" -type "double3" 90.40939744335644 -0.92997645683961727 -104.22551288746934 ;
	setAttr -k on ".qsm_distance" 3.1664084826285754;
createNode transform -n "shoulder_R_ctl" -p "shoulder_R_grp";
	rename -uid "C0F5034B-4AC8-0561-BF27-5BA4463C3B95";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "shoulder_R_ctl_x_Shape" -p "shoulder_R_ctl";
	rename -uid "7BFBD194-44A5-15B8-5F0F-F885C66B4A02";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "shoulder_R_ctl_y_Shape" -p "shoulder_R_ctl";
	rename -uid "28180D17-4734-31A7-7632-9AB25C6DEFD9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "shoulder_R_ctl_z_Shape" -p "shoulder_R_ctl";
	rename -uid "1106310C-41CC-06CB-E290-0AB2BAB20CC3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 1.5832042413142877 ;
	setAttr ".los" -type "double3" 0 0 1.5832042413142877 ;
createNode transform -n "shoulder_R_geo_copy" -p "shoulder_R_ctl";
	rename -uid "933C09B9-4A74-C97B-ADC5-6B91EFB7BD89";
createNode mesh -n "shoulder_R_geo_copyShape" -p "shoulder_R_geo_copy";
	rename -uid "4A7BBDD5-4A35-7E70-9A1E-83BD9EF7CF2F";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.25 0.375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.125 0.125 0.375 0.625 0.375 0.125 0.625 0.125 0.625
		 0.625 0.875 0.125 0.625 0.875 0.75 0 0.25 0 0.375 0.875 0.25 0.125 0.25 0.25 0.375
		 0.375 0.625 0.375 0.75 0.25 0.75 0.125 0.5 0.5 0.5 0.625 0.5 0.75 0.5 0.875 0.5 0
		 0.5 1 0.5 0.125 0.5 0.25 0.5 0.375;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".vt[0:25]"  0.5 -0.48582172 3.24631047 -0.50000024 -0.48582172 3.24631214
		 0.50000012 0.48618698 3.011368752 -0.5 0.48618698 3.011369228 0.5 0.81454849 0.73616397
		 -0.76238537 0.5876627 -0.0022406448 0.50000012 -0.5 0.73616409 -0.76238537 -0.61986637 -0.0022399426
		 0.50000012 0 0.73616397 0.50000024 0.00018215179 3.12883997 -0.65430307 0.00018310547 3.12884068
		 -0.91668868 0 -0.0022400022 -0.49999976 -0.61986637 1.62441325 0.50000012 -0.61986732 1.62441969
		 0.50000012 0 1.62441945 0.5 0.92142391 1.62441945 -0.49999976 0.73777008 1.62441325
		 -0.65430284 0 1.62441325 -0.058619261 0.79471493 -0.57743472 -0.096727371 0 -0.77149129
		 -0.058619499 -0.61986637 -0.5774349 2.3841858e-07 -0.74456215 1.62441683 2.3841858e-07 -0.57201385 3.26714611
		 0 0.00018310547 3.12883997 0 0.66284752 2.9686687 0 0.92142391 1.62441623;
	setAttr -s 48 ".ed[0:47]"  0 22 1 2 24 1 4 18 1 6 20 1 0 9 1 1 10 1
		 2 15 1 3 16 1 4 8 1 5 11 1 6 13 1 7 12 1 8 6 1 9 2 1 8 14 1 10 3 1 9 23 1 11 7 1
		 10 17 1 11 19 1 12 1 1 13 0 1 12 21 1 14 9 1 13 14 1 15 4 1 14 15 1 16 5 1 15 25 1
		 17 11 1 16 17 1 17 12 1 18 5 1 19 8 1 18 19 1 20 7 1 19 20 1 21 13 1 20 21 1 22 1 1
		 21 22 1 23 10 1 22 23 1 24 3 1 23 24 1 25 16 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 13 1 -45 -17
		mu 0 4 16 2 37 36
		f 4 25 2 -48 -29
		mu 0 4 26 4 30 38
		f 4 8 -34 -35 -3
		mu 0 4 4 15 31 30
		f 4 10 -38 -39 -4
		mu 0 4 6 23 33 32
		f 4 -31 27 9 -30
		mu 0 4 29 28 11 19
		f 4 -9 -26 -27 -15
		mu 0 4 14 13 25 24
		f 4 -13 14 -25 -11
		mu 0 4 12 14 24 22
		f 4 4 16 -43 -1
		mu 0 4 0 16 36 34
		f 4 29 17 11 -32
		mu 0 4 29 19 10 21
		f 4 12 3 -37 33
		mu 0 4 15 6 32 31
		f 4 21 0 -41 37
		mu 0 4 23 8 35 33
		f 4 23 -5 -22 24
		mu 0 4 24 16 0 22
		f 4 -7 -14 -24 26
		mu 0 4 25 2 16 24
		f 4 6 28 -47 -2
		mu 0 4 2 26 38 37
		f 4 15 7 30 -19
		mu 0 4 17 3 28 29
		f 4 5 18 31 20
		mu 0 4 1 17 29 21
		f 4 34 -20 -10 -33
		mu 0 4 30 31 18 5
		f 4 35 -18 19 36
		mu 0 4 32 7 18 31
		f 4 -23 -12 -36 38
		mu 0 4 33 20 7 32
		f 4 39 -21 22 40
		mu 0 4 35 9 20 33
		f 4 41 -6 -40 42
		mu 0 4 36 17 1 34
		f 4 43 -16 -42 44
		mu 0 4 37 3 17 36
		f 4 45 -8 -44 46
		mu 0 4 38 27 3 37
		f 4 32 -28 -46 47
		mu 0 4 30 5 27 38;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "elbow_L_grp" -p "skin_proxy_dgc";
	rename -uid "EEC8A536-4246-BDFB-29D0-089FB81D6B98";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.0173750526175991 10.208083171629031 -0.50816251278078328 ;
	setAttr ".r" -type "double3" -89.541709447897176 26.722045947738319 104.42494697360172 ;
	setAttr -k on ".qsm_distance" 2.6511749919438121;
createNode transform -n "elbow_L_ctl" -p "elbow_L_grp";
	rename -uid "9570E270-4B8E-F99B-656E-1384E754D792";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "elbow_L_ctl_x_Shape" -p "elbow_L_ctl";
	rename -uid "20868D21-40BF-2C15-9A87-B9A020FF194E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "elbow_L_ctl_y_Shape" -p "elbow_L_ctl";
	rename -uid "AB47367E-4E54-E132-7B2E-03B833B541FB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "elbow_L_ctl_z_Shape" -p "elbow_L_ctl";
	rename -uid "A0B26019-43F4-CCB6-0930-489CF693A048";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 1.3255874959719061 ;
	setAttr ".los" -type "double3" 0 0 1.3255874959719061 ;
createNode transform -n "elbow_L_geo_copy" -p "elbow_L_ctl";
	rename -uid "6471DE8A-454D-5AA8-F660-5282B5DAEE64";
createNode mesh -n "elbow_R_geoShape" -p "elbow_L_geo_copy";
	rename -uid "68562A3E-4DFA-C5AB-FCE1-27AE8302F19C";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.875 0.75 0 0.25 0 0.375 0.875 0.25 0.25 0.375
		 0.375 0.625 0.375 0.75 0.25 0.125 0.125 0.375 0.625 0.25 0.125 0.375 0.125 0.625
		 0.125 0.75 0.125 0.625 0.625 0.875 0.125 0.5 0.375 0.5 0.5 0.5 0.625 0.5 0.75 0.5
		 0.875 0.5 0 0.5 1 0.5 0.125 0.5 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -3.6384101 -7.9791989 2.1659737 
		-3.6248906 -8.0875044 2.1691241 -3.5924342 -7.7311497 1.7721316 -3.5789144 -7.8394561 
		1.7752812 -3.0043118 -9.7215338 0.12316824 -2.9736514 -9.9671535 0.13031226 -3.0618639 
		-10.446037 0.88790572 -3.0312037 -10.691657 0.89504975 -3.2031019 -10.167007 1.4144957 
		-3.241724 -9.857604 1.4054961 -3.1497025 -9.0126553 0.38849175 -3.1110804 -9.3220587 
		0.39749137 -3.033088 -10.083785 0.50553697 -3.1995361 -9.4045038 0.89610285 -3.617094 
		-7.8417797 1.9686626 -3.6002305 -7.9768753 1.9725922 -3.1532683 -9.7751579 0.90688455 
		-3.0024276 -10.329406 0.51268101 -3.1162105 -9.0371466 0.23626684 -2.982254 -9.759655 
		0.037347734 -3.0177577 -10.206595 0.50910896 -3.0532613 -10.653536 0.98087025 -3.236594 
		-10.142515 1.5667205 -3.6373363 -8.0640297 2.2162571 -3.6086621 -7.9093275 1.9706274 
		-3.579988 -7.7546253 1.7249976;
	setAttr -s 26 ".vt[0:25]"  3.41793561 7.75872421 0.4914242 3.84536505 7.86703014 0.48827386
		 3.37195945 7.95162392 0.88526654 3.79938889 8.059930801 0.8821162 2.50431156 10.21138668 -0.021230489
		 3.47365141 10.45700741 -0.028374821 2.5618639 9.95618343 -0.98640347 3.53120375 10.20180416 -0.9935478
		 3.83294272 9.54570675 -0.78414273 2.61188316 9.23630333 -0.77514315 2.5198617 9.633955 0.41057396
		 3.74092126 9.94335842 0.40157437 2.53308773 10.083785057 -0.50381696 2.44500828 9.40450382 -0.1813938
		 3.34208488 7.84177971 0.68873501 3.87523937 7.97687531 0.68480539 3.90779591 9.77515793 -0.19217497
		 3.50242758 10.32940578 -0.51096129 3.11621046 9.84993649 0.58879828 2.98225403 10.36402893 0.088018775
		 3.017757654 10.20659542 -0.50738913 3.05326128 10.049161911 -1.10279703 3.23659372 9.32972527 -0.962367
		 3.63733625 7.78902054 0.44114041 3.60866213 7.90932751 0.6867702 3.579988 8.029634476 0.93239999;
	setAttr -s 48 ".ed[0:47]"  0 23 1 2 25 1 4 19 1 6 21 1 0 14 1 1 15 1
		 2 10 1 3 11 1 4 12 1 5 17 1 6 9 1 7 8 1 8 1 1 9 0 1 8 22 1 10 4 1 9 13 1 11 5 1 10 18 1
		 11 16 1 12 6 1 13 10 1 12 13 1 14 2 1 13 14 1 15 3 1 14 24 1 16 8 1 15 16 1 17 7 1
		 16 17 1 17 20 1 18 11 1 19 5 1 18 19 1 20 12 1 19 20 1 21 7 1 20 21 1 22 9 1 21 22 1
		 23 1 1 22 23 1 24 15 1 23 24 1 25 3 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 26 46 -2 -24
		mu 0 4 25 37 38 2
		f 4 18 34 -3 -16
		mu 0 4 19 30 31 4
		f 4 2 36 35 -9
		mu 0 4 4 31 32 23
		f 4 3 40 39 -11
		mu 0 4 6 33 34 17
		f 4 19 30 -10 -18
		mu 0 4 21 27 29 11
		f 4 22 21 15 8
		mu 0 4 22 24 18 13
		f 4 -40 42 -1 -14
		mu 0 4 17 34 36 8
		f 4 -22 24 23 6
		mu 0 4 18 24 25 2
		f 4 1 47 -19 -7
		mu 0 4 2 38 30 19
		f 4 28 -20 -8 -26
		mu 0 4 26 27 21 3
		f 4 10 16 -23 20
		mu 0 4 12 16 24 22
		f 4 -25 -17 13 4
		mu 0 4 25 24 16 0
		f 4 0 44 -27 -5
		mu 0 4 0 35 37 25
		f 4 -13 -28 -29 -6
		mu 0 4 1 15 27 26
		f 4 -31 27 -12 -30
		mu 0 4 29 27 15 10
		f 4 -36 38 -4 -21
		mu 0 4 23 32 33 6
		f 4 32 17 -34 -35
		mu 0 4 30 20 5 31
		f 4 -37 33 9 31
		mu 0 4 32 31 5 28
		f 4 -39 -32 29 -38
		mu 0 4 33 32 28 7
		f 4 -41 37 11 14
		mu 0 4 34 33 7 14
		f 4 -43 -15 12 -42
		mu 0 4 36 34 14 9
		f 4 -45 41 5 -44
		mu 0 4 37 35 1 26
		f 4 -47 43 25 -46
		mu 0 4 38 37 26 3
		f 4 -48 45 7 -33
		mu 0 4 30 38 3 20;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "elbow_R_grp" -p "skin_proxy_dgc";
	rename -uid "12A17940-47EF-53A9-68A0-3FBAB56B1E79";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.0173750943642417 10.208083207150541 -0.5081625141186541 ;
	setAttr ".r" -type "double3" 90.458290545301097 -26.722045923602547 -104.42494774988585 ;
	setAttr -k on ".qsm_distance" 2.6511749919438117;
createNode transform -n "elbow_R_ctl" -p "elbow_R_grp";
	rename -uid "1D26F76F-4BD3-6DAA-2F6B-ACB584ECC7B1";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "elbow_R_ctl_x_Shape" -p "elbow_R_ctl";
	rename -uid "EFC38A7A-4E73-6293-0AFE-4AB66857A212";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "elbow_R_ctl_y_Shape" -p "elbow_R_ctl";
	rename -uid "D2083BD7-49FC-AB09-5404-F2B257E096E2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "elbow_R_ctl_z_Shape" -p "elbow_R_ctl";
	rename -uid "3638E0AD-4F3A-43D2-B731-649ADB83F98B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 1.3255874959719058 ;
	setAttr ".los" -type "double3" 0 0 1.3255874959719058 ;
createNode transform -n "elbow_R_geo_copy" -p "elbow_R_ctl";
	rename -uid "BC0A734B-403E-5824-6E4A-67B218135582";
createNode mesh -n "elbow_R_geo_copyShape" -p "elbow_R_geo_copy";
	rename -uid "6078B4C6-4B3C-B6F3-F4CB-76A70109E6E5";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.875 0.75 0 0.25 0 0.375 0.875 0.25 0.25 0.375
		 0.375 0.625 0.375 0.75 0.25 0.125 0.125 0.375 0.625 0.25 0.125 0.375 0.125 0.625
		 0.125 0.75 0.125 0.625 0.625 0.875 0.125 0.5 0.375 0.5 0.5 0.5 0.625 0.5 0.75 0.5
		 0.875 0.5 0 0.5 1 0.5 0.125 0.5 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".vt[0:25]"  0.22047448 -0.22047472 2.65739775 -0.22047424 -0.22047424 2.65739799
		 0.22047472 0.22047424 2.65739822 -0.22047472 0.22047472 2.65739727 0.50000024 0.48985291 0.10193777
		 -0.49999976 0.48985386 0.10193746 0.5 -0.48985386 -0.098497748 -0.5 -0.48985291 -0.098498046
		 -0.62984061 -0.6213007 0.63035297 0.62984097 -0.6213007 0.63035297 0.62984085 0.62129974 0.79906571
		 -0.62984061 0.62129974 0.79906577 0.50000024 0 0.0017200112 0.75452793 0 0.71470904
		 0.27500916 0 2.65739775 -0.27500916 0 2.65739775 -0.75452757 0 0.71470964 -0.5 0 0.0017197132
		 2.3841858e-07 0.81278992 0.82506514 2.3841858e-07 0.60437393 0.12536654 2.3841858e-07 0 0.001719892
		 2.3841858e-07 -0.60437393 -0.12192678 2.3841858e-07 -0.81278992 0.60435361 2.3841858e-07 -0.27500916 2.65739775
		 2.3841858e-07 0 2.65739775 2.3841858e-07 0.27500916 2.65739775;
	setAttr -s 48 ".ed[0:47]"  0 23 1 2 25 1 4 19 1 6 21 1 0 14 1 1 15 1
		 2 10 1 3 11 1 4 12 1 5 17 1 6 9 1 7 8 1 8 1 1 9 0 1 8 22 1 10 4 1 9 13 1 11 5 1 10 18 1
		 11 16 1 12 6 1 13 10 1 12 13 1 14 2 1 13 14 1 15 3 1 14 24 1 16 8 1 15 16 1 17 7 1
		 16 17 1 17 20 1 18 11 1 19 5 1 18 19 1 20 12 1 19 20 1 21 7 1 20 21 1 22 9 1 21 22 1
		 23 1 1 22 23 1 24 15 1 23 24 1 25 3 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 23 1 -47 -27
		mu 0 4 25 2 38 37
		f 4 15 2 -35 -19
		mu 0 4 19 4 31 30
		f 4 8 -36 -37 -3
		mu 0 4 4 23 32 31
		f 4 10 -40 -41 -4
		mu 0 4 6 17 34 33
		f 4 17 9 -31 -20
		mu 0 4 21 11 29 27
		f 4 -9 -16 -22 -23
		mu 0 4 22 13 18 24
		f 4 13 0 -43 39
		mu 0 4 17 8 36 34
		f 4 -7 -24 -25 21
		mu 0 4 18 2 25 24
		f 4 6 18 -48 -2
		mu 0 4 2 19 30 38
		f 4 25 7 19 -29
		mu 0 4 26 3 21 27
		f 4 -21 22 -17 -11
		mu 0 4 12 22 24 16
		f 4 -5 -14 16 24
		mu 0 4 25 0 16 24
		f 4 4 26 -45 -1
		mu 0 4 0 25 37 35
		f 4 5 28 27 12
		mu 0 4 1 26 27 15
		f 4 29 11 -28 30
		mu 0 4 29 10 15 27
		f 4 20 3 -39 35
		mu 0 4 23 6 33 32
		f 4 34 33 -18 -33
		mu 0 4 30 31 5 20
		f 4 -32 -10 -34 36
		mu 0 4 32 28 5 31
		f 4 37 -30 31 38
		mu 0 4 33 7 28 32
		f 4 -15 -12 -38 40
		mu 0 4 34 14 7 33
		f 4 41 -13 14 42
		mu 0 4 36 9 14 34
		f 4 43 -6 -42 44
		mu 0 4 37 26 1 35
		f 4 45 -26 -44 46
		mu 0 4 38 3 26 37
		f 4 32 -8 -46 47
		mu 0 4 30 20 3 38;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "wrist_L_grp" -p "skin_proxy_dgc";
	rename -uid "38C69C5F-4F31-480C-BB8F-9496322A346D";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.6072776172240215 7.9147103171440705 0.6839720234568597 ;
	setAttr ".r" -type "double3" -132.55120388182175 15.825308780534312 83.5705758489852 ;
	setAttr -k on ".qsm_distance" 0.98276182552289837;
createNode transform -n "wrist_L_ctl" -p "wrist_L_grp";
	rename -uid "3E9BFB5C-467A-5235-5549-CE9223D87034";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "wrist_L_ctl_x_Shape" -p "wrist_L_ctl";
	rename -uid "FA9C9691-4418-F311-6E2A-D1B2EA1699E0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "wrist_L_ctl_y_Shape" -p "wrist_L_ctl";
	rename -uid "8C3D8D2B-4F8C-EF12-B601-16849A352A51";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "wrist_L_ctl_z_Shape" -p "wrist_L_ctl";
	rename -uid "3E5B6548-4957-8913-9D8C-1FA5B7EEB86A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.49138091276144918 ;
	setAttr ".los" -type "double3" 0 0 0.49138091276144918 ;
createNode transform -n "wrist_L_geo_copy" -p "wrist_L_ctl";
	rename -uid "8BD424D9-4F56-AF0D-2841-AC87FC32365E";
createNode mesh -n "wrist_R_geoShape" -p "wrist_L_geo_copy";
	rename -uid "C8232FE7-4C64-5D3A-F71D-6A8FAF801C79";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.625 0.25 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.625 0.875 0.125 0.125 0.125 0.375 0.625 0.375
		 0.125 0.625 0.125 0.5 0.5 0.5 0.625 0.5 0.75 0.5 0 0.5 1 0.5 0.125 0.5 0.25 0.625
		 0.375 0.75 0.25 0.5 0.375 0.25 0.25 0.375 0.375 0.25 0.125 0.25 0 0.375 0.875 0.5
		 0.875 0.625 0.875 0.75 0 0.75 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -3.9219322 -7.4690013 0.46474481 
		-3.8175182 -7.5115438 0.19005427 -3.310704 -6.6964078 -0.11061755 -3.2074127 -6.7564273 
		-0.40048248 -3.4759429 -7.5873508 -0.64450854 -3.3416286 -7.6856461 -1.0419 -3.8786509 
		-8.0366497 -0.20506251 -3.7446179 -8.1226034 -0.58935523 -3.5320678 -7.9147429 -0.85089183 
		-3.6772969 -7.8120003 -0.42478529 -3.5913177 -7.0261531 0.17874992 -3.4768507 -7.0843892 
		-0.13411011 -3.4105291 -7.6703811 -0.87358403 -3.6064255 -7.8972545 -0.66821855 -3.8416638 
		-8.1586065 -0.41040626 -3.8913298 -7.4850426 0.3806248 -3.5351894 -7.038074 0.042154759 
		-3.2319181 -6.6867642 -0.27569154 -3.2733366 -7.218956 -0.72171533 -3.3166683 -7.1707416 
		-0.57683039 -3.3956895 -7.1691041 -0.39983153 -3.6366732 -7.4463019 -0.1452864 -3.9026575 
		-7.7800503 0.1075727 -3.8711536 -7.8300223 -0.012843365 -3.7803047 -7.8299022 -0.21431118 
		-3.5034056 -7.5006008 -0.49588493;
	setAttr -s 26 ".vt[0:25]"  3.68445396 6.93460226 0.38147774 4.002240181 6.97714472 0.6561687
		 3.073225498 7.085095406 1.06529212 3.38556004 7.14960098 1.3327837 3.18087339 7.88808489 0.72787488
		 3.59704471 7.99166346 1.076467156 3.58358145 7.71735573 0.2884289 4.0037584305 7.80395174 0.64074153
		 3.83161855 7.9107461 0.88545901 3.38222742 7.80272007 0.50815189 3.35383916 6.9861021 0.75598538
		 3.70536137 7.045209408 1.056385517 3.38415074 7.98039532 0.89138818 3.60211468 7.89725447 0.68602258
		 3.81089592 7.80825567 0.41760549 3.86570549 6.91121578 0.50103235 3.52677965 6.99488783 0.90663111
		 3.20782113 7.11508417 1.23290324 3.49432635 7.56830692 1.20795476 3.28606939 7.54881907 1.065210581
		 3.12194324 7.51845503 0.88607097 3.36292696 7.42627621 0.6215561 3.62891126 7.35784388 0.32444078
		 3.84038568 7.36253071 0.45252097 4.0012946129 7.40769577 0.64632463 3.76853013 7.48057508 0.97215486;
	setAttr -s 48 ".ed[0:47]"  0 15 1 2 17 1 4 12 1 6 14 1 0 10 1 1 11 1
		 2 20 1 3 18 1 4 9 1 5 8 1 6 22 1 7 24 1 8 7 1 9 6 1 8 13 1 10 2 1 9 21 1 11 3 1 10 16 1
		 11 25 1 12 5 1 13 9 1 12 13 1 14 7 1 13 14 1 15 1 1 14 23 1 16 11 1 15 16 1 17 3 1
		 16 17 1 17 19 1 18 5 1 19 12 1 18 19 1 20 4 1 19 20 1 21 10 1 20 21 1 22 0 1 21 22 1
		 23 15 1 22 23 1 24 1 1 23 24 1 25 8 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 18 30 -2 -16
		mu 0 4 18 25 26 2
		f 4 1 31 36 -7
		mu 0 4 2 26 29 31
		f 4 2 22 21 -9
		mu 0 4 4 20 21 17
		f 4 42 41 -1 -40
		mu 0 4 34 35 24 8
		f 4 19 47 -8 -18
		mu 0 4 19 38 28 3
		f 4 37 15 6 38
		mu 0 4 32 18 2 30
		f 4 -22 24 -4 -14
		mu 0 4 17 21 22 6
		f 4 39 4 -38 40
		mu 0 4 33 0 18 32
		f 4 0 28 -19 -5
		mu 0 4 0 23 25 18
		f 4 -44 46 -20 -6
		mu 0 4 1 37 38 19
		f 4 20 9 14 -23
		mu 0 4 20 5 14 21
		f 4 -25 -15 12 -24
		mu 0 4 22 21 14 7
		f 4 -42 44 43 -26
		mu 0 4 24 35 36 9
		f 4 -29 25 5 -28
		mu 0 4 25 23 1 19
		f 4 -31 27 17 -30
		mu 0 4 26 25 19 3
		f 4 -32 29 7 34
		mu 0 4 29 26 3 27
		f 4 -34 -35 32 -21
		mu 0 4 20 29 27 5
		f 4 -37 33 -3 -36
		mu 0 4 31 29 20 4
		f 4 16 -39 35 8
		mu 0 4 16 32 30 13
		f 4 10 -41 -17 13
		mu 0 4 12 33 32 16
		f 4 3 26 -43 -11
		mu 0 4 6 22 35 34
		f 4 -45 -27 23 11
		mu 0 4 36 35 22 7
		f 4 -47 -12 -13 -46
		mu 0 4 38 37 10 15
		f 4 -48 45 -10 -33
		mu 0 4 28 38 15 11;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "wrist_R_grp" -p "skin_proxy_dgc";
	rename -uid "223BEB9B-44E0-FCB8-EF12-5EAE2EFCC0BA";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.6072776901680932 7.9147103601724762 0.6839720211230168 ;
	setAttr ".r" -type "double3" 47.448796121203522 -15.825308755816963 -83.570576629154061 ;
	setAttr -k on ".qsm_distance" 0.98276182552289781;
createNode transform -n "wrist_R_ctl" -p "wrist_R_grp";
	rename -uid "4EAB49EC-4AE6-6DDA-DD3D-DAA6DCB18A70";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "wrist_R_ctl_x_Shape" -p "wrist_R_ctl";
	rename -uid "21F07CE9-40FC-775A-FAE5-4CB179D212B5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "wrist_R_ctl_y_Shape" -p "wrist_R_ctl";
	rename -uid "9A8B4661-4090-A577-6A8E-EA97297EC2FF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "wrist_R_ctl_z_Shape" -p "wrist_R_ctl";
	rename -uid "E2DD9070-42EB-3E6E-8FE1-64B1A4934890";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.49138091276144891 ;
	setAttr ".los" -type "double3" 0 0 0.49138091276144891 ;
createNode transform -n "wrist_R_geo_copy" -p "wrist_R_ctl";
	rename -uid "59D1B9C1-4C27-6AE8-457E-F9BBF1DC638D";
createNode mesh -n "wrist_R_geo_copyShape" -p "wrist_R_geo_copy";
	rename -uid "EB865178-4AF0-C73B-92A0-DE8C80CC68DC";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.625 0.25 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.625 0.875 0.125 0.125 0.125 0.375 0.625 0.375
		 0.125 0.625 0.125 0.5 0.5 0.5 0.625 0.5 0.75 0.5 0 0.5 1 0.5 0.125 0.5 0.25 0.625
		 0.375 0.75 0.25 0.5 0.375 0.25 0.25 0.375 0.375 0.25 0.125 0.25 0 0.375 0.875 0.5
		 0.875 0.625 0.875 0.75 0 0.75 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".vt[0:25]"  0.23747826 -0.53439903 0.84622264 -0.18472195 -0.53439903 0.846223
		 0.23747849 0.38868761 0.9546746 -0.17814732 0.39317369 0.93230128 0.29506946 0.30073404 0.083366394
		 -0.25541592 0.3060174 0.034567237 0.29506946 -0.31929398 0.083366439 -0.25914049 -0.31865168 0.051386356
		 -0.29955077 -0.0039968491 0.034567237 0.29506946 -0.0092802048 0.083366632 0.23747849 -0.040050983 0.93473536
		 -0.22851038 -0.039179802 0.92227548 0.026378393 0.31001425 0.017804146 0.0043108463 0 0.017804086
		 0.030767918 -0.35035086 0.0071992874 0.025624275 -0.57382679 0.88165724 0.0084097385 -0.043186188 0.9487859
		 0.024097204 0.42831993 0.95721173 -0.2209897 0.34935093 0.48623949 0.030599117 0.37807751 0.48838025
		 0.27374625 0.34935093 0.48623949 0.27374625 -0.020025253 0.47626978 0.27374625 -0.4222064 0.43201354
		 0.030767918 -0.46749115 0.43967766 -0.2209897 -0.4222064 0.43201351 -0.26512456 -0.02002573 0.47626999;
	setAttr -s 48 ".ed[0:47]"  0 15 1 2 17 1 4 12 1 6 14 1 0 10 1 1 11 1
		 2 20 1 3 18 1 4 9 1 5 8 1 6 22 1 7 24 1 8 7 1 9 6 1 8 13 1 10 2 1 9 21 1 11 3 1 10 16 1
		 11 25 1 12 5 1 13 9 1 12 13 1 14 7 1 13 14 1 15 1 1 14 23 1 16 11 1 15 16 1 17 3 1
		 16 17 1 17 19 1 18 5 1 19 12 1 18 19 1 20 4 1 19 20 1 21 10 1 20 21 1 22 0 1 21 22 1
		 23 15 1 22 23 1 24 1 1 23 24 1 25 8 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 15 1 -31 -19
		mu 0 4 18 2 26 25
		f 4 6 -37 -32 -2
		mu 0 4 2 31 29 26
		f 4 8 -22 -23 -3
		mu 0 4 4 17 21 20
		f 4 39 0 -42 -43
		mu 0 4 34 8 24 35
		f 4 17 7 -48 -20
		mu 0 4 19 3 28 38
		f 4 -39 -7 -16 -38
		mu 0 4 32 30 2 18
		f 4 13 3 -25 21
		mu 0 4 17 6 22 21
		f 4 -41 37 -5 -40
		mu 0 4 33 32 18 0
		f 4 4 18 -29 -1
		mu 0 4 0 18 25 23
		f 4 5 19 -47 43
		mu 0 4 1 19 38 37
		f 4 22 -15 -10 -21
		mu 0 4 20 21 14 5
		f 4 23 -13 14 24
		mu 0 4 22 7 14 21
		f 4 25 -44 -45 41
		mu 0 4 24 9 36 35
		f 4 27 -6 -26 28
		mu 0 4 25 19 1 23
		f 4 29 -18 -28 30
		mu 0 4 26 3 19 25
		f 4 -35 -8 -30 31
		mu 0 4 29 27 3 26
		f 4 20 -33 34 33
		mu 0 4 20 5 27 29
		f 4 35 2 -34 36
		mu 0 4 31 4 20 29
		f 4 -9 -36 38 -17
		mu 0 4 16 13 30 32
		f 4 -14 16 40 -11
		mu 0 4 12 16 32 33
		f 4 10 42 -27 -4
		mu 0 4 6 34 35 22
		f 4 -12 -24 26 44
		mu 0 4 36 7 22 35
		f 4 45 12 11 46
		mu 0 4 38 15 10 37
		f 4 32 9 -46 47
		mu 0 4 28 11 15 38;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_thumb_a_L_grp" -p "skin_proxy_dgc";
	rename -uid "F616F15E-48C2-C5D4-9584-5CA42343D7EC";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.3392040601542847 7.7841179672836356 0.94588353482715481 ;
	setAttr ".r" -type "double3" 176.62126295622178 24.993836642168176 42.310608858665638 ;
	setAttr -k on ".qsm_distance" 0.570235155124454;
createNode transform -n "finger_thumb_a_L_ctl" -p "finger_thumb_a_L_grp";
	rename -uid "1FA23CC7-46B6-2754-D5EE-E999A15B8A17";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 0 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_thumb_a_L_ctl_x_Shape" -p "finger_thumb_a_L_ctl";
	rename -uid "30300241-410A-A50D-5FD7-A6ABE2DC70B7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_thumb_a_L_ctl_y_Shape" -p "finger_thumb_a_L_ctl";
	rename -uid "DDC77146-4D5C-CB29-28CF-06B3FF54F8AF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_thumb_a_L_ctl_z_Shape" -p "finger_thumb_a_L_ctl";
	rename -uid "4CEA4223-40C3-5EF8-FB7A-2C98D0158C91";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.285117577562227 ;
	setAttr ".los" -type "double3" 0 0 0.285117577562227 ;
createNode transform -n "finger_thumb_a_L_geo_copy" -p "finger_thumb_a_L_ctl";
	rename -uid "0B869585-4E13-F4B4-1EFC-3C85C44328FB";
createNode mesh -n "finger_thumb_a_R_geoShape" -p "finger_thumb_a_L_geo_copy";
	rename -uid "930B7CE9-45B5-9344-5153-FC9C06D31A08";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -2.9611182 -7.5897794 -0.51102257 
		-2.8929007 -7.4308167 -0.5227918 -3.0211024 -7.4416056 -0.7103771 -2.9528854 -7.2826428 
		-0.72214687 -3.4033051 -7.7895126 -1.0396762 -3.3350875 -7.6305494 -1.0514457 -3.3433204 
		-7.9376864 -0.84032118 -3.2751033 -7.7787232 -0.85209095;
	setAttr -s 8 ".vt[0:7]"  2.85095024 7.47961187 1.081257582 3.0030684471 7.32064867 1.093027115
		 2.91093445 7.55177355 1.28061235 3.063052893 7.39281082 1.292382 3.29313684 7.89968061 1.039676189
		 3.44525528 7.74071741 1.051445842 3.23315239 7.82751846 0.84032142 3.38527083 7.66855574 0.85209107;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_thumb_a_R_grp" -p "skin_proxy_dgc";
	rename -uid "5C53F852-48ED-D76A-3BD8-CCAF205CA900";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.3392041348752564 7.7841180065521121 0.94588353243727064 ;
	setAttr ".r" -type "double3" -3.3787370233794771 -24.993836625507001 -42.310609646628421 ;
	setAttr -k on ".qsm_distance" 0.57023515512445777;
createNode transform -n "finger_thumb_a_R_ctl" -p "finger_thumb_a_R_grp";
	rename -uid "23596D1B-4848-C3BF-D7F9-A1A2320196E1";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 0 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_thumb_a_R_ctl_x_Shape" -p "finger_thumb_a_R_ctl";
	rename -uid "2EAAF9A6-4BCA-A4C8-A547-1EA3151EFA2D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_thumb_a_R_ctl_y_Shape" -p "finger_thumb_a_R_ctl";
	rename -uid "8583373F-43A1-6F97-33EA-9E933307102A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_thumb_a_R_ctl_z_Shape" -p "finger_thumb_a_R_ctl";
	rename -uid "D97C92BF-40ED-000C-78BF-73B6E10FF710";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.28511757756222889 ;
	setAttr ".los" -type "double3" 0 0 0.28511757756222889 ;
createNode transform -n "finger_thumb_a_R_geo_copy" -p "finger_thumb_a_R_ctl";
	rename -uid "5B50664C-413A-3826-6276-718738114475";
createNode mesh -n "finger_thumb_a_R_geo_copyShape" -p "finger_thumb_a_R_geo_copy";
	rename -uid "3E5D7B9B-4D41-2FB8-67A2-169340149AF3";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016798 -0.1101675 0.57023513 -0.11016774 -0.11016798 0.57023537
		 0.11016798 0.11016798 0.57023531 -0.1101675 0.11016798 0.57023519 0.11016822 0.11016798 1.1920929e-07
		 -0.11016774 0.11016798 2.3841858e-07 0.11016798 -0.11016798 2.9802322e-07 -0.1101675 -0.1101675 1.7881393e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_thumb_b_L_grp" -p "skin_proxy_dgc";
	rename -uid "5F20036E-427E-D79B-36C7-6E95AE147227";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 2.9570016178417844 7.4362111189396272 1.1868197299193599 ;
	setAttr ".r" -type "double3" 176.91952334039431 -6.2734720577713263 44.076493322844982 ;
	setAttr -k on ".qsm_distance" 0.29538424775485633;
createNode transform -n "finger_thumb_b_L_ctl" -p "finger_thumb_b_L_grp";
	rename -uid "0D02913D-4D06-5B9B-7A02-6D8BD4BBB111";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 0 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_thumb_b_L_ctl_x_Shape" -p "finger_thumb_b_L_ctl";
	rename -uid "9A514EAF-4B50-F07E-EC91-79A7A0AD0988";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_thumb_b_L_ctl_y_Shape" -p "finger_thumb_b_L_ctl";
	rename -uid "543E314F-42CD-B4AB-F058-FB9C358894B9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_thumb_b_L_ctl_z_Shape" -p "finger_thumb_b_L_ctl";
	rename -uid "2E7887C5-4259-D681-A9F8-E4835A7D178F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.14769212387742817 ;
	setAttr ".los" -type "double3" 0 0 0.14769212387742817 ;
createNode transform -n "finger_thumb_b_L_geo_copy" -p "finger_thumb_b_L_ctl";
	rename -uid "39013BF7-4E39-FD49-F5E8-F98BDADC3EF1";
createNode mesh -n "finger_thumb_b_R_geoShape" -p "finger_thumb_b_L_geo_copy";
	rename -uid "C3A0D407-417E-281B-785B-CC927042919D";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -2.792928 -7.4257255 -0.74392295 
		-2.7247107 -7.2667623 -0.75569248 -2.7674193 -7.1971722 -0.9626227 -2.6992018 -7.038209 
		-0.97439218 -2.9783556 -7.4014158 -1.2902843 -2.9101386 -7.2424531 -1.302054 -3.0038643 
		-7.6299691 -1.0715846 -2.9356472 -7.4710064 -1.0833544;
	setAttr -s 8 ".vt[0:7]"  2.68276 7.31555748 1.039307117 2.83487844 7.15659428 1.05107677
		 2.65725136 7.30733967 1.25800681 2.8093698 7.14837646 1.26977646 2.8681879 7.51158333 1.29028463
		 3.020306349 7.3526206 1.30205429 2.89369655 7.51980114 1.07158494 3.045814991 7.36083841 1.083354592;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_thumb_b_R_grp" -p "skin_proxy_dgc";
	rename -uid "B7175F8F-4586-D1DA-14A0-CFA374147CA0";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -2.9570016972955484 7.4362111529048684 1.1868197273794572 ;
	setAttr ".r" -type "double3" -3.0804766415312077 6.2734720749943316 -44.076494100213822 ;
	setAttr -k on ".qsm_distance" 0.29538424775485533;
createNode transform -n "finger_thumb_b_R_ctl" -p "finger_thumb_b_R_grp";
	rename -uid "B274B6A7-4944-A24A-DCB0-D386D12B5449";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 0 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_thumb_b_R_ctl_x_Shape" -p "finger_thumb_b_R_ctl";
	rename -uid "0348C05C-421F-9B09-B644-C2ACA92F27C3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_thumb_b_R_ctl_y_Shape" -p "finger_thumb_b_R_ctl";
	rename -uid "E2BBC791-46AA-2C27-026D-4892D998DFFC";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_thumb_b_R_ctl_z_Shape" -p "finger_thumb_b_R_ctl";
	rename -uid "54BD107B-4BB8-902D-3386-DCBD9AAAB751";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.14769212387742767 ;
	setAttr ".los" -type "double3" 0 0 0.14769212387742767 ;
createNode transform -n "finger_thumb_b_R_geo_copy" -p "finger_thumb_b_R_ctl";
	rename -uid "74BDA79F-4F03-8F70-988D-DC8E72290F84";
createNode mesh -n "finger_thumb_b_R_geo_copyShape" -p "finger_thumb_b_R_geo_copy";
	rename -uid "55445F09-4B3E-A750-465C-6FB46E3136DE";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016798 -0.11016798 0.29538423 -0.11016774 -0.11016798 0.29538435
		 0.11016798 0.1101675 0.29538423 -0.11016774 0.11016798 0.29538435 0.11016774 0.1101675 4.7683716e-07
		 -0.11016774 0.11016798 2.3841858e-07 0.11016774 -0.11016798 4.7683716e-07 -0.11016774 -0.11016798 3.5762787e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_thumb_c_L_grp" -p "skin_proxy_dgc";
	rename -uid "FF8D1BE6-41D3-16B5-F241-E3AB4EDCA820";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 2.7460648754879604 7.2319669386736516 1.1545418834246119 ;
	setAttr ".r" -type "double3" 176.78397422094588 17.794769039860743 42.755774972988746 ;
	setAttr -k on ".qsm_distance" 0.3610347937297983;
createNode transform -n "finger_thumb_c_L_ctl" -p "finger_thumb_c_L_grp";
	rename -uid "4FC75535-41B3-B675-8B9F-3F968E212994";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 0 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_thumb_c_L_ctl_x_Shape" -p "finger_thumb_c_L_ctl";
	rename -uid "BB0ACA44-44EB-8772-45B6-C4973708EE1C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_thumb_c_L_ctl_y_Shape" -p "finger_thumb_c_L_ctl";
	rename -uid "C29F597C-4BF9-7B85-294D-3F9B721A332E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_thumb_c_L_ctl_z_Shape" -p "finger_thumb_c_L_ctl";
	rename -uid "AA70AA77-49B9-ED10-0AB3-B1B3D58BE470";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.18051739686489915 ;
	setAttr ".los" -type "double3" 0 0 0.18051739686489915 ;
createNode transform -n "finger_thumb_c_L_geo_copy" -p "finger_thumb_c_L_ctl";
	rename -uid "B98F6886-4D9D-6A23-1F64-0AA5C11BDC4B";
createNode mesh -n "finger_thumb_c_R_geoShape" -p "finger_thumb_c_L_geo_copy";
	rename -uid "4E118712-421B-6E6B-33D5-229EF3306030";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -2.5072787 -7.1608868 -0.79322588 
		-2.4390614 -7.0019236 -0.8049953 -2.5482514 -6.9952679 -1.0026895 -2.4800339 -6.8363051 
		-1.014459 -2.8006599 -7.2286391 -1.253389 -2.7324426 -7.0696759 -1.2651585 -2.7596869 
		-7.3942575 -1.0439249 -2.6914699 -7.2352948 -1.0556947;
	setAttr -s 8 ".vt[0:7]"  2.39711094 7.050718784 1.1542604 2.54922938 6.89175558 1.16602993
		 2.43808341 7.10543585 1.36372411 2.59020185 6.94647264 1.37549376 2.69049191 7.33880711 1.253389
		 2.84261036 7.1798439 1.26515865 2.64951921 7.28408957 1.043925285 2.80163765 7.12512684 1.055694818;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_thumb_c_R_grp" -p "skin_proxy_dgc";
	rename -uid "BED9C858-4D5B-CF92-63E6-9DB17F85C933";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -2.7460649577198057 7.2319669697837057 1.1545418807966072 ;
	setAttr ".r" -type "double3" -3.2160257597732684 -17.794769023056432 -42.755775758225063 ;
	setAttr -k on ".qsm_distance" 0.3610347937298008;
createNode transform -n "finger_thumb_c_R_ctl" -p "finger_thumb_c_R_grp";
	rename -uid "588AFAB4-41AF-0285-9815-76A7EB234214";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 0 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_thumb_c_R_ctl_x_Shape" -p "finger_thumb_c_R_ctl";
	rename -uid "E0B291FD-42EA-5773-9810-E5B518FE08A0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_thumb_c_R_ctl_y_Shape" -p "finger_thumb_c_R_ctl";
	rename -uid "03C73CF7-4A4A-03F2-ED04-8A98B174868B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_thumb_c_R_ctl_z_Shape" -p "finger_thumb_c_R_ctl";
	rename -uid "46D194AF-4F32-EC7C-0D44-829C89A3F05E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1805173968649004 ;
	setAttr ".los" -type "double3" 0 0 0.1805173968649004 ;
createNode transform -n "finger_thumb_c_R_geo_copy" -p "finger_thumb_c_R_ctl";
	rename -uid "375CCB22-4625-6A5E-9BF3-C5A155F9085D";
createNode mesh -n "finger_thumb_c_R_geo_copyShape" -p "finger_thumb_c_R_geo_copy";
	rename -uid "C23FC5BF-46AF-E407-7E1C-B09F8C716FF7";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016774 -0.11016798 0.36103463 -0.11016798 -0.11016798 0.36103475
		 0.11016798 0.1101675 0.36103475 -0.11016774 0.1101675 0.36103487 0.11016798 0.11016798 0
		 -0.11016774 0.11016798 2.3841858e-07 0.11016774 -0.11016798 3.5762787e-07 -0.11016774 -0.11016798 2.3841858e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_index_a_L_grp" -p "skin_proxy_dgc";
	rename -uid "2010A9C4-46C3-C6AA-4AD7-40A1BE508F43";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.285410641958789 7.0235057175204654 1.1278620307175966 ;
	setAttr ".r" -type "double3" -136.57547108373907 6.2209308612199488 70.259693098729144 ;
	setAttr -k on ".qsm_distance" 0.58613790824373324;
createNode transform -n "finger_index_a_L_ctl" -p "finger_index_a_L_grp";
	rename -uid "87D026CD-41AF-7856-C72F-EF8BE9498F34";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_index_a_L_ctl_x_Shape" -p "finger_index_a_L_ctl";
	rename -uid "59D3486B-4439-7408-85E1-9AB79F31DECF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_index_a_L_ctl_y_Shape" -p "finger_index_a_L_ctl";
	rename -uid "F097B422-4386-A403-8EA4-378780EBE63A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_index_a_L_ctl_z_Shape" -p "finger_index_a_L_ctl";
	rename -uid "C4F3486A-47F8-3753-5B08-D99934A91C2A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.29306895412186662 ;
	setAttr ".los" -type "double3" 0 0 0.29306895412186662 ;
createNode transform -n "finger_index_a_L_geo_copy" -p "finger_index_a_L_ctl";
	rename -uid "51DE5B60-4B3B-44A4-D144-A8945F7497AE";
createNode mesh -n "finger_index_a_R_geoShape" -p "finger_index_a_L_geo_copy";
	rename -uid "107564B3-4D60-FA84-4A9E-8A9B38B66FB2";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.2024431 -6.5827785 -0.46459416 
		-3.130522 -6.5479436 -0.62367696 -3.0573652 -6.4319401 -0.61516064 -2.9854443 -6.3971057 
		-0.77424389 -3.2488322 -6.9655037 -1.1236035 -3.1769111 -6.9306693 -1.2826867 -3.3939102 
		-7.1163421 -0.97303712 -3.3219891 -7.0815072 -1.1321199;
	setAttr -s 8 ".vt[0:7]"  3.092275143 6.47261047 1.034829259 3.24068975 6.43777561 1.19391239
		 2.94719744 6.54210806 1.18539584 3.095612049 6.50727367 1.34447896 3.13866425 7.075671673 1.1236037
		 3.28707886 7.040837288 1.28268683 3.28374219 7.0061740875 0.97303718 3.4321568 6.97133923 1.13212025;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_index_a_R_grp" -p "skin_proxy_dgc";
	rename -uid "FF7F80EA-4A8A-C275-7BAD-E2B4884D9BB6";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.2854107270260933 7.0235057559783307 1.12786202799803 ;
	setAttr ".r" -type "double3" 43.424528924834654 -6.2209308378367361 -70.259693879002086 ;
	setAttr -k on ".qsm_distance" 0.58613790824373702;
createNode transform -n "finger_index_a_R_ctl" -p "finger_index_a_R_grp";
	rename -uid "EE09B88E-4223-C980-D606-DC8858F615DD";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_index_a_R_ctl_x_Shape" -p "finger_index_a_R_ctl";
	rename -uid "8ABC577D-41CA-C69E-6FCF-87BBF72F0C25";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_index_a_R_ctl_y_Shape" -p "finger_index_a_R_ctl";
	rename -uid "9DF52D1C-4975-6587-85A8-038D760AB140";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_index_a_R_ctl_z_Shape" -p "finger_index_a_R_ctl";
	rename -uid "3E834B02-4E9A-D270-C39E-34B22DEE3C5F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.29306895412186851 ;
	setAttr ".los" -type "double3" 0 0 0.29306895412186851 ;
createNode transform -n "finger_index_a_R_geo_copy" -p "finger_index_a_R_ctl";
	rename -uid "72F42462-438C-1B0D-F482-83919A0690BE";
createNode mesh -n "finger_index_a_R_geo_copyShape" -p "finger_index_a_R_geo_copy";
	rename -uid "AAAA1A89-4EC7-DC37-E82C-8B81C63F951E";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016798 -0.11016798 0.57023513 -0.11016774 -0.11016798 0.57023549
		 0.11016774 0.11016798 0.57023525 -0.11016774 0.11016798 0.57023513 0.11016798 0.11016798 2.3841858e-07
		 -0.11016774 0.11016798 1.1920929e-07 0.11016798 -0.11016798 1.1920929e-07 -0.11016774 -0.11016798 4.7683716e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_index_b_L_grp" -p "skin_proxy_dgc";
	rename -uid "45867E3A-43EE-A210-87BE-3391070FF8AA";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.0886039462006831 6.4750619482305183 1.1913774139892945 ;
	setAttr ".r" -type "double3" -136.23692303002568 -8.8996225333098895 55.975959195482183 ;
	setAttr -k on ".qsm_distance" 0.27738495560852122;
createNode transform -n "finger_index_b_L_ctl" -p "finger_index_b_L_grp";
	rename -uid "CC04CCFF-46B0-8CC8-08A1-A6917A276507";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_index_b_L_ctl_x_Shape" -p "finger_index_b_L_ctl";
	rename -uid "F8984C5C-44FA-3A69-D7B9-B592C6565C4D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_index_b_L_ctl_y_Shape" -p "finger_index_b_L_ctl";
	rename -uid "96BD866A-4789-E905-8174-BBA1B767D879";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_index_b_L_ctl_z_Shape" -p "finger_index_b_L_ctl";
	rename -uid "6DFFA50E-4F88-858E-CFE5-60A9FEB85612";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.13869247780426061 ;
	setAttr ".los" -type "double3" 0 0 0.13869247780426061 ;
createNode transform -n "finger_index_b_L_geo_copy" -p "finger_index_b_L_ctl";
	rename -uid "3D1D41DA-4540-4685-C8AA-A9A4FB410307";
createNode mesh -n "finger_index_b_R_geoShape" -p "finger_index_b_L_geo_copy";
	rename -uid "1F3047C3-42B4-53AD-5A60-22B0EA3D8323";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.061703 -6.3761902 -0.7171905 
		-2.9539034 -6.2705121 -0.87440223 -2.916625 -6.2253518 -0.86775678 -2.8088253 -6.1196737 
		-1.0249686 -3.0699646 -6.4524817 -1.1880546 -2.9621651 -6.3468037 -1.3452663 -3.2150426 
		-6.6033196 -1.0374877 -3.1072431 -6.497642 -1.1947;
	setAttr -s 8 ".vt[0:7]"  2.95153522 6.26602221 0.99457562 3.064071178 6.16034412 1.15178752
		 2.80645728 6.33551979 1.14514208 2.91899323 6.22984171 1.3023541 2.95979691 6.56264973 1.18805468
		 3.072332859 6.45697165 1.34526658 3.10487485 6.49315166 1.037488103 3.2174108 6.38747406 1.19470012;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_index_b_R_grp" -p "skin_proxy_dgc";
	rename -uid "558FC921-4EBA-BD40-8019-2CA98D9A84AC";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.0886040387281191 6.4750619839838528 1.1913774110323521 ;
	setAttr ".r" -type "double3" 43.763076984174191 8.8996225538673386 -55.975959972629262 ;
	setAttr -k on ".qsm_distance" 0.27738495560851983;
createNode transform -n "finger_index_b_R_ctl" -p "finger_index_b_R_grp";
	rename -uid "11725478-4923-B9AC-A826-D9B94AC426FF";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_index_b_R_ctl_x_Shape" -p "finger_index_b_R_ctl";
	rename -uid "A85A725B-45CF-2EC2-6FE8-14A0F56A6CA1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_index_b_R_ctl_y_Shape" -p "finger_index_b_R_ctl";
	rename -uid "89162FC4-48A2-F9EA-030A-A1B050084009";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_index_b_R_ctl_z_Shape" -p "finger_index_b_R_ctl";
	rename -uid "BB97883F-48D1-85FC-1652-828A639420B1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.13869247780425992 ;
	setAttr ".los" -type "double3" 0 0 0.13869247780425992 ;
createNode transform -n "finger_index_b_R_geo_copy" -p "finger_index_b_R_ctl";
	rename -uid "9C06CA0F-4253-E5DC-695A-57846CA6BD64";
createNode mesh -n "finger_index_b_R_geo_copyShape" -p "finger_index_b_R_geo_copy";
	rename -uid "7270D18B-4CAD-45B3-0029-B1AF5AAA8F05";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016774 -0.11016798 0.27738518 -0.11016774 -0.11016798 0.27738535
		 0.11016774 0.11016798 0.27738535 -0.11016798 0.11016798 0.27738547 0.11016798 0.11016798 1.1920929e-07
		 -0.11016774 0.11016798 3.5762787e-07 0.11016774 -0.11016798 4.7683716e-07 -0.11016774 -0.11016798 2.3841858e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_index_c_L_grp" -p "skin_proxy_dgc";
	rename -uid "D4169C95-44C8-5146-D0CB-EFB009563927";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 2.9352643399646756 6.2479322635138352 1.1484648857740098 ;
	setAttr ".r" -type "double3" -136.39126191073444 7.7986341636662351 71.768895202380591 ;
	setAttr -k on ".qsm_distance" 0.28976619929115321;
createNode transform -n "finger_index_c_L_ctl" -p "finger_index_c_L_grp";
	rename -uid "A990B6F7-45A3-7D02-90DF-5ABE3166B0E6";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_index_c_L_ctl_x_Shape" -p "finger_index_c_L_ctl";
	rename -uid "DD318838-4AB4-269E-96E8-8886A1A7C1F4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_index_c_L_ctl_y_Shape" -p "finger_index_c_L_ctl";
	rename -uid "DD459312-457C-0F88-084A-28BA5EB66786";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_index_c_L_ctl_z_Shape" -p "finger_index_c_L_ctl";
	rename -uid "4047BC6C-4500-6822-ABBF-A28C8A9AF3F0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.14488309964557661 ;
	setAttr ".los" -type "double3" 0 0 0.14488309964557661 ;
createNode transform -n "finger_index_c_L_geo_copy" -p "finger_index_c_L_ctl";
	rename -uid "14CB5CF9-488F-6383-402F-5DB40D845459";
createNode mesh -n "finger_index_c_R_geoShape" -p "finger_index_c_L_geo_copy";
	rename -uid "9C9A3D75-4047-EA0F-ACDE-EFA4B581F870";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -2.9525979 -6.0641675 -0.74370342 
		-2.8833785 -6.0371847 -0.90176553 -2.8075202 -5.9133301 -0.89427024 -2.7383006 -5.8863468 
		-1.0523323 -2.8973351 -6.1860046 -1.144717 -2.8281157 -6.1590214 -1.3027791 -3.042413 
		-6.336843 -0.99415064 -2.9731934 -6.3098593 -1.1522127;
	setAttr -s 8 ".vt[0:7]"  2.84243011 5.954 1.033469558 2.99354625 5.92701674 1.19153166
		 2.69735241 6.023498058 1.18403602 2.8484683 5.9965148 1.34209812 2.78716731 6.29617262 1.1447171
		 2.93828344 6.26918936 1.3027792 2.93224525 6.22667503 0.99415064 3.083361149 6.19969177 1.15221274;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_index_c_R_grp" -p "skin_proxy_dgc";
	rename -uid "2AB5D654-4BED-5492-23B8-DF9874FB1C24";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -2.9352644355814639 6.247932297200034 1.1484648827189192 ;
	setAttr ".r" -type "double3" 43.608738097243759 -7.7986341400666639 -71.768895982807024 ;
	setAttr -k on ".qsm_distance" 0.28976619929115438;
createNode transform -n "finger_index_c_R_ctl" -p "finger_index_c_R_grp";
	rename -uid "B1E914D2-4DAC-F195-20AB-0096D1992EB6";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_index_c_R_ctl_x_Shape" -p "finger_index_c_R_ctl";
	rename -uid "2784D0F9-43A2-3D81-CA57-F1A6B550FD8B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_index_c_R_ctl_y_Shape" -p "finger_index_c_R_ctl";
	rename -uid "CE86F49F-43F6-1CDB-387E-64B5EC2B2868";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_index_c_R_ctl_z_Shape" -p "finger_index_c_R_ctl";
	rename -uid "000B74F3-428A-0F18-FDAA-3B948D8AEF51";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.14488309964557719 ;
	setAttr ".los" -type "double3" 0 0 0.14488309964557719 ;
createNode transform -n "finger_index_c_R_geo_copy" -p "finger_index_c_R_ctl";
	rename -uid "1DB33FFF-43EA-8E07-4326-2BB1701A4143";
createNode mesh -n "finger_index_c_R_geo_copyShape" -p "finger_index_c_R_geo_copy";
	rename -uid "2D890BA2-44DD-070A-1AB9-A5B849A8B101";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016798 -0.1101675 0.28976619 -0.11016774 -0.11016798 0.28976619
		 0.11016798 0.11016798 0.28976583 -0.11016774 0.11016798 0.28976583 0.11016798 0.11016798 2.3841858e-07
		 -0.11016774 0.11016798 1.1920929e-07 0.11016774 -0.1101675 5.9604645e-08 -0.11016774 -0.1101675 1.1920929e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_middle_a_L_grp" -p "skin_proxy_dgc";
	rename -uid "48141D10-4281-5C7E-D913-47838BF2C499";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.5013997861909965 6.975144258121829 0.95197633561294404 ;
	setAttr ".r" -type "double3" -132.69146356577471 3.0446790690673229 72.962424653271256 ;
	setAttr -k on ".qsm_distance" 0.63570722673301105;
createNode transform -n "finger_middle_a_L_ctl" -p "finger_middle_a_L_grp";
	rename -uid "0B108EF5-4E35-E120-7019-E2BF37577FE1";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_middle_a_L_ctl_x_Shape" -p "finger_middle_a_L_ctl";
	rename -uid "ED30F7EA-4324-A674-8CF2-89BCFA929F46";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_middle_a_L_ctl_y_Shape" -p "finger_middle_a_L_ctl";
	rename -uid "27493163-49B3-9398-DCFF-A4A125F6127F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_middle_a_L_ctl_z_Shape" -p "finger_middle_a_L_ctl";
	rename -uid "F068CB23-4E46-6D23-E69E-77829909F0AD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.31785361336650553 ;
	setAttr ".los" -type "double3" 0 0 0.31785361336650553 ;
createNode transform -n "finger_middle_a_L_geo_copy" -p "finger_middle_a_L_ctl";
	rename -uid "8F83C316-4912-D229-5B67-69BF80D68A64";
createNode mesh -n "finger_middle_a_R_geoShape" -p "finger_middle_a_L_geo_copy";
	rename -uid "ADB5BE91-4D44-DF6A-B6A8-CCA9BB84B3FC";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.417146 -6.4722953 -0.19457975 
		-3.3539779 -6.4324307 -0.34376749 -3.2768245 -6.3039575 -0.35630134 -3.2136564 -6.2640934 
		-0.50548917 -3.4628229 -6.9109073 -0.95824313 -3.3996549 -6.8710432 -1.1074309 -3.6031444 
		-7.0792451 -0.79652154 -3.5399766 -7.039381 -0.94570935;
	setAttr -s 8 ".vt[0:7]"  3.30697823 6.3621273 0.83028716 3.46414566 6.32226324 0.97947484
		 3.16665673 6.41412544 0.99200863 3.32382417 6.37426138 1.14119637 3.35265517 7.021075249 0.95824325
		 3.50982261 6.98121119 1.10743093 3.49297667 6.96907711 0.79652178 3.65014434 6.92921305 0.94570947;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_middle_a_R_grp" -p "skin_proxy_dgc";
	rename -uid "AF78000E-400F-41C2-62D1-71BF8DDB9863";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.5013998719157362 6.9751442995938673 0.95197633287193861 ;
	setAttr ".r" -type "double3" 47.308536441646936 -3.0446790453082246 -72.962425433009273 ;
	setAttr -k on ".qsm_distance" 0.63570722673301217;
createNode transform -n "finger_middle_a_R_ctl" -p "finger_middle_a_R_grp";
	rename -uid "AF5A4C28-49E9-D616-7198-478B6E6D6803";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_middle_a_R_ctl_x_Shape" -p "finger_middle_a_R_ctl";
	rename -uid "2DF056ED-4F04-EEB5-A944-5CB455D1CC8D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_middle_a_R_ctl_y_Shape" -p "finger_middle_a_R_ctl";
	rename -uid "39C83CFC-4C8C-5327-9406-B6A96D1D3EC7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_middle_a_R_ctl_z_Shape" -p "finger_middle_a_R_ctl";
	rename -uid "DF524CCB-4A9D-E4E8-F75C-429DBFA6C453";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.31785361336650608 ;
	setAttr ".los" -type "double3" 0 0 0.31785361336650608 ;
createNode transform -n "finger_middle_a_R_geo_copy" -p "finger_middle_a_R_ctl";
	rename -uid "67348B19-4AD0-B131-98CC-5DB1BCA1682A";
createNode mesh -n "finger_middle_a_R_geo_copyShape" -p "finger_middle_a_R_geo_copy";
	rename -uid "5BB770A2-46AF-84A2-52BD-F4B05B8E14DD";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016774 -0.11016798 0.6357075 -0.11016774 -0.1101675 0.63570738
		 0.11016774 0.11016798 0.63570738 -0.11016774 0.11016798 0.63570726 0.11016774 0.11016798 1.7881393e-07
		 -0.1101675 0.11016798 1.1920929e-07 0.11016774 -0.1101675 2.9802322e-07 -0.11016774 -0.11016798 1.7881393e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_middle_b_L_grp" -p "skin_proxy_dgc";
	rename -uid "E0A84AD5-4659-1EBB-F2A6-DAB2777DFB00";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.3154012549899528 6.3681944053976025 0.98574171417842082 ;
	setAttr ".r" -type "double3" -131.47368224367474 -11.59180693341688 56.859797483508935 ;
	setAttr -k on ".qsm_distance" 0.24758933579228604;
createNode transform -n "finger_middle_b_L_ctl" -p "finger_middle_b_L_grp";
	rename -uid "40C586E3-4B52-2104-79D8-4F9BE5EB5B35";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_middle_b_L_ctl_x_Shape" -p "finger_middle_b_L_ctl";
	rename -uid "4146E9AB-48BF-3B4E-33F0-E69AB4BC0846";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_middle_b_L_ctl_y_Shape" -p "finger_middle_b_L_ctl";
	rename -uid "E66A6632-4C4B-7E7E-47C2-7F9BAA2DEA17";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_middle_b_L_ctl_z_Shape" -p "finger_middle_b_L_ctl";
	rename -uid "58BA2C91-4219-03EE-F0CF-7FB57E06662A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.12379466789614302 ;
	setAttr ".los" -type "double3" 0 0 0.12379466789614302 ;
createNode transform -n "finger_middle_b_L_geo_copy" -p "finger_middle_b_L_ctl";
	rename -uid "3081BD76-4111-FAF2-0603-DF85C1542DCC";
createNode mesh -n "finger_middle_b_R_geoShape" -p "finger_middle_b_L_geo_copy";
	rename -uid "4D874C6C-4169-B421-1513-FF959105B021";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.3020337 -6.3066783 -0.53606832 
		-3.203903 -6.1918745 -0.67901504 -3.1617119 -6.1383405 -0.69778955 -3.0635812 -6.0235367 
		-0.84073651 -3.2943058 -6.3414278 -0.99512887 -3.1961751 -6.2266235 -1.1380759 -3.4346275 
		-6.5097651 -0.8334077 -3.3364966 -6.3949609 -0.9763543;
	setAttr -s 8 ".vt[0:7]"  3.19186568 6.19651079 0.78365755 3.3140707 6.081706524 0.92660427
		 3.051544189 6.24850845 0.94537902 3.17374897 6.13370466 1.088325739 3.18413806 6.45159531 0.99512905
		 3.30634284 6.33679152 1.13807583 3.32445955 6.39959764 0.83340758 3.44666433 6.28479338 0.9763543;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_middle_b_R_grp" -p "skin_proxy_dgc";
	rename -uid "9594FB8F-469C-59F2-EBA4-1085EB4B1F0B";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.315401348970568 6.3681944443250256 0.98574171117464904 ;
	setAttr ".r" -type "double3" 48.526317770320873 11.591806954188291 -56.859798260040542 ;
	setAttr -k on ".qsm_distance" 0.2475893357922811;
createNode transform -n "finger_middle_b_R_ctl" -p "finger_middle_b_R_grp";
	rename -uid "0B07AC81-4A00-E62C-EA64-3F80E8AFABDD";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_middle_b_R_ctl_x_Shape" -p "finger_middle_b_R_ctl";
	rename -uid "8B2A2361-4116-C241-DC06-EEA40EAF6A7E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_middle_b_R_ctl_y_Shape" -p "finger_middle_b_R_ctl";
	rename -uid "EFABF09B-4713-D0E8-7E7C-FC9BCE1B442C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_middle_b_R_ctl_z_Shape" -p "finger_middle_b_R_ctl";
	rename -uid "816E29C8-4B7E-2C07-6DE5-1D9349B90785";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.12379466789614055 ;
	setAttr ".los" -type "double3" 0 0 0.12379466789614055 ;
createNode transform -n "finger_middle_b_R_geo_copy" -p "finger_middle_b_R_ctl";
	rename -uid "7B224D66-4738-CAD6-4116-2E87E215DDAC";
createNode mesh -n "finger_middle_b_R_geo_copyShape" -p "finger_middle_b_R_geo_copy";
	rename -uid "794423C2-45B1-0436-2AC9-4997EBB53833";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016798 -0.1101675 0.24758929 -0.11016774 -0.11016798 0.24758929
		 0.11016774 0.11016798 0.24758953 -0.1101675 0.11016798 0.24758929 0.11016774 0.11016798 2.3841858e-07
		 -0.11016774 0.11016798 0 0.11016798 -0.1101675 0 -0.11016774 -0.1101675 1.1920929e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_middle_c_L_grp" -p "skin_proxy_dgc";
	rename -uid "03E7D207-40F3-C35B-EAF4-51878D37A474";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.1828074254995622 6.1651075117152683 0.9359916469061158 ;
	setAttr ".r" -type "double3" -132.75036498278317 1.7438596501755814 71.552642804428189 ;
	setAttr -k on ".qsm_distance" 0.34748014773175684;
createNode transform -n "finger_middle_c_L_ctl" -p "finger_middle_c_L_grp";
	rename -uid "0C3486F2-4856-B6DE-BAAE-CFBD919096DE";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_middle_c_L_ctl_x_Shape" -p "finger_middle_c_L_ctl";
	rename -uid "F4F41060-4F3B-7ACB-F714-ABBE221EF0F7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_middle_c_L_ctl_y_Shape" -p "finger_middle_c_L_ctl";
	rename -uid "BDAE33AB-4EC7-371D-5FEE-61859FA881C6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_middle_c_L_ctl_z_Shape" -p "finger_middle_c_L_ctl";
	rename -uid "BB1FC291-41A3-BA7C-E891-1AAB3E0E4FFF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.17374007386587842 ;
	setAttr ".los" -type "double3" 0 0 0.17374007386587842 ;
createNode transform -n "finger_middle_c_L_geo_copy" -p "finger_middle_c_L_ctl";
	rename -uid "54608F6E-42D8-866B-30C8-08BCFC7C4585";
createNode mesh -n "finger_middle_c_R_geoShape" -p "finger_middle_c_L_geo_copy";
	rename -uid "FD759B59-4327-AD0A-E872-39B9E0A8F08B";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.1757715 -5.9432445 -0.44347766 
		-3.1103585 -5.8963642 -0.59297329 -3.0354497 -5.7749066 -0.60519886 -2.970037 -5.7280264 
		-0.75469446 -3.1453531 -6.1043787 -0.94210458 -3.0799403 -6.0574985 -1.0916003 -3.2856746 
		-6.2727165 -0.78038293 -3.2202618 -6.2258363 -0.92987865;
	setAttr -s 8 ".vt[0:7]"  3.065603495 5.83307695 0.79095733 3.22052622 5.78619671 0.94045305
		 2.925282 5.88507462 0.95267886 3.080204725 5.83819437 1.10217452 3.035185337 6.21454668 0.94210452
		 3.19010806 6.16766644 1.091600299 3.17550683 6.16254854 0.78038299 3.33042955 6.1156683 0.92987877;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_middle_c_R_grp" -p "skin_proxy_dgc";
	rename -uid "77CDBFE6-4F31-AAAE-C7D8-58842C8FA424";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.1828075222424816 6.1651075488607114 0.93599164381457534 ;
	setAttr ".r" -type "double3" 47.249635025213962 -1.7438596266060167 -71.552643584015385 ;
	setAttr -k on ".qsm_distance" 0.34748014773175478;
createNode transform -n "finger_middle_c_R_ctl" -p "finger_middle_c_R_grp";
	rename -uid "74C5AB3A-4443-A3CF-DB1E-2D954742C13D";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_middle_c_R_ctl_x_Shape" -p "finger_middle_c_R_ctl";
	rename -uid "2938D590-49E4-B02F-DC60-FD98618F3C7E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_middle_c_R_ctl_y_Shape" -p "finger_middle_c_R_ctl";
	rename -uid "6ED051DD-4C5B-F86C-43F7-ABAAAE5C5C8D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_middle_c_R_ctl_z_Shape" -p "finger_middle_c_R_ctl";
	rename -uid "CCD6ACBE-4A4A-98C3-7D0B-24933D28E653";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.17374007386587739 ;
	setAttr ".los" -type "double3" 0 0 0.17374007386587739 ;
createNode transform -n "finger_middle_c_R_geo_copy" -p "finger_middle_c_R_ctl";
	rename -uid "803A3EA7-40E2-958E-A1A5-9292700DC054";
createNode mesh -n "finger_middle_c_R_geo_copyShape" -p "finger_middle_c_R_geo_copy";
	rename -uid "A06CE2FA-47D1-4F9B-B0B8-B1AAABFC7393";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016798 -0.1101675 0.34747973 -0.11016774 -0.1101675 0.34747982
		 0.11016774 0.11016798 0.34748006 -0.11016774 0.11016798 0.34748012 0.11016774 0.11016798 0
		 -0.11016774 0.11016798 0 0.11016798 -0.11016798 1.1920929e-07 -0.11016774 -0.11016798 1.7881393e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_ring_a_L_grp" -p "skin_proxy_dgc";
	rename -uid "A7012E2B-4F4A-3B51-52C5-E9A7C6AF3A9C";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.6443397604203605 6.9115229070343167 0.71186893576177357 ;
	setAttr ".r" -type "double3" -116.74631998790271 -0.015402942348255556 77.027999249778603 ;
	setAttr -k on ".qsm_distance" 0.55691868554591151;
createNode transform -n "finger_ring_a_L_ctl" -p "finger_ring_a_L_grp";
	rename -uid "2CB86035-42F7-33CC-B6F8-E2A97D9453E5";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_ring_a_L_ctl_x_Shape" -p "finger_ring_a_L_ctl";
	rename -uid "DBAE9BDF-4C06-4E0C-D509-86949CA08661";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_ring_a_L_ctl_y_Shape" -p "finger_ring_a_L_ctl";
	rename -uid "F03D1020-4E29-02AD-2B7E-D394734E91F8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_ring_a_L_ctl_z_Shape" -p "finger_ring_a_L_ctl";
	rename -uid "410ECA57-43ED-20FB-1AA9-98BCDC30A738";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.27845934277295575 ;
	setAttr ".los" -type "double3" 0 0 0.27845934277295575 ;
createNode transform -n "finger_ring_a_L_geo_copy" -p "finger_ring_a_L_ctl";
	rename -uid "5992FA93-4298-1BF0-E671-D1815FB60DA3";
createNode mesh -n "finger_ring_a_R_geoShape" -p "finger_ring_a_L_geo_copy";
	rename -uid "A2A99A77-4F45-CA8C-3798-B580E18ECCEA";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.5819511 -6.4899964 -0.0068585821 
		-3.5533497 -6.4458027 -0.10601889 -3.4853098 -6.2918682 -0.20362036 -3.4567084 -6.2476745 
		-0.30278012 -3.6103199 -6.8345556 -0.76066917 -3.5817182 -6.7903619 -0.85982943 -3.7069612 
		-7.0326838 -0.56390792 -3.6783597 -6.9884901 -0.66306818;
	setAttr -s 8 ".vt[0:7]"  3.4717834 6.37982845 0.56375849 3.66351748 6.33563471 0.66291857
		 3.3751421 6.40203619 0.76051992 3.56687617 6.35784197 0.85967994 3.50015211 6.94472313 0.76066959
		 3.69188619 6.90052938 0.85982966 3.59679341 6.92251587 0.56390822 3.78852749 6.87832212 0.66306829;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_ring_a_R_grp" -p "skin_proxy_dgc";
	rename -uid "F039ECCB-4DB2-3F7D-E274-7E9A9339AE0E";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.6443398470099644 6.911522950554744 0.71186893299287124 ;
	setAttr ".r" -type "double3" 63.253680017805273 0.015402966573021138 -77.028000029120903 ;
	setAttr -k on ".qsm_distance" 0.55691868554591051;
createNode transform -n "finger_ring_a_R_ctl" -p "finger_ring_a_R_grp";
	rename -uid "8DC42E37-4EF1-83C2-5449-4AB379789C8E";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_ring_a_R_ctl_x_Shape" -p "finger_ring_a_R_ctl";
	rename -uid "6B417EBC-4735-0069-C076-C09D7D7E8578";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_ring_a_R_ctl_y_Shape" -p "finger_ring_a_R_ctl";
	rename -uid "FDB4F25A-4BEB-7346-DC43-7F9469D7B601";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_ring_a_R_ctl_z_Shape" -p "finger_ring_a_R_ctl";
	rename -uid "2D938F06-448C-4315-54E0-73A13FB9F5AF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.27845934277295525 ;
	setAttr ".los" -type "double3" 0 0 0.27845934277295525 ;
createNode transform -n "finger_ring_a_R_geo_copy" -p "finger_ring_a_R_ctl";
	rename -uid "11B72162-4C74-DF03-E189-F2B58E168F8A";
createNode mesh -n "finger_ring_a_R_geo_copyShape" -p "finger_ring_a_R_geo_copy";
	rename -uid "5A5F2AE3-4234-36F3-D32E-97973126C4A8";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016774 -0.11016798 0.55689996 -0.11016774 -0.1101675 0.55689973
		 0.11016774 0.11016798 0.55689961 -0.11016774 0.11016798 0.55689991 0.11016774 0.11016798 4.7683716e-07
		 -0.11016774 0.11016798 2.9802322e-07 0.11016774 -0.11016798 3.5762787e-07 -0.11016774 -0.11016798 1.7881393e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_ring_b_L_grp" -p "skin_proxy_dgc";
	rename -uid "7E5E0AD3-4771-2B1F-309A-47AB0C22D9DC";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.5193255136061854 6.3688168742796476 0.71171921816651562 ;
	setAttr ".r" -type "double3" -114.44469319883183 -11.205055063104458 53.887691663502622 ;
	setAttr -k on ".qsm_distance" 0.29236417174526902;
createNode transform -n "finger_ring_b_L_ctl" -p "finger_ring_b_L_grp";
	rename -uid "B5F5225D-4D82-6362-D4FB-CCA410722653";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_ring_b_L_ctl_x_Shape" -p "finger_ring_b_L_ctl";
	rename -uid "AF113C6B-4171-48B7-31ED-8A9EE80CBF48";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_ring_b_L_ctl_y_Shape" -p "finger_ring_b_L_ctl";
	rename -uid "49531AEE-470F-E32B-A65B-8D8AE7633EDF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_ring_b_L_ctl_z_Shape" -p "finger_ring_b_L_ctl";
	rename -uid "153CDE6E-4C82-AE57-F3D9-11BF09EC182D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.14618208587263451 ;
	setAttr ".los" -type "double3" 0 0 0.14618208587263451 ;
createNode transform -n "finger_ring_b_L_geo_copy" -p "finger_ring_b_L_ctl";
	rename -uid "F0A9A74D-4ACF-23A9-1C24-F0B928849FC0";
createNode mesh -n "finger_ring_b_R_geoShape" -p "finger_ring_b_L_geo_copy";
	rename -uid "4F21F712-4F49-7DFB-F5A4-058916F3FE6B";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.4329815 -6.3024383 -0.21944144 
		-3.364249 -6.1699061 -0.3088817 -3.3363497 -6.104351 -0.41620281 -3.267617 -5.9718189 
		-0.50564301 -3.5053756 -6.3360391 -0.76537937 -3.4366431 -6.2035069 -0.8548196 -3.6020076 
		-6.5341263 -0.56861812 -3.5332749 -6.4015942 -0.65805823;
	setAttr -s 8 ".vt[0:7]"  3.32281375 6.19227028 0.51180595 3.47441673 6.059738159 0.601246
		 3.22618198 6.21451902 0.70856738 3.37778473 6.081986904 0.79800749 3.39520788 6.44620705 0.76537985
		 3.54681087 6.31367493 0.85481989 3.49183989 6.4239583 0.56861842 3.64344263 6.29142618 0.65805846;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_ring_b_R_grp" -p "skin_proxy_dgc";
	rename -uid "1162D5C9-4464-7B45-E802-72A5561D8519";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.5193256075777368 6.368816916099683 0.71171921516256986 ;
	setAttr ".r" -type "double3" 65.555306816223862 11.205055083137053 -53.887692439920805 ;
	setAttr -k on ".qsm_distance" 0.29236417174527646;
createNode transform -n "finger_ring_b_R_ctl" -p "finger_ring_b_R_grp";
	rename -uid "3923E435-44A9-053F-EC28-C3B6774CBA85";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_ring_b_R_ctl_x_Shape" -p "finger_ring_b_R_ctl";
	rename -uid "E1256E4D-43E7-F44D-6323-5A9FC1D5B1F3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_ring_b_R_ctl_y_Shape" -p "finger_ring_b_R_ctl";
	rename -uid "61231312-46D4-A949-3812-668B98E12989";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_ring_b_R_ctl_z_Shape" -p "finger_ring_b_R_ctl";
	rename -uid "22957606-4618-F554-6265-30AF3E012AEF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.14618208587263823 ;
	setAttr ".los" -type "double3" 0 0 0.14618208587263823 ;
createNode transform -n "finger_ring_b_R_geo_copy" -p "finger_ring_b_R_ctl";
	rename -uid "5CDDA037-404E-A6D3-9A00-7A8EB493C324";
createNode mesh -n "finger_ring_b_R_geo_copyShape" -p "finger_ring_b_R_geo_copy";
	rename -uid "3C45E859-49A3-B4EA-9336-5294A7ED19BD";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016774 -0.11016798 0.2923646 -0.11016774 -0.11016798 0.29236439
		 0.11016774 0.11016798 0.29236466 -0.11016774 0.11016798 0.2923646 0.11016774 0.11016798 5.9604645e-07
		 -0.11016774 0.11016798 3.5762787e-07 0.11016774 -0.11016798 4.1723251e-07 -0.11016774 -0.1101675 2.9802322e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_ring_c_L_grp" -p "skin_proxy_dgc";
	rename -uid "87DB3CE9-437F-85A5-BE03-73B9398B90BD";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.3502994490140074 6.1371288472819696 0.65490674986332276 ;
	setAttr ".r" -type "double3" -116.74279523359864 -0.45112495028733218 76.138766984922199 ;
	setAttr -k on ".qsm_distance" 0.33620356488749981;
createNode transform -n "finger_ring_c_L_ctl" -p "finger_ring_c_L_grp";
	rename -uid "BF530D70-4086-62DB-9EB9-149CEF388CD6";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_ring_c_L_ctl_x_Shape" -p "finger_ring_c_L_ctl";
	rename -uid "2A1349D1-4E49-78E3-5C74-3E81AC70C8A7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_ring_c_L_ctl_y_Shape" -p "finger_ring_c_L_ctl";
	rename -uid "14393A94-4966-5E88-BF72-D3B9DD948E7B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_ring_c_L_ctl_z_Shape" -p "finger_ring_c_L_ctl";
	rename -uid "4DFEA9C5-4FB0-CCF6-E70A-3FBCC02652B1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1681017824437499 ;
	setAttr ".los" -type "double3" 0 0 0.1681017824437499 ;
createNode transform -n "finger_ring_c_L_geo_copy" -p "finger_ring_c_L_ctl";
	rename -uid "785CB972-4EC9-1109-6B02-C6A63ACFD339";
createNode mesh -n "finger_ring_c_R_geoShape" -p "finger_ring_c_L_geo_copy";
	rename -uid "D3AD1D0D-4B44-0650-AF80-78A7C50689EF";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.3328159 -5.9337187 -0.16810305 
		-3.3033307 -5.8858209 -0.26724795 -3.2361839 -5.7356315 -0.36486444 -3.2066987 -5.6877337 
		-0.46400923 -3.3167262 -6.0620341 -0.70371497 -3.287241 -6.0141363 -0.80285972 -3.4133577 
		-6.2601209 -0.50695318 -3.3838727 -6.2122231 -0.606098;
	setAttr -s 8 ".vt[0:7]"  3.22264791 5.8235507 0.50430644 3.4134984 5.77565289 0.60345137
		 3.12601614 5.84579945 0.70106792 3.3168664 5.79790163 0.8002128 3.20655823 6.17220211 0.70371503
		 3.39740849 6.12430429 0.8028599 3.30318999 6.14995289 0.5069536 3.49404049 6.10205507 0.60609847;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_ring_c_R_grp" -p "skin_proxy_dgc";
	rename -uid "CEEA71F6-4A9F-F7D9-9F8B-879AFB5C7AB2";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.3502995461368767 6.1371288868275222 0.65490674675928306 ;
	setAttr ".r" -type "double3" 63.257204772484798 0.45112497442056748 -76.138767764218144 ;
	setAttr -k on ".qsm_distance" 0.33620356488749892;
createNode transform -n "finger_ring_c_R_ctl" -p "finger_ring_c_R_grp";
	rename -uid "4C932D06-4123-8145-B6DC-519E0E30D5D6";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_ring_c_R_ctl_x_Shape" -p "finger_ring_c_R_ctl";
	rename -uid "6711DA4C-4885-8533-756C-E9B15F0762E4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_ring_c_R_ctl_y_Shape" -p "finger_ring_c_R_ctl";
	rename -uid "A3ACDE92-4A55-B093-CE13-5982C8539F03";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_ring_c_R_ctl_z_Shape" -p "finger_ring_c_R_ctl";
	rename -uid "D73AE76A-41DF-9590-7D5F-C4A8FE72BC1D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.16810178244374946 ;
	setAttr ".los" -type "double3" 0 0 0.16810178244374946 ;
createNode transform -n "finger_ring_c_R_geo_copy" -p "finger_ring_c_R_ctl";
	rename -uid "7E933FFB-4915-8E46-49D7-88A27D78C674";
createNode mesh -n "finger_ring_c_R_geo_copyShape" -p "finger_ring_c_R_geo_copy";
	rename -uid "57D6A03E-4EA2-3846-1A92-8BBEC22980EA";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016798 -0.11016798 0.33620346 -0.11016774 -0.11016798 0.33620349
		 0.11016798 0.11016798 0.33620355 -0.1101675 0.11016798 0.33620363 0.11016798 0.11016798 1.1920929e-07
		 -0.1101675 0.11016798 2.3841858e-07 0.11016798 -0.1101675 4.7683716e-07 -0.11016774 -0.11016798 5.364418e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_pinky_a_L_grp" -p "skin_proxy_dgc";
	rename -uid "668317A9-499D-8589-123B-1DA48EBBF643";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.7306276584747202 6.9592235440370818 0.46498816863606302 ;
	setAttr ".r" -type "double3" -112.54853441155299 -3.4184689944956794 81.166657606870984 ;
	setAttr -k on ".qsm_distance" 0.46105262977498329;
createNode transform -n "finger_pinky_a_L_ctl" -p "finger_pinky_a_L_grp";
	rename -uid "ED5BEA07-491A-B8F1-9762-0FBB1EE462E6";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_pinky_a_L_ctl_x_Shape" -p "finger_pinky_a_L_ctl";
	rename -uid "6317FF12-4C01-3769-1DE4-03A24588C79B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_pinky_a_L_ctl_y_Shape" -p "finger_pinky_a_L_ctl";
	rename -uid "2A397BEE-464C-0FF6-5DE6-4E9A8E521890";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_pinky_a_L_ctl_z_Shape" -p "finger_pinky_a_L_ctl";
	rename -uid "6EFA68F0-4BDB-F77B-211F-0A97FF60CD1D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.23052631488749165 ;
	setAttr ".los" -type "double3" 0 0 0.23052631488749165 ;
createNode transform -n "finger_pinky_a_L_geo_copy" -p "finger_pinky_a_L_ctl";
	rename -uid "80FB2A58-42E4-215D-61C4-9384779F4D04";
createNode mesh -n "finger_pinky_a_R_geoShape" -p "finger_pinky_a_L_geo_copy";
	rename -uid "9CB35214-4678-5280-B4F4-D996CA745915";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.7126455 -6.6322393 0.16729125 
		-3.6926148 -6.5960126 0.082950458 -3.6272933 -6.4128885 -0.035838775 -3.6072624 -6.3766613 
		-0.12017957 -3.6979668 -6.867661 -0.52438247 -3.6779361 -6.8314342 -0.60872334 -3.7833192 
		-7.0870123 -0.32125247 -3.7632885 -7.0507855 -0.40559328;
	setAttr -s 8 ".vt[0:7]"  3.60247779 6.52207136 0.29376107 3.80278254 6.48584461 0.37810192
		 3.51712561 6.52305603 0.49689102 3.71743011 6.48682928 0.58123189 3.58779907 6.97782898 0.52438271
		 3.78810382 6.94160223 0.60872358 3.67315149 6.97684431 0.32125273 3.87345624 6.94061756 0.4055936;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode mesh -n "polySurfaceShape6" -p "finger_pinky_a_L_geo_copy";
	rename -uid "C9A5EACD-43CA-5D29-3737-D3BBB1652BCA";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  0.3898322 0.3898322 0.056899615 
		-0.3898322 0.3898322 0.056899615 0.3898322 -0.3898322 0.056899615 -0.3898322 -0.3898322 
		0.056899615 0.3898322 -0.3898322 0.50000024 -0.3898322 -0.3898322 0.50000024 0.3898322 
		0.3898322 0.50000024 -0.3898322 0.3898322 0.50000024;
	setAttr -s 8 ".vt[0:7]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 0.5 0.5 0.5
		 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 -0.5 -0.5 0.5 -0.5 -0.5;
	setAttr -s 12 ".ed[0:11]"  0 1 0 2 3 0 4 5 0 6 7 0 0 2 0 1 3 0 2 4 0
		 3 5 0 4 6 0 5 7 0 6 0 0 7 1 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_pinky_a_R_grp" -p "skin_proxy_dgc";
	rename -uid "69BAB417-461A-4AD5-132E-E6AF59F404C2";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.7306277444149587 6.9592235888382561 0.46498816588765779 ;
	setAttr ".r" -type "double3" 67.451465592398833 3.418469019069216 -81.16665838597919 ;
	setAttr -k on ".qsm_distance" 0.46105262977498462;
createNode transform -n "finger_pinky_a_R_ctl" -p "finger_pinky_a_R_grp";
	rename -uid "6B18D54F-4B10-FE07-8476-C295BAE51C50";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_pinky_a_R_ctl_x_Shape" -p "finger_pinky_a_R_ctl";
	rename -uid "44584C0B-4E1C-A563-7562-4090F42A3CFB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_pinky_a_R_ctl_y_Shape" -p "finger_pinky_a_R_ctl";
	rename -uid "7A139774-40DC-F53D-9649-079762583936";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_pinky_a_R_ctl_z_Shape" -p "finger_pinky_a_R_ctl";
	rename -uid "BC198A3A-4453-C055-08E5-C7B35F44BFE2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.23052631488749231 ;
	setAttr ".los" -type "double3" 0 0 0.23052631488749231 ;
createNode transform -n "finger_pinky_a_R_geo_copy" -p "finger_pinky_a_R_ctl";
	rename -uid "B1F4110A-4FAB-917F-589F-6A8E247BB1AC";
createNode mesh -n "finger_pinky_a_R_geo_copyShape" -p "finger_pinky_a_R_geo_copy";
	rename -uid "78DE8355-41B9-076F-10C5-54BB7FD32404";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016798 -0.11016798 0.46105239 -0.11016774 -0.1101675 0.46105242
		 0.11016774 0.11016798 0.4610523 -0.1101675 0.11016798 0.46105239 0.11016774 0.11016798 2.9802322e-07
		 -0.11016774 0.11016798 2.9802322e-07 0.11016774 -0.11016798 3.2782555e-07 -0.11016774 -0.11016798 3.8743019e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode mesh -n "polySurfaceShape6" -p "finger_pinky_a_R_geo_copy";
	rename -uid "D3344C05-404E-CE45-12C7-B7950DA45D9E";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  0.3898322 0.3898322 0.056899615 
		-0.3898322 0.3898322 0.056899615 0.3898322 -0.3898322 0.056899615 -0.3898322 -0.3898322 
		0.056899615 0.3898322 -0.3898322 0.50000024 -0.3898322 -0.3898322 0.50000024 0.3898322 
		0.3898322 0.50000024 -0.3898322 0.3898322 0.50000024;
	setAttr -s 8 ".vt[0:7]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 0.5 0.5 0.5
		 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 -0.5 -0.5 0.5 -0.5 -0.5;
	setAttr -s 12 ".ed[0:11]"  0 1 0 2 3 0 4 5 0 6 7 0 0 2 0 1 3 0 2 4 0
		 3 5 0 4 6 0 5 7 0 6 0 0 7 1 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_pinky_b_L_grp" -p "skin_proxy_dgc";
	rename -uid "54F662E1-446A-11B5-82DA-87A263ABD188";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.6599539809298154 6.5044500131836473 0.4374964542514167 ;
	setAttr ".r" -type "double3" -109.5987023477131 -11.872656847309573 59.318958422309485 ;
	setAttr -k on ".qsm_distance" 0.2525949212619476;
createNode transform -n "finger_pinky_b_L_ctl" -p "finger_pinky_b_L_grp";
	rename -uid "93D4678F-467D-F835-46A9-3BA6CA3F55EA";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_pinky_b_L_ctl_x_Shape" -p "finger_pinky_b_L_ctl";
	rename -uid "BF51796D-4913-60B4-9E4E-AFA521210D13";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_pinky_b_L_ctl_y_Shape" -p "finger_pinky_b_L_ctl";
	rename -uid "1FEFE063-49EA-DDFB-CFAA-B195525FC7C1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_pinky_b_L_ctl_z_Shape" -p "finger_pinky_b_L_ctl";
	rename -uid "D58E06F8-4399-2951-BCD6-689DE7B4DA51";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1262974606309738 ;
	setAttr ".los" -type "double3" 0 0 0.1262974606309738 ;
createNode transform -n "finger_pinky_b_L_geo_copy" -p "finger_pinky_b_L_ctl";
	rename -uid "DE4B4A76-483D-40DB-CAA4-F498BAA36C48";
createNode mesh -n "finger_pinky_b_R_geoShape" -p "finger_pinky_b_L_geo_copy";
	rename -uid "5B318AD4-4BD1-1A34-471F-F180B9E94E96";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.6012886 -6.4610319 0.0047944579 
		-3.5517089 -6.3420401 -0.067531392 -3.5159361 -6.2416806 -0.19833553 -3.466357 -6.1226892 
		-0.27066183 -3.6420674 -6.4542699 -0.50289816 -3.5924881 -6.3352785 -0.57522434 -3.7274196 
		-6.6736212 -0.29976803 -3.6778402 -6.5546293 -0.37209395;
	setAttr -s 8 ".vt[0:7]"  3.49112082 6.35086393 0.24780026 3.66187692 6.23187208 0.32012641
		 3.40576839 6.3518486 0.45093024 3.5765245 6.23285723 0.52325642 3.53189969 6.56443787 0.50289834
		 3.70265579 6.44544649 0.57522446 3.61725187 6.5634532 0.29976836 3.78800821 6.44446135 0.37209448;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode mesh -n "polySurfaceShape6" -p "finger_pinky_b_L_geo_copy";
	rename -uid "884A0B51-4952-7D3E-2619-B6B0329DA3D3";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  0.3898322 0.3898322 0.056899615 
		-0.3898322 0.3898322 0.056899615 0.3898322 -0.3898322 0.056899615 -0.3898322 -0.3898322 
		0.056899615 0.3898322 -0.3898322 0.50000024 -0.3898322 -0.3898322 0.50000024 0.3898322 
		0.3898322 0.50000024 -0.3898322 0.3898322 0.50000024;
	setAttr -s 8 ".vt[0:7]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 0.5 0.5 0.5
		 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 -0.5 -0.5 0.5 -0.5 -0.5;
	setAttr -s 12 ".ed[0:11]"  0 1 0 2 3 0 4 5 0 6 7 0 0 2 0 1 3 0 2 4 0
		 3 5 0 4 6 0 5 7 0 6 0 0 7 1 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_pinky_b_R_grp" -p "skin_proxy_dgc";
	rename -uid "A079C730-466B-7ACD-8903-E8A16E9D4AF0";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.6599540730558764 6.5044500570354291 0.43749645130597786 ;
	setAttr ".r" -type "double3" 70.401297665373122 11.87265686865012 -59.318959198960989 ;
	setAttr -k on ".qsm_distance" 0.25259492126194988;
createNode transform -n "finger_pinky_b_R_ctl" -p "finger_pinky_b_R_grp";
	rename -uid "4226CEA3-4DD7-62E2-BBE7-ED868CBCCFE1";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_pinky_b_R_ctl_x_Shape" -p "finger_pinky_b_R_ctl";
	rename -uid "EEC3D121-4F08-F924-8DC1-DB9FDCB43EC2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_pinky_b_R_ctl_y_Shape" -p "finger_pinky_b_R_ctl";
	rename -uid "4145ABCE-451A-3B2E-A895-078EFAB894A2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_pinky_b_R_ctl_z_Shape" -p "finger_pinky_b_R_ctl";
	rename -uid "92EBBC0F-42FE-517A-15F2-AC854C9C4BB3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.12629746063097494 ;
	setAttr ".los" -type "double3" 0 0 0.12629746063097494 ;
createNode transform -n "finger_pinky_b_R_geo_copy" -p "finger_pinky_b_R_ctl";
	rename -uid "8CBC43F7-4A19-86D2-D736-AFB0A3C2E3A8";
createNode mesh -n "finger_pinky_b_R_geo_copyShape" -p "finger_pinky_b_R_geo_copy";
	rename -uid "2D407AAC-465D-8147-E333-CC9BC62DD236";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016774 -0.11016798 0.2525948 -0.11016774 -0.1101675 0.25259513
		 0.11016774 0.11016798 0.25259477 -0.1101675 0.11016798 0.25259468 0.11016774 0.11016798 2.9802322e-07
		 -0.11016774 0.11016798 1.7881393e-07 0.11016774 -0.11016798 4.1723251e-07 -0.11016798 -0.11016798 6.2584877e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode mesh -n "polySurfaceShape6" -p "finger_pinky_b_R_geo_copy";
	rename -uid "9AA4EB1A-4328-05D3-8B2A-B1AE69EEFCF6";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  0.3898322 0.3898322 0.056899615 
		-0.3898322 0.3898322 0.056899615 0.3898322 -0.3898322 0.056899615 -0.3898322 -0.3898322 
		0.056899615 0.3898322 -0.3898322 0.50000024 -0.3898322 -0.3898322 0.50000024 0.3898322 
		0.3898322 0.50000024 -0.3898322 0.3898322 0.50000024;
	setAttr -s 8 ".vt[0:7]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 0.5 0.5 0.5
		 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 -0.5 -0.5 0.5 -0.5 -0.5;
	setAttr -s 12 ".ed[0:11]"  0 1 0 2 3 0 4 5 0 6 7 0 0 2 0 1 3 0 2 4 0
		 3 5 0 4 6 0 5 7 0 6 0 0 7 1 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_pinky_c_L_grp" -p "skin_proxy_dgc";
	rename -uid "BFDA2A0F-4676-6B67-8BA4-C597AC2A2702";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 3.5338225858990704 6.2918603266664999 0.38552828494107233 ;
	setAttr ".r" -type "double3" -112.61426003459687 -2.9252205283329911 82.354469688319938 ;
	setAttr -k on ".qsm_distance" 0.26516992821796947;
createNode transform -n "finger_pinky_c_L_ctl" -p "finger_pinky_c_L_grp";
	rename -uid "D2A942E3-481A-0A26-1725-3FB25365297C";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_pinky_c_L_ctl_x_Shape" -p "finger_pinky_c_L_ctl";
	rename -uid "5F3578F3-4E83-D654-4E9A-57B27D16692E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_pinky_c_L_ctl_y_Shape" -p "finger_pinky_c_L_ctl";
	rename -uid "8323C0BC-4685-C076-8872-5A9C3F2A247C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_pinky_c_L_ctl_z_Shape" -p "finger_pinky_c_L_ctl";
	rename -uid "ED71284E-4E3C-533E-D84F-E982B5159D3A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.13258496410898474 ;
	setAttr ".los" -type "double3" 0 0 0.13258496410898474 ;
createNode transform -n "finger_pinky_c_L_geo_copy" -p "finger_pinky_c_L_ctl";
	rename -uid "EA4D86C3-4C4D-3566-DBF7-75AD48EE1175";
createNode mesh -n "finger_pinky_c_R_geoShape" -p "finger_pinky_c_L_geo_copy";
	rename -uid "F1659918-4AAD-AFBE-8E2B-FD87AA64C055";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  -3.5509274 -6.1547384 0.037046295 
		-3.5316036 -6.1233931 -0.047568262 -3.4655752 -5.9353876 -0.16608424 -3.4462512 -5.9040418 
		-0.2506983 -3.5008085 -6.1978579 -0.44478601 -3.4814844 -6.1665115 -0.52940011 -3.5861607 
		-6.4172087 -0.24165598 -3.5668368 -6.3858628 -0.32627007;
	setAttr -s 8 ".vt[0:7]"  3.44075966 6.044570446 0.22812393 3.64177132 6.013225079 0.31273809
		 3.35540748 6.045555592 0.43125391 3.5564189 6.014209747 0.51586807 3.39064074 6.30802536 0.44478616
		 3.59165215 6.27667952 0.52940035 3.47599292 6.30704069 0.2416562 3.67700458 6.27569485 0.32627037;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode mesh -n "polySurfaceShape6" -p "finger_pinky_c_L_geo_copy";
	rename -uid "296760C5-4067-7161-DEF8-1D8B46F22A01";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  0.3898322 0.3898322 0.056899615 
		-0.3898322 0.3898322 0.056899615 0.3898322 -0.3898322 0.056899615 -0.3898322 -0.3898322 
		0.056899615 0.3898322 -0.3898322 0.50000024 -0.3898322 -0.3898322 0.50000024 0.3898322 
		0.3898322 0.50000024 -0.3898322 0.3898322 0.50000024;
	setAttr -s 8 ".vt[0:7]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 0.5 0.5 0.5
		 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 -0.5 -0.5 0.5 -0.5 -0.5;
	setAttr -s 12 ".ed[0:11]"  0 1 0 2 3 0 4 5 0 6 7 0 0 2 0 1 3 0 2 4 0
		 3 5 0 4 6 0 5 7 0 6 0 0 7 1 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_pinky_c_R_grp" -p "skin_proxy_dgc";
	rename -uid "8C3EF9F6-4961-DAF7-7546-0FA5B1ACA08E";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -3.5338226809166877 6.2918603688251586 0.38552828190372868 ;
	setAttr ".r" -type "double3" 67.385739968842131 2.925220552982994 -82.354470467488255 ;
	setAttr -k on ".qsm_distance" 0.26516992821796836;
createNode transform -n "finger_pinky_c_R_ctl" -p "finger_pinky_c_R_grp";
	rename -uid "91422E49-4291-2253-F802-A49D38DE411D";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_pinky_c_R_ctl_x_Shape" -p "finger_pinky_c_R_ctl";
	rename -uid "2EC0381D-4158-1A04-E075-9CB837B02F55";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_pinky_c_R_ctl_y_Shape" -p "finger_pinky_c_R_ctl";
	rename -uid "DF443DF5-47D5-A735-B660-97BE2E85A9F9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_pinky_c_R_ctl_z_Shape" -p "finger_pinky_c_R_ctl";
	rename -uid "D42F9B5E-4F0E-D944-D565-AEA30BD2AA40";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.13258496410898418 ;
	setAttr ".los" -type "double3" 0 0 0.13258496410898418 ;
createNode transform -n "finger_pinky_c_R_geo_copy" -p "finger_pinky_c_R_ctl";
	rename -uid "D9A16EC2-4303-EFAD-8A3C-5FBF9C95D6AC";
createNode mesh -n "finger_pinky_c_R_geo_copyShape" -p "finger_pinky_c_R_geo_copy";
	rename -uid "1371CF11-42A7-2B1A-AA27-DE9568EAD856";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  0.11016774 -0.11016798 0.26517028 -0.11016774 -0.11016798 0.26516989
		 0.11016774 0.11016798 0.26516974 -0.11016774 0.11016798 0.26516983 0.11016774 0.11016798 1.7881393e-07
		 -0.11016774 0.11016798 2.9802322e-07 0.11016798 -0.11016798 2.682209e-07 -0.11016774 -0.11016798 3.5762787e-07;
	setAttr -s 12 ".ed[0:11]"  0 1 1 2 3 1 4 5 1 6 7 1 0 2 1 1 3 1 2 4 1
		 3 5 1 4 6 1 5 7 1 6 0 1 7 1 1;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 4 1 -6 -1
		mu 0 4 0 2 3 1
		f 4 6 2 -8 -2
		mu 0 4 2 4 5 3
		f 4 8 3 -10 -3
		mu 0 4 4 6 7 5
		f 4 10 0 -12 -4
		mu 0 4 6 8 9 7
		f 4 5 7 9 11
		mu 0 4 1 3 11 10
		f 4 -9 -7 -5 -11
		mu 0 4 12 13 2 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode mesh -n "polySurfaceShape6" -p "finger_pinky_c_R_geo_copy";
	rename -uid "831CB0A6-43F5-ED17-621D-3B8EC50C8842";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt[0:7]" -type "float3"  0.3898322 0.3898322 0.056899615 
		-0.3898322 0.3898322 0.056899615 0.3898322 -0.3898322 0.056899615 -0.3898322 -0.3898322 
		0.056899615 0.3898322 -0.3898322 0.50000024 -0.3898322 -0.3898322 0.50000024 0.3898322 
		0.3898322 0.50000024 -0.3898322 0.3898322 0.50000024;
	setAttr -s 8 ".vt[0:7]"  -0.5 -0.5 0.5 0.5 -0.5 0.5 -0.5 0.5 0.5 0.5 0.5 0.5
		 -0.5 0.5 -0.5 0.5 0.5 -0.5 -0.5 -0.5 -0.5 0.5 -0.5 -0.5;
	setAttr -s 12 ".ed[0:11]"  0 1 0 2 3 0 4 5 0 6 7 0 0 2 0 1 3 0 2 4 0
		 3 5 0 4 6 0 5 7 0 6 0 0 7 1 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "finger_end_thumb_L_grp" -p "skin_proxy_dgc";
	rename -uid "B9326A9E-4A0A-9FA6-A3D2-A2A8840C2FEE";
	setAttr ".t" -type "double3" 2.4936562851337305 6.9985956533584854 1.2648771406602566 ;
	setAttr ".r" -type "double3" 176.78397422094588 17.794769039860753 42.755774972988732 ;
createNode transform -n "finger_end_thumb_L_ctl" -p "finger_end_thumb_L_grp";
	rename -uid "CA2EBA79-4AAE-F4C8-5BDB-209E4DD3F23B";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 0 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_thumb_L_ctl_x_Shape" -p "finger_end_thumb_L_ctl";
	rename -uid "7A9CB39A-494B-4D73-C247-C188E89FC502";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_thumb_L_ctl_y_Shape" -p "finger_end_thumb_L_ctl";
	rename -uid "670FD97F-44D4-0C0A-81AD-52BD853F0D3A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_thumb_L_ctl_z_Shape" -p "finger_end_thumb_L_ctl";
	rename -uid "01CDA2E5-4BCE-A5B6-7414-7FAF26BA6AD9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "finger_end_thumb_R_grp" -p "skin_proxy_dgc";
	rename -uid "B7A693FE-4DEB-46E7-CBCD-46A70F1C68A2";
	setAttr ".t" -type "double3" -2.4936563705401573 6.998595680987405 1.2648771379316104 ;
	setAttr ".r" -type "double3" -3.2160257597732667 -17.794769023056428 -42.755775758225063 ;
createNode transform -n "finger_end_thumb_R_ctl" -p "finger_end_thumb_R_grp";
	rename -uid "E216447E-4C55-6FC7-5495-FF87CF4316C2";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 0 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_thumb_R_ctl_x_Shape" -p "finger_end_thumb_R_ctl";
	rename -uid "99F3AE41-41F4-7E99-1AF9-CCB90FF8A737";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_thumb_R_ctl_y_Shape" -p "finger_end_thumb_R_ctl";
	rename -uid "8588436D-4854-4D31-0605-73B5F6BCF05E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_thumb_R_ctl_z_Shape" -p "finger_end_thumb_R_ctl";
	rename -uid "9FF0ADA9-4395-9880-8F2A-05BFA091E8D9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "finger_end_index_L_grp" -p "skin_proxy_dgc";
	rename -uid "64AB2243-43C4-5B56-3B31-55AA4F3EB97C";
	setAttr ".t" -type "double3" 2.8454492599299659 5.9752571409723618 1.1877838277357597 ;
	setAttr ".r" -type "double3" -136.39126191073444 7.7986341636662333 71.768895202380605 ;
createNode transform -n "finger_end_index_L_ctl" -p "finger_end_index_L_grp";
	rename -uid "B4EFCE72-46D2-FD4D-3D16-C1A3B18C2560";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_index_L_ctl_x_Shape" -p "finger_end_index_L_ctl";
	rename -uid "9198FF74-4967-25A4-58B7-02AF14D8C7B4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_index_L_ctl_y_Shape" -p "finger_end_index_L_ctl";
	rename -uid "30D9BF1E-4F12-80B8-1C98-638FA39EC725";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_index_L_ctl_z_Shape" -p "finger_end_index_L_ctl";
	rename -uid "7EA77C7F-43EE-876C-DC2C-AA994AD31296";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "finger_end_index_R_grp" -p "skin_proxy_dgc";
	rename -uid "E70D810E-40C7-4A7B-84D3-E0AE26B1F2F1";
	setAttr ".t" -type "double3" -2.8454493592557975 5.9752571734198359 1.1877838245626333 ;
	setAttr ".r" -type "double3" 43.608738097243759 -7.7986341400666577 -71.768895982807024 ;
createNode transform -n "finger_end_index_R_ctl" -p "finger_end_index_R_grp";
	rename -uid "7D73CBE3-4F91-61D2-F699-1C944B046CC2";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_index_R_ctl_x_Shape" -p "finger_end_index_R_ctl";
	rename -uid "BE7980C5-4E9C-0940-EE0F-05B923A95C9C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_index_R_ctl_y_Shape" -p "finger_end_index_R_ctl";
	rename -uid "62CFEA6A-4DAF-D88F-9BCD-0FBB225414A0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_index_R_ctl_z_Shape" -p "finger_end_index_R_ctl";
	rename -uid "371736ED-4775-23AE-2E4A-8CA0B9DAE7B9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "finger_end_middle_L_grp" -p "skin_proxy_dgc";
	rename -uid "398C4CB4-4770-4F13-28B0-929FFE156BE2";
	setAttr ".t" -type "double3" 3.0729040906752534 5.8356353670168248 0.94656595208363925 ;
	setAttr ".r" -type "double3" -132.75036498278317 1.7438596501755876 71.552642804428174 ;
createNode transform -n "finger_end_middle_L_ctl" -p "finger_end_middle_L_grp";
	rename -uid "94183E8C-446E-56A9-9F00-D881B80AB464";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_middle_L_ctl_x_Shape" -p "finger_end_middle_L_ctl";
	rename -uid "C42E6B42-4E46-4E12-D818-D4B4E30590C8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_middle_L_ctl_y_Shape" -p "finger_end_middle_L_ctl";
	rename -uid "27095315-4FFA-0B20-7BA3-4786716607F2";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_middle_L_ctl_z_Shape" -p "finger_end_middle_L_ctl";
	rename -uid "F45FFB23-47AF-3AF2-4A0D-9E9B64595985";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "finger_end_middle_R_grp" -p "skin_proxy_dgc";
	rename -uid "DB7DF8CE-4ECA-BDE2-5A3D-FB8D5C09529C";
	setAttr ".t" -type "double3" -3.0729041918997151 5.835635402662767 0.94656594884947975 ;
	setAttr ".r" -type "double3" 47.249635025213969 -1.7438596266060133 -71.552643584015385 ;
createNode transform -n "finger_end_middle_R_ctl" -p "finger_end_middle_R_grp";
	rename -uid "F38338CB-4CF3-307F-A229-03A588E6107F";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_middle_R_ctl_x_Shape" -p "finger_end_middle_R_ctl";
	rename -uid "181DC12E-4288-C5AE-7554-A089D3AF78C1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_middle_R_ctl_y_Shape" -p "finger_end_middle_R_ctl";
	rename -uid "21346368-4A1D-B09F-A581-8E84307C02E7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_middle_R_ctl_z_Shape" -p "finger_end_middle_R_ctl";
	rename -uid "B1B2F8CA-4D51-F923-73CE-ABB5CE242856";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "finger_end_ring_L_grp" -p "skin_proxy_dgc";
	rename -uid "16698BE1-4154-04BD-F3C4-FCBE41AACD11";
	setAttr ".t" -type "double3" 3.2697572576576115 5.8107260512438375 0.65225963954025901 ;
	setAttr ".r" -type "double3" -116.74279523359864 -0.45112495028734501 76.138766984922214 ;
createNode transform -n "finger_end_ring_L_ctl" -p "finger_end_ring_L_grp";
	rename -uid "9402639A-41C4-0FC5-3F52-DE8D7982F3C2";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_ring_L_ctl_x_Shape" -p "finger_end_ring_L_ctl";
	rename -uid "3F6A256A-4CD0-A025-FF1E-02B19EF14EEA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_ring_L_ctl_y_Shape" -p "finger_end_ring_L_ctl";
	rename -uid "00B27922-4182-A869-D86A-6295E87E3BE4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_ring_L_ctl_z_Shape" -p "finger_end_ring_L_ctl";
	rename -uid "9064468E-479D-8541-038B-4B9A1ADFD044";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "finger_end_ring_R_grp" -p "skin_proxy_dgc";
	rename -uid "56522C30-4D0B-9578-6795-719135D605E7";
	setAttr ".t" -type "double3" -3.2697573592202445 5.8107260896949944 0.65225963629486716 ;
	setAttr ".r" -type "double3" 63.257204772484812 0.45112497442057392 -76.138767764218144 ;
createNode transform -n "finger_end_ring_R_ctl" -p "finger_end_ring_R_grp";
	rename -uid "2EAA6F7F-4FBC-1E08-39E0-A9A446D325A9";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_ring_R_ctl_x_Shape" -p "finger_end_ring_R_ctl";
	rename -uid "8C2BA562-46CE-9753-2DEE-09B28BA7EBD7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_ring_R_ctl_y_Shape" -p "finger_end_ring_R_ctl";
	rename -uid "DC3ED6A1-4ADC-169D-19B5-C2A8C3005E03";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_ring_R_ctl_z_Shape" -p "finger_end_ring_R_ctl";
	rename -uid "C7FEE1E4-4695-EEFE-3197-1383EC48B7A1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "finger_end_pinky_L_grp" -p "skin_proxy_dgc";
	rename -uid "45D9EDA8-427C-09F2-2D91-E3A46D5A09E6";
	setAttr ".t" -type "double3" 3.4985892814592954 6.0293901721896956 0.37199598660340039 ;
	setAttr ".r" -type "double3" -112.61426003459688 -2.9252205283329933 82.354469688319924 ;
createNode transform -n "finger_end_pinky_L_ctl" -p "finger_end_pinky_L_grp";
	rename -uid "EB0DFB79-4824-AC42-87C6-B085F892EDB4";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_pinky_L_ctl_x_Shape" -p "finger_end_pinky_L_ctl";
	rename -uid "F4C8A3F5-48F7-7C89-BE1B-C693363F8407";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_pinky_L_ctl_y_Shape" -p "finger_end_pinky_L_ctl";
	rename -uid "041F6B87-4B45-A281-328B-94BB4A6A8A43";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_pinky_L_ctl_z_Shape" -p "finger_end_pinky_L_ctl";
	rename -uid "2C95A000-45AF-D54A-15E4-B59623B85E49";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "finger_end_pinky_R_grp" -p "skin_proxy_dgc";
	rename -uid "330A2706-493D-BF83-9D22-2E8B9F3F6C12";
	setAttr ".t" -type "double3" -3.4985893800470325 6.0293902138749758 0.37199598345232682 ;
	setAttr ".r" -type "double3" 67.385739968842145 2.9252205529830069 -82.354470467488241 ;
createNode transform -n "finger_end_pinky_R_ctl" -p "finger_end_pinky_R_grp";
	rename -uid "4D662903-4E51-E0FD-A4FB-7DAC67CB2591";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "finger_end_pinky_R_ctl_x_Shape" -p "finger_end_pinky_R_ctl";
	rename -uid "1903F475-4152-2C81-08D5-3DA7B1D0A2DD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "finger_end_pinky_R_ctl_y_Shape" -p "finger_end_pinky_R_ctl";
	rename -uid "7B136F37-451C-541D-3A95-F2871B22895E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "finger_end_pinky_R_ctl_z_Shape" -p "finger_end_pinky_R_ctl";
	rename -uid "AC78EFF3-4699-F4B5-58D9-7784AAB871A5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "hip_L_grp" -p "skin_proxy_dgc";
	rename -uid "3E44AA19-4D38-1A7F-F904-279FC9A413EA";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 0.6260950106885671 8.4758472432758332 -0.23069922884796745 ;
	setAttr ".r" -type "double3" -89.753305444342942 3.6612312179360145 99.213713385257009 ;
	setAttr -k on ".qsm_distance" 3.7212052345275879;
createNode transform -n "hip_L_ctl" -p "hip_L_grp";
	rename -uid "0D9C8136-40C6-47C7-2DE2-3D907CA74B1C";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "hip_L_ctl_x_Shape" -p "hip_L_ctl";
	rename -uid "41879AD5-4B51-D44B-1916-768419CC38F5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "hip_L_ctl_y_Shape" -p "hip_L_ctl";
	rename -uid "0DA9FFCF-43BA-5972-497F-4FA3FB35AA50";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "hip_L_ctl_z_Shape" -p "hip_L_ctl";
	rename -uid "7D574796-47BE-2939-569A-338ECAB793AE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 1.8606026172637939 ;
	setAttr ".los" -type "double3" 0 0 1.8606026172637939 ;
createNode transform -n "hip_L_geo_copy" -p "hip_L_ctl";
	rename -uid "2D67C285-4533-994A-323F-87AD3E96E6FC";
createNode mesh -n "hip_R_geoShape" -p "hip_L_geo_copy";
	rename -uid "9F10C987-49A5-8DC9-7ACE-FBB597DB8C1F";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.375 0.75 0.25 0.25 0.25 0.375 0.375 0.25 0
		 0.375 0.875 0.625 0.875 0.75 0 0.5 0.375 0.5 0.25 0.5 0 0.5 1 0.5 0.875 0.5 0.75
		 0.5 0.5 0.75 0.125 0.625 0.125 0.5 0.125 0.375 0.125 0.25 0.125 0.125 0.125 0.375
		 0.625 0.5 0.625 0.625 0.625 0.875 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -1.2243361 -5.1414857 4.0855341 
		-1.2152374 -5.2545166 4.0885725 -1.2444309 -4.2688122 3.4622865 -1.2353321 -4.3818431 
		3.4653246 -0.6876744 -6.966548 -0.52641034 -0.55412668 -7.8533468 -1.2459712 -0.69744146 
		-8.4971867 1.1050491 -0.56389385 -9.3839846 0.38548869 -0.95300341 -5.5776892 1.2723091 
		-0.96931887 -5.3750072 1.2668605 -0.90589648 -7.2153277 2.329494 -0.88958091 -7.4180102 
		2.3349421 -0.9603318 -5.4866505 1.2698615 -1.2426358 -4.2057128 3.3783798 -1.2170324 
		-5.317616 4.1724792 -0.88926613 -7.5487556 2.460557 -0.63748336 -8.9832745 0.8690213 
		-0.62663043 -7.2824812 -0.9438023 -0.91852212 -6.5322609 1.8045504 -1.2240376 -4.8336725 
		3.7773652 -1.2298341 -4.7616644 3.7754295 -1.2356306 -4.6896563 3.7734938 -0.93871909 
		-6.2813606 1.7978063 -0.69255799 -7.7318668 0.28931969 -0.63206142 -8.1335831 -0.036638469 
		-0.54726428 -8.6966629 -0.4935292;
	setAttr -s 26 ".vt[0:25]"  0.96727318 4.75674343 -0.37671399 1.66530395 4.86977434 -0.37975243
		 0.98736793 4.65355444 0.401061 1.68539882 4.76658535 0.39802259 0.3725186 8.10135937 0.9288376
		 1.027577877 8.98815823 0.87613457 0.38228571 7.99718618 -0.70262218 1.037344933 8.88398457 -0.75532514
		 1.75390863 6.55117702 0.87443632 0.50222814 6.34849501 0.87988466 0.43880576 6.6994338 -0.63534534
		 1.69048619 6.9021163 -0.64079368 1.19168997 6.46013832 0.87688357 1.33913767 4.69592571 0.50614858
		 1.31353426 4.82740307 -0.48483998 1.1206243 6.85337019 -0.82095259 0.67956328 8.39315987 -0.81642646
		 0.66871035 8.50891399 0.99639708 1.93470526 6.76105785 0.1158963 1.7710278 4.83367252 0.0087186247
		 1.32633591 4.76166439 0.0106543 0.88164395 4.68965626 0.012589976 0.38525257 6.51015759 0.1226408
		 0.37740216 8.049272537 0.11310767 0.67414129 8.45098877 0.089233443 1.090076566 9.014068604 0.05576925;
	setAttr -s 48 ".ed[0:47]"  0 14 1 2 13 1 4 17 1 6 16 1 0 21 1 1 19 1
		 2 9 1 3 8 1 4 23 1 5 25 1 6 10 1 7 11 1 8 5 1 9 4 1 8 12 1 10 0 1 9 22 1 11 1 1 10 15 1
		 11 18 1 12 9 1 13 3 1 12 13 1 14 1 1 13 20 1 15 11 1 14 15 1 16 7 1 15 16 1 17 5 1
		 16 24 1 17 12 1 18 8 1 19 3 1 18 19 1 20 14 1 19 20 1 21 2 1 20 21 1 22 10 1 21 22 1
		 23 6 1 22 23 1 24 17 1 23 24 1 25 7 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 23 5 36 35
		mu 0 4 24 1 30 31
		f 4 21 7 14 22
		mu 0 4 23 3 14 22
		f 4 46 45 -28 30
		mu 0 4 36 37 7 27
		f 4 25 17 -24 26
		mu 0 4 26 20 9 25
		f 4 -18 19 34 -6
		mu 0 4 1 21 29 30
		f 4 15 4 40 39
		mu 0 4 18 0 32 33
		f 4 31 -15 12 -30
		mu 0 4 28 22 14 5
		f 4 10 -40 42 41
		mu 0 4 12 18 33 34
		f 4 27 11 -26 28
		mu 0 4 27 7 20 26
		f 4 47 -20 -12 -46
		mu 0 4 38 29 21 10
		f 4 1 -23 20 -7
		mu 0 4 2 23 22 17
		f 4 0 -36 38 -5
		mu 0 4 0 24 31 32
		f 4 18 -27 -1 -16
		mu 0 4 19 26 25 8
		f 4 3 -29 -19 -11
		mu 0 4 6 27 26 19
		f 4 44 -31 -4 -42
		mu 0 4 35 36 27 6
		f 4 -21 -32 -3 -14
		mu 0 4 17 22 28 4
		f 4 -35 32 -8 -34
		mu 0 4 30 29 15 3
		f 4 -37 33 -22 24
		mu 0 4 31 30 3 23
		f 4 -39 -25 -2 -38
		mu 0 4 32 31 23 2
		f 4 -41 37 6 16
		mu 0 4 33 32 2 16
		f 4 -43 -17 13 8
		mu 0 4 34 33 16 13
		f 4 2 -44 -45 -9
		mu 0 4 4 28 36 35
		f 4 29 9 -47 43
		mu 0 4 28 5 37 36
		f 4 -33 -48 -10 -13
		mu 0 4 15 29 38 11;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "hip_R_grp" -p "skin_proxy_dgc";
	rename -uid "659D337D-4EE1-4DC4-0ED0-53855EC948FA";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -0.62609501068856654 8.4758472432758403 -0.23069922884796668 ;
	setAttr ".r" -type "double3" 90.246694545150859 -3.6612312703786052 -99.213713090997402 ;
	setAttr -k on ".qsm_distance" 3.7212052345275901;
createNode transform -n "hip_R_ctl" -p "hip_R_grp";
	rename -uid "B2A31254-4F94-4F65-1069-26B867F156BC";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "hip_R_ctl_x_Shape" -p "hip_R_ctl";
	rename -uid "C40D1F0A-4F86-D9C0-1E70-BFBCA396B487";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "hip_R_ctl_y_Shape" -p "hip_R_ctl";
	rename -uid "0B51FE09-4FCB-D5AF-2267-73904DD39FFF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "hip_R_ctl_z_Shape" -p "hip_R_ctl";
	rename -uid "0E62B77C-4229-D810-C7C6-1CB66DA2D386";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 1.8606026172637951 ;
	setAttr ".los" -type "double3" 0 0 1.8606026172637951 ;
createNode transform -n "hip_R_geo_copy" -p "hip_R_ctl";
	rename -uid "C7ED5EDE-48D9-9EB4-32F3-3994BA179B86";
createNode mesh -n "hip_R_geo_copyShape" -p "hip_R_geo_copy";
	rename -uid "9C012B63-4554-9E3F-5C86-4FAB5EDD0862";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.375 0.75 0.25 0.25 0.25 0.375 0.375 0.25 0
		 0.375 0.875 0.625 0.875 0.75 0 0.5 0.375 0.5 0.25 0.5 0 0.5 1 0.5 0.875 0.5 0.75
		 0.5 0.5 0.75 0.125 0.625 0.125 0.5 0.125 0.375 0.125 0.25 0.125 0.125 0.125 0.375
		 0.625 0.5 0.625 0.625 0.625 0.875 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".vt[0:25]"  0.25706297 -0.38474226 3.7088201 -0.45006657 -0.38474226 3.7088201
		 0.25706291 0.38474226 3.86334753 -0.4500668 0.38474226 3.86334729 0.3151558 1.1348114 0.40242726
		 -0.47345114 1.1348114 -0.36983663 0.31515574 -0.50000048 0.40242696 -0.47345102 -0.5 -0.36983645
		 -0.80090523 0.97348785 2.14674544 0.46709073 0.97348785 2.1467452 0.4670907 -0.51589394 1.69414866
		 -0.80090523 -0.51589394 1.69414842 -0.23135817 0.97348785 2.14674497 -0.096501827 0.49021292 3.8845284
		 -0.096501946 -0.49021292 3.68763924 -0.23135817 -0.69538546 1.63960433 -0.042079926 -0.59011459 0.052594841
		 -0.042079926 1.2264328 0.052594781 -1.016183138 0.22879696 1.92044675 -0.54699016 0 3.78608394
		 -0.096501827 0 3.7860837 0.35398668 0 3.7860837 0.55346656 0.22879696 1.92044711
		 0.3151558 0.3174057 0.40242738 -0.042079866 0.3174057 0.052594975 -0.54281223 0.3174057 -0.43775994;
	setAttr -s 48 ".ed[0:47]"  0 14 1 2 13 1 4 17 1 6 16 1 0 21 1 1 19 1
		 2 9 1 3 8 1 4 23 1 5 25 1 6 10 1 7 11 1 8 5 1 9 4 1 8 12 1 10 0 1 9 22 1 11 1 1 10 15 1
		 11 18 1 12 9 1 13 3 1 12 13 1 14 1 1 13 20 1 15 11 1 14 15 1 16 7 1 15 16 1 17 5 1
		 16 24 1 17 12 1 18 8 1 19 3 1 18 19 1 20 14 1 19 20 1 21 2 1 20 21 1 22 10 1 21 22 1
		 23 6 1 22 23 1 24 17 1 23 24 1 25 7 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 -36 -37 -6 -24
		mu 0 4 24 31 30 1
		f 4 -23 -15 -8 -22
		mu 0 4 23 22 14 3
		f 4 -31 27 -46 -47
		mu 0 4 36 27 7 37
		f 4 -27 23 -18 -26
		mu 0 4 26 25 9 20
		f 4 5 -35 -20 17
		mu 0 4 1 30 29 21
		f 4 -40 -41 -5 -16
		mu 0 4 18 33 32 0
		f 4 29 -13 14 -32
		mu 0 4 28 5 14 22
		f 4 -42 -43 39 -11
		mu 0 4 12 34 33 18
		f 4 -29 25 -12 -28
		mu 0 4 27 26 20 7
		f 4 45 11 19 -48
		mu 0 4 38 10 21 29
		f 4 6 -21 22 -2
		mu 0 4 2 17 22 23
		f 4 4 -39 35 -1
		mu 0 4 0 32 31 24
		f 4 15 0 26 -19
		mu 0 4 19 8 25 26
		f 4 10 18 28 -4
		mu 0 4 6 19 26 27
		f 4 41 3 30 -45
		mu 0 4 35 6 27 36
		f 4 13 2 31 20
		mu 0 4 17 4 28 22
		f 4 33 7 -33 34
		mu 0 4 30 3 15 29
		f 4 -25 21 -34 36
		mu 0 4 31 23 3 30
		f 4 37 1 24 38
		mu 0 4 32 2 23 31
		f 4 -17 -7 -38 40
		mu 0 4 33 16 2 32
		f 4 -9 -14 16 42
		mu 0 4 34 13 16 33
		f 4 8 44 43 -3
		mu 0 4 4 35 36 28
		f 4 -44 46 -10 -30
		mu 0 4 28 36 37 5
		f 4 12 9 47 32
		mu 0 4 15 11 38 29;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "knee_L_grp" -p "skin_proxy_dgc";
	rename -uid "63C4476F-4D56-3810-CB6F-96AD43DE8EF7";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 1.2207088403160751 4.8101498961807643 0.0069260025383537094 ;
	setAttr ".r" -type "double3" -89.752121882237475 -6.6884958632023457 99.169089229530897 ;
	setAttr -k on ".qsm_distance" 3.9919075965881325;
createNode transform -n "knee_L_ctl" -p "knee_L_grp";
	rename -uid "F51C7B6F-441E-CF32-4014-808DAF2BCA72";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 90 -90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "knee_L_ctl_x_Shape" -p "knee_L_ctl";
	rename -uid "A315D3B6-48EB-8FC4-FF5A-27BF50718752";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "knee_L_ctl_y_Shape" -p "knee_L_ctl";
	rename -uid "D23405C4-4DFC-E6A2-BACD-4EA539460D64";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "knee_L_ctl_z_Shape" -p "knee_L_ctl";
	rename -uid "76E369DA-44B6-278B-303A-BCB061552D7A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 1.9959537982940663 ;
	setAttr ".los" -type "double3" 0 0 1.9959537982940663 ;
createNode transform -n "knee_L_geo_copy" -p "knee_L_ctl";
	rename -uid "10C79436-4527-63A7-69DD-439315AB0C40";
createNode mesh -n "knee_R_geoShape" -p "knee_L_geo_copy";
	rename -uid "5363E516-4AC4-D188-80CF-11A8FE3FC66C";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.25 0 0.375 0.875 0.25 0.25 0.375 0.375 0.625 0.375
		 0.75 0.25 0.625 0.875 0.75 0 0.5 0.5 0.5 0.75 0.5 0.875 0.5 0 0.5 1 0.5 0.25 0.5
		 0.375 0.625 0.625 0.875 0.125 0.5 0.625 0.125 0.125 0.375 0.625 0.25 0.125 0.375
		 0.125 0.5 0.125 0.625 0.125 0.75 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -1.8595827 -1.0873275 4.7790904 
		-1.8617457 -1.0942067 4.8184109 -1.8357246 -0.74520612 4.0295053 -1.8378878 -0.75208515 
		4.0688262 -1.2510048 -4.2674298 -0.21442451 -1.242112 -4.377902 -0.21145511 -1.2352263 
		-5.0375409 0.47198659 -1.2263335 -5.1480131 0.47495598 -1.4140997 -4.4026947 2.2954402 
		-1.4399906 -3.1390183 1.1691073 -1.4261831 -3.3105447 1.1737182 -1.4002922 -4.5742211 
		2.300051 -1.2488236 -4.2121081 -0.3114818 -1.2285147 -5.2033353 0.57201332 -1.4030781 
		-4.689435 2.4768794 -1.8661031 -1.1687614 4.9696345 -1.8313673 -0.67065179 3.8782814 
		-1.4372047 -3.0238044 0.99227887 -1.232946 -4.7788172 0.13217667 -1.2386692 -4.7077217 
		0.1302655 -1.2443922 -4.6366262 0.12835436 -1.4292412 -3.7435768 1.7315404 -1.8471605 
		-0.91469914 4.3953333 -1.8487351 -0.91970682 4.4239578 -1.8503098 -0.92471451 4.4525824 
		-1.4110416 -3.9696629 1.7376179;
	setAttr -s 26 ".vt[0:25]"  1.59083092 0.82339501 -0.72610903 2.14066291 0.85453629 -0.7107358
		 1.56697297 0.98487663 -0.19991909 2.11680484 1.016017675 -0.18454596 1.0028909445 4.61192751 0.33598369
		 1.68511939 4.72239971 0.33301407 0.9871124 4.69091749 -0.35042733 1.66934085 4.80138969 -0.35339695
		 1.020968318 3.55757833 -0.98354036 1.046859264 3.4279635 0.1427924 2.10613441 3.59948993 0.13818154
		 2.080243349 3.72910476 -0.98815113 1.34627032 4.65582371 0.43304086 1.32596147 4.7574935 -0.45045415
		 1.54648805 3.66395569 -1.16497946 1.87118578 0.80215263 -0.83837891 1.83644998 1.037260532 -0.072276086
		 1.58061457 3.49311256 0.31962085 1.77517176 4.77775431 -0.010617761 1.33611596 4.70665884 -0.0087066218
		 0.89706016 4.63556337 -0.0067954822 0.8654449 3.46549106 -0.4196406 1.45355582 0.89703703 -0.4665187
		 1.85381794 0.91970682 -0.45532745 2.2540803 0.94237661 -0.44413623 2.26165771 3.6915772 -0.4257181;
	setAttr -s 48 ".ed[0:47]"  0 15 1 2 16 1 4 12 1 6 13 1 0 22 1 1 24 1
		 2 9 1 3 10 1 4 20 1 5 18 1 6 8 1 7 11 1 8 0 1 9 4 1 8 21 1 10 5 1 9 17 1 11 1 1 10 25 1
		 11 14 1 12 5 1 13 7 1 12 19 1 14 8 1 13 14 1 15 1 1 14 15 1 16 3 1 15 23 1 17 10 1
		 16 17 1 17 12 1 18 7 1 19 13 1 18 19 1 20 6 1 19 20 1 21 9 1 20 21 1 22 2 1 21 22 1
		 23 16 1 22 23 1 24 3 1 23 24 1 25 11 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 42 41 -2 -40
		mu 0 4 35 36 27 2
		f 4 16 31 -3 -14
		mu 0 4 17 28 22 4
		f 4 2 22 36 -9
		mu 0 4 4 22 31 33
		f 4 3 24 23 -11
		mu 0 4 6 23 24 15
		f 4 47 -10 -16 18
		mu 0 4 38 30 11 19
		f 4 38 37 13 8
		mu 0 4 32 34 16 13
		f 4 40 39 6 -38
		mu 0 4 34 35 2 16
		f 4 1 30 -17 -7
		mu 0 4 2 27 28 17
		f 4 46 -19 -8 -44
		mu 0 4 37 38 19 3
		f 4 -24 26 -1 -13
		mu 0 4 15 24 26 8
		f 4 20 9 34 -23
		mu 0 4 22 5 29 31
		f 4 -25 21 11 19
		mu 0 4 24 23 7 20
		f 4 -27 -20 17 -26
		mu 0 4 26 24 20 9
		f 4 -42 44 43 -28
		mu 0 4 27 36 37 3
		f 4 -31 27 7 -30
		mu 0 4 28 27 3 18
		f 4 -32 29 15 -21
		mu 0 4 22 28 18 5
		f 4 -35 32 -22 -34
		mu 0 4 31 29 7 23
		f 4 -37 33 -4 -36
		mu 0 4 33 31 23 6
		f 4 10 14 -39 35
		mu 0 4 12 14 34 32
		f 4 12 4 -41 -15
		mu 0 4 14 0 35 34
		f 4 0 28 -43 -5
		mu 0 4 0 25 36 35
		f 4 -45 -29 25 5
		mu 0 4 37 36 25 1
		f 4 -18 -46 -47 -6
		mu 0 4 1 21 38 37
		f 4 -12 -33 -48 45
		mu 0 4 21 10 30 38;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "knee_R_grp" -p "skin_proxy_dgc";
	rename -uid "0AC4CDDF-4B6C-86ED-BFA8-BB98BCA50973";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -1.2207088214648953 4.8101498932357423 0.0069260042788880372 ;
	setAttr ".r" -type "double3" 90.247878107164794 6.6884958107675487 -99.169088937176497 ;
	setAttr -k on ".qsm_distance" 3.9919075965881361;
createNode transform -n "knee_R_ctl" -p "knee_R_grp";
	rename -uid "C2BE6A1A-4E4B-03F6-FE19-C1BD4A7D9423";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "knee_R_ctl_x_Shape" -p "knee_R_ctl";
	rename -uid "0946BD27-4DCF-6555-F537-BB9C45882B62";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "knee_R_ctl_y_Shape" -p "knee_R_ctl";
	rename -uid "D39F5C20-4C2A-2BFC-B9D2-098A69AB17F4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "knee_R_ctl_z_Shape" -p "knee_R_ctl";
	rename -uid "2C639FFA-4CBD-4E0D-EC9D-BC874C40AD01";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 1.995953798294068 ;
	setAttr ".los" -type "double3" 0 0 1.995953798294068 ;
createNode transform -n "knee_R_geo_copy" -p "knee_R_ctl";
	rename -uid "131AE62B-4A06-61F7-FEDC-7E9A9C5DAA0F";
createNode mesh -n "knee_R_geo_copyShape" -p "knee_R_geo_copy";
	rename -uid "E87EAD18-4B96-76A1-1D11-D288DC22AEA6";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.25 0 0.375 0.875 0.25 0.25 0.375 0.375 0.625 0.375
		 0.75 0.25 0.625 0.875 0.75 0 0.5 0.5 0.5 0.75 0.5 0.875 0.5 0 0.5 1 0.5 0.25 0.5
		 0.375 0.625 0.625 0.875 0.125 0.5 0.625 0.125 0.125 0.375 0.625 0.25 0.125 0.375
		 0.125 0.5 0.125 0.625 0.125 0.75 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".vt[0:25]"  0.26875162 -0.26393247 4.052981377 -0.27891731 -0.2396704 4.10767508
		 0.26875162 0.23967052 3.82958627 -0.27891707 0.26393253 3.8842802 0.24811387 0.34449768 0.12155919
		 -0.44300747 0.34449768 0.12155896 0.24811387 -0.34662342 0.12155926 -0.44300747 -0.34662342 0.12155902
		 0.39313132 -0.84511638 1.3118999 0.39313138 0.2889452 1.31189966 -0.67995119 0.2889452 1.31189978
		 -0.67995119 -0.84511638 1.3118999 -0.09744668 0.44371557 0.12155905 -0.097446799 -0.44584179 0.12155917
		 -0.14340997 -1.025479317 1.3118999 -0.0050827265 -0.36660874 4.13125563 -0.0050828457 0.36660874 3.80600524
		 -0.14340997 0.46930814 1.31189966 -0.5422256 -0.00106287 0.12155889 -0.097446918 -0.00106287 0.12155888
		 0.347332 -0.00106287 0.12155887 0.56379616 -0.27808571 1.3118999 0.39360464 -0.017662108 3.92881465
		 -0.0050828457 0 3.96863031 -0.40377045 0.017662108 4.0084462166 -0.85061598 -0.27808571 1.31189978;
	setAttr -s 48 ".ed[0:47]"  0 15 1 2 16 1 4 12 1 6 13 1 0 22 1 1 24 1
		 2 9 1 3 10 1 4 20 1 5 18 1 6 8 1 7 11 1 8 0 1 9 4 1 8 21 1 10 5 1 9 17 1 11 1 1 10 25 1
		 11 14 1 12 5 1 13 7 1 12 19 1 14 8 1 13 14 1 15 1 1 14 15 1 16 3 1 15 23 1 17 10 1
		 16 17 1 17 12 1 18 7 1 19 13 1 18 19 1 20 6 1 19 20 1 21 9 1 20 21 1 22 2 1 21 22 1
		 23 16 1 22 23 1 24 3 1 23 24 1 25 11 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 39 1 -42 -43
		mu 0 4 35 2 27 36
		f 4 13 2 -32 -17
		mu 0 4 17 4 22 28
		f 4 8 -37 -23 -3
		mu 0 4 4 33 31 22
		f 4 10 -24 -25 -4
		mu 0 4 6 15 24 23
		f 4 -19 15 9 -48
		mu 0 4 38 19 11 30
		f 4 -9 -14 -38 -39
		mu 0 4 32 13 16 34
		f 4 37 -7 -40 -41
		mu 0 4 34 16 2 35
		f 4 6 16 -31 -2
		mu 0 4 2 17 28 27
		f 4 43 7 18 -47
		mu 0 4 37 3 19 38
		f 4 12 0 -27 23
		mu 0 4 15 8 26 24
		f 4 22 -35 -10 -21
		mu 0 4 22 31 29 5
		f 4 -20 -12 -22 24
		mu 0 4 24 20 7 23
		f 4 25 -18 19 26
		mu 0 4 26 9 20 24
		f 4 27 -44 -45 41
		mu 0 4 27 3 37 36
		f 4 29 -8 -28 30
		mu 0 4 28 18 3 27
		f 4 20 -16 -30 31
		mu 0 4 22 5 18 28
		f 4 33 21 -33 34
		mu 0 4 31 23 7 29
		f 4 35 3 -34 36
		mu 0 4 33 6 23 31
		f 4 -36 38 -15 -11
		mu 0 4 12 32 34 14
		f 4 14 40 -5 -13
		mu 0 4 14 34 35 0
		f 4 4 42 -29 -1
		mu 0 4 0 35 36 25
		f 4 -6 -26 28 44
		mu 0 4 37 1 25 36
		f 4 5 46 45 17
		mu 0 4 1 37 38 21
		f 4 -46 47 32 11
		mu 0 4 21 38 30 10;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "ankle_L_grp" -p "skin_proxy_dgc";
	rename -uid "B4BF6205-4630-932E-10D3-949A4AEB2F76";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 1.8524844707074828 0.89607094287452016 -0.45801674643906298 ;
	setAttr ".r" -type "double3" -90.688653962556472 -3.4464060899012326e-06 90.000000190951368 ;
	setAttr -k on ".qsm_distance" 1.4730362833935331;
createNode transform -n "ankle_L_ctl" -p "ankle_L_grp";
	rename -uid "7DBB552B-4F82-1C5F-1C79-7C8663127008";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 90 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "ankle_L_ctl_x_Shape" -p "ankle_L_ctl";
	rename -uid "8B354D50-4ADC-A96B-0C20-EBB225D88F49";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "ankle_L_ctl_y_Shape" -p "ankle_L_ctl";
	rename -uid "1884E781-484E-DB59-839C-54AA13B5FAE0";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "ankle_L_ctl_z_Shape" -p "ankle_L_ctl";
	rename -uid "BFD1181A-4445-B8CF-CC94-9CB0CC4CEB40";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.73651814169676655 ;
	setAttr ".los" -type "double3" 0 0 0.73651814169676655 ;
createNode transform -n "ankle_L_geo_copy" -p "ankle_L_ctl";
	rename -uid "1CA529D3-4566-6616-2059-A4B76E039B38";
createNode mesh -n "ankle_R_geoShape" -p "ankle_L_geo_copy";
	rename -uid "3D842F40-44BC-FB2B-7000-189A02B4086E";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.125 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.625 0.875 0.125 0.125 0.125 0.375 0.625 0.375
		 0.125 0.625 0.125 0.5 0.5 0.5 0.625 0.5 0.75 0.5 0 0.5 1 0.5 0.125 0.5 0.25 0.625
		 0.875 0.75 0 0.5 0.875 0.25 0 0.375 0.875 0.25 0.125 0.25 0.25 0.375 0.375 0.5 0.375
		 0.625 0.375 0.75 0.25 0.75 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -1.8364669 -0.89607084 0.46381688 
		-1.836545 -0.89607084 0.45083028 -1.8488547 -0.8960709 0.46222505 -1.8488042 -0.8960709 
		0.45385239 -1.8556125 -0.89607096 0.46218222 -1.8555622 -0.89607096 0.45381397 -1.8567538 
		-0.89607096 0.46313083 -1.8566868 -0.89607096 0.45198184 -1.8566868 -0.89607096 0.45198181 
		-1.8567538 -0.89607096 0.4631308 -1.8367442 -0.89607084 0.46203876 -1.8368069 -0.89607084 
		0.45161694 -1.8583834 -0.89607096 0.45798129 -1.8595189 -0.89607096 0.45797449 -1.8595189 
		-0.89607096 0.45797452 -1.8365012 -0.89607084 0.45811459 -1.8367678 -0.89607084 0.45812362 
		-1.8488294 -0.8960709 0.45803872 -1.8470018 -0.8960709 0.45096633 -1.8470443 -0.8960709 
		0.45804951 -1.8470732 -0.8960709 0.46285498 -1.8483348 -0.8960709 0.46317503 -1.8525071 
		-0.89607096 0.46298784 -1.8524772 -0.89607096 0.45801678 -1.8524451 -0.89607096 0.4526712 
		-1.8486117 -0.8960709 0.45203033;
	setAttr -s 26 ".vt[0:25]"  1.36191726 -0.0013944507 0.87172282 2.44242334 -0.0013944507 0.87172306
		 1.50054431 0.96687061 -0.15812054 2.19711447 0.96687061 -0.14974788 1.50748587 0.81846678 -0.72035193
		 2.20368886 0.81846678 -0.71198368 1.42913973 5.9604645e-08 -0.8157742 2.35668683 5.9604645e-08 -0.80462521
		 2.35668683 0.44043964 -0.80462515 1.42913973 0.44043964 -0.8157742 1.50999069 0.51147401 0.84953976
		 2.37710381 0.51147401 0.84953976 1.85838342 0.79488772 -0.94878531 1.85951889 0.44043964 -1.04325211
		 1.85951889 1.1920929e-07 -1.04325223 1.83635581 -0.0013944507 0.87172282 1.8357358 0.51147401 0.84953976
		 1.84882939 0.96687061 -0.15393421 2.43633199 5.9604645e-08 0.0016646981 1.84704435 5.9604645e-08 -0.0054184496
		 1.44724905 5.9604645e-08 -0.010223925 1.42125094 0.41782349 -0.11534613 1.4389081 0.88087916 -0.46238559
		 1.85247719 0.88087916 -0.45741457 2.29720783 0.88087916 -0.45206895 2.34861183 0.44043958 -0.13281521;
	setAttr -s 48 ".ed[0:47]"  0 15 1 2 17 1 4 12 1 6 14 1 0 10 1 1 11 1
		 2 22 1 3 24 1 4 9 1 5 8 1 6 20 1 7 18 1 8 7 1 9 6 1 8 13 1 10 2 1 9 21 1 11 3 1 10 16 1
		 11 25 1 12 5 1 13 9 1 12 13 1 14 7 1 13 14 1 15 1 1 14 19 1 16 11 1 15 16 1 17 3 1
		 16 17 1 17 23 1 18 1 1 19 15 1 18 19 1 20 0 1 19 20 1 21 10 1 20 21 1 22 4 1 21 22 1
		 23 12 1 22 23 1 24 5 1 23 24 1 25 8 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 18 30 -2 -16
		mu 0 4 18 25 26 2
		f 4 42 41 -3 -40
		mu 0 4 34 35 20 4
		f 4 2 22 21 -9
		mu 0 4 4 20 21 17
		f 4 3 26 36 -11
		mu 0 4 6 22 29 31
		f 4 45 -10 -44 46
		mu 0 4 38 15 11 37
		f 4 16 40 39 8
		mu 0 4 16 32 33 13
		f 4 -22 24 -4 -14
		mu 0 4 17 21 22 6
		f 4 10 38 -17 13
		mu 0 4 12 30 32 16
		f 4 0 28 -19 -5
		mu 0 4 0 23 25 18
		f 4 47 -12 -13 -46
		mu 0 4 38 28 10 15
		f 4 20 9 14 -23
		mu 0 4 20 5 14 21
		f 4 -25 -15 12 -24
		mu 0 4 22 21 14 7
		f 4 -27 23 11 34
		mu 0 4 29 22 7 27
		f 4 -29 25 5 -28
		mu 0 4 25 23 1 19
		f 4 -31 27 17 -30
		mu 0 4 26 25 19 3
		f 4 -42 44 43 -21
		mu 0 4 20 35 36 5
		f 4 -34 -35 32 -26
		mu 0 4 24 29 27 9
		f 4 -37 33 -1 -36
		mu 0 4 31 29 24 8
		f 4 -39 35 4 -38
		mu 0 4 32 30 0 18
		f 4 -41 37 15 6
		mu 0 4 33 32 18 2
		f 4 1 31 -43 -7
		mu 0 4 2 26 35 34
		f 4 -45 -32 29 7
		mu 0 4 36 35 26 3
		f 4 19 -47 -8 -18
		mu 0 4 19 38 37 3
		f 4 -33 -48 -20 -6
		mu 0 4 1 28 38 19;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "ankle_R_grp" -p "skin_proxy_dgc";
	rename -uid "0958B069-4CE6-202E-845E-7D9539C761FC";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -1.8524844319628189 0.89607093649782277 -0.45801674284106086 ;
	setAttr ".r" -type "double3" 89.311346018696995 3.396318530305372e-06 -89.999999897362613 ;
	setAttr -k on ".qsm_distance" 1.473036283393532;
createNode transform -n "ankle_R_ctl" -p "ankle_R_grp";
	rename -uid "7F39A6FF-4673-8143-F0FF-028B9B91EBAC";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "ankle_R_ctl_x_Shape" -p "ankle_R_ctl";
	rename -uid "4D1D5294-4BB9-6CF5-3E01-DE9B21981B95";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "ankle_R_ctl_y_Shape" -p "ankle_R_ctl";
	rename -uid "B13AD41A-47AB-27A5-DE81-C997E125A126";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "ankle_R_ctl_z_Shape" -p "ankle_R_ctl";
	rename -uid "6F68ED94-4895-222E-60BD-BD89B216FA49";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.73651814169676599 ;
	setAttr ".los" -type "double3" 0 0 0.73651814169676599 ;
createNode transform -n "ankle_R_geo_copy" -p "ankle_R_ctl";
	rename -uid "E454113B-40E8-5AED-69E6-F1BE25033033";
createNode mesh -n "ankle_R_geo_copyShape" -p "ankle_R_geo_copy";
	rename -uid "21810591-4A97-1D92-A762-BFA8EC71C3C8";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.125 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.625 0.625 0.875 0.125 0.125 0.125 0.375 0.625 0.375
		 0.125 0.625 0.125 0.5 0.5 0.5 0.625 0.5 0.75 0.5 0 0.5 1 0.5 0.125 0.5 0.25 0.625
		 0.875 0.75 0 0.5 0.875 0.25 0 0.375 0.875 0.25 0.125 0.25 0.25 0.375 0.375 0.5 0.375
		 0.625 0.375 0.75 0.25 0.75 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".vt[0:25]"  0.47454959 -0.89746529 1.3355397 -0.60587835 -0.89746529 1.3225534
		 0.34831023 0.070799708 0.30410451 -0.34831023 0.070799708 0.30410448 0.34812665 -0.077604175 -0.25816971
		 -0.34812665 -0.077604175 -0.25816971 0.42761397 -0.8960709 -0.3526434 -0.5 -0.8960709 -0.35264337
		 -0.5 -0.45563132 -0.35264334 0.42761397 -0.45563132 -0.35264343 0.3267535 -0.38459682 1.31157851
		 -0.54029703 -0.38459682 1.30115664 0 -0.10118324 -0.49080402 0 -0.45563132 -0.58527762
		 0 -0.89607084 -0.58527768 0.00014531612 -0.89746529 1.32983744 0.0010318756 -0.38459682 1.30766344
		 0 0.070799708 0.30410451 -0.5893302 -0.89607084 0.45263103 -1.1920929e-07 -0.89607084 0.45263103
		 0.39982414 -0.89607084 0.45263106 0.42708379 -0.4782474 0.34782887 0.41359901 -0.015191793 0.00060224533
		 0 -0.015191793 0.00060221553 -0.44476271 -0.015191793 0.00060224533 -0.50000024 -0.45563132 0.31921512;
	setAttr -s 48 ".ed[0:47]"  0 15 1 2 17 1 4 12 1 6 14 1 0 10 1 1 11 1
		 2 22 1 3 24 1 4 9 1 5 8 1 6 20 1 7 18 1 8 7 1 9 6 1 8 13 1 10 2 1 9 21 1 11 3 1 10 16 1
		 11 25 1 12 5 1 13 9 1 12 13 1 14 7 1 13 14 1 15 1 1 14 19 1 16 11 1 15 16 1 17 3 1
		 16 17 1 17 23 1 18 1 1 19 15 1 18 19 1 20 0 1 19 20 1 21 10 1 20 21 1 22 4 1 21 22 1
		 23 12 1 22 23 1 24 5 1 23 24 1 25 8 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 15 1 -31 -19
		mu 0 4 18 2 26 25
		f 4 39 2 -42 -43
		mu 0 4 34 4 20 35
		f 4 8 -22 -23 -3
		mu 0 4 4 17 21 20
		f 4 10 -37 -27 -4
		mu 0 4 6 31 29 22
		f 4 -47 43 9 -46
		mu 0 4 38 37 11 15
		f 4 -9 -40 -41 -17
		mu 0 4 16 13 33 32
		f 4 13 3 -25 21
		mu 0 4 17 6 22 21
		f 4 -14 16 -39 -11
		mu 0 4 12 16 32 30
		f 4 4 18 -29 -1
		mu 0 4 0 18 25 23
		f 4 45 12 11 -48
		mu 0 4 38 15 10 28
		f 4 22 -15 -10 -21
		mu 0 4 20 21 14 5
		f 4 23 -13 14 24
		mu 0 4 22 7 14 21
		f 4 -35 -12 -24 26
		mu 0 4 29 27 7 22
		f 4 27 -6 -26 28
		mu 0 4 25 19 1 23
		f 4 29 -18 -28 30
		mu 0 4 26 3 19 25
		f 4 20 -44 -45 41
		mu 0 4 20 5 36 35
		f 4 25 -33 34 33
		mu 0 4 24 9 27 29
		f 4 35 0 -34 36
		mu 0 4 31 8 24 29
		f 4 37 -5 -36 38
		mu 0 4 32 18 0 30
		f 4 -7 -16 -38 40
		mu 0 4 33 2 18 32
		f 4 6 42 -32 -2
		mu 0 4 2 34 35 26
		f 4 -8 -30 31 44
		mu 0 4 36 3 26 35
		f 4 17 7 46 -20
		mu 0 4 19 3 37 38
		f 4 5 19 47 32
		mu 0 4 1 19 38 28;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "toes_L_grp" -p "skin_proxy_dgc";
	rename -uid "CDB3FD43-4E8B-CD4F-6AD6-369B4F637E1B";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" 1.8362301253667555 0.31222088681427296 0.89427419876830028 ;
	setAttr ".r" -type "double3" -89.999838143326897 67.528071975035743 90.000149495230005 ;
	setAttr -k on ".qsm_distance" 0.8206293441713407;
createNode transform -n "toes_L_ctl" -p "toes_L_grp";
	rename -uid "0DE5D809-4F4D-643B-AB96-BBAB50A2CB75";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "toes_L_ctl_x_Shape" -p "toes_L_ctl";
	rename -uid "1EFBAF92-47C2-E15E-DC9A-24AF207F83D5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "toes_L_ctl_y_Shape" -p "toes_L_ctl";
	rename -uid "C97324D1-4043-74AB-7BE1-BF94A23178B8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "toes_L_ctl_z_Shape" -p "toes_L_ctl";
	rename -uid "A9F624B5-4C1C-5074-7B63-2AAEBA32E7C1";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.41031467208567035 ;
	setAttr ".los" -type "double3" 0 0 0.41031467208567035 ;
createNode transform -n "toes_L_geo_copy" -p "toes_L_ctl";
	rename -uid "FCAA4764-4E8A-4B1D-D0A5-DE89220FD50A";
createNode mesh -n "toes_R_geoShape" -p "toes_L_geo_copy";
	rename -uid "42B71753-4F1B-C19C-E3B0-CD87955E1CB4";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.5 0.5 0.5 0.75 0.5 0 0.5 1 0.5 0.25 0.25 0 0.375
		 0.875 0.25 0.25 0.375 0.375 0.5 0.375 0.625 0.375 0.75 0.25 0.625 0.875 0.75 0 0.5
		 0.875 0.625 0.625 0.875 0.125 0.5 0.625 0.125 0.125 0.375 0.625 0.25 0.125 0.375
		 0.125 0.5 0.125 0.625 0.125 0.75 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".pt[0:25]" -type "float3"  -1.836231 0.005105556 -0.82717454 
		-1.836231 0.010292144 -0.84053409 -1.8362309 -0.06668476 -0.98090297 -1.8362309 -0.053239476 
		-0.99262196 -1.8362302 -0.31808782 -0.97017485 -1.8362302 -0.31808782 -0.97017407 
		-1.8362302 -0.28517726 -0.77661794 -1.8362302 -0.28517723 -0.77661687 -1.8362302 
		-0.31808779 -0.97017437 -1.8362302 -0.28517726 -0.77661741 -1.836231 0.025808519 
		-0.83745193 -1.8362309 -0.0418524 -0.99036008 -1.8362305 -0.13846424 -0.80169791 
		-1.8362305 -0.19279011 -0.96334088 -1.8362305 -0.18037391 -0.9680692 -1.8362305 -0.18606748 
		-0.96920002 -1.8362305 -0.13587095 -0.80837715 -1.8362306 -0.12811275 -0.80683637 
		-1.8362302 -0.3033714 -0.88637877 -1.8362302 -0.3033714 -0.88637918 -1.8362302 -0.30337143 
		-0.88637972 -1.8362305 -0.16812383 -0.89508694 -1.8362309 -0.03078956 -0.90403879 
		-1.836231 -0.0080219628 -0.91390604 -1.8362309 -0.021473667 -0.91657805 -1.8362305 
		-0.16346583 -0.90135604;
	setAttr -s 26 ".vt[0:25]"  1.50087857 -0.015325755 1.65940094 2.23304796 0.015707344 1.67913437
		 1.67768455 0.40748763 1.55557656 2.21500325 0.43026197 1.59527612 1.52391577 0.5061872 0.91745824
		 2.36661553 0.50618756 0.9174574 1.35904408 0.0025696754 0.90351218 2.47965479 0.0025700927 0.90351117
		 2.00072860718 0.50618738 0.91745782 1.92807031 0.0025698841 0.90351164 1.86696327 0.00019082427 1.71664655
		 1.9463439 0.41887477 1.62280536 1.41855443 -0.0076630414 1.28531301 1.57961583 0.4263382 1.22940207
		 1.97353625 0.43203187 1.26301622 2.28681064 0.43772554 1.24925137 2.37647915 0.0078537762 1.29517913
		 1.89751673 9.5367432e-05 1.31393552 2.44786286 0.28792584 0.91259933 1.96439946 0.28792566 0.9125998
		 1.4177711 0.28792545 0.91260028 1.49908519 0.24221706 1.25735748 1.58928156 0.19608095 1.60748887
		 1.90665352 0.20953278 1.66972589 2.22402549 0.22298466 1.63720524 2.37196779 0.25566912 1.27221525;
	setAttr -s 48 ".ed[0:47]"  0 10 1 2 11 1 4 8 1 6 9 1 0 22 1 1 24 1 2 13 1
		 3 15 1 4 20 1 5 18 1 6 12 1 7 16 1 8 5 1 9 7 1 8 19 1 10 1 1 9 17 1 11 3 1 10 23 1
		 11 14 1 12 0 1 13 4 1 12 21 1 14 8 1 13 14 1 15 5 1 14 15 1 16 1 1 15 25 1 17 10 1
		 16 17 1 17 12 1 18 7 1 19 9 1 18 19 1 20 6 1 19 20 1 21 13 1 20 21 1 22 2 1 21 22 1
		 23 11 1 22 23 1 24 3 1 23 24 1 25 16 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 42 41 -2 -40
		mu 0 4 35 36 18 2
		f 4 24 23 -3 -22
		mu 0 4 22 23 14 4
		f 4 2 14 36 -9
		mu 0 4 4 14 31 33
		f 4 3 16 31 -11
		mu 0 4 6 15 28 20
		f 4 47 -10 -26 28
		mu 0 4 38 30 11 25
		f 4 38 37 21 8
		mu 0 4 32 34 21 13
		f 4 12 9 34 -15
		mu 0 4 14 5 29 31
		f 4 -17 13 11 30
		mu 0 4 28 15 7 26
		f 4 -42 44 43 -18
		mu 0 4 18 36 37 3
		f 4 -24 26 25 -13
		mu 0 4 14 23 24 5
		f 4 40 39 6 -38
		mu 0 4 34 35 2 21
		f 4 1 19 -25 -7
		mu 0 4 2 18 23 22
		f 4 -27 -20 17 7
		mu 0 4 24 23 18 3
		f 4 46 -29 -8 -44
		mu 0 4 37 38 25 3
		f 4 -30 -31 27 -16
		mu 0 4 17 28 26 9
		f 4 -32 29 -1 -21
		mu 0 4 20 28 17 8
		f 4 -35 32 -14 -34
		mu 0 4 31 29 7 15
		f 4 -37 33 -4 -36
		mu 0 4 33 31 15 6
		f 4 10 22 -39 35
		mu 0 4 12 19 34 32
		f 4 20 4 -41 -23
		mu 0 4 19 0 35 34
		f 4 0 18 -43 -5
		mu 0 4 0 16 36 35
		f 4 -45 -19 15 5
		mu 0 4 37 36 16 1
		f 4 -28 -46 -47 -6
		mu 0 4 1 27 38 37
		f 4 -12 -33 -48 45
		mu 0 4 27 10 30 38;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "toes_R_grp" -p "skin_proxy_dgc";
	rename -uid "730650E5-460E-BADE-B5D8-F69CBDBC8668";
	addAttr -ci true -k true -sn "qsm_distance" -ln "qsm_distance" -at "double";
	setAttr ".t" -type "double3" -1.836230082717734 0.31222088110432655 0.89427420260724033 ;
	setAttr ".r" -type "double3" 89.999839180244706 -67.528072025123734 -89.999851289143493 ;
	setAttr -k on ".qsm_distance" 0.82062934417134037;
createNode transform -n "toes_R_ctl" -p "toes_R_grp";
	rename -uid "8AED4E93-45D8-73C4-1F01-E791FCCFD9D7";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "toes_R_ctl_x_Shape" -p "toes_R_ctl";
	rename -uid "0A85DB30-4D2B-90D4-A55F-409853F52826";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "toes_R_ctl_y_Shape" -p "toes_R_ctl";
	rename -uid "68EEF14A-430E-AB8F-78B7-B6B422E9E704";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "toes_R_ctl_z_Shape" -p "toes_R_ctl";
	rename -uid "DDD9F881-439C-5110-265A-4FBAC6523E89";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.41031467208567018 ;
	setAttr ".los" -type "double3" 0 0 0.41031467208567018 ;
createNode transform -n "toes_R_geo_copy" -p "toes_R_ctl";
	rename -uid "5DAB6D0C-4B99-D97C-D7C4-A3B56DB8165E";
createNode mesh -n "toes_R_geo_copyShape" -p "toes_R_geo_copy";
	rename -uid "3035DF97-4E32-550D-E086-05BEE0DE0A22";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.375 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.375 0 0.625 0 0.375
		 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 0
		 0.875 0.25 0.125 0 0.125 0.25 0.5 0.5 0.5 0.75 0.5 0 0.5 1 0.5 0.25 0.25 0 0.375
		 0.875 0.25 0.25 0.375 0.375 0.5 0.375 0.625 0.375 0.75 0.25 0.625 0.875 0.75 0 0.5
		 0.875 0.625 0.625 0.875 0.125 0.5 0.625 0.125 0.125 0.375 0.625 0.25 0.125 0.375
		 0.125 0.5 0.125 0.625 0.125 0.75 0.125;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".op" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 26 ".vt[0:25]"  0.33535063 -0.01021992 0.83222705 -0.39681864 0.025999164 0.8385995
		 0.15854478 0.340803 0.57467389 -0.37877393 0.37702218 0.60265338 0.31231427 0.18809962 -0.052715957
		 -0.53038549 0.18809929 -0.052717745 0.47718602 -0.2826072 0.12689519 -0.64342475 -0.28260767 0.12689298
		 -0.16449857 0.18809944 -0.052716911 -0.091840267 -0.28260744 0.12689406 -0.030734062 0.025999321 0.87919456
		 -0.11011457 0.37702227 0.63244504 0.41767526 -0.14612693 0.48361593 0.25661385 0.23354831 0.26606166
		 -0.13730645 0.25165784 0.29494673 -0.45058084 0.25165772 0.28005046 -0.54024959 -0.1280176 0.48680091
		 -0.061287045 -0.12801744 0.50709903 -0.61163282 -0.015446067 0.026219368 -0.12816942 -0.015445858 0.026220322
		 0.41845894 -0.01544565 0.026221395 0.33714449 0.074093506 0.36227119 0.24694777 0.16529161 0.70345056
		 -0.070424318 0.20151076 0.75581974 -0.38779616 0.20151067 0.72062641 -0.53573823 0.092202842 0.37085813;
	setAttr -s 48 ".ed[0:47]"  0 10 1 2 11 1 4 8 1 6 9 1 0 22 1 1 24 1 2 13 1
		 3 15 1 4 20 1 5 18 1 6 12 1 7 16 1 8 5 1 9 7 1 8 19 1 10 1 1 9 17 1 11 3 1 10 23 1
		 11 14 1 12 0 1 13 4 1 12 21 1 14 8 1 13 14 1 15 5 1 14 15 1 16 1 1 15 25 1 17 10 1
		 16 17 1 17 12 1 18 7 1 19 9 1 18 19 1 20 6 1 19 20 1 21 13 1 20 21 1 22 2 1 21 22 1
		 23 11 1 22 23 1 24 3 1 23 24 1 25 16 1 24 25 1 25 18 1;
	setAttr -s 24 -ch 96 ".fc[0:23]" -type "polyFaces" 
		f 4 39 1 -42 -43
		mu 0 4 35 2 18 36
		f 4 21 2 -24 -25
		mu 0 4 22 4 14 23
		f 4 8 -37 -15 -3
		mu 0 4 4 33 31 14
		f 4 10 -32 -17 -4
		mu 0 4 6 20 28 15
		f 4 -29 25 9 -48
		mu 0 4 38 25 11 30
		f 4 -9 -22 -38 -39
		mu 0 4 32 13 21 34
		f 4 14 -35 -10 -13
		mu 0 4 14 31 29 5
		f 4 -31 -12 -14 16
		mu 0 4 28 26 7 15
		f 4 17 -44 -45 41
		mu 0 4 18 3 37 36
		f 4 12 -26 -27 23
		mu 0 4 14 5 24 23
		f 4 37 -7 -40 -41
		mu 0 4 34 21 2 35
		f 4 6 24 -20 -2
		mu 0 4 2 22 23 18
		f 4 -8 -18 19 26
		mu 0 4 24 3 18 23
		f 4 43 7 28 -47
		mu 0 4 37 3 25 38
		f 4 15 -28 30 29
		mu 0 4 17 9 26 28
		f 4 20 0 -30 31
		mu 0 4 20 8 17 28
		f 4 33 13 -33 34
		mu 0 4 31 15 7 29
		f 4 35 3 -34 36
		mu 0 4 33 6 15 31
		f 4 -36 38 -23 -11
		mu 0 4 12 32 34 19
		f 4 22 40 -5 -21
		mu 0 4 19 34 35 0
		f 4 4 42 -19 -1
		mu 0 4 0 35 36 16
		f 4 -6 -16 18 44
		mu 0 4 37 1 16 36
		f 4 5 46 45 27
		mu 0 4 1 37 38 27
		f 4 -46 47 32 11
		mu 0 4 27 38 30 10;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".de" 1;
createNode transform -n "toes_end_L_grp" -p "skin_proxy_dgc";
	rename -uid "D306961E-425D-2936-D807-A19DC65ABC47";
	setAttr ".t" -type "double3" 1.836230933960509 -0.0014488690602530441 1.6525906266294184 ;
	setAttr ".r" -type "double3" -89.999836548047853 67.528071975035772 90.000149495230005 ;
createNode transform -n "toes_end_L_ctl" -p "toes_end_L_grp";
	rename -uid "7DFE057A-4FE9-03BF-9D53-FABB3951F294";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" -90 90 90 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "toes_end_L_ctl_x_Shape" -p "toes_end_L_ctl";
	rename -uid "CDD48337-4494-A81B-6BB5-41992E297543";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "toes_end_L_ctl_y_Shape" -p "toes_end_L_ctl";
	rename -uid "98D21732-4D17-D1BB-F734-8DBB3AB718AA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "toes_end_L_ctl_z_Shape" -p "toes_end_L_ctl";
	rename -uid "5D066681-4F08-7106-7063-1FBCDEDF453A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode transform -n "toes_end_R_grp" -p "skin_proxy_dgc";
	rename -uid "5397AA6D-4057-B3DB-C621-DB9B398DD9F8";
	setAttr ".t" -type "double3" -1.8362308987664815 -0.0014488741072933853 1.6525906307425542 ;
	setAttr ".r" -type "double3" 90.000163300701033 -67.528072025072632 -90.000149061707845 ;
createNode transform -n "toes_end_R_ctl" -p "toes_end_R_grp";
	rename -uid "B7E6C140-4541-D247-70DF-D7AF2C43BD4C";
	addAttr -ci true -k true -sn "qsm_scale" -ln "qsm_scale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "qsm_scale_weight" -ln "qsm_scale_weight" -dv 1 -at "double";
	setAttr ".r" -type "double3" 0 90 0 ;
	setAttr -k on ".qsm_scale";
	setAttr -k on ".qsm_scale_weight";
createNode locator -n "toes_end_R_ctl_x_Shape" -p "toes_end_R_ctl";
	rename -uid "42714ABC-429A-323D-3C4A-01A61690B6D5";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr ".lp" -type "double3" 0.1 0 0 ;
	setAttr ".los" -type "double3" 0.1 0 0 ;
createNode locator -n "toes_end_R_ctl_y_Shape" -p "toes_end_R_ctl";
	rename -uid "6F5D229D-47F8-3090-C4CC-7580D69C447F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 14;
	setAttr ".lp" -type "double3" 0 0.1 0 ;
	setAttr ".los" -type "double3" 0 0.1 0 ;
createNode locator -n "toes_end_R_ctl_z_Shape" -p "toes_end_R_ctl";
	rename -uid "C09E9A85-42F7-8035-B7B9-18B587AF586C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".lp" -type "double3" 0 0 0.1 ;
	setAttr ".los" -type "double3" 0 0 0.1 ;
createNode multiplyDivide -n "finger_index_a_R_ctl_mtp";
	rename -uid "AC61BA89-40DC-F904-3BAF-3AB7B8BF67AB";
createNode multiplyDivide -n "finger_ring_c_R_ctl_mtp";
	rename -uid "F96DD5D3-471E-4F78-D2AE-AE81FAAC14D6";
createNode multiplyDivide -n "finger_pinky_b_L_ctl_mtp";
	rename -uid "D4DE5A56-4D69-A776-D02B-E48BEE98DD80";
createNode multiplyDivide -n "finger_pinky_c_R_ctl_mtp";
	rename -uid "63097D5F-49BD-588F-1A8D-CF9F11CB272B";
createNode multiplyDivide -n "finger_end_thumb_R_ctl_mtp";
	rename -uid "7AA0D613-469C-C1EF-C529-0BA9EDF9B440";
createNode multiplyDivide -n "finger_end_index_R_ctl_mtp";
	rename -uid "7FE446D7-4E08-F4F9-7A27-8D8474042EEA";
createNode multiplyDivide -n "finger_end_middle_L_ctl_mtp";
	rename -uid "2BD3FA3C-40F4-51A1-0FF2-1D9452BBC943";
createNode multiplyDivide -n "chest_M_ctl_mtp";
	rename -uid "5DE19604-43A8-DB5E-16F5-3FA359F07247";
createNode multiplyDivide -n "finger_thumb_c_R_ctl_mtp";
	rename -uid "6504A78C-44E9-8028-3BBB-6A9FC4B303B6";
createNode multiplyDivide -n "finger_middle_a_L_ctl_mtp";
	rename -uid "5490C24E-4383-72B7-1EA4-63B6CC34C022";
createNode multiplyDivide -n "finger_middle_c_L_ctl_mtp";
	rename -uid "AB249F9E-4E4E-8BB9-565C-DBA1653EA983";
createNode multiplyDivide -n "shoulder_R_ctl_mtp";
	rename -uid "0F2FC79E-42F3-7A74-6DA0-1EB77D1A1F68";
createNode multiplyDivide -n "finger_ring_b_L_ctl_mtp";
	rename -uid "6953FE63-497B-31E8-722C-D4A921B604BF";
createNode multiplyDivide -n "finger_end_ring_L_ctl_mtp";
	rename -uid "542341AB-4C12-C251-A929-A79D204F8C3B";
createNode multiplyDivide -n "finger_middle_a_R_ctl_mtp";
	rename -uid "C74BFF0D-4D25-69D6-F6D4-82A25F6DC6BF";
createNode multiplyDivide -n "neck_M_ctl_mtp";
	rename -uid "B5F83ED2-464E-61C1-BAE8-528E01FDB751";
createNode multiplyDivide -n "wrist_L_ctl_mtp";
	rename -uid "FDB050CB-4FE8-A443-8698-4B80C5CCD68F";
createNode multiplyDivide -n "finger_thumb_a_R_ctl_mtp";
	rename -uid "97D03873-4274-E304-D9EE-38A0B2F87C46";
createNode multiplyDivide -n "root_M_ctl_mtp";
	rename -uid "BE8B8029-4351-EBFF-D957-26B91F383E51";
createNode multiplyDivide -n "scapula_R_ctl_mtp";
	rename -uid "4B2FD296-4CAF-E257-ADA5-21BE09C1F511";
createNode multiplyDivide -n "finger_thumb_b_R_ctl_mtp";
	rename -uid "8C8B8350-41F2-4A46-114E-6B91F4F8E7F3";
createNode multiplyDivide -n "spine_b_M_ctl_mtp";
	rename -uid "90987178-43DD-0937-BE58-B1B83F9D12BB";
createNode multiplyDivide -n "spine_a_M_ctl_mtp";
	rename -uid "FC363937-48C8-3B0A-6BF3-B9900C1D7DC8";
createNode multiplyDivide -n "wrist_R_ctl_mtp";
	rename -uid "EB00C1A9-4590-32FE-6831-BF80E009BC73";
createNode multiplyDivide -n "finger_thumb_a_L_ctl_mtp";
	rename -uid "454D7806-4156-D98B-220B-39B546D0E282";
createNode multiplyDivide -n "finger_index_a_L_ctl_mtp";
	rename -uid "DD5DDF9F-40A6-A17E-1FAF-7AB6295B472F";
createNode multiplyDivide -n "finger_index_b_L_ctl_mtp";
	rename -uid "B3C0E084-4F1F-CA34-34F0-69BF8CCE4FEF";
createNode multiplyDivide -n "finger_middle_b_L_ctl_mtp";
	rename -uid "75108AD7-4B1F-0C5F-804C-978E47400DAB";
createNode multiplyDivide -n "finger_middle_c_R_ctl_mtp";
	rename -uid "251DDDB2-428D-431A-752C-24A1322CE440";
createNode multiplyDivide -n "head_end_M_ctl_mtp";
	rename -uid "65F13360-484F-FC78-257F-E09718E6E79F";
createNode multiplyDivide -n "finger_ring_a_L_ctl_mtp";
	rename -uid "0B258618-4328-7B88-0027-F185A24093F3";
createNode multiplyDivide -n "elbow_R_ctl_mtp";
	rename -uid "864E7766-4CBD-78FA-4122-B3BA6C253FC2";
createNode multiplyDivide -n "elbow_L_ctl_mtp";
	rename -uid "77D373EE-40D4-DC57-1F97-7CB4414FA09F";
createNode multiplyDivide -n "scapula_L_ctl_mtp";
	rename -uid "B3DC3FF5-4E43-4DA2-90B9-CC8B2D8CA6CD";
createNode multiplyDivide -n "finger_thumb_b_L_ctl_mtp";
	rename -uid "3D8704B9-4A39-C355-A8F6-97AFFF8A0F4B";
createNode multiplyDivide -n "finger_index_c_L_ctl_mtp";
	rename -uid "3FC0BC0B-4CFE-92F2-9834-35A9323C1B0F";
createNode multiplyDivide -n "finger_middle_b_R_ctl_mtp";
	rename -uid "F7C5BD6A-4966-E1B2-8CFE-69A2A9DDE09C";
createNode multiplyDivide -n "finger_ring_a_R_ctl_mtp";
	rename -uid "47A03DC8-4309-DC24-AA30-668F5EA3D641";
createNode multiplyDivide -n "head_M_ctl_mtp";
	rename -uid "2001A388-4FF0-4B3C-68AC-799E7A557E15";
createNode multiplyDivide -n "finger_index_b_R_ctl_mtp";
	rename -uid "01F2CE19-4A12-4325-BCE0-C4B818FFFE89";
createNode multiplyDivide -n "shoulder_L_ctl_mtp";
	rename -uid "95031DE2-4EFF-C07C-FC1D-ED931A1D6ED4";
createNode multiplyDivide -n "finger_index_c_R_ctl_mtp";
	rename -uid "EE328D11-44BD-2C64-2A74-26939055558C";
createNode multiplyDivide -n "finger_thumb_c_L_ctl_mtp";
	rename -uid "E4362AE8-4588-279C-5D3D-6F8991980959";
createNode multiplyDivide -n "finger_ring_b_R_ctl_mtp";
	rename -uid "C927177B-4214-79A6-28FD-1DB985C7AACE";
createNode multiplyDivide -n "finger_ring_c_L_ctl_mtp";
	rename -uid "E402BB73-403E-C0D2-2F45-86AD0F6E0244";
createNode multiplyDivide -n "finger_pinky_a_L_ctl_mtp";
	rename -uid "1F238584-47B4-311F-01E0-2AB0EA6D1BD2";
createNode multiplyDivide -n "finger_pinky_a_R_ctl_mtp";
	rename -uid "828D07B7-4AEA-8E53-B583-2695ACC3B59E";
createNode multiplyDivide -n "finger_pinky_b_R_ctl_mtp";
	rename -uid "6954F042-40A2-CCF4-2881-17A18BBBD886";
createNode multiplyDivide -n "finger_pinky_c_L_ctl_mtp";
	rename -uid "DFEFC459-4732-A55E-AFB6-56AFFEE240DD";
createNode multiplyDivide -n "finger_end_thumb_L_ctl_mtp";
	rename -uid "6F4E11C4-4501-B6FA-2884-9C98F8533D01";
createNode multiplyDivide -n "finger_end_index_L_ctl_mtp";
	rename -uid "E71DE45F-44D3-341A-EFA5-848FF6F35323";
createNode multiplyDivide -n "finger_end_middle_R_ctl_mtp";
	rename -uid "A8269264-4700-1957-4893-BABCBE2B990F";
createNode multiplyDivide -n "hip_L_ctl_mtp";
	rename -uid "FF030BD4-462F-73C2-8843-199D4FEB7A99";
createNode multiplyDivide -n "finger_end_pinky_R_ctl_mtp";
	rename -uid "C3528746-4599-AB74-D10B-BA9390AA13DC";
createNode multiplyDivide -n "knee_R_ctl_mtp";
	rename -uid "088ED49B-4217-10EC-77A4-C888E137E0D8";
createNode multiplyDivide -n "toes_R_ctl_mtp";
	rename -uid "7644D996-425E-3BAD-D2DA-FC8F186FB9BB";
createNode multiplyDivide -n "toes_end_R_ctl_mtp";
	rename -uid "1571F243-4BEB-3734-BEE7-5886F0BDCE18";
createNode multiplyDivide -n "finger_end_ring_R_ctl_mtp";
	rename -uid "EB3CDF61-4807-CE89-4872-DCB41780DD59";
createNode multiplyDivide -n "finger_end_pinky_L_ctl_mtp";
	rename -uid "71AF3DC4-4367-C88A-27C3-CCBD89D76551";
createNode multiplyDivide -n "toes_L_ctl_mtp";
	rename -uid "1003291D-45C3-D6F7-6F67-AFADE36DD070";
createNode multiplyDivide -n "ankle_L_ctl_mtp";
	rename -uid "7861080F-42D6-1CEB-D1A1-3296D47CF3DC";
createNode multiplyDivide -n "hip_R_ctl_mtp";
	rename -uid "D145F561-4F27-37C9-F06E-3C875A7E13D8";
createNode multiplyDivide -n "toes_end_L_ctl_mtp";
	rename -uid "FA792F4D-4CBA-699B-1992-8B8014ECD593";
createNode multiplyDivide -n "knee_L_ctl_mtp";
	rename -uid "F4A37C3C-4936-73F9-81DD-0FBF645DA8C7";
createNode multiplyDivide -n "ankle_R_ctl_mtp";
	rename -uid "6C8055F0-4F25-6F68-91D6-42972FED9DBD";
createNode hyperLayout -n "hyperLayout1";
	rename -uid "C9C3A4FB-4BA6-F571-BB34-5A9903B93A4D";
	setAttr ".ihi" 0;
	setAttr -s 588 ".hyp";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 11 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 13 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -s 4 ".r";
select -ne :initialShadingGroup;
	setAttr -s 54 ".dsm";
	setAttr ".ro" yes;
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
	setAttr -s 3 ".sol";
connectAttr "hyperLayout1.msg" "skin_proxy_dgc.hl";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "root_M_ctl.qsm_scale_weight";
connectAttr "root_M_ctl_mtp.ox" "root_M_ctl.sx";
connectAttr "root_M_ctl_mtp.ox" "root_M_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "root_M_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "root_M_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "root_M_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "spine_a_M_ctl.qsm_scale_weight";
connectAttr "spine_a_M_ctl_mtp.ox" "spine_a_M_ctl.sx";
connectAttr "spine_a_M_ctl_mtp.ox" "spine_a_M_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "spine_a_M_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "spine_a_M_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "spine_a_M_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "spine_b_M_ctl.qsm_scale_weight";
connectAttr "spine_b_M_ctl_mtp.ox" "spine_b_M_ctl.sx";
connectAttr "spine_b_M_ctl_mtp.ox" "spine_b_M_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "spine_b_M_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "spine_b_M_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "spine_b_M_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "chest_M_ctl.qsm_scale_weight";
connectAttr "chest_M_ctl_mtp.ox" "chest_M_ctl.sx";
connectAttr "chest_M_ctl_mtp.ox" "chest_M_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "chest_M_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "chest_M_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "chest_M_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "neck_M_ctl.qsm_scale_weight";
connectAttr "neck_M_ctl_mtp.ox" "neck_M_ctl.sx";
connectAttr "neck_M_ctl_mtp.ox" "neck_M_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "neck_M_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "neck_M_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "neck_M_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "head_M_ctl.qsm_scale_weight";
connectAttr "head_M_ctl_mtp.ox" "head_M_ctl.sx";
connectAttr "head_M_ctl_mtp.ox" "head_M_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "head_M_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "head_M_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "head_M_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "head_end_M_ctl.qsm_scale_weight";
connectAttr "head_end_M_ctl_mtp.ox" "head_end_M_ctl.sx";
connectAttr "head_end_M_ctl_mtp.ox" "head_end_M_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "head_end_M_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "head_end_M_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "head_end_M_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "scapula_L_ctl.qsm_scale_weight";
connectAttr "scapula_L_ctl_mtp.ox" "scapula_L_ctl.sx";
connectAttr "scapula_L_ctl_mtp.ox" "scapula_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "scapula_L_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "scapula_L_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "scapula_L_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "scapula_R_ctl.qsm_scale_weight";
connectAttr "scapula_R_ctl_mtp.ox" "scapula_R_ctl.sx";
connectAttr "scapula_R_ctl_mtp.ox" "scapula_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "scapula_R_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "scapula_R_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "scapula_R_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "shoulder_L_ctl.qsm_scale_weight";
connectAttr "shoulder_L_ctl_mtp.ox" "shoulder_L_ctl.sx";
connectAttr "shoulder_L_ctl_mtp.ox" "shoulder_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "shoulder_L_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "shoulder_L_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "shoulder_L_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "shoulder_R_ctl.qsm_scale_weight";
connectAttr "shoulder_R_ctl_mtp.ox" "shoulder_R_ctl.sx";
connectAttr "shoulder_R_ctl_mtp.ox" "shoulder_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "shoulder_R_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "shoulder_R_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "shoulder_R_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "elbow_L_ctl.qsm_scale_weight";
connectAttr "elbow_L_ctl_mtp.ox" "elbow_L_ctl.sx";
connectAttr "elbow_L_ctl_mtp.ox" "elbow_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "elbow_L_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "elbow_L_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "elbow_L_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "elbow_R_ctl.qsm_scale_weight";
connectAttr "elbow_R_ctl_mtp.ox" "elbow_R_ctl.sx";
connectAttr "elbow_R_ctl_mtp.ox" "elbow_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "elbow_R_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "elbow_R_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "elbow_R_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "wrist_L_ctl.qsm_scale_weight";
connectAttr "wrist_L_ctl_mtp.ox" "wrist_L_ctl.sx";
connectAttr "wrist_L_ctl_mtp.ox" "wrist_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "wrist_L_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "wrist_L_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "wrist_L_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "wrist_R_ctl.qsm_scale_weight";
connectAttr "wrist_R_ctl_mtp.ox" "wrist_R_ctl.sx";
connectAttr "wrist_R_ctl_mtp.ox" "wrist_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "wrist_R_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "wrist_R_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "wrist_R_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_thumb_a_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_thumb_a_L_ctl_mtp.ox" "finger_thumb_a_L_ctl.sx";
connectAttr "finger_thumb_a_L_ctl_mtp.ox" "finger_thumb_a_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_a_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_a_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_a_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_thumb_a_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_thumb_a_R_ctl_mtp.ox" "finger_thumb_a_R_ctl.sx";
connectAttr "finger_thumb_a_R_ctl_mtp.ox" "finger_thumb_a_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_a_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_a_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_a_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_thumb_b_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_thumb_b_L_ctl_mtp.ox" "finger_thumb_b_L_ctl.sx";
connectAttr "finger_thumb_b_L_ctl_mtp.ox" "finger_thumb_b_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_b_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_b_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_b_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_thumb_b_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_thumb_b_R_ctl_mtp.ox" "finger_thumb_b_R_ctl.sx";
connectAttr "finger_thumb_b_R_ctl_mtp.ox" "finger_thumb_b_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_b_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_b_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_b_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_thumb_c_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_thumb_c_L_ctl_mtp.ox" "finger_thumb_c_L_ctl.sx";
connectAttr "finger_thumb_c_L_ctl_mtp.ox" "finger_thumb_c_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_c_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_c_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_c_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_thumb_c_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_thumb_c_R_ctl_mtp.ox" "finger_thumb_c_R_ctl.sx";
connectAttr "finger_thumb_c_R_ctl_mtp.ox" "finger_thumb_c_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_c_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_c_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_thumb_c_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_index_a_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_index_a_L_ctl_mtp.ox" "finger_index_a_L_ctl.sx";
connectAttr "finger_index_a_L_ctl_mtp.ox" "finger_index_a_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_a_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_a_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_a_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_index_a_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_index_a_R_ctl_mtp.ox" "finger_index_a_R_ctl.sx";
connectAttr "finger_index_a_R_ctl_mtp.ox" "finger_index_a_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_a_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_a_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_a_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_index_b_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_index_b_L_ctl_mtp.ox" "finger_index_b_L_ctl.sx";
connectAttr "finger_index_b_L_ctl_mtp.ox" "finger_index_b_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_b_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_b_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_b_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_index_b_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_index_b_R_ctl_mtp.ox" "finger_index_b_R_ctl.sx";
connectAttr "finger_index_b_R_ctl_mtp.ox" "finger_index_b_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_b_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_b_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_b_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_index_c_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_index_c_L_ctl_mtp.ox" "finger_index_c_L_ctl.sx";
connectAttr "finger_index_c_L_ctl_mtp.ox" "finger_index_c_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_c_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_c_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_c_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_index_c_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_index_c_R_ctl_mtp.ox" "finger_index_c_R_ctl.sx";
connectAttr "finger_index_c_R_ctl_mtp.ox" "finger_index_c_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_c_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_c_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_index_c_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_middle_a_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_middle_a_L_ctl_mtp.ox" "finger_middle_a_L_ctl.sx";
connectAttr "finger_middle_a_L_ctl_mtp.ox" "finger_middle_a_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_a_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_a_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_a_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_middle_a_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_middle_a_R_ctl_mtp.ox" "finger_middle_a_R_ctl.sx";
connectAttr "finger_middle_a_R_ctl_mtp.ox" "finger_middle_a_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_a_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_a_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_a_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_middle_b_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_middle_b_L_ctl_mtp.ox" "finger_middle_b_L_ctl.sx";
connectAttr "finger_middle_b_L_ctl_mtp.ox" "finger_middle_b_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_b_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_b_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_b_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_middle_b_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_middle_b_R_ctl_mtp.ox" "finger_middle_b_R_ctl.sx";
connectAttr "finger_middle_b_R_ctl_mtp.ox" "finger_middle_b_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_b_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_b_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_b_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_middle_c_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_middle_c_L_ctl_mtp.ox" "finger_middle_c_L_ctl.sx";
connectAttr "finger_middle_c_L_ctl_mtp.ox" "finger_middle_c_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_c_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_c_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_c_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_middle_c_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_middle_c_R_ctl_mtp.ox" "finger_middle_c_R_ctl.sx";
connectAttr "finger_middle_c_R_ctl_mtp.ox" "finger_middle_c_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_c_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_c_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_middle_c_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_ring_a_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_ring_a_L_ctl_mtp.ox" "finger_ring_a_L_ctl.sx";
connectAttr "finger_ring_a_L_ctl_mtp.ox" "finger_ring_a_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_a_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_a_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_a_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_ring_a_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_ring_a_R_ctl_mtp.ox" "finger_ring_a_R_ctl.sx";
connectAttr "finger_ring_a_R_ctl_mtp.ox" "finger_ring_a_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_a_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_a_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_a_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_ring_b_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_ring_b_L_ctl_mtp.ox" "finger_ring_b_L_ctl.sx";
connectAttr "finger_ring_b_L_ctl_mtp.ox" "finger_ring_b_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_b_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_b_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_b_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_ring_b_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_ring_b_R_ctl_mtp.ox" "finger_ring_b_R_ctl.sx";
connectAttr "finger_ring_b_R_ctl_mtp.ox" "finger_ring_b_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_b_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_b_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_b_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_ring_c_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_ring_c_L_ctl_mtp.ox" "finger_ring_c_L_ctl.sx";
connectAttr "finger_ring_c_L_ctl_mtp.ox" "finger_ring_c_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_c_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_c_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_c_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_ring_c_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_ring_c_R_ctl_mtp.ox" "finger_ring_c_R_ctl.sx";
connectAttr "finger_ring_c_R_ctl_mtp.ox" "finger_ring_c_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_c_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_c_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_ring_c_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_pinky_a_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_pinky_a_L_ctl_mtp.ox" "finger_pinky_a_L_ctl.sx";
connectAttr "finger_pinky_a_L_ctl_mtp.ox" "finger_pinky_a_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_a_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_a_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_a_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_pinky_a_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_pinky_a_R_ctl_mtp.ox" "finger_pinky_a_R_ctl.sx";
connectAttr "finger_pinky_a_R_ctl_mtp.ox" "finger_pinky_a_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_a_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_a_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_a_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_pinky_b_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_pinky_b_L_ctl_mtp.ox" "finger_pinky_b_L_ctl.sx";
connectAttr "finger_pinky_b_L_ctl_mtp.ox" "finger_pinky_b_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_b_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_b_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_b_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_pinky_b_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_pinky_b_R_ctl_mtp.ox" "finger_pinky_b_R_ctl.sx";
connectAttr "finger_pinky_b_R_ctl_mtp.ox" "finger_pinky_b_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_b_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_b_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_b_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_pinky_c_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_pinky_c_L_ctl_mtp.ox" "finger_pinky_c_L_ctl.sx";
connectAttr "finger_pinky_c_L_ctl_mtp.ox" "finger_pinky_c_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_c_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_c_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_c_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_pinky_c_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_pinky_c_R_ctl_mtp.ox" "finger_pinky_c_R_ctl.sx";
connectAttr "finger_pinky_c_R_ctl_mtp.ox" "finger_pinky_c_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_c_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_c_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_pinky_c_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_thumb_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_thumb_L_ctl_mtp.ox" "finger_end_thumb_L_ctl.sx";
connectAttr "finger_end_thumb_L_ctl_mtp.ox" "finger_end_thumb_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_thumb_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_thumb_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_thumb_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_thumb_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_thumb_R_ctl_mtp.ox" "finger_end_thumb_R_ctl.sx";
connectAttr "finger_end_thumb_R_ctl_mtp.ox" "finger_end_thumb_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_thumb_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_thumb_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_thumb_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_index_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_index_L_ctl_mtp.ox" "finger_end_index_L_ctl.sx";
connectAttr "finger_end_index_L_ctl_mtp.ox" "finger_end_index_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_index_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_index_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_index_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_index_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_index_R_ctl_mtp.ox" "finger_end_index_R_ctl.sx";
connectAttr "finger_end_index_R_ctl_mtp.ox" "finger_end_index_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_index_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_index_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_index_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_middle_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_middle_L_ctl_mtp.ox" "finger_end_middle_L_ctl.sx";
connectAttr "finger_end_middle_L_ctl_mtp.ox" "finger_end_middle_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_middle_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_middle_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_middle_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_middle_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_middle_R_ctl_mtp.ox" "finger_end_middle_R_ctl.sx";
connectAttr "finger_end_middle_R_ctl_mtp.ox" "finger_end_middle_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_middle_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_middle_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_middle_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_ring_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_ring_L_ctl_mtp.ox" "finger_end_ring_L_ctl.sx";
connectAttr "finger_end_ring_L_ctl_mtp.ox" "finger_end_ring_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_ring_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_ring_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_ring_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_ring_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_ring_R_ctl_mtp.ox" "finger_end_ring_R_ctl.sx";
connectAttr "finger_end_ring_R_ctl_mtp.ox" "finger_end_ring_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_ring_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_ring_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_ring_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_pinky_L_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_pinky_L_ctl_mtp.ox" "finger_end_pinky_L_ctl.sx";
connectAttr "finger_end_pinky_L_ctl_mtp.ox" "finger_end_pinky_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_pinky_L_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_pinky_L_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_pinky_L_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "finger_end_pinky_R_ctl.qsm_scale_weight"
		;
connectAttr "finger_end_pinky_R_ctl_mtp.ox" "finger_end_pinky_R_ctl.sx";
connectAttr "finger_end_pinky_R_ctl_mtp.ox" "finger_end_pinky_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_pinky_R_ctl_x_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_pinky_R_ctl_y_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "finger_end_pinky_R_ctl_z_Shape.v"
		;
connectAttr "skin_proxy_dgc.qsm_scale_weight" "hip_L_ctl.qsm_scale_weight";
connectAttr "hip_L_ctl_mtp.ox" "hip_L_ctl.sx";
connectAttr "hip_L_ctl_mtp.ox" "hip_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "hip_L_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "hip_L_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "hip_L_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "hip_R_ctl.qsm_scale_weight";
connectAttr "hip_R_ctl_mtp.ox" "hip_R_ctl.sx";
connectAttr "hip_R_ctl_mtp.ox" "hip_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "hip_R_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "hip_R_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "hip_R_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "knee_L_ctl.qsm_scale_weight";
connectAttr "knee_L_ctl_mtp.ox" "knee_L_ctl.sx";
connectAttr "knee_L_ctl_mtp.ox" "knee_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "knee_L_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "knee_L_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "knee_L_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "knee_R_ctl.qsm_scale_weight";
connectAttr "knee_R_ctl_mtp.ox" "knee_R_ctl.sx";
connectAttr "knee_R_ctl_mtp.ox" "knee_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "knee_R_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "knee_R_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "knee_R_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "ankle_L_ctl.qsm_scale_weight";
connectAttr "ankle_L_ctl_mtp.ox" "ankle_L_ctl.sx";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "ankle_L_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "ankle_L_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "ankle_L_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "ankle_R_ctl.qsm_scale_weight";
connectAttr "ankle_R_ctl_mtp.ox" "ankle_R_ctl.sx";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "ankle_R_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "ankle_R_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "ankle_R_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "toes_L_ctl.qsm_scale_weight";
connectAttr "toes_L_ctl_mtp.ox" "toes_L_ctl.sx";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_L_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_L_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_L_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "toes_R_ctl.qsm_scale_weight";
connectAttr "toes_R_ctl_mtp.ox" "toes_R_ctl.sx";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_R_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_R_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_R_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "toes_end_L_ctl.qsm_scale_weight";
connectAttr "toes_end_L_ctl_mtp.ox" "toes_end_L_ctl.sx";
connectAttr "toes_end_L_ctl_mtp.ox" "toes_end_L_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_end_L_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_end_L_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_end_L_ctl_z_Shape.v";
connectAttr "skin_proxy_dgc.qsm_scale_weight" "toes_end_R_ctl.qsm_scale_weight";
connectAttr "toes_end_R_ctl_mtp.ox" "toes_end_R_ctl.sx";
connectAttr "toes_end_R_ctl_mtp.ox" "toes_end_R_ctl.sy";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_end_R_ctl_x_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_end_R_ctl_y_Shape.v";
connectAttr "skin_proxy_dgc.qsm_locator_visibility" "toes_end_R_ctl_z_Shape.v";
connectAttr "finger_index_a_R_ctl.qsm_scale" "finger_index_a_R_ctl_mtp.i1x";
connectAttr "finger_index_a_R_ctl.qsm_scale_weight" "finger_index_a_R_ctl_mtp.i2x"
		;
connectAttr "finger_ring_c_R_ctl.qsm_scale" "finger_ring_c_R_ctl_mtp.i1x";
connectAttr "finger_ring_c_R_ctl.qsm_scale_weight" "finger_ring_c_R_ctl_mtp.i2x"
		;
connectAttr "finger_pinky_b_L_ctl.qsm_scale" "finger_pinky_b_L_ctl_mtp.i1x";
connectAttr "finger_pinky_b_L_ctl.qsm_scale_weight" "finger_pinky_b_L_ctl_mtp.i2x"
		;
connectAttr "finger_pinky_c_R_ctl.qsm_scale" "finger_pinky_c_R_ctl_mtp.i1x";
connectAttr "finger_pinky_c_R_ctl.qsm_scale_weight" "finger_pinky_c_R_ctl_mtp.i2x"
		;
connectAttr "finger_end_thumb_R_ctl.qsm_scale" "finger_end_thumb_R_ctl_mtp.i1x";
connectAttr "finger_end_thumb_R_ctl.qsm_scale_weight" "finger_end_thumb_R_ctl_mtp.i2x"
		;
connectAttr "finger_end_index_R_ctl.qsm_scale" "finger_end_index_R_ctl_mtp.i1x";
connectAttr "finger_end_index_R_ctl.qsm_scale_weight" "finger_end_index_R_ctl_mtp.i2x"
		;
connectAttr "finger_end_middle_L_ctl.qsm_scale" "finger_end_middle_L_ctl_mtp.i1x"
		;
connectAttr "finger_end_middle_L_ctl.qsm_scale_weight" "finger_end_middle_L_ctl_mtp.i2x"
		;
connectAttr "chest_M_ctl.qsm_scale" "chest_M_ctl_mtp.i1x";
connectAttr "chest_M_ctl.qsm_scale_weight" "chest_M_ctl_mtp.i2x";
connectAttr "finger_thumb_c_R_ctl.qsm_scale" "finger_thumb_c_R_ctl_mtp.i1x";
connectAttr "finger_thumb_c_R_ctl.qsm_scale_weight" "finger_thumb_c_R_ctl_mtp.i2x"
		;
connectAttr "finger_middle_a_L_ctl.qsm_scale" "finger_middle_a_L_ctl_mtp.i1x";
connectAttr "finger_middle_a_L_ctl.qsm_scale_weight" "finger_middle_a_L_ctl_mtp.i2x"
		;
connectAttr "finger_middle_c_L_ctl.qsm_scale" "finger_middle_c_L_ctl_mtp.i1x";
connectAttr "finger_middle_c_L_ctl.qsm_scale_weight" "finger_middle_c_L_ctl_mtp.i2x"
		;
connectAttr "shoulder_R_ctl.qsm_scale" "shoulder_R_ctl_mtp.i1x";
connectAttr "shoulder_R_ctl.qsm_scale_weight" "shoulder_R_ctl_mtp.i2x";
connectAttr "finger_ring_b_L_ctl.qsm_scale" "finger_ring_b_L_ctl_mtp.i1x";
connectAttr "finger_ring_b_L_ctl.qsm_scale_weight" "finger_ring_b_L_ctl_mtp.i2x"
		;
connectAttr "finger_end_ring_L_ctl.qsm_scale" "finger_end_ring_L_ctl_mtp.i1x";
connectAttr "finger_end_ring_L_ctl.qsm_scale_weight" "finger_end_ring_L_ctl_mtp.i2x"
		;
connectAttr "finger_middle_a_R_ctl.qsm_scale" "finger_middle_a_R_ctl_mtp.i1x";
connectAttr "finger_middle_a_R_ctl.qsm_scale_weight" "finger_middle_a_R_ctl_mtp.i2x"
		;
connectAttr "neck_M_ctl.qsm_scale" "neck_M_ctl_mtp.i1x";
connectAttr "neck_M_ctl.qsm_scale_weight" "neck_M_ctl_mtp.i2x";
connectAttr "wrist_L_ctl.qsm_scale" "wrist_L_ctl_mtp.i1x";
connectAttr "wrist_L_ctl.qsm_scale_weight" "wrist_L_ctl_mtp.i2x";
connectAttr "finger_thumb_a_R_ctl.qsm_scale" "finger_thumb_a_R_ctl_mtp.i1x";
connectAttr "finger_thumb_a_R_ctl.qsm_scale_weight" "finger_thumb_a_R_ctl_mtp.i2x"
		;
connectAttr "root_M_ctl.qsm_scale" "root_M_ctl_mtp.i1x";
connectAttr "root_M_ctl.qsm_scale_weight" "root_M_ctl_mtp.i2x";
connectAttr "scapula_R_ctl.qsm_scale" "scapula_R_ctl_mtp.i1x";
connectAttr "scapula_R_ctl.qsm_scale_weight" "scapula_R_ctl_mtp.i2x";
connectAttr "finger_thumb_b_R_ctl.qsm_scale" "finger_thumb_b_R_ctl_mtp.i1x";
connectAttr "finger_thumb_b_R_ctl.qsm_scale_weight" "finger_thumb_b_R_ctl_mtp.i2x"
		;
connectAttr "spine_b_M_ctl.qsm_scale" "spine_b_M_ctl_mtp.i1x";
connectAttr "spine_b_M_ctl.qsm_scale_weight" "spine_b_M_ctl_mtp.i2x";
connectAttr "spine_a_M_ctl.qsm_scale" "spine_a_M_ctl_mtp.i1x";
connectAttr "spine_a_M_ctl.qsm_scale_weight" "spine_a_M_ctl_mtp.i2x";
connectAttr "wrist_R_ctl.qsm_scale" "wrist_R_ctl_mtp.i1x";
connectAttr "wrist_R_ctl.qsm_scale_weight" "wrist_R_ctl_mtp.i2x";
connectAttr "finger_thumb_a_L_ctl.qsm_scale" "finger_thumb_a_L_ctl_mtp.i1x";
connectAttr "finger_thumb_a_L_ctl.qsm_scale_weight" "finger_thumb_a_L_ctl_mtp.i2x"
		;
connectAttr "finger_index_a_L_ctl.qsm_scale" "finger_index_a_L_ctl_mtp.i1x";
connectAttr "finger_index_a_L_ctl.qsm_scale_weight" "finger_index_a_L_ctl_mtp.i2x"
		;
connectAttr "finger_index_b_L_ctl.qsm_scale" "finger_index_b_L_ctl_mtp.i1x";
connectAttr "finger_index_b_L_ctl.qsm_scale_weight" "finger_index_b_L_ctl_mtp.i2x"
		;
connectAttr "finger_middle_b_L_ctl.qsm_scale" "finger_middle_b_L_ctl_mtp.i1x";
connectAttr "finger_middle_b_L_ctl.qsm_scale_weight" "finger_middle_b_L_ctl_mtp.i2x"
		;
connectAttr "finger_middle_c_R_ctl.qsm_scale" "finger_middle_c_R_ctl_mtp.i1x";
connectAttr "finger_middle_c_R_ctl.qsm_scale_weight" "finger_middle_c_R_ctl_mtp.i2x"
		;
connectAttr "head_end_M_ctl.qsm_scale" "head_end_M_ctl_mtp.i1x";
connectAttr "head_end_M_ctl.qsm_scale_weight" "head_end_M_ctl_mtp.i2x";
connectAttr "finger_ring_a_L_ctl.qsm_scale" "finger_ring_a_L_ctl_mtp.i1x";
connectAttr "finger_ring_a_L_ctl.qsm_scale_weight" "finger_ring_a_L_ctl_mtp.i2x"
		;
connectAttr "elbow_R_ctl.qsm_scale" "elbow_R_ctl_mtp.i1x";
connectAttr "elbow_R_ctl.qsm_scale_weight" "elbow_R_ctl_mtp.i2x";
connectAttr "elbow_L_ctl.qsm_scale" "elbow_L_ctl_mtp.i1x";
connectAttr "elbow_L_ctl.qsm_scale_weight" "elbow_L_ctl_mtp.i2x";
connectAttr "scapula_L_ctl.qsm_scale" "scapula_L_ctl_mtp.i1x";
connectAttr "scapula_L_ctl.qsm_scale_weight" "scapula_L_ctl_mtp.i2x";
connectAttr "finger_thumb_b_L_ctl.qsm_scale" "finger_thumb_b_L_ctl_mtp.i1x";
connectAttr "finger_thumb_b_L_ctl.qsm_scale_weight" "finger_thumb_b_L_ctl_mtp.i2x"
		;
connectAttr "finger_index_c_L_ctl.qsm_scale" "finger_index_c_L_ctl_mtp.i1x";
connectAttr "finger_index_c_L_ctl.qsm_scale_weight" "finger_index_c_L_ctl_mtp.i2x"
		;
connectAttr "finger_middle_b_R_ctl.qsm_scale" "finger_middle_b_R_ctl_mtp.i1x";
connectAttr "finger_middle_b_R_ctl.qsm_scale_weight" "finger_middle_b_R_ctl_mtp.i2x"
		;
connectAttr "finger_ring_a_R_ctl.qsm_scale" "finger_ring_a_R_ctl_mtp.i1x";
connectAttr "finger_ring_a_R_ctl.qsm_scale_weight" "finger_ring_a_R_ctl_mtp.i2x"
		;
connectAttr "head_M_ctl.qsm_scale" "head_M_ctl_mtp.i1x";
connectAttr "head_M_ctl.qsm_scale_weight" "head_M_ctl_mtp.i2x";
connectAttr "finger_index_b_R_ctl.qsm_scale" "finger_index_b_R_ctl_mtp.i1x";
connectAttr "finger_index_b_R_ctl.qsm_scale_weight" "finger_index_b_R_ctl_mtp.i2x"
		;
connectAttr "shoulder_L_ctl.qsm_scale" "shoulder_L_ctl_mtp.i1x";
connectAttr "shoulder_L_ctl.qsm_scale_weight" "shoulder_L_ctl_mtp.i2x";
connectAttr "finger_index_c_R_ctl.qsm_scale" "finger_index_c_R_ctl_mtp.i1x";
connectAttr "finger_index_c_R_ctl.qsm_scale_weight" "finger_index_c_R_ctl_mtp.i2x"
		;
connectAttr "finger_thumb_c_L_ctl.qsm_scale" "finger_thumb_c_L_ctl_mtp.i1x";
connectAttr "finger_thumb_c_L_ctl.qsm_scale_weight" "finger_thumb_c_L_ctl_mtp.i2x"
		;
connectAttr "finger_ring_b_R_ctl.qsm_scale" "finger_ring_b_R_ctl_mtp.i1x";
connectAttr "finger_ring_b_R_ctl.qsm_scale_weight" "finger_ring_b_R_ctl_mtp.i2x"
		;
connectAttr "finger_ring_c_L_ctl.qsm_scale" "finger_ring_c_L_ctl_mtp.i1x";
connectAttr "finger_ring_c_L_ctl.qsm_scale_weight" "finger_ring_c_L_ctl_mtp.i2x"
		;
connectAttr "finger_pinky_a_L_ctl.qsm_scale" "finger_pinky_a_L_ctl_mtp.i1x";
connectAttr "finger_pinky_a_L_ctl.qsm_scale_weight" "finger_pinky_a_L_ctl_mtp.i2x"
		;
connectAttr "finger_pinky_a_R_ctl.qsm_scale" "finger_pinky_a_R_ctl_mtp.i1x";
connectAttr "finger_pinky_a_R_ctl.qsm_scale_weight" "finger_pinky_a_R_ctl_mtp.i2x"
		;
connectAttr "finger_pinky_b_R_ctl.qsm_scale" "finger_pinky_b_R_ctl_mtp.i1x";
connectAttr "finger_pinky_b_R_ctl.qsm_scale_weight" "finger_pinky_b_R_ctl_mtp.i2x"
		;
connectAttr "finger_pinky_c_L_ctl.qsm_scale" "finger_pinky_c_L_ctl_mtp.i1x";
connectAttr "finger_pinky_c_L_ctl.qsm_scale_weight" "finger_pinky_c_L_ctl_mtp.i2x"
		;
connectAttr "finger_end_thumb_L_ctl.qsm_scale" "finger_end_thumb_L_ctl_mtp.i1x";
connectAttr "finger_end_thumb_L_ctl.qsm_scale_weight" "finger_end_thumb_L_ctl_mtp.i2x"
		;
connectAttr "finger_end_index_L_ctl.qsm_scale" "finger_end_index_L_ctl_mtp.i1x";
connectAttr "finger_end_index_L_ctl.qsm_scale_weight" "finger_end_index_L_ctl_mtp.i2x"
		;
connectAttr "finger_end_middle_R_ctl.qsm_scale" "finger_end_middle_R_ctl_mtp.i1x"
		;
connectAttr "finger_end_middle_R_ctl.qsm_scale_weight" "finger_end_middle_R_ctl_mtp.i2x"
		;
connectAttr "hip_L_ctl.qsm_scale" "hip_L_ctl_mtp.i1x";
connectAttr "hip_L_ctl.qsm_scale_weight" "hip_L_ctl_mtp.i2x";
connectAttr "finger_end_pinky_R_ctl.qsm_scale" "finger_end_pinky_R_ctl_mtp.i1x";
connectAttr "finger_end_pinky_R_ctl.qsm_scale_weight" "finger_end_pinky_R_ctl_mtp.i2x"
		;
connectAttr "knee_R_ctl.qsm_scale" "knee_R_ctl_mtp.i1x";
connectAttr "knee_R_ctl.qsm_scale_weight" "knee_R_ctl_mtp.i2x";
connectAttr "toes_R_ctl.qsm_scale" "toes_R_ctl_mtp.i1x";
connectAttr "toes_R_ctl.qsm_scale_weight" "toes_R_ctl_mtp.i2x";
connectAttr "toes_end_R_ctl.qsm_scale" "toes_end_R_ctl_mtp.i1x";
connectAttr "toes_end_R_ctl.qsm_scale_weight" "toes_end_R_ctl_mtp.i2x";
connectAttr "finger_end_ring_R_ctl.qsm_scale" "finger_end_ring_R_ctl_mtp.i1x";
connectAttr "finger_end_ring_R_ctl.qsm_scale_weight" "finger_end_ring_R_ctl_mtp.i2x"
		;
connectAttr "finger_end_pinky_L_ctl.qsm_scale" "finger_end_pinky_L_ctl_mtp.i1x";
connectAttr "finger_end_pinky_L_ctl.qsm_scale_weight" "finger_end_pinky_L_ctl_mtp.i2x"
		;
connectAttr "toes_L_ctl.qsm_scale" "toes_L_ctl_mtp.i1x";
connectAttr "toes_L_ctl.qsm_scale_weight" "toes_L_ctl_mtp.i2x";
connectAttr "ankle_L_ctl.qsm_scale" "ankle_L_ctl_mtp.i1x";
connectAttr "ankle_L_ctl.qsm_scale_weight" "ankle_L_ctl_mtp.i2x";
connectAttr "hip_R_ctl.qsm_scale" "hip_R_ctl_mtp.i1x";
connectAttr "hip_R_ctl.qsm_scale_weight" "hip_R_ctl_mtp.i2x";
connectAttr "toes_end_L_ctl.qsm_scale" "toes_end_L_ctl_mtp.i1x";
connectAttr "toes_end_L_ctl.qsm_scale_weight" "toes_end_L_ctl_mtp.i2x";
connectAttr "knee_L_ctl.qsm_scale" "knee_L_ctl_mtp.i1x";
connectAttr "knee_L_ctl.qsm_scale_weight" "knee_L_ctl_mtp.i2x";
connectAttr "ankle_R_ctl.qsm_scale" "ankle_R_ctl_mtp.i1x";
connectAttr "ankle_R_ctl.qsm_scale_weight" "ankle_R_ctl_mtp.i2x";
connectAttr "root_M_grp.msg" "hyperLayout1.hyp[0].dn";
connectAttr "root_M_ctl.msg" "hyperLayout1.hyp[1].dn";
connectAttr "root_M_ctl_x_Shape.msg" "hyperLayout1.hyp[2].dn";
connectAttr "root_M_ctl_y_Shape.msg" "hyperLayout1.hyp[3].dn";
connectAttr "root_M_ctl_z_Shape.msg" "hyperLayout1.hyp[4].dn";
connectAttr "spine_a_M_grp.msg" "hyperLayout1.hyp[5].dn";
connectAttr "spine_a_M_ctl.msg" "hyperLayout1.hyp[6].dn";
connectAttr "spine_a_M_ctl_x_Shape.msg" "hyperLayout1.hyp[7].dn";
connectAttr "spine_a_M_ctl_y_Shape.msg" "hyperLayout1.hyp[8].dn";
connectAttr "spine_a_M_ctl_z_Shape.msg" "hyperLayout1.hyp[9].dn";
connectAttr "spine_b_M_grp.msg" "hyperLayout1.hyp[10].dn";
connectAttr "spine_b_M_ctl.msg" "hyperLayout1.hyp[11].dn";
connectAttr "spine_b_M_ctl_x_Shape.msg" "hyperLayout1.hyp[12].dn";
connectAttr "spine_b_M_ctl_y_Shape.msg" "hyperLayout1.hyp[13].dn";
connectAttr "spine_b_M_ctl_z_Shape.msg" "hyperLayout1.hyp[14].dn";
connectAttr "chest_M_grp.msg" "hyperLayout1.hyp[15].dn";
connectAttr "chest_M_ctl.msg" "hyperLayout1.hyp[16].dn";
connectAttr "chest_M_ctl_x_Shape.msg" "hyperLayout1.hyp[17].dn";
connectAttr "chest_M_ctl_y_Shape.msg" "hyperLayout1.hyp[18].dn";
connectAttr "chest_M_ctl_z_Shape.msg" "hyperLayout1.hyp[19].dn";
connectAttr "neck_M_grp.msg" "hyperLayout1.hyp[20].dn";
connectAttr "neck_M_ctl.msg" "hyperLayout1.hyp[21].dn";
connectAttr "neck_M_ctl_x_Shape.msg" "hyperLayout1.hyp[22].dn";
connectAttr "neck_M_ctl_y_Shape.msg" "hyperLayout1.hyp[23].dn";
connectAttr "neck_M_ctl_z_Shape.msg" "hyperLayout1.hyp[24].dn";
connectAttr "head_M_grp.msg" "hyperLayout1.hyp[25].dn";
connectAttr "head_M_ctl.msg" "hyperLayout1.hyp[26].dn";
connectAttr "head_M_ctl_x_Shape.msg" "hyperLayout1.hyp[27].dn";
connectAttr "head_M_ctl_y_Shape.msg" "hyperLayout1.hyp[28].dn";
connectAttr "head_M_ctl_z_Shape.msg" "hyperLayout1.hyp[29].dn";
connectAttr "head_end_M_grp.msg" "hyperLayout1.hyp[30].dn";
connectAttr "head_end_M_ctl.msg" "hyperLayout1.hyp[31].dn";
connectAttr "head_end_M_ctl_x_Shape.msg" "hyperLayout1.hyp[32].dn";
connectAttr "head_end_M_ctl_y_Shape.msg" "hyperLayout1.hyp[33].dn";
connectAttr "head_end_M_ctl_z_Shape.msg" "hyperLayout1.hyp[34].dn";
connectAttr "scapula_L_grp.msg" "hyperLayout1.hyp[35].dn";
connectAttr "scapula_L_ctl.msg" "hyperLayout1.hyp[36].dn";
connectAttr "scapula_L_ctl_x_Shape.msg" "hyperLayout1.hyp[37].dn";
connectAttr "scapula_L_ctl_y_Shape.msg" "hyperLayout1.hyp[38].dn";
connectAttr "scapula_L_ctl_z_Shape.msg" "hyperLayout1.hyp[39].dn";
connectAttr "scapula_R_grp.msg" "hyperLayout1.hyp[40].dn";
connectAttr "scapula_R_ctl.msg" "hyperLayout1.hyp[41].dn";
connectAttr "scapula_R_ctl_x_Shape.msg" "hyperLayout1.hyp[42].dn";
connectAttr "scapula_R_ctl_y_Shape.msg" "hyperLayout1.hyp[43].dn";
connectAttr "scapula_R_ctl_z_Shape.msg" "hyperLayout1.hyp[44].dn";
connectAttr "shoulder_L_grp.msg" "hyperLayout1.hyp[45].dn";
connectAttr "shoulder_L_ctl.msg" "hyperLayout1.hyp[46].dn";
connectAttr "shoulder_L_ctl_x_Shape.msg" "hyperLayout1.hyp[47].dn";
connectAttr "shoulder_L_ctl_y_Shape.msg" "hyperLayout1.hyp[48].dn";
connectAttr "shoulder_L_ctl_z_Shape.msg" "hyperLayout1.hyp[49].dn";
connectAttr "shoulder_R_grp.msg" "hyperLayout1.hyp[50].dn";
connectAttr "shoulder_R_ctl.msg" "hyperLayout1.hyp[51].dn";
connectAttr "shoulder_R_ctl_x_Shape.msg" "hyperLayout1.hyp[52].dn";
connectAttr "shoulder_R_ctl_y_Shape.msg" "hyperLayout1.hyp[53].dn";
connectAttr "shoulder_R_ctl_z_Shape.msg" "hyperLayout1.hyp[54].dn";
connectAttr "elbow_L_grp.msg" "hyperLayout1.hyp[55].dn";
connectAttr "elbow_L_ctl.msg" "hyperLayout1.hyp[56].dn";
connectAttr "elbow_L_ctl_x_Shape.msg" "hyperLayout1.hyp[57].dn";
connectAttr "elbow_L_ctl_y_Shape.msg" "hyperLayout1.hyp[58].dn";
connectAttr "elbow_L_ctl_z_Shape.msg" "hyperLayout1.hyp[59].dn";
connectAttr "elbow_R_grp.msg" "hyperLayout1.hyp[60].dn";
connectAttr "elbow_R_ctl.msg" "hyperLayout1.hyp[61].dn";
connectAttr "elbow_R_ctl_x_Shape.msg" "hyperLayout1.hyp[62].dn";
connectAttr "elbow_R_ctl_y_Shape.msg" "hyperLayout1.hyp[63].dn";
connectAttr "elbow_R_ctl_z_Shape.msg" "hyperLayout1.hyp[64].dn";
connectAttr "wrist_L_grp.msg" "hyperLayout1.hyp[65].dn";
connectAttr "wrist_L_ctl.msg" "hyperLayout1.hyp[66].dn";
connectAttr "wrist_L_ctl_x_Shape.msg" "hyperLayout1.hyp[67].dn";
connectAttr "wrist_L_ctl_y_Shape.msg" "hyperLayout1.hyp[68].dn";
connectAttr "wrist_L_ctl_z_Shape.msg" "hyperLayout1.hyp[69].dn";
connectAttr "wrist_R_grp.msg" "hyperLayout1.hyp[70].dn";
connectAttr "wrist_R_ctl.msg" "hyperLayout1.hyp[71].dn";
connectAttr "wrist_R_ctl_x_Shape.msg" "hyperLayout1.hyp[72].dn";
connectAttr "wrist_R_ctl_y_Shape.msg" "hyperLayout1.hyp[73].dn";
connectAttr "wrist_R_ctl_z_Shape.msg" "hyperLayout1.hyp[74].dn";
connectAttr "finger_thumb_a_L_grp.msg" "hyperLayout1.hyp[75].dn";
connectAttr "finger_thumb_a_L_ctl.msg" "hyperLayout1.hyp[76].dn";
connectAttr "finger_thumb_a_L_ctl_x_Shape.msg" "hyperLayout1.hyp[77].dn";
connectAttr "finger_thumb_a_L_ctl_y_Shape.msg" "hyperLayout1.hyp[78].dn";
connectAttr "finger_thumb_a_L_ctl_z_Shape.msg" "hyperLayout1.hyp[79].dn";
connectAttr "finger_thumb_a_R_grp.msg" "hyperLayout1.hyp[80].dn";
connectAttr "finger_thumb_a_R_ctl.msg" "hyperLayout1.hyp[81].dn";
connectAttr "finger_thumb_a_R_ctl_x_Shape.msg" "hyperLayout1.hyp[82].dn";
connectAttr "finger_thumb_a_R_ctl_y_Shape.msg" "hyperLayout1.hyp[83].dn";
connectAttr "finger_thumb_a_R_ctl_z_Shape.msg" "hyperLayout1.hyp[84].dn";
connectAttr "finger_thumb_b_L_grp.msg" "hyperLayout1.hyp[85].dn";
connectAttr "finger_thumb_b_L_ctl.msg" "hyperLayout1.hyp[86].dn";
connectAttr "finger_thumb_b_L_ctl_x_Shape.msg" "hyperLayout1.hyp[87].dn";
connectAttr "finger_thumb_b_L_ctl_y_Shape.msg" "hyperLayout1.hyp[88].dn";
connectAttr "finger_thumb_b_L_ctl_z_Shape.msg" "hyperLayout1.hyp[89].dn";
connectAttr "finger_thumb_b_R_grp.msg" "hyperLayout1.hyp[90].dn";
connectAttr "finger_thumb_b_R_ctl.msg" "hyperLayout1.hyp[91].dn";
connectAttr "finger_thumb_b_R_ctl_x_Shape.msg" "hyperLayout1.hyp[92].dn";
connectAttr "finger_thumb_b_R_ctl_y_Shape.msg" "hyperLayout1.hyp[93].dn";
connectAttr "finger_thumb_b_R_ctl_z_Shape.msg" "hyperLayout1.hyp[94].dn";
connectAttr "finger_thumb_c_L_grp.msg" "hyperLayout1.hyp[95].dn";
connectAttr "finger_thumb_c_L_ctl.msg" "hyperLayout1.hyp[96].dn";
connectAttr "finger_thumb_c_L_ctl_x_Shape.msg" "hyperLayout1.hyp[97].dn";
connectAttr "finger_thumb_c_L_ctl_y_Shape.msg" "hyperLayout1.hyp[98].dn";
connectAttr "finger_thumb_c_L_ctl_z_Shape.msg" "hyperLayout1.hyp[99].dn";
connectAttr "finger_thumb_c_R_grp.msg" "hyperLayout1.hyp[100].dn";
connectAttr "finger_thumb_c_R_ctl.msg" "hyperLayout1.hyp[101].dn";
connectAttr "finger_thumb_c_R_ctl_x_Shape.msg" "hyperLayout1.hyp[102].dn";
connectAttr "finger_thumb_c_R_ctl_y_Shape.msg" "hyperLayout1.hyp[103].dn";
connectAttr "finger_thumb_c_R_ctl_z_Shape.msg" "hyperLayout1.hyp[104].dn";
connectAttr "finger_index_a_L_grp.msg" "hyperLayout1.hyp[105].dn";
connectAttr "finger_index_a_L_ctl.msg" "hyperLayout1.hyp[106].dn";
connectAttr "finger_index_a_L_ctl_x_Shape.msg" "hyperLayout1.hyp[107].dn";
connectAttr "finger_index_a_L_ctl_y_Shape.msg" "hyperLayout1.hyp[108].dn";
connectAttr "finger_index_a_L_ctl_z_Shape.msg" "hyperLayout1.hyp[109].dn";
connectAttr "finger_index_a_R_grp.msg" "hyperLayout1.hyp[110].dn";
connectAttr "finger_index_a_R_ctl.msg" "hyperLayout1.hyp[111].dn";
connectAttr "finger_index_a_R_ctl_x_Shape.msg" "hyperLayout1.hyp[112].dn";
connectAttr "finger_index_a_R_ctl_y_Shape.msg" "hyperLayout1.hyp[113].dn";
connectAttr "finger_index_a_R_ctl_z_Shape.msg" "hyperLayout1.hyp[114].dn";
connectAttr "finger_index_b_L_grp.msg" "hyperLayout1.hyp[115].dn";
connectAttr "finger_index_b_L_ctl.msg" "hyperLayout1.hyp[116].dn";
connectAttr "finger_index_b_L_ctl_x_Shape.msg" "hyperLayout1.hyp[117].dn";
connectAttr "finger_index_b_L_ctl_y_Shape.msg" "hyperLayout1.hyp[118].dn";
connectAttr "finger_index_b_L_ctl_z_Shape.msg" "hyperLayout1.hyp[119].dn";
connectAttr "finger_index_b_R_grp.msg" "hyperLayout1.hyp[120].dn";
connectAttr "finger_index_b_R_ctl.msg" "hyperLayout1.hyp[121].dn";
connectAttr "finger_index_b_R_ctl_x_Shape.msg" "hyperLayout1.hyp[122].dn";
connectAttr "finger_index_b_R_ctl_y_Shape.msg" "hyperLayout1.hyp[123].dn";
connectAttr "finger_index_b_R_ctl_z_Shape.msg" "hyperLayout1.hyp[124].dn";
connectAttr "finger_index_c_L_grp.msg" "hyperLayout1.hyp[125].dn";
connectAttr "finger_index_c_L_ctl.msg" "hyperLayout1.hyp[126].dn";
connectAttr "finger_index_c_L_ctl_x_Shape.msg" "hyperLayout1.hyp[127].dn";
connectAttr "finger_index_c_L_ctl_y_Shape.msg" "hyperLayout1.hyp[128].dn";
connectAttr "finger_index_c_L_ctl_z_Shape.msg" "hyperLayout1.hyp[129].dn";
connectAttr "finger_index_c_R_grp.msg" "hyperLayout1.hyp[130].dn";
connectAttr "finger_index_c_R_ctl.msg" "hyperLayout1.hyp[131].dn";
connectAttr "finger_index_c_R_ctl_x_Shape.msg" "hyperLayout1.hyp[132].dn";
connectAttr "finger_index_c_R_ctl_y_Shape.msg" "hyperLayout1.hyp[133].dn";
connectAttr "finger_index_c_R_ctl_z_Shape.msg" "hyperLayout1.hyp[134].dn";
connectAttr "finger_middle_a_L_grp.msg" "hyperLayout1.hyp[135].dn";
connectAttr "finger_middle_a_L_ctl.msg" "hyperLayout1.hyp[136].dn";
connectAttr "finger_middle_a_L_ctl_x_Shape.msg" "hyperLayout1.hyp[137].dn";
connectAttr "finger_middle_a_L_ctl_y_Shape.msg" "hyperLayout1.hyp[138].dn";
connectAttr "finger_middle_a_L_ctl_z_Shape.msg" "hyperLayout1.hyp[139].dn";
connectAttr "finger_middle_a_R_grp.msg" "hyperLayout1.hyp[140].dn";
connectAttr "finger_middle_a_R_ctl.msg" "hyperLayout1.hyp[141].dn";
connectAttr "finger_middle_a_R_ctl_x_Shape.msg" "hyperLayout1.hyp[142].dn";
connectAttr "finger_middle_a_R_ctl_y_Shape.msg" "hyperLayout1.hyp[143].dn";
connectAttr "finger_middle_a_R_ctl_z_Shape.msg" "hyperLayout1.hyp[144].dn";
connectAttr "finger_middle_b_L_grp.msg" "hyperLayout1.hyp[145].dn";
connectAttr "finger_middle_b_L_ctl.msg" "hyperLayout1.hyp[146].dn";
connectAttr "finger_middle_b_L_ctl_x_Shape.msg" "hyperLayout1.hyp[147].dn";
connectAttr "finger_middle_b_L_ctl_y_Shape.msg" "hyperLayout1.hyp[148].dn";
connectAttr "finger_middle_b_L_ctl_z_Shape.msg" "hyperLayout1.hyp[149].dn";
connectAttr "finger_middle_b_R_grp.msg" "hyperLayout1.hyp[150].dn";
connectAttr "finger_middle_b_R_ctl.msg" "hyperLayout1.hyp[151].dn";
connectAttr "finger_middle_b_R_ctl_x_Shape.msg" "hyperLayout1.hyp[152].dn";
connectAttr "finger_middle_b_R_ctl_y_Shape.msg" "hyperLayout1.hyp[153].dn";
connectAttr "finger_middle_b_R_ctl_z_Shape.msg" "hyperLayout1.hyp[154].dn";
connectAttr "finger_middle_c_L_grp.msg" "hyperLayout1.hyp[155].dn";
connectAttr "finger_middle_c_L_ctl.msg" "hyperLayout1.hyp[156].dn";
connectAttr "finger_middle_c_L_ctl_x_Shape.msg" "hyperLayout1.hyp[157].dn";
connectAttr "finger_middle_c_L_ctl_y_Shape.msg" "hyperLayout1.hyp[158].dn";
connectAttr "finger_middle_c_L_ctl_z_Shape.msg" "hyperLayout1.hyp[159].dn";
connectAttr "finger_middle_c_R_grp.msg" "hyperLayout1.hyp[160].dn";
connectAttr "finger_middle_c_R_ctl.msg" "hyperLayout1.hyp[161].dn";
connectAttr "finger_middle_c_R_ctl_x_Shape.msg" "hyperLayout1.hyp[162].dn";
connectAttr "finger_middle_c_R_ctl_y_Shape.msg" "hyperLayout1.hyp[163].dn";
connectAttr "finger_middle_c_R_ctl_z_Shape.msg" "hyperLayout1.hyp[164].dn";
connectAttr "finger_ring_a_L_grp.msg" "hyperLayout1.hyp[165].dn";
connectAttr "finger_ring_a_L_ctl.msg" "hyperLayout1.hyp[166].dn";
connectAttr "finger_ring_a_L_ctl_x_Shape.msg" "hyperLayout1.hyp[167].dn";
connectAttr "finger_ring_a_L_ctl_y_Shape.msg" "hyperLayout1.hyp[168].dn";
connectAttr "finger_ring_a_L_ctl_z_Shape.msg" "hyperLayout1.hyp[169].dn";
connectAttr "finger_ring_a_R_grp.msg" "hyperLayout1.hyp[170].dn";
connectAttr "finger_ring_a_R_ctl.msg" "hyperLayout1.hyp[171].dn";
connectAttr "finger_ring_a_R_ctl_x_Shape.msg" "hyperLayout1.hyp[172].dn";
connectAttr "finger_ring_a_R_ctl_y_Shape.msg" "hyperLayout1.hyp[173].dn";
connectAttr "finger_ring_a_R_ctl_z_Shape.msg" "hyperLayout1.hyp[174].dn";
connectAttr "finger_ring_b_L_grp.msg" "hyperLayout1.hyp[175].dn";
connectAttr "finger_ring_b_L_ctl.msg" "hyperLayout1.hyp[176].dn";
connectAttr "finger_ring_b_L_ctl_x_Shape.msg" "hyperLayout1.hyp[177].dn";
connectAttr "finger_ring_b_L_ctl_y_Shape.msg" "hyperLayout1.hyp[178].dn";
connectAttr "finger_ring_b_L_ctl_z_Shape.msg" "hyperLayout1.hyp[179].dn";
connectAttr "finger_ring_b_R_grp.msg" "hyperLayout1.hyp[180].dn";
connectAttr "finger_ring_b_R_ctl.msg" "hyperLayout1.hyp[181].dn";
connectAttr "finger_ring_b_R_ctl_x_Shape.msg" "hyperLayout1.hyp[182].dn";
connectAttr "finger_ring_b_R_ctl_y_Shape.msg" "hyperLayout1.hyp[183].dn";
connectAttr "finger_ring_b_R_ctl_z_Shape.msg" "hyperLayout1.hyp[184].dn";
connectAttr "finger_ring_c_L_grp.msg" "hyperLayout1.hyp[185].dn";
connectAttr "finger_ring_c_L_ctl.msg" "hyperLayout1.hyp[186].dn";
connectAttr "finger_ring_c_L_ctl_x_Shape.msg" "hyperLayout1.hyp[187].dn";
connectAttr "finger_ring_c_L_ctl_y_Shape.msg" "hyperLayout1.hyp[188].dn";
connectAttr "finger_ring_c_L_ctl_z_Shape.msg" "hyperLayout1.hyp[189].dn";
connectAttr "finger_ring_c_R_grp.msg" "hyperLayout1.hyp[190].dn";
connectAttr "finger_ring_c_R_ctl.msg" "hyperLayout1.hyp[191].dn";
connectAttr "finger_ring_c_R_ctl_x_Shape.msg" "hyperLayout1.hyp[192].dn";
connectAttr "finger_ring_c_R_ctl_y_Shape.msg" "hyperLayout1.hyp[193].dn";
connectAttr "finger_ring_c_R_ctl_z_Shape.msg" "hyperLayout1.hyp[194].dn";
connectAttr "finger_pinky_a_L_grp.msg" "hyperLayout1.hyp[195].dn";
connectAttr "finger_pinky_a_L_ctl.msg" "hyperLayout1.hyp[196].dn";
connectAttr "finger_pinky_a_L_ctl_x_Shape.msg" "hyperLayout1.hyp[197].dn";
connectAttr "finger_pinky_a_L_ctl_y_Shape.msg" "hyperLayout1.hyp[198].dn";
connectAttr "finger_pinky_a_L_ctl_z_Shape.msg" "hyperLayout1.hyp[199].dn";
connectAttr "finger_pinky_a_R_grp.msg" "hyperLayout1.hyp[200].dn";
connectAttr "finger_pinky_a_R_ctl.msg" "hyperLayout1.hyp[201].dn";
connectAttr "finger_pinky_a_R_ctl_x_Shape.msg" "hyperLayout1.hyp[202].dn";
connectAttr "finger_pinky_a_R_ctl_y_Shape.msg" "hyperLayout1.hyp[203].dn";
connectAttr "finger_pinky_a_R_ctl_z_Shape.msg" "hyperLayout1.hyp[204].dn";
connectAttr "finger_pinky_b_L_grp.msg" "hyperLayout1.hyp[205].dn";
connectAttr "finger_pinky_b_L_ctl.msg" "hyperLayout1.hyp[206].dn";
connectAttr "finger_pinky_b_L_ctl_x_Shape.msg" "hyperLayout1.hyp[207].dn";
connectAttr "finger_pinky_b_L_ctl_y_Shape.msg" "hyperLayout1.hyp[208].dn";
connectAttr "finger_pinky_b_L_ctl_z_Shape.msg" "hyperLayout1.hyp[209].dn";
connectAttr "finger_pinky_b_R_grp.msg" "hyperLayout1.hyp[210].dn";
connectAttr "finger_pinky_b_R_ctl.msg" "hyperLayout1.hyp[211].dn";
connectAttr "finger_pinky_b_R_ctl_x_Shape.msg" "hyperLayout1.hyp[212].dn";
connectAttr "finger_pinky_b_R_ctl_y_Shape.msg" "hyperLayout1.hyp[213].dn";
connectAttr "finger_pinky_b_R_ctl_z_Shape.msg" "hyperLayout1.hyp[214].dn";
connectAttr "finger_pinky_c_L_grp.msg" "hyperLayout1.hyp[215].dn";
connectAttr "finger_pinky_c_L_ctl.msg" "hyperLayout1.hyp[216].dn";
connectAttr "finger_pinky_c_L_ctl_x_Shape.msg" "hyperLayout1.hyp[217].dn";
connectAttr "finger_pinky_c_L_ctl_y_Shape.msg" "hyperLayout1.hyp[218].dn";
connectAttr "finger_pinky_c_L_ctl_z_Shape.msg" "hyperLayout1.hyp[219].dn";
connectAttr "finger_pinky_c_R_grp.msg" "hyperLayout1.hyp[220].dn";
connectAttr "finger_pinky_c_R_ctl.msg" "hyperLayout1.hyp[221].dn";
connectAttr "finger_pinky_c_R_ctl_x_Shape.msg" "hyperLayout1.hyp[222].dn";
connectAttr "finger_pinky_c_R_ctl_y_Shape.msg" "hyperLayout1.hyp[223].dn";
connectAttr "finger_pinky_c_R_ctl_z_Shape.msg" "hyperLayout1.hyp[224].dn";
connectAttr "finger_end_thumb_L_grp.msg" "hyperLayout1.hyp[225].dn";
connectAttr "finger_end_thumb_L_ctl.msg" "hyperLayout1.hyp[226].dn";
connectAttr "finger_end_thumb_L_ctl_x_Shape.msg" "hyperLayout1.hyp[227].dn";
connectAttr "finger_end_thumb_L_ctl_y_Shape.msg" "hyperLayout1.hyp[228].dn";
connectAttr "finger_end_thumb_L_ctl_z_Shape.msg" "hyperLayout1.hyp[229].dn";
connectAttr "finger_end_thumb_R_grp.msg" "hyperLayout1.hyp[230].dn";
connectAttr "finger_end_thumb_R_ctl.msg" "hyperLayout1.hyp[231].dn";
connectAttr "finger_end_thumb_R_ctl_x_Shape.msg" "hyperLayout1.hyp[232].dn";
connectAttr "finger_end_thumb_R_ctl_y_Shape.msg" "hyperLayout1.hyp[233].dn";
connectAttr "finger_end_thumb_R_ctl_z_Shape.msg" "hyperLayout1.hyp[234].dn";
connectAttr "finger_end_index_L_grp.msg" "hyperLayout1.hyp[235].dn";
connectAttr "finger_end_index_L_ctl.msg" "hyperLayout1.hyp[236].dn";
connectAttr "finger_end_index_L_ctl_x_Shape.msg" "hyperLayout1.hyp[237].dn";
connectAttr "finger_end_index_L_ctl_y_Shape.msg" "hyperLayout1.hyp[238].dn";
connectAttr "finger_end_index_L_ctl_z_Shape.msg" "hyperLayout1.hyp[239].dn";
connectAttr "finger_end_index_R_grp.msg" "hyperLayout1.hyp[240].dn";
connectAttr "finger_end_index_R_ctl.msg" "hyperLayout1.hyp[241].dn";
connectAttr "finger_end_index_R_ctl_x_Shape.msg" "hyperLayout1.hyp[242].dn";
connectAttr "finger_end_index_R_ctl_y_Shape.msg" "hyperLayout1.hyp[243].dn";
connectAttr "finger_end_index_R_ctl_z_Shape.msg" "hyperLayout1.hyp[244].dn";
connectAttr "finger_end_middle_L_grp.msg" "hyperLayout1.hyp[245].dn";
connectAttr "finger_end_middle_L_ctl.msg" "hyperLayout1.hyp[246].dn";
connectAttr "finger_end_middle_L_ctl_x_Shape.msg" "hyperLayout1.hyp[247].dn";
connectAttr "finger_end_middle_L_ctl_y_Shape.msg" "hyperLayout1.hyp[248].dn";
connectAttr "finger_end_middle_L_ctl_z_Shape.msg" "hyperLayout1.hyp[249].dn";
connectAttr "finger_end_middle_R_grp.msg" "hyperLayout1.hyp[250].dn";
connectAttr "finger_end_middle_R_ctl.msg" "hyperLayout1.hyp[251].dn";
connectAttr "finger_end_middle_R_ctl_x_Shape.msg" "hyperLayout1.hyp[252].dn";
connectAttr "finger_end_middle_R_ctl_y_Shape.msg" "hyperLayout1.hyp[253].dn";
connectAttr "finger_end_middle_R_ctl_z_Shape.msg" "hyperLayout1.hyp[254].dn";
connectAttr "finger_end_ring_L_grp.msg" "hyperLayout1.hyp[255].dn";
connectAttr "finger_end_ring_L_ctl.msg" "hyperLayout1.hyp[256].dn";
connectAttr "finger_end_ring_L_ctl_x_Shape.msg" "hyperLayout1.hyp[257].dn";
connectAttr "finger_end_ring_L_ctl_y_Shape.msg" "hyperLayout1.hyp[258].dn";
connectAttr "finger_end_ring_L_ctl_z_Shape.msg" "hyperLayout1.hyp[259].dn";
connectAttr "finger_end_ring_R_grp.msg" "hyperLayout1.hyp[260].dn";
connectAttr "finger_end_ring_R_ctl.msg" "hyperLayout1.hyp[261].dn";
connectAttr "finger_end_ring_R_ctl_x_Shape.msg" "hyperLayout1.hyp[262].dn";
connectAttr "finger_end_ring_R_ctl_y_Shape.msg" "hyperLayout1.hyp[263].dn";
connectAttr "finger_end_ring_R_ctl_z_Shape.msg" "hyperLayout1.hyp[264].dn";
connectAttr "finger_end_pinky_L_grp.msg" "hyperLayout1.hyp[265].dn";
connectAttr "finger_end_pinky_L_ctl.msg" "hyperLayout1.hyp[266].dn";
connectAttr "finger_end_pinky_L_ctl_x_Shape.msg" "hyperLayout1.hyp[267].dn";
connectAttr "finger_end_pinky_L_ctl_y_Shape.msg" "hyperLayout1.hyp[268].dn";
connectAttr "finger_end_pinky_L_ctl_z_Shape.msg" "hyperLayout1.hyp[269].dn";
connectAttr "finger_end_pinky_R_grp.msg" "hyperLayout1.hyp[270].dn";
connectAttr "finger_end_pinky_R_ctl.msg" "hyperLayout1.hyp[271].dn";
connectAttr "finger_end_pinky_R_ctl_x_Shape.msg" "hyperLayout1.hyp[272].dn";
connectAttr "finger_end_pinky_R_ctl_y_Shape.msg" "hyperLayout1.hyp[273].dn";
connectAttr "finger_end_pinky_R_ctl_z_Shape.msg" "hyperLayout1.hyp[274].dn";
connectAttr "hip_L_grp.msg" "hyperLayout1.hyp[275].dn";
connectAttr "hip_L_ctl.msg" "hyperLayout1.hyp[276].dn";
connectAttr "hip_L_ctl_x_Shape.msg" "hyperLayout1.hyp[277].dn";
connectAttr "hip_L_ctl_y_Shape.msg" "hyperLayout1.hyp[278].dn";
connectAttr "hip_L_ctl_z_Shape.msg" "hyperLayout1.hyp[279].dn";
connectAttr "hip_R_grp.msg" "hyperLayout1.hyp[280].dn";
connectAttr "hip_R_ctl.msg" "hyperLayout1.hyp[281].dn";
connectAttr "hip_R_ctl_x_Shape.msg" "hyperLayout1.hyp[282].dn";
connectAttr "hip_R_ctl_y_Shape.msg" "hyperLayout1.hyp[283].dn";
connectAttr "hip_R_ctl_z_Shape.msg" "hyperLayout1.hyp[284].dn";
connectAttr "knee_L_grp.msg" "hyperLayout1.hyp[285].dn";
connectAttr "knee_L_ctl.msg" "hyperLayout1.hyp[286].dn";
connectAttr "knee_L_ctl_x_Shape.msg" "hyperLayout1.hyp[287].dn";
connectAttr "knee_L_ctl_y_Shape.msg" "hyperLayout1.hyp[288].dn";
connectAttr "knee_L_ctl_z_Shape.msg" "hyperLayout1.hyp[289].dn";
connectAttr "knee_R_grp.msg" "hyperLayout1.hyp[290].dn";
connectAttr "knee_R_ctl.msg" "hyperLayout1.hyp[291].dn";
connectAttr "knee_R_ctl_x_Shape.msg" "hyperLayout1.hyp[292].dn";
connectAttr "knee_R_ctl_y_Shape.msg" "hyperLayout1.hyp[293].dn";
connectAttr "knee_R_ctl_z_Shape.msg" "hyperLayout1.hyp[294].dn";
connectAttr "ankle_L_grp.msg" "hyperLayout1.hyp[295].dn";
connectAttr "ankle_L_ctl.msg" "hyperLayout1.hyp[296].dn";
connectAttr "ankle_L_ctl_x_Shape.msg" "hyperLayout1.hyp[297].dn";
connectAttr "ankle_L_ctl_y_Shape.msg" "hyperLayout1.hyp[298].dn";
connectAttr "ankle_L_ctl_z_Shape.msg" "hyperLayout1.hyp[299].dn";
connectAttr "ankle_R_grp.msg" "hyperLayout1.hyp[300].dn";
connectAttr "ankle_R_ctl.msg" "hyperLayout1.hyp[301].dn";
connectAttr "ankle_R_ctl_x_Shape.msg" "hyperLayout1.hyp[302].dn";
connectAttr "ankle_R_ctl_y_Shape.msg" "hyperLayout1.hyp[303].dn";
connectAttr "ankle_R_ctl_z_Shape.msg" "hyperLayout1.hyp[304].dn";
connectAttr "toes_L_grp.msg" "hyperLayout1.hyp[305].dn";
connectAttr "toes_L_ctl.msg" "hyperLayout1.hyp[306].dn";
connectAttr "toes_L_ctl_x_Shape.msg" "hyperLayout1.hyp[307].dn";
connectAttr "toes_L_ctl_y_Shape.msg" "hyperLayout1.hyp[308].dn";
connectAttr "toes_L_ctl_z_Shape.msg" "hyperLayout1.hyp[309].dn";
connectAttr "toes_R_grp.msg" "hyperLayout1.hyp[310].dn";
connectAttr "toes_R_ctl.msg" "hyperLayout1.hyp[311].dn";
connectAttr "toes_R_ctl_x_Shape.msg" "hyperLayout1.hyp[312].dn";
connectAttr "toes_R_ctl_y_Shape.msg" "hyperLayout1.hyp[313].dn";
connectAttr "toes_R_ctl_z_Shape.msg" "hyperLayout1.hyp[314].dn";
connectAttr "toes_end_L_grp.msg" "hyperLayout1.hyp[315].dn";
connectAttr "toes_end_L_ctl.msg" "hyperLayout1.hyp[316].dn";
connectAttr "toes_end_L_ctl_x_Shape.msg" "hyperLayout1.hyp[317].dn";
connectAttr "toes_end_L_ctl_y_Shape.msg" "hyperLayout1.hyp[318].dn";
connectAttr "toes_end_L_ctl_z_Shape.msg" "hyperLayout1.hyp[319].dn";
connectAttr "toes_end_R_grp.msg" "hyperLayout1.hyp[320].dn";
connectAttr "toes_end_R_ctl.msg" "hyperLayout1.hyp[321].dn";
connectAttr "toes_end_R_ctl_x_Shape.msg" "hyperLayout1.hyp[322].dn";
connectAttr "toes_end_R_ctl_y_Shape.msg" "hyperLayout1.hyp[323].dn";
connectAttr "toes_end_R_ctl_z_Shape.msg" "hyperLayout1.hyp[324].dn";
connectAttr "root_M_ctl_mtp.msg" "hyperLayout1.hyp[325].dn";
connectAttr "spine_a_M_ctl_mtp.msg" "hyperLayout1.hyp[326].dn";
connectAttr "spine_b_M_ctl_mtp.msg" "hyperLayout1.hyp[327].dn";
connectAttr "chest_M_ctl_mtp.msg" "hyperLayout1.hyp[328].dn";
connectAttr "neck_M_ctl_mtp.msg" "hyperLayout1.hyp[329].dn";
connectAttr "head_M_ctl_mtp.msg" "hyperLayout1.hyp[330].dn";
connectAttr "head_end_M_ctl_mtp.msg" "hyperLayout1.hyp[331].dn";
connectAttr "scapula_L_ctl_mtp.msg" "hyperLayout1.hyp[332].dn";
connectAttr "scapula_R_ctl_mtp.msg" "hyperLayout1.hyp[333].dn";
connectAttr "shoulder_L_ctl_mtp.msg" "hyperLayout1.hyp[334].dn";
connectAttr "shoulder_R_ctl_mtp.msg" "hyperLayout1.hyp[335].dn";
connectAttr "elbow_L_ctl_mtp.msg" "hyperLayout1.hyp[336].dn";
connectAttr "elbow_R_ctl_mtp.msg" "hyperLayout1.hyp[337].dn";
connectAttr "wrist_L_ctl_mtp.msg" "hyperLayout1.hyp[338].dn";
connectAttr "wrist_R_ctl_mtp.msg" "hyperLayout1.hyp[339].dn";
connectAttr "finger_thumb_a_L_ctl_mtp.msg" "hyperLayout1.hyp[340].dn";
connectAttr "finger_thumb_a_R_ctl_mtp.msg" "hyperLayout1.hyp[341].dn";
connectAttr "finger_thumb_b_L_ctl_mtp.msg" "hyperLayout1.hyp[342].dn";
connectAttr "finger_thumb_b_R_ctl_mtp.msg" "hyperLayout1.hyp[343].dn";
connectAttr "finger_thumb_c_L_ctl_mtp.msg" "hyperLayout1.hyp[344].dn";
connectAttr "finger_thumb_c_R_ctl_mtp.msg" "hyperLayout1.hyp[345].dn";
connectAttr "finger_index_a_L_ctl_mtp.msg" "hyperLayout1.hyp[346].dn";
connectAttr "finger_index_a_R_ctl_mtp.msg" "hyperLayout1.hyp[347].dn";
connectAttr "finger_index_b_L_ctl_mtp.msg" "hyperLayout1.hyp[348].dn";
connectAttr "finger_index_b_R_ctl_mtp.msg" "hyperLayout1.hyp[349].dn";
connectAttr "finger_index_c_L_ctl_mtp.msg" "hyperLayout1.hyp[350].dn";
connectAttr "finger_index_c_R_ctl_mtp.msg" "hyperLayout1.hyp[351].dn";
connectAttr "finger_middle_a_L_ctl_mtp.msg" "hyperLayout1.hyp[352].dn";
connectAttr "finger_middle_a_R_ctl_mtp.msg" "hyperLayout1.hyp[353].dn";
connectAttr "finger_middle_b_L_ctl_mtp.msg" "hyperLayout1.hyp[354].dn";
connectAttr "finger_middle_b_R_ctl_mtp.msg" "hyperLayout1.hyp[355].dn";
connectAttr "finger_middle_c_L_ctl_mtp.msg" "hyperLayout1.hyp[356].dn";
connectAttr "finger_middle_c_R_ctl_mtp.msg" "hyperLayout1.hyp[357].dn";
connectAttr "finger_ring_a_L_ctl_mtp.msg" "hyperLayout1.hyp[358].dn";
connectAttr "finger_ring_a_R_ctl_mtp.msg" "hyperLayout1.hyp[359].dn";
connectAttr "finger_ring_b_L_ctl_mtp.msg" "hyperLayout1.hyp[360].dn";
connectAttr "finger_ring_b_R_ctl_mtp.msg" "hyperLayout1.hyp[361].dn";
connectAttr "finger_ring_c_L_ctl_mtp.msg" "hyperLayout1.hyp[362].dn";
connectAttr "finger_ring_c_R_ctl_mtp.msg" "hyperLayout1.hyp[363].dn";
connectAttr "finger_pinky_a_L_ctl_mtp.msg" "hyperLayout1.hyp[364].dn";
connectAttr "finger_pinky_a_R_ctl_mtp.msg" "hyperLayout1.hyp[365].dn";
connectAttr "finger_pinky_b_L_ctl_mtp.msg" "hyperLayout1.hyp[366].dn";
connectAttr "finger_pinky_b_R_ctl_mtp.msg" "hyperLayout1.hyp[367].dn";
connectAttr "finger_pinky_c_L_ctl_mtp.msg" "hyperLayout1.hyp[368].dn";
connectAttr "finger_pinky_c_R_ctl_mtp.msg" "hyperLayout1.hyp[369].dn";
connectAttr "finger_end_thumb_L_ctl_mtp.msg" "hyperLayout1.hyp[370].dn";
connectAttr "finger_end_thumb_R_ctl_mtp.msg" "hyperLayout1.hyp[371].dn";
connectAttr "finger_end_index_L_ctl_mtp.msg" "hyperLayout1.hyp[372].dn";
connectAttr "finger_end_index_R_ctl_mtp.msg" "hyperLayout1.hyp[373].dn";
connectAttr "finger_end_middle_L_ctl_mtp.msg" "hyperLayout1.hyp[374].dn";
connectAttr "finger_end_middle_R_ctl_mtp.msg" "hyperLayout1.hyp[375].dn";
connectAttr "finger_end_ring_L_ctl_mtp.msg" "hyperLayout1.hyp[376].dn";
connectAttr "finger_end_ring_R_ctl_mtp.msg" "hyperLayout1.hyp[377].dn";
connectAttr "finger_end_pinky_L_ctl_mtp.msg" "hyperLayout1.hyp[378].dn";
connectAttr "finger_end_pinky_R_ctl_mtp.msg" "hyperLayout1.hyp[379].dn";
connectAttr "hip_L_ctl_mtp.msg" "hyperLayout1.hyp[380].dn";
connectAttr "hip_R_ctl_mtp.msg" "hyperLayout1.hyp[381].dn";
connectAttr "knee_L_ctl_mtp.msg" "hyperLayout1.hyp[382].dn";
connectAttr "knee_R_ctl_mtp.msg" "hyperLayout1.hyp[383].dn";
connectAttr "ankle_L_ctl_mtp.msg" "hyperLayout1.hyp[384].dn";
connectAttr "ankle_R_ctl_mtp.msg" "hyperLayout1.hyp[385].dn";
connectAttr "toes_L_ctl_mtp.msg" "hyperLayout1.hyp[386].dn";
connectAttr "toes_R_ctl_mtp.msg" "hyperLayout1.hyp[387].dn";
connectAttr "toes_end_L_ctl_mtp.msg" "hyperLayout1.hyp[388].dn";
connectAttr "toes_end_R_ctl_mtp.msg" "hyperLayout1.hyp[389].dn";
connectAttr "root_M_geo_copy.msg" "hyperLayout1.hyp[455].dn";
connectAttr "root_M_geo_copyShape.msg" "hyperLayout1.hyp[456].dn";
connectAttr "spine_a_M_geo_copy.msg" "hyperLayout1.hyp[457].dn";
connectAttr "spine_a_M_geo_copyShape.msg" "hyperLayout1.hyp[458].dn";
connectAttr "spine_b_M_geo_copy.msg" "hyperLayout1.hyp[459].dn";
connectAttr "spine_b_M_geo_copyShape.msg" "hyperLayout1.hyp[460].dn";
connectAttr "chest_M_geo_copy.msg" "hyperLayout1.hyp[461].dn";
connectAttr "chest_M_geo_copyShape.msg" "hyperLayout1.hyp[462].dn";
connectAttr "neck_M_geo_copy.msg" "hyperLayout1.hyp[463].dn";
connectAttr "neck_M_geo_copyShape.msg" "hyperLayout1.hyp[464].dn";
connectAttr "head_M_geo_copy.msg" "hyperLayout1.hyp[465].dn";
connectAttr "head_M_geo_copyShape.msg" "hyperLayout1.hyp[466].dn";
connectAttr "scapula_L_geo_copy.msg" "hyperLayout1.hyp[467].dn";
connectAttr "scapula_R_geoShape.msg" "hyperLayout1.hyp[468].dn";
connectAttr "scapula_R_geo_copy.msg" "hyperLayout1.hyp[469].dn";
connectAttr "scapula_R_geo_copyShape.msg" "hyperLayout1.hyp[470].dn";
connectAttr "shoulder_L_geo_copy.msg" "hyperLayout1.hyp[472].dn";
connectAttr "shoulder_R_geoShape.msg" "hyperLayout1.hyp[473].dn";
connectAttr "shoulder_R_geo_copy.msg" "hyperLayout1.hyp[474].dn";
connectAttr "shoulder_R_geo_copyShape.msg" "hyperLayout1.hyp[475].dn";
connectAttr "elbow_L_geo_copy.msg" "hyperLayout1.hyp[477].dn";
connectAttr "elbow_R_geoShape.msg" "hyperLayout1.hyp[478].dn";
connectAttr "elbow_R_geo_copy.msg" "hyperLayout1.hyp[479].dn";
connectAttr "elbow_R_geo_copyShape.msg" "hyperLayout1.hyp[480].dn";
connectAttr "wrist_L_geo_copy.msg" "hyperLayout1.hyp[482].dn";
connectAttr "wrist_R_geoShape.msg" "hyperLayout1.hyp[483].dn";
connectAttr "wrist_R_geo_copy.msg" "hyperLayout1.hyp[484].dn";
connectAttr "wrist_R_geo_copyShape.msg" "hyperLayout1.hyp[485].dn";
connectAttr "finger_thumb_a_L_geo_copy.msg" "hyperLayout1.hyp[487].dn";
connectAttr "finger_thumb_a_R_geoShape.msg" "hyperLayout1.hyp[488].dn";
connectAttr "finger_thumb_a_R_geo_copy.msg" "hyperLayout1.hyp[489].dn";
connectAttr "finger_thumb_a_R_geo_copyShape.msg" "hyperLayout1.hyp[490].dn";
connectAttr "finger_thumb_b_L_geo_copy.msg" "hyperLayout1.hyp[492].dn";
connectAttr "finger_thumb_b_R_geoShape.msg" "hyperLayout1.hyp[493].dn";
connectAttr "finger_thumb_b_R_geo_copy.msg" "hyperLayout1.hyp[494].dn";
connectAttr "finger_thumb_b_R_geo_copyShape.msg" "hyperLayout1.hyp[495].dn";
connectAttr "finger_thumb_c_L_geo_copy.msg" "hyperLayout1.hyp[497].dn";
connectAttr "finger_thumb_c_R_geoShape.msg" "hyperLayout1.hyp[498].dn";
connectAttr "finger_thumb_c_R_geo_copy.msg" "hyperLayout1.hyp[499].dn";
connectAttr "finger_thumb_c_R_geo_copyShape.msg" "hyperLayout1.hyp[500].dn";
connectAttr "finger_index_a_L_geo_copy.msg" "hyperLayout1.hyp[502].dn";
connectAttr "finger_index_a_R_geoShape.msg" "hyperLayout1.hyp[503].dn";
connectAttr "finger_index_a_R_geo_copy.msg" "hyperLayout1.hyp[504].dn";
connectAttr "finger_index_a_R_geo_copyShape.msg" "hyperLayout1.hyp[505].dn";
connectAttr "finger_index_b_L_geo_copy.msg" "hyperLayout1.hyp[507].dn";
connectAttr "finger_index_b_R_geoShape.msg" "hyperLayout1.hyp[508].dn";
connectAttr "finger_index_b_R_geo_copy.msg" "hyperLayout1.hyp[509].dn";
connectAttr "finger_index_b_R_geo_copyShape.msg" "hyperLayout1.hyp[510].dn";
connectAttr "finger_index_c_L_geo_copy.msg" "hyperLayout1.hyp[512].dn";
connectAttr "finger_index_c_R_geoShape.msg" "hyperLayout1.hyp[513].dn";
connectAttr "finger_index_c_R_geo_copy.msg" "hyperLayout1.hyp[514].dn";
connectAttr "finger_index_c_R_geo_copyShape.msg" "hyperLayout1.hyp[515].dn";
connectAttr "finger_middle_a_L_geo_copy.msg" "hyperLayout1.hyp[517].dn";
connectAttr "finger_middle_a_R_geoShape.msg" "hyperLayout1.hyp[518].dn";
connectAttr "finger_middle_a_R_geo_copy.msg" "hyperLayout1.hyp[519].dn";
connectAttr "finger_middle_a_R_geo_copyShape.msg" "hyperLayout1.hyp[520].dn";
connectAttr "finger_middle_b_L_geo_copy.msg" "hyperLayout1.hyp[522].dn";
connectAttr "finger_middle_b_R_geoShape.msg" "hyperLayout1.hyp[523].dn";
connectAttr "finger_middle_b_R_geo_copy.msg" "hyperLayout1.hyp[524].dn";
connectAttr "finger_middle_b_R_geo_copyShape.msg" "hyperLayout1.hyp[525].dn";
connectAttr "finger_middle_c_L_geo_copy.msg" "hyperLayout1.hyp[527].dn";
connectAttr "finger_middle_c_R_geoShape.msg" "hyperLayout1.hyp[528].dn";
connectAttr "finger_middle_c_R_geo_copy.msg" "hyperLayout1.hyp[529].dn";
connectAttr "finger_middle_c_R_geo_copyShape.msg" "hyperLayout1.hyp[530].dn";
connectAttr "finger_ring_a_L_geo_copy.msg" "hyperLayout1.hyp[532].dn";
connectAttr "finger_ring_a_R_geoShape.msg" "hyperLayout1.hyp[533].dn";
connectAttr "finger_ring_a_R_geo_copy.msg" "hyperLayout1.hyp[534].dn";
connectAttr "finger_ring_a_R_geo_copyShape.msg" "hyperLayout1.hyp[535].dn";
connectAttr "finger_ring_b_L_geo_copy.msg" "hyperLayout1.hyp[537].dn";
connectAttr "finger_ring_b_R_geoShape.msg" "hyperLayout1.hyp[538].dn";
connectAttr "finger_ring_b_R_geo_copy.msg" "hyperLayout1.hyp[539].dn";
connectAttr "finger_ring_b_R_geo_copyShape.msg" "hyperLayout1.hyp[540].dn";
connectAttr "finger_ring_c_L_geo_copy.msg" "hyperLayout1.hyp[542].dn";
connectAttr "finger_ring_c_R_geoShape.msg" "hyperLayout1.hyp[543].dn";
connectAttr "finger_ring_c_R_geo_copy.msg" "hyperLayout1.hyp[544].dn";
connectAttr "finger_ring_c_R_geo_copyShape.msg" "hyperLayout1.hyp[545].dn";
connectAttr "finger_pinky_a_L_geo_copy.msg" "hyperLayout1.hyp[547].dn";
connectAttr "finger_pinky_a_R_geoShape.msg" "hyperLayout1.hyp[548].dn";
connectAttr "|skin_proxy_dgc|finger_pinky_a_L_grp|finger_pinky_a_L_ctl|finger_pinky_a_L_geo_copy|polySurfaceShape6.msg" "hyperLayout1.hyp[549].dn"
		;
connectAttr "finger_pinky_a_R_geo_copy.msg" "hyperLayout1.hyp[550].dn";
connectAttr "finger_pinky_a_R_geo_copyShape.msg" "hyperLayout1.hyp[551].dn";
connectAttr "|skin_proxy_dgc|finger_pinky_a_R_grp|finger_pinky_a_R_ctl|finger_pinky_a_R_geo_copy|polySurfaceShape6.msg" "hyperLayout1.hyp[552].dn"
		;
connectAttr "finger_pinky_b_L_geo_copy.msg" "hyperLayout1.hyp[554].dn";
connectAttr "finger_pinky_b_R_geoShape.msg" "hyperLayout1.hyp[555].dn";
connectAttr "|skin_proxy_dgc|finger_pinky_b_L_grp|finger_pinky_b_L_ctl|finger_pinky_b_L_geo_copy|polySurfaceShape6.msg" "hyperLayout1.hyp[556].dn"
		;
connectAttr "finger_pinky_b_R_geo_copy.msg" "hyperLayout1.hyp[557].dn";
connectAttr "finger_pinky_b_R_geo_copyShape.msg" "hyperLayout1.hyp[558].dn";
connectAttr "|skin_proxy_dgc|finger_pinky_b_R_grp|finger_pinky_b_R_ctl|finger_pinky_b_R_geo_copy|polySurfaceShape6.msg" "hyperLayout1.hyp[559].dn"
		;
connectAttr "finger_pinky_c_L_geo_copy.msg" "hyperLayout1.hyp[561].dn";
connectAttr "finger_pinky_c_R_geoShape.msg" "hyperLayout1.hyp[562].dn";
connectAttr "|skin_proxy_dgc|finger_pinky_c_L_grp|finger_pinky_c_L_ctl|finger_pinky_c_L_geo_copy|polySurfaceShape6.msg" "hyperLayout1.hyp[563].dn"
		;
connectAttr "finger_pinky_c_R_geo_copy.msg" "hyperLayout1.hyp[564].dn";
connectAttr "finger_pinky_c_R_geo_copyShape.msg" "hyperLayout1.hyp[565].dn";
connectAttr "|skin_proxy_dgc|finger_pinky_c_R_grp|finger_pinky_c_R_ctl|finger_pinky_c_R_geo_copy|polySurfaceShape6.msg" "hyperLayout1.hyp[566].dn"
		;
connectAttr "hip_L_geo_copy.msg" "hyperLayout1.hyp[568].dn";
connectAttr "hip_R_geoShape.msg" "hyperLayout1.hyp[569].dn";
connectAttr "hip_R_geo_copy.msg" "hyperLayout1.hyp[570].dn";
connectAttr "hip_R_geo_copyShape.msg" "hyperLayout1.hyp[571].dn";
connectAttr "knee_L_geo_copy.msg" "hyperLayout1.hyp[573].dn";
connectAttr "knee_R_geoShape.msg" "hyperLayout1.hyp[574].dn";
connectAttr "knee_R_geo_copy.msg" "hyperLayout1.hyp[575].dn";
connectAttr "knee_R_geo_copyShape.msg" "hyperLayout1.hyp[576].dn";
connectAttr "ankle_L_geo_copy.msg" "hyperLayout1.hyp[578].dn";
connectAttr "ankle_R_geoShape.msg" "hyperLayout1.hyp[579].dn";
connectAttr "ankle_R_geo_copy.msg" "hyperLayout1.hyp[580].dn";
connectAttr "ankle_R_geo_copyShape.msg" "hyperLayout1.hyp[581].dn";
connectAttr "toes_L_geo_copy.msg" "hyperLayout1.hyp[583].dn";
connectAttr "toes_R_geoShape.msg" "hyperLayout1.hyp[584].dn";
connectAttr "toes_R_geo_copy.msg" "hyperLayout1.hyp[585].dn";
connectAttr "toes_R_geo_copyShape.msg" "hyperLayout1.hyp[586].dn";
connectAttr "root_M_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "spine_a_M_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "spine_b_M_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "chest_M_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "neck_M_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "head_M_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "scapula_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "scapula_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "shoulder_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "shoulder_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "elbow_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "elbow_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "wrist_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "wrist_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_thumb_a_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_thumb_a_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_thumb_b_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_thumb_b_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_thumb_c_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_thumb_c_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_index_a_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_index_a_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_index_b_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_index_b_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_index_c_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_index_c_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_middle_a_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_middle_a_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "finger_middle_b_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_middle_b_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "finger_middle_c_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_middle_c_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na
		;
connectAttr "finger_ring_a_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_ring_a_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_ring_b_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_ring_b_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_ring_c_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_ring_c_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_pinky_a_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_pinky_a_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_pinky_b_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_pinky_b_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_pinky_c_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "finger_pinky_c_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "hip_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "hip_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "knee_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "knee_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "ankle_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "ankle_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "toes_R_geoShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "toes_R_geo_copyShape.iog" ":initialShadingGroup.dsm" -na;
// End of skin_proxy.ma
