##########################################################################################
# Script: design_setup.tcl
# Version: T-2022.03
# Copyright (C) 2014-2022 Synopsys, Inc. All rights reserved.
# 说明: 整个 RM 流程的设计与输入配置中心，init_design 及后续各阶段脚本均会 source 本文件
##########################################################################################

set DESIGN_NAME 		"" ;# 【必填】设计/顶层模块名；save_block、copy_block 的 block 名
				   ;# Required; name of the design to be worked on; used as the block name for save_block or copy_block operations
				   ;# If you are starting from init_design with verilog or RTL, this is also the top module name
set LIBRARY_SUFFIX		"" ;# 【可选】NDM 设计库名后缀
				   ;# Optional; suffix for the design library name ; default is unspecified  
set DESIGN_LIBRARY 		"${DESIGN_NAME}${LIBRARY_SUFFIX}" ;# NDM 设计库名，默认由 DESIGN_NAME + LIBRARY_SUFFIX 组成
				   ;# Optional; name of the design library; 
				   ;# If you are starting from init_design, no need to change this; it will be populated with values from DESIGN_NAME & LIBRARY_SUFFIX

set TECHLIB_DATA_DIR		"" ;# 站点工艺数据安装根目录，供依赖工艺路径的变量引用
                                   ;# Used to point to directory where technology data is installed for the site. 
                                   ;# Used by variables which use data from those directories.

##########################################################################################
## Variables for design prep which are used by init_design.tcl
## init_design 输入配置：按需填写下方 1、2、3、4 节变量
## Fill in the variables in 1, 2, 3, and 4 below as needed.
##########################################################################################
set INIT_DESIGN_INPUT 		"ASCII"	;# 设计输入方式: ASCII | DC_ASCII | DP_RM_NDM；默认 ASCII
				;# Specify one of the 3 options: ASCII | DC_ASCII | DP_RM_NDM; default is ASCII.
				;# 1.ASCII: assumes all design input files are ASCII and will read them in individually.
				;# 2.NDM: specify your own floorplanned NDM path and skip the design creation steps (read_verilog, load_upf, read_def etc);
				;#   script opens $DESIGN_LIBRARY and copies over INIT_DESIGN_INPUT_BLOCK as $DESIGN_NAME/$INIT_DESIGN_BLOCK_NAME to start with;
				;#   INIT_DESIGN_INPUT_BLOCK_NAME is required
				;# 3.DC_ASCII: for design transfer from DC using the write_icc2_files command;
				;#   sources ${DCRM_RESULTS_DIR}/${DCRM_FINAL_DESIGN_ICC2}/${DESIGN_NAME}.icc2_script.tcl;
			      	;#   you can change the default of DC_RESULTS_DIR and DCRM_FINAL_DESIGN_ICC2 below;
				;#   commonly used in combination with SPG flow (set PLACE_OPT_SPG_FLOW true below) 
				;# 1.ASCII: 逐个读入 Verilog/UPF/DEF 等 ASCII 文件
				;# 2.DP_RM_NDM: 使用已有 floorplan 的 NDM，跳过 read_verilog/load_upf/read_def
				;# 3.DC_ASCII: 从 DC write_icc2_files 产物启动，常与 SPG 流配合
set INIT_DESIGN_INPUT_LIBRARY 	"" ;# DP_RM_NDM 时：源 NDM 库名
				   ;# specify a library name as the source library for copying if INIT_DESIGN_INPUT = NDM
set INIT_DESIGN_INPUT_BLOCK_NAME "" ;# DP_RM_NDM 时：源 block 名（可带 label）
				   ;# specify a block name (with or witout label) as the input block if INIT_DESIGN_INPUT = NDM
set EARLY_DATA_CHECK_POLICY	"none" ;# 早期数据检查策略: none|lenient|strict；默认 none 关闭
				;# none|lenient|strict ;RM default is none;
				;# lenient and strict trigger corresponding set_early_data_check_policy -policy $EARLY_DATA_CHECK_POLICY command and report_early_data_checks; 
				;# specify none to disable the set_early_data_check_policy command

##################################################
### 1. Reference libraries（参考库）
##################################################
set REFERENCE_LIBRARY 		[list ]	;# 【必填】参考库列表（.nlib 等）；层次化需含子块库或 ETM 库
					;# Required; a list of reference libraries for the design library.
					;#	for library configuration flow (LIBRARY_CONFIGURATION_FLOW set to true below): 
					;#		- specify the list of physical source files to be used for library configuration during create_lib
				       	;# 	for hierarchical designs using bottom-up flows: include subblock design libraries in the list;
					;# 	for hierarchical designs using ETMs: include the ETM library in the list.
					;# 		- If unpack_rm_dirs.pl is used to create dir structures for hierarchical designs, 
					;#		  in order to transition between hierarchical DP and hierarchical PNR flows properly, 
					;#		  absolute paths are a requirement.
set COMPRESS_LIBS               "false" ;# DP 流程中是否以压缩格式保存 NDM 库
					;# Save libs as compressed NDM; only used in DP.
set LIBRARY_CONFIGURATION_FLOW	false	;# 是否启用库配置流：从 .db + 物理源文件自动生成 .nlib 并链接
					;# Optional; set it to true enables library configuration flow which calls the library manager under the hood to generate .nlibs, 
					;# save them to disk, and automatically link them to the design.
					;# Requires LINK_LIBRARY to be specified with .db files and REFERENCE_LIBRARY to be specified with physical
					;# source files for the library configuration flow. Also search_path (in icc2_pnr_setup.tcl) should include paths 
					;# to these .db and physical source files.

set LINK_LIBRARY		""	;# .db 文件列表；VC-LP/FM 或库配置流时必填，纯 PNR 通常不需要
					;# Optional; specify .db files;
					;# 	for running VC-LP (vc_lp.tcl) and Formality (fm.tcl): required
					;# 	for ICC-II without LIBRARY_CONFIGURATION_FLOW enabled: not required
					;#	for ICC-II with LIBRARY_CONFIGURATION_FLOW enabled: required; 
					;#      	- the .db files specified will be used for the library configuration under the hood during create_lib

##################################################
### 2. Tech files and setup（工艺文件与设置）
##################################################
set TECH_FILE 			"" 	;# 工艺文件路径；与 TECH_LIB 二选一，推荐 TECH_FILE
					;# A technology file; TECH_FILE and TECH_LIB are mutually exclusive ways to specify technology information; 
					;# TECH_FILE is recommended, although TECH_LIB is also supported in ICC2 RM. 
set TECH_LIB			""	;# 专用工艺参考库；建议同时放在 REFERENCE_LIBRARY 列表首位
                        		;# Specify the reference library to be used as a dedicated technology library;
                        		;# as a best practice, please list it as the first library in the REFERENCE_LIBRARY list 
set TECH_LIB_INCLUDES_TECH_SETUP_INFO true ;# TECH_LIB 是否已含布线层方向/offset/site 等 setup 信息
					;# Indicate whether TECH_LIB contains technology setup information such as routing layer direction, offset, 
					;# site default, and site symmetry, etc. TECH_LIB may contain this information if loaded during library prep.
					;# true|false; this variable is associated with TECH_LIB. 
set TCL_TECH_SETUP_FILE		"init_design.tech_setup.tcl" ;# 设置布线层方向、offset、site 等的 Tcl 脚本
					;# Specify a TCL script for setting routing layer direction, offset, site default, and site symmetry list, etc.
					;# init_design.tech_setup.tcl is the default. Use it as a template or provide your own script.
					;# This script will only get sourced if the following conditions are met: 
					;# (1) TECH_FILE is specified (2) TECH_LIB is specified && TECH_LIB_INCLUDES_TECH_SETUP_INFO is false
set DESIGN_LIBRARY_SCALE_FACTOR	""	;# 库长度精度；设计库与参考库必须一致；默认 10000（0.1nm）
					;# Optional; Specify the length precision for the library. Length precision for the design
					;# library and its ref libraries must be identical. Tool default is 10000, which implies one unit is one Angstrom or 0.1nm. 

##################################################
### 3. Verilog, dc inputs, upf, mcmm, timing, etc（网表/UPF/MCMM/时序）
##################################################

set DCRM_RESULTS_DIR  		"./results" ;# DC_ASCII 时 DC-RM 输出根目录
				   ;# used by DC_ASCII to specify DC-RM output directory. Default is results.   
set DCRM_FINAL_DESIGN_ICC2 	"ICC2_files" ;# DC write_icc2_files 生成的子目录名
				;# output directory name generated by DC-RM's write_icc2_files command;
				;# only valid if you specify DC_ASCII for INIT_DESIGN_INPUT;
                                ;# The directory contains verilog, floorplan, scenario settings, and constraints from DC
                                ;# in a format that IC Compiler II can source.    
set VERILOG_NETLIST_FILES	""	;# 【ASCII 必填】Verilog 网表文件列表
					;# Verilog netlist files;
					;# 	for DP: required
					;# 	for PNR: required if INIT_DESIGN_INPUT is ASCII in icc2_pnr_setup.tcl; not required for DC_ASCII or DP_RM_NDM

set UPF_FILE 			""	;# 【ASCII 必填】Golden UPF 电源意图文件；层次化 ETM 需 load_upf -scope
					;# A UPF file
					;# 	for DP: required
					;# 	for PNR: required if INIT_DESIGN_INPUT is ASCII in icc2_pnr_setup.tcl; not required for DC_ASCII or DP_RM_NDM
                                        ;#      for hierarchical designs using ETMs, load the block upf file
                                        ;#      for each sub-block linked to ETM, include the following line in the UPF_FILE 
                			;#		load_upf block.upf -scope block_instance_name
set UPF_SUPPLEMENTAL_FILE	""      ;# Golden UPF 流的 supplemental UPF；与 UPF_FILE 配合使用
					;# The supplemental UPF file. Only needed if you are running golden UPF flow, in which case, you need both UPF_FILE and this.
					;# 	for DP: required
					;# 	for PNR: required if INIT_DESIGN_INPUT is ASCII in icc2_pnr_setup.tcl; not required for DC_ASCII or DP_RM_NDM
					;#	    If UPF_SUPPLEMENTAL_FILE is specified, scripts assume golden UPF flow. load_upf and save_upf commands will be different.
set UPF_UPDATE_SUPPLY_SET_FILE	""	;# 用于解析/修正 UPF supply set 的补充 UPF 文件
					;# A UPF file to resolve UPF supply sets

set TCL_MCMM_SETUP_FILE		""	;# 【ASCII 必填】创建 mode/corner/scenario 并加载约束的 Tcl 脚本
					;# Specify a Tcl script to create your corners, modes, scenarios and load respective constraints;
					;# two examples are provided : 
					;# examples/TCL_MCMM_SETUP_FILE.explicit.tcl: provide mode, corner, and scenario constraints; create modes, corners, 
					;# and scenarios; source mode, corner, and scenario constraints, respectively 
					;# examples/TCL_MCMM_SETUP_FILE.auto_expanded.tcl: provide constraints for the scenarios; create modes, corners, 
					;# and scenarios; source scenario constraints which are then expanded to associated modes and corners
					;# 	for DP: required
					;# 	for PNR: required if INIT_DESIGN_INPUT is ASCII in icc2_pnr_setup.tcl; not required for DC_ASCII or DP_RM_NDM
set TCL_PARASITIC_SETUP_FILE	""	;# 【ASCII 必填】read_parasitic_tech 读取 TLU+ 的 Tcl 脚本
					;# Specify a Tcl script to read in your TLU+ files by using the read_parasitic_tech command;
					;# refer to the example in examples/TCL_PARASITIC_SETUP_FILE.tcl
set UNIQUIFY_OPTIONS			"-force" ;# uniquify 命令选项，默认 -force
					;# default is "-force"; Set options for the uniquify command.

set TCL_MODE_CORNER_SCENARIO_MODEL_ADJUSTMENT_FILE      "" ;# 每步 scenario 管理后 source 的 MCMM/模型微调脚本
					;# Optional; specify a file for adjustment of modes/corners/scenarios/models

set TCL_POCV_SETUP_FILE			"" ;# POCV 映射等设置脚本（可选）
					;# Optional; provide your own file for POCV setup such as POCV mapping; 
					;# Refer to examples/TCL_POCV_SETUP_FILE.tcl for sample commands
set TCL_AOCV_SETUP_FILE			"" ;# AOCV 映射脚本；仅当 TCL_POCV_SETUP_FILE 为空时执行
					;# Optional; provide your own file for AOCV setup such as AOCV mapping; 
					;# Refer to examples/TCL_AOCV_SETUP_FILE.tcl for sample commands; only executes if TCL_POCV_SETUP_FILE is null
set TCL_PVT_CONFIGURATION_FILE		"" ;# 自定义 set_pvt_configuration 脚本；init_design 后每步 open_lib 前 source
					;# Optional; specify a file for user customized set_pvt_configuration commmands;

##################################################
### 4. DEF, floorplan, placement constraints, etc（Floorplan 与布局约束）
##################################################
set TCL_FLOORPLAN_FILE			"" ;# write_floorplan 输出的 Tcl floorplan；与 DEF 互斥
					;# Optional; Tcl floorplan file written by the write_floorplan command; for example, floorplan/floorplan.tcl;
					;# TCL_FLOORPLAN_FILE and DEF_FLOORPLAN_FILES are mutually exclusive; please specify only one of them;
					;# Not effective if INIT_DESIGN_INPUT = DC_ASCII or DP_RM_NDM.
					;# The write_floorplan command writes a floorplan.tcl Tcl script and a floorplan.def DEF file;
					;# reading floorplan.tcl alone can restore the entire floorplan - refer to write_floorplan man for more details

set DEF_FLOORPLAN_FILES			"" ;# Floorplan DEF 文件；ASCII 且无 Tcl/initialize_floorplan 时必填；与 Tcl 互斥
					;# Optional; DEF files which contain the floorplan information; for ex: "1.def 2.def"; not required for DP
					;# 	for PNR: required if INIT_DESIGN_INPUT = ASCII in icc2_pnr_setup.tcl and neither TCL_FLOORPLAN_FILE or 
					;#		 initialize_floorplan is used; DEF_FLOORPLAN_FILES and TCL_FLOORPLAN_FILE are mutually exclusive;
					;# 	         not required if INIT_DESIGN_INPUT = DC_ASCII or DP_RM_NDM
set DEF_READ_OPTIONS			"-add_def_only_objects all" ;# read_def 命令选项
					;# default is "-add_def_only_objects all"; set it to "" (empty) if you don't need any option
					;# specifies the options used by read_def command
set DEF_RESOLVE_PG_NETS			true ;# 是否协调 PG 网络与 power domain 之间的冲突
					;# false|true (default); Resolves conflicts between pg network with power domains.
set TCL_ADDITIONAL_FLOORPLAN_FILE 	"" ;# DEF/Tcl floorplan 读入后的补充约束（bound、pin/route guide 等）
					;# a supplementary Tcl constraint file; sourced after TCL_FLOORPLAN_FILE or DEF_FLOORPLAN_FILE is read; 

set SITE_SYMMETRY_LIST			"" ;# site 对称性列表，如 "{unit Y} {unit1 Y}"
					;# Optional; Specify a list of site def and its symmetry value;

set DEF_SCAN_FILE			"" ;# Scan chain 的 SCANDEF 文件
					;# Optional; A scan DEF file for scan chain information;

set TCL_FLOORPLAN_RULE_SCRIPT		"" ;# floorplan 规则脚本（set_floorplan_*_rules / check_floorplan_rules）
					;# Specify your floorplan rule file (which contains set_floorplan_*_rules commands) or a script to generate such rules;

set TCL_USER_SPARE_CELL_PRE_SCRIPT	"" ;# place_opt 前插入 spare cell 的用户脚本
					   ;# An optional Tcl file for spare cell insertion to be sourced before place_opt;
set TCL_USER_SPARE_CELL_POST_SCRIPT	"" ;# place_opt 后插入 spare cell 的用户脚本
					   ;# An optional Tcl file for spare cell insertion to be sourced after place_opt;

########################################################################################## 
## Variables for general optimization use（通用优化设置）
##########################################################################################
## For redundant via insertion（冗余 via 插入）
set ENABLE_REDUNDANT_VIA_INSERTION	false ;# 是否在 clock_opt_opto/route_auto/route_opt 中插入冗余 via
					;# false|true; tool default false; optional in RM; enables redundant via insertion in clock_opt_opto.tcl, route_auto.tcl, and route_opt.tcl
set TCL_USER_REDUNDANT_VIA_MAPPING_FILE "" ;# 冗余 via 映射文件（启用冗余 via 时必填）
					;# ICC-II via mapping file is required for redundant via insertion; 

## For performance via ladder（性能 via ladder，≤7nm 常用）
set ENABLE_PERFORMANCE_VIA_LADDER	false ;# 是否在 placement 阶段启用 performance via ladder
					;# false|true; RM default false; enables performance via ladder insertion in the set_stage command -step synthesis (FC) or placement (ICC2)


set SAIF_FILE_LIST			"" ;# 功耗分析用 SAIF 文件（可多个，带 scaling/weight/path 选项）；place_opt 开头 source
					;# Specify a SAIF file or a list of SAIF files and options for accurate power computation
set SAIF_FILE_POWER_SCENARIO		"" ;# SAIF 作用的 power scenario
					;# SAIF_FILE_LIST related; specify a power scenario where the SAIF is to be applied
set SAIF_FILE_SOURCE_INSTANCE		"" ;# SAIF 中当前设计实例名
					;# SAIF_FILE_LIST related; name of the instance of the current design as it appears in SAIF file.
set SAIF_FILE_TARGET_INSTANCE		"" ;# 活动 annotate 的目标实例名
					;# SAIF_FILE_LIST related; name of the target instance on which activity is to be annotated.
set OPTIMIZATION_FREEZE_PORT_LIST 	"" ;# 禁止优化改动的单元列表（冻结 clock/data 端口，利于分模块形式验证）
					;# List of cells (for ex, clock gen modules, or customized logics that should not be touched) to which freeze_clock_ports 

set TCL_MULTI_VT_CONSTRAINT_FILE	"multi_vth_constraint_script.tcl" ;# Multi-Vt 约束定义与应用脚本
					;# A Tcl file which defines and applies multi Vt constraints
set TCL_LIB_CELL_PURPOSE_FILE 		"set_lib_cell_purpose.tcl" ;# lib cell purpose 限制脚本（TIE/hold/CTS/dont_use 等）
					;# A Tcl file which applies lib cell purpose related restrictions;

## Below are set_lib_cell_purpose.tcl specific variables. Only applicable if set_lib_cell_purpose.tcl is used.
## 以下变量仅在 set_lib_cell_purpose.tcl 被使用时生效
set TIE_LIB_CELL_PATTERN_LIST 		"" ;# TIE 单元 pattern 列表
					;# A list of TIE lib cell patterns to be included for optimization;
set HOLD_FIX_LIB_CELL_PATTERN_LIST 	"" ;# 仅用于 hold 修复的单元 pattern
					;# A list of hold time fixing lib cell patterns to be included only for hold
set CTS_LIB_CELL_PATTERN_LIST 		"" ;# CTS 可用单元 pattern（含 repeater/AO buffer/触发器）
					;# List of CTS lib cell patterns to be used by CTS; 
set CTS_ONLY_LIB_CELL_PATTERN_LIST 	"" ;# 仅 CTS 专用单元 pattern（不参与其他优化）
					;# List of CTS lib cell patterns to be used by CTS "exclusively", such as clock specific

set PREROUTE_CTS_PRIMARY_CORNER		"" ;# 手动指定 CTS compile 主 corner；空则工具自动选最差 delay corner
					;# <a corner>; RM default is unspecified; sets cts.compile.primary_corner; optional in RM;
set TCL_USER_MSCTS_MESH_ROUTING_SCRIPT 	"" ;# 时钟 mesh 布线用户脚本
					;# An optional Tcl file that can be provided for clock mesh net routing

set TCL_ANTENNA_RULE_FILE		"" ;# Antenna 规则文件
					;# Antenna rule file; Example : examples/TCL_ANTENNA_RULE_FILE.txt

set SWITCH_CONNECTIVITY_FILE    	"" ;# Power switch 连接关系文件
					;# Specify switch connectivity file

########################################################################################## 
## Variables for scenario activation and focused scenario（各阶段 scenario 激活）
##########################################################################################
set PLACE_OPT_ACTIVE_SCENARIO_LIST	"" ;# place_opt 阶段激活的 scenario 子集；设后会传递到后续步骤
					;# A subset of scenarios to be made active during place_opt step;
set CLOCK_OPT_CTS_ACTIVE_SCENARIO_LIST  "" ;# clock_opt_cts 阶段激活的 scenario 子集
					;# A subset of scenarios to be made active during clock_opt_cts step;
set ROUTE_OPT_ACTIVE_SCENARIO_LIST 	"" ;# route_opt 阶段激活的 scenario 子集
					;# A subset of scenarios to be made active during route_opt step;
set CLOCK_OPT_OPTO_ACTIVE_SCENARIO_LIST "$ROUTE_OPT_ACTIVE_SCENARIO_LIST" ;# clock_opt_opto 阶段；GRE 建议与 route_auto/route_opt 一致
					;# A subset of scenarios to be made active during clock_opt_opto step;
set ROUTE_AUTO_ACTIVE_SCENARIO_LIST 	"$ROUTE_OPT_ACTIVE_SCENARIO_LIST" ;# route_auto 阶段激活的 scenario 子集
					;# A subset of scenarios to be made active during route_auto step;
set CHIP_FINISH_ACTIVE_SCENARIO_LIST 	"" ;# chip_finish 阶段激活的 scenario 子集
					;# A subset of scenarios to be made active during chip_finish step.
set ICV_IN_DESIGN_ACTIVE_SCENARIO_LIST 	"" ;# icv_in_design 阶段激活的 scenario 子集
					;# A subset of scenarios to be made active during icv_in_design step;
set ENDPOINT_OPT_ACTIVE_SCENARIO_LIST 	"" ;# endpoint_opt 阶段激活的 scenario 子集
					;# A subset of scenarios to be made active during endpoint_opt step;
set TIMING_ECO_ACTIVE_SCENARIO_LIST 	"" ;# timing_eco 阶段激活的 scenario 子集
					;# A subset of scenarios to be made active during the timing_eco step;

set ROUTE_FOCUSED_SCENARIO		"" ;# 时序驱动布线的主 scenario；空则工具按 QoR 自动选择
					;# Specify a dominant scenario for timing driven route. Timing driven route assigns layer based on the dominant scenario;
					;# default is not specified and tool will pick it based on timing QoR per scenario.
					;# If specified, script sets route.common.focus_scenario in clock_opt_opto.tcl before GRE. 

########################################################################################## 
## Variables for incremental route_detail for fixing routing DRCs（增量 route_detail 修 DRC）
## Used by route_opt.tcl and endpoint_opt.tcl
##########################################################################################
set INCR_ROUTE_DETAIL_MODE		"auto" ;# 增量 route_detail 模式: auto|true|false
					;# auto|false|true; triggers "route_detail -incremental true -initial_drc_from_input true" after the core command (hyper_route_opt in route_opt.tcl and 
set INCR_ROUTE_DETAIL_DRC_INCREASE_THRESHOLD_MIN "0.1" ;# auto 模式：DRC 增幅比例下限（默认 0.1）
					;# a float between 0 and 1; default is 0.1; this variable only takes effect if INCR_ROUTE_DETAIL_MODE = auto;
set INCR_ROUTE_DETAIL_DRC_THRESHOLD_MAX "10000" ;# auto 模式：core 命令前 DRC 超过此值则跳过
					;# a positive integer as the DRC maximum threshold; default 10000; if routing DRC before the core command (hyper_route_opt or endpoint) is larger than 
set INCR_ROUTE_DETAIL_DRC_THRESHOLD_MIN "50" ;# auto 模式：core 命令后 DRC 低于此值则跳过
					;# a positive integer as the DRC minimum threshold; default 50; if routing DRC after the core command (hyper_route_opt or endpoint) is smaller than this value,
set INCR_ROUTE_DETAIL_MAX_ITERATIONS	"" ;# route_detail 最大迭代次数（可选）
					;# (optional) a positive integer; if specified, add "-max_number_iterations $INCR_ROUTE_DETAIL_MAX_ITERATIONS" to the route_detail command;
					;# default is null which means -max_number_iterations is not used and route_detail runs with its own default max iterations

########################################################################################## 
## Variables for chip finishing related settings（chip_finish 收尾设置）
## Used by chip_finish.tcl
##########################################################################################
## Std cell filler and decap cells used by chip_finish step and post ECO refill in timing_eco step
set CHIP_FINISH_METAL_FILLER_PREFIX 	"RM_filler" ;# metal filler/decap 单元名前缀；ECO 流需要
					;# A string to specify the prefix for metal filler (decap) cells. Required if running ECO flow.
set CHIP_FINISH_NON_METAL_FILLER_PREFIX $CHIP_FINISH_METAL_FILLER_PREFIX ;# 非 metal filler 单元名前缀
					;# A string to specify the prefix for non-metal fillers.

## Signal EM（信号电迁移）
set CHIP_FINISH_SIGNAL_EM_CONSTRAINT_FORMAT "ITF" ;# 信号 EM 约束格式: ITF | ALF
					;# Specify signal EM constraint format: ITF | ALF; string is uppercase and ITF is default
set CHIP_FINISH_SIGNAL_EM_CONSTRAINT_FILE "" ;# 信号 EM 约束文件（启用 EM 分析/修复时必填）
					   ;# A constraint file which contains signal electromigration constraints;
set CHIP_FINISH_SIGNAL_EM_SAIF 		"" ;# 信号 EM 分析用 SAIF（可选）
					   ;# An optional SAIF file for the signal EM analysis.
set CHIP_FINISH_SIGNAL_EM_SCENARIO 	"" ;# 信号 EM 分析用的 active scenario（需开 setup/hold）
					   ;# Specify an active scenario which is enabled for setup and hold analysis;
set CHIP_FINISH_SIGNAL_EM_FIXING 	false ;# 是否启用信号 EM 自动修复
					   ;# Enable signal EM fixing; false | true; false is default

########################################################################################## 
## Variables for ICV in-design related settings（ICV In-Design 签核设置）
## used by icv_in_design.tcl
##########################################################################################
## signoff_check_drc specific variables
set ICV_IN_DESIGN_DRC_CHECK_RUNSET 		"" ;# signoff_check_drc 用的 foundry runset
					;# The foundry runset for ICV used by signoff_check_drc
set ICV_IN_DESIGN_DRC_CHECK_RUNDIR 		"z_check_drc" ;# signoff_check_drc 工作目录（ADR 前初始 DRC 库）

set ICV_IN_DESIGN_DRC_USER_DEFINED_OPTIONS 	"" ;# signoff_check_drc 用户自定义 ICV 选项
set ICV_IN_DESIGN_DRC_FILL_VIEW_DATA 		"read" ;# fill view 读取策略: read | read_if_uptodate | discard
set ICV_IN_DESIGN_DRC_CELL_VIEWS 		"frame" ;# 读入的 cell view: frame | layout | design
set ICV_IN_DESIGN_DRC_EXCLUDED_CELL_TYPES 	"" ;# 排除的 cell 类型: lib_cell | macro | pad | filler
set ICV_IN_DESIGN_DRC_EXCLUDED_CELL_TYPES_SYNDP "" ;# DP 阶段排除的 cell 类型
set ICV_IN_DESIGN_DRC_EXCLUDED_CELL_TYPES_SYNPNR "" ;# PNR 阶段排除的 cell 类型
set ICV_IN_DESIGN_DRC_EXCLUDED_CELL_TYPES_FINISH "" ;# finish 阶段排除的 cell 类型

set ICV_IN_DESIGN_DRC_IGNORE_CHILD_CELL_ERRORS 	false ;# true 时不报告子单元内部 DRC
set ICV_IN_DESIGN_DRC_IGNORE_CHILD_CELL_ERRORS_SYNDP	false ;# DP 阶段是否忽略子单元 DRC
set ICV_IN_DESIGN_DRC_IGNORE_CHILD_CELL_ERRORS_SYNPNR 	false ;# PNR 阶段是否忽略子单元 DRC
set ICV_IN_DESIGN_DRC_IGNORE_CHILD_CELL_ERRORS_FINISH 	false ;# finish 阶段是否忽略子单元 DRC
set ICV_IN_DESIGN_DRC_SELECT_RULES 		"" ;# 仅检查指定 DRC 规则
set ICV_IN_DESIGN_DRC_SELECT_RULES_SYNDP		"" ;# DP 阶段 select 规则
set ICV_IN_DESIGN_DRC_SELECT_RULES_SYNPNR 		"" ;# PNR 阶段 select 规则
set ICV_IN_DESIGN_DRC_SELECT_RULES_FINISH		"" ;# finish 阶段 select 规则
set ICV_IN_DESIGN_DRC_UNSELECT_RULES 		"" ;# 跳过指定 DRC 规则
set ICV_IN_DESIGN_DRC_UNSELECT_RULES_SYNDP		"" ;# DP 阶段 unselect 规则
set ICV_IN_DESIGN_DRC_UNSELECT_RULES_SYNPNR		"" ;# PNR 阶段 unselect 规则
set ICV_IN_DESIGN_DRC_UNSELECT_RULES_FINISH		"" ;# finish 阶段 unselect 规则
set STREAM_FILES_FOR_MERGE 			"" ;# 合并进设计的 GDS/OASIS 流文件列表

## singoff_fix_drc specific variables（自动 DRC 修复 ADR）
set ICV_IN_DESIGN_DRC				true ;# 是否启用 signoff_check_drc
set ICV_IN_DESIGN_ADR 				false ;# 是否在 check 之外启用 signoff_fix_drc（ADR）
set ICV_IN_DESIGN_ADR_RUNDIR 			"z_adr"	;# signoff_fix_drc 工作目录
set ICV_IN_DESIGN_ADR_USER_DEFINED_OPTIONS 	"" ;# signoff_fix_drc 用户自定义 ICV 选项

set ICV_IN_DESIGN_POST_ADR_RUNDIR 		"z_post_adr" ;# ADR 完成后的 signoff_check_drc 工作目录

set ICV_IN_DESIGN_ADR_DPT_RULES 		"" ;# ADR 中 DPT 规则修复列表
set ICV_IN_DESIGN_ADR_DPT_RUNDIR		"z_adr_with_dpt" ;# 含 DPT 修复的 ADR 工作目录
set ICV_IN_DESIGN_POST_ADR_DPT_RUNDIR		"z_post_adr_with_dpt" ;# DPT 修复后的 check_drc 工作目录

## Metal fill specific variables（金属填充）
set ICV_IN_DESIGN_METAL_FILL 			false ;# 是否启用 signoff_create_metal_fill
set ICV_IN_DESIGN_METAL_FILL_RUNSET		"" ;# metal fill runset（非 track-based 时必填）
set ICV_IN_DESIGN_METAL_FILL_RUNDIR		"z_icvFill" ;# metal fill 工作目录

set ICV_IN_DESIGN_METAL_FILL_USER_DEFINED_OPTIONS "" ;# metal fill 用户自定义 ICV 选项
set ICV_IN_DESIGN_METAL_FILL_FIX_DENSITY_ERRORS "false" ;# 插入/删除 fill 时是否遵守密度规则
set ICV_IN_DESIGN_METAL_FILL_SELECT_LAYERS 	"" ;# 指定插入 metal fill 的层；空则所有布线层

set ICV_IN_DESIGN_METAL_FILL_TIMING_DRIVEN_THRESHOLD "" ;# 时序驱动 fill 的 setup slack 阈值；空则关闭
set ICV_IN_DESIGN_METAL_FILL_TRACK_BASED 	"off" ;# track-based fill: off | 工艺节点 | generic
set ICV_IN_DESIGN_METAL_FILL_ECO_THRESHOLD 	"" ;# 增量 fill 的百分比变化阈值
set ICV_IN_DESIGN_POST_METAL_FILL_RUNDIR 	"z_MFILL_after" ;# metal fill 完成后的 check_drc 工作目录
set ICV_IN_DESIGN_METAL_FILL_TRACK_BASED_PARAMETER_FILE "auto" ;# track-based fill 参数文件: auto | 自定义文件
set ICV_IN_DESIGN_BASE_FILL false               ; # 是否启用 in-design base fill


set ICV_IN_DESIGN_BASE_FILL_RUNSET ""           ;# base layer fill 的 runset

set ICV_IN_DESIGN_BASE_FILL_RUNDIR "z_icvFill"  ; # base fill 工作目录

set ICV_IN_DESIGN_BASE_FILL_FOUNDRY_NODE ""          ; # base fill 的 foundry 工艺节点

########################################################################################## 
## Variables for route_opt target endpoint PBA CCD（endpoint_opt 目标端点 PBA CCD）
## used by endpoint_opt.tcl 
##########################################################################################
set ENDPOINT_OPT_MAX_PATHS 		"10000" ;# 收集的路径条数上限
					;# Required input; an integer; specify number of paths to collect; default 10000
set ENDPOINT_OPT_SLACK_THRESHOLD	"-0.001" ;# 收集 slack 劣于此值的路径（单位 ns）
					;# Required input; a float with unit in ns; collect paths with slack worse than the specified value for target endpoint to work on; 
set ENDPOINT_OPT_TARGET_SCENARIOS	"*" ;# 参与优化的 scenario 列表；* 表示所有 active setup scenario
					;# Required input; a list of scenarios; collect timing paths from the specified scenarios for target endpoint to work on; 
set ENDPOINT_OPT_LOOP			1 ;# 优化循环次数
					;# Required input; an integer; specify number of loops; default is 1
set ENDPOINT_OPT_PATH_GROUP_FILTER 	"" ;# 排除特定 path group 的 filter 表达式
					;# Optional input; specify a filter to exclude certain path groups from route_opt target endpoint PBA CCD; to be used by get_path_groups -filter  

########################################################################################## 
## Variables for Redhawk & Redhawk-SC (RHSC) in-design related settings（电源完整性 In-Design）
## used by redhawk_in_design_pnr.tcl & rhsc_in_design_pnr.tcl ; SNPS_INDESIGN_RH_RAIL license required
##########################################################################################
set REDHAWK_SC_DIR                      "" ;# 【必填】RedHawk-SC 可执行文件路径
set REDHAWK_DIR				"" ;# 【必填】RedHawk 可执行文件路径
set REDHAWK_GRID_FARM	        	"" ;# 提交到 GRID 运行 RedHawk/RHSC 的命令
					
set REDHAWK_PAD_FILE_NDM                "" ;# NDM 上 tap 点文件；默认用顶层 pin
set REDHAWK_PAD_FILE_PLOC               "" ;# RedHawk pad 文件
set REDHAWK_PAD_CUSTOMIZED_SCRIPT       "" ;# 自定义 create_taps 脚本

set REDHAWK_FREQUENCY			"" ;# 传给 RedHawk 的工作频率
set REDHAWK_TEMPERATURE			"" ;# 传给 RedHawk 的温度
set REDHAWK_SCENARIO		        "" ;# RedHawk 分析用的当前 scenario
set REDHAWK_MCMM_SCENARIO_CONFIG        "" ;# GRID/本地运行 RedHawk/RHSC 的 MCMM 配置脚本

set REDHAWK_USE_FC_POWER                false;# true 时用 ICC2/FC 功耗引擎代替 RedHawk/RHSC 引擎

set REDHAWK_ANALYSIS_NETS 		"" ;# 【必填】电源/地网列表，成对列出，如 "VDD1 VSS1 VDD2 VSS2"

set REDHAWK_LAYER_MAP_FILE              "" ;# 工艺层名与 LEF 层名映射文件

set REDHAWK_TECH_FILE 			"" ;# 【必填】Apache Technology File
set REDHAWK_MACROS 			"" ;# Macro 名与目录列表（成对）
set REDHAWK_SWITCH_MODEL_FILES 		"" ;# Power switch 模型文件列表
set REDHAWK_LIB_FILES 			"" ;# 【必填】.lib 文件列表
set REDHAWK_APL_FILES			"" ;# 动态分析必填：APL 文件列表（cdev/current）
set REDHAWK_EXTRA_GSR 			"" ;# 自定义 RedHawk 设置文件
set REDHAWK_ANALYSIS 			"static" ;# 【必填】分析类型: static | dynamic_vcd | dynamic_vectorless | effective_resistance | min_path_resistance | check_missing_via
set REDHAWK_OUTPUT_REPORT 		"" ;# 分析报告输出文件名
set REDHAWK_EM_ANALYSIS 	   	false ;# 是否在 static/dynamic 分析中做 EM 分析
set REDHAWK_EM_REPORT 			"" ;# EM 报告输出文件名

set REDHAWK_SCRIPT_FILE 		"" ;# RedHawk 独立运行 Tcl 脚本
set RHSC_PYTHON_SCRIPT_FILE             "" ;# RHSC 独立运行 Python 脚本
set RHSC_GENERATE_COLLATERAL	        "" ;# analyze_rail 仅生成 TWF/DEF/SPEF/PLOC 等附属文件

set REDHAWK_SWITCHING_ACTIVITY_FILE 	"" ;# 向量动态分析必填：翻转活动文件 {format file [strip_path]}
set REDHAWK_FIX_MISSING_VIAS       	false ;# check_missing_via 后是否在缺 via 处自动插 via
set REDHAWK_MISSING_VIA_POS_THRESHOLD	"" ;# 缺 via 过滤的正电压阈值
set REDHAWK_RAIL_DATABASE               RAIL_DATABASE  ;# ICC2 RedHawk Fusion 输出目录
set REDHAWK_PGA_POWER_NET               "" ;# PGA 分析用电源网
set REDHAWK_PGA_GROUND_NET              "" ;# PGA 分析用地网
set REDHAWK_PGA_NODE                    "" ;# PGA 工艺节点，如 tsmc16
set REDHAWK_PGA_ICV_DIR                 "" ;# ICV 可执行文件路径
set REDHAWK_PGA_CUSTOMIZED_SCRIPT       "" ;# PGA 自定义设置脚本

########################################################################################## 
## Variables for Timing ECO related settings（时序 ECO 设置）
## used by timing_eco.tcl
##########################################################################################
## The following ECO_OPT* variables are for ECO fusion.
set ECO_OPT_ENGINE                      "pt" ;# ECO 引擎: pt | primeeco | tweaker
set ECO_OPT_EXEC_PATH                   "" ;# 覆盖 ECO 引擎可执行文件路径；空则用环境变量中的
set ECO_OPT_DB_PATH			"" ;# PT 读取 .db 的搜索路径（eco_opt 需要）
set ECO_OPT_RECIPE_INFO			"" ;# 【eco_opt 必填】修复类型: max_capacitance|max_transition|setup|hold 等，可组合
set ECO_OPT_ENGINE_SCRIPT		"" ;# primeeco/tweaker 引擎必填：各修复类型的执行脚本
set ECO_OPT_PHYSICAL_MODE		"" ;# 物理影响模式: none | open_site | occupied_site
set ECO_OPT_WITH_PBA 			false ;# 是否为 eco_opt 启用 PBA
set ECO_OPT_EXTRACTION_MODE		"fusion_adv" ;# 寄生提取模式: fusion_adv | in_design | none
set ECO_OPT_STARRC_CONFIG_FILE 		"" ;# fusion_adv/in_design 模式必填：StarRC 配置文件
set ECO_OPT_WORK_DIR			"eco_opt_dir" ;# eco_opt 工作目录（PT 日志等）
set ECO_OPT_PRE_LINK_SCRIPT		"" ;# PT link 前执行的自定义脚本
set ECO_OPT_POST_LINK_SCRIPT		"" ;# PT link 后执行的自定义脚本
set ECO_OPT_PT_CORES_PER_SCENARIO	"4" ;# PT DMSA 每 scenario 核数
set ECO_OPT_SIGNOFF_SCENARIO_PAIR	"" ;# PT scenario 约束：{scenario sdc} 对列表
set ECO_OPT_FILLER_CELL_PREFIX 		"$CHIP_FINISH_METAL_FILLER_PREFIX" ;# eco_opt 前移除的 filler 单元前缀
set ECO_OPT_CUSTOM_OPTIONS 		"" ;# eco_opt 额外自定义选项

## The following variables apply when using a user provided PT change file.（用户提供 PT change file 时）
set PT_ECO_CHANGE_FILE 			"" ;# PT ECO change 文件；空则走 eco_opt 融合流
set PT_ECO_MODE				"default" ;# PT-ECO 模式: default | freeze_silicon
set PT_ECO_DISPLACEMENT_THRESHOLD 	"10" ;# place_eco_cells 最大位移阈值

########################################################################################## 
## Variables for Functional ECO related settings（功能 ECO 设置）
## used by functional_eco.tcl
##########################################################################################
set FUNCTIONAL_ECO_ACTIVE_SCENARIO_LIST	"" ;# functional_eco 阶段激活的 scenario 子集
set TCL_USER_FUNCTIONAL_ECO_PRE_SCRIPT	"" ;# 功能 ECO 操作前 source 的用户脚本
set TCL_USER_FUNCTIONAL_ECO_POST_SCRIPT	"" ;# route_eco 后 source 的用户脚本
set FUNCTIONAL_ECO_DISPLACEMENT_THRESHOLD "10" ;# place_eco_cells 最大位移阈值
set FUNCTIONAL_ECO_VERILOG_FILE		"" ;# 【必填】功能 ECO 用 Verilog 网表
set FUNCTIONAL_ECO_MODE			"default" ;# 功能 ECO 模式: default | freeze_silicon
set TCL_USER_PSC_AUTO_DERIVE_MAPPING_RULE_FILE "" ;# freeze silicon PSC 自动映射规则文件（eco_netlist 前 source）

########################################################################################## 
## Variables for pre and post plugins（各阶段前后插件脚本）
#  Placeholder plugin scripts are available in the rm_user_plugin_scripts directory.
##########################################################################################
set TCL_USER_NON_PERSISTENT_SCRIPT 	"non_persistent_script.tcl" ;# 每步 open block 后 source 的非持久化脚本
set TCL_USER_INIT_DESIGN_PRE_SCRIPT 	"init_design_pre_script.tcl" ;# init_design 最开始 source
set TCL_USER_INIT_DESIGN_POST_SCRIPT 	"init_design_post_script.tcl" ;# init_design save_block 前 source
set TCL_USER_PLACE_OPT_PRE_SCRIPT 	"place_opt_pre_script.tcl" ;# place_opt 前
set TCL_USER_PLACE_OPT_SCRIPT 		"" ;# 非空则替换 place_opt 默认主命令
set TCL_USER_PLACE_OPT_POST_SCRIPT 	"place_opt_post_script.tcl" ;# place_opt 后
set TCL_USER_PLACE_OPT_INCREMENTAL_PLACEMENT_POST_SCRIPT "place_opt_incremental_placement_post_script.tcl" ;# 增量布局后；仅非 SPG 流
set TCL_USER_CLOCK_OPT_CTS_PRE_SCRIPT 	"clock_opt_cts_pre_script.tcl" ;# clock_opt_cts 前
set TCL_USER_CLOCK_OPT_CTS_SCRIPT 	"" ;# 非空则替换 clock_opt_cts 默认主命令
set TCL_USER_CLOCK_OPT_CTS_POST_SCRIPT 	"clock_opt_cts_post_script.tcl" ;# clock_opt_cts 后

set TCL_USER_CLOCK_OPT_OPTO_PRE_SCRIPT 	"clock_opt_opto_pre_script.tcl" ;# clock_opt_opto 前
set TCL_USER_CLOCK_OPT_OPTO_SCRIPT 	"" ;# 非空则替换 clock_opt_opto 默认主命令
set TCL_USER_CLOCK_OPT_OPTO_POST_SCRIPT "clock_opt_opto_post_script.tcl" ;# clock_opt_opto 后

set TCL_USER_ROUTE_AUTO_PRE_SCRIPT 	"route_auto_pre_script.tcl" ;# route_auto 前
set TCL_USER_ROUTE_AUTO_SCRIPT 		"" ;# 非空则替换 route_auto 默认布线命令
set TCL_USER_ROUTE_AUTO_POST_SCRIPT 	"route_auto_post_script.tcl" ;# route_auto 后

set TCL_USER_ROUTE_OPT_PRE_SCRIPT 	"route_opt_pre_script.tcl" ;# route_opt 前
set TCL_USER_ROUTE_OPT_SCRIPT 		"" ;# 非空则替换 route_opt 默认主命令
set TCL_USER_ROUTE_OPT_1_POST_SCRIPT    "route_opt_1_post_script.tcl" ;# 第一次 route_opt 后（如二次 PG 布线）
set TCL_USER_ROUTE_OPT_2_POST_SCRIPT    "route_opt_2_post_script.tcl" ;# 第二次 route_opt 后
set TCL_USER_ROUTE_OPT_POST_SCRIPT 	"route_opt_post_script.tcl" ;# route_opt 最后

set TCL_USER_ENDPOINT_OPT_PRE_SCRIPT 	"endpoint_opt_pre_script.tcl" ;# endpoint_opt 主命令前
set TCL_USER_ENDPOINT_OPT_SCRIPT 	"" ;# 非空则替换 endpoint_opt 默认主命令
set TCL_USER_ENDPOINT_OPT_POST_SCRIPT 	"endpoint_opt_post_script.tcl" ;# endpoint_opt 主命令后

set TCL_USER_TIMING_ECO_PRE_SCRIPT 	"timing_eco_pre_script.tcl" ;# timing ECO 操作前
set TCL_USER_TIMING_ECO_POST_SCRIPT 	"timing_eco_post_script.tcl" ;# timing ECO 操作后
set ENABLE_INCR_ROUTE_POST_ECO          "1" ;# ECO 后是否做增量布线

set TCL_USER_CHIP_FINISH_PRE_SCRIPT 	"chip_finish_pre_script.tcl" ;# chip_finish filler 插入前
set TCL_USER_CHIP_FINISH_POST_SCRIPT 	"chip_finish_post_script.tcl" ;# chip_finish metal fill 后

set TCL_USER_ICV_IN_DESIGN_PRE_SCRIPT 	"icv_in_design_pre_script.tcl" ;# signoff_check_drc 前
set TCL_USER_ICV_IN_DESIGN_POST_SCRIPT 	"icv_in_design_post_script.tcl" ;# 第二次 signoff_check_drc 后

set TCL_USER_WRITE_DATA_PRE_SCRIPT 	"" ;# write_data 前
set TCL_USER_WRITE_DATA_POST_SCRIPT	"" ;# write_data 后

##########################################################################################
## Label names（各阶段 block label；$DESIGN_NAME 为 block 名，一般无需修改）
##########################################################################################
set INIT_DESIGN_BLOCK_NAME		"init_design"			;# init_design.tcl 保存的 label
set PLACE_OPT_BLOCK_NAME 		"place_opt" 			;# place_opt.tcl 保存的 label
set CLOCK_OPT_CTS_BLOCK_NAME 		"clock_opt_cts" 		;# clock_opt_cts.tcl 保存的 label
set CLOCK_OPT_OPTO_BLOCK_NAME 		"clock_opt_opto" 		;# clock_opt_opto.tcl 保存的 label
set ROUTE_AUTO_BLOCK_NAME 		"route_auto" 			;# route_auto.tcl 保存的 label
set ROUTE_OPT_BLOCK_NAME 		"route_opt" 			;# route_opt.tcl 保存的 label

set CHIP_FINISH_BLOCK_NAME 		"chip_finish" 			;# chip_finish.tcl 保存的 label
set ICV_IN_DESIGN_FROM_BLOCK_NAME	"chip_finish" 			;# icv_in_design.tcl 输入 block label
set ICV_IN_DESIGN_BLOCK_NAME		"icv_in_design" 		;# icv_in_design.tcl 保存的 label

set WRITE_DATA_FROM_BLOCK_NAME 		$ICV_IN_DESIGN_BLOCK_NAME 	;# write_data.tcl 源 block label
set WRITE_DATA_BLOCK_NAME 		"write_data" 			;# write_data.tcl 保存的 label

set ENDPOINT_OPT_BLOCK_NAME		"endpoint_opt"			;# endpoint_opt.tcl 保存的 label
set TIMING_ECO_FROM_BLOCK_NAME		"icv_in_design"			;# timing_eco.tcl 输入 block label
set TIMING_ECO_BLOCK_NAME		"timing_eco" 			;# timing_eco.tcl 保存的 label
set FUNCTIONAL_ECO_FROM_BLOCK_NAME	"icv_in_design" 		;# functional_eco.tcl 输入 block label
set FUNCTIONAL_ECO_BLOCK_NAME		"functional_eco"		;# functional_eco.tcl 保存的 label

set REDHAWK_IN_DESIGN_FROM_BLOCK_NAME   $ROUTE_OPT_BLOCK_NAME		;# RedHawk In-Design 起始 block label
set REDHAWK_IN_DESIGN_BLOCK_NAME 	"redhawk_in_design"		;# RedHawk In-Design 保存的 label

##########################################################################################
## Reporting and other variables（报告与目录设置）
##########################################################################################
set SUPPLEMENTAL_SEARCH_PATH		"" ;# 额外 search_path 列表（header_*.tcl 中 set search_path 使用）
set OUTPUTS_DIR				"./outputs_icc2" ;# 交付物输出目录（write_data.tcl）
set REPORTS_DIR				"./rpts_icc2" ;# 报告输出目录（report_qor.tcl）
set LOGS_DIR				"./logs_icc2" ;# 日志目录（Makefile*）

set REPORT_QOR				true ;# 每步结束是否跑 QoR 报告
set REPORT_VERBOSE			false ;# 是否额外跑 report_timing -max_paths 300
set REPORT_QOR_REPORT_CONGESTION	true ;# 布线前步骤是否报告拥堵

set REPORT_QOR_REPORT_POWER		true ;# 是否报告功耗/时钟功耗 QoR
set REPORT_POWER_SAIF_FILE		"" ;# report_power 用 SAIF 文件（可选）
set REPORT_POWER_SAIF_MAP		"" ;# report_power 用 SAIF map（可选）

set WRITE_QOR_DATA			true ;# 是否生成 QoR HTML（compare_qor_data）
set WRITE_QOR_DATA_DIR			"./qor_data" ;# write_qor_data 目录
set COMPARE_QOR_DATA_DIR		"./compare_qor_data" ;# compare_qor_data 目录
set REPORT_PARALLEL_SUBMIT_COMMAND 	"" ;# 并行报告的作业提交命令；空则串行
set REPORT_PARALLEL_MAX_CORES 		4 ;# 并行报告最大核数
set SET_HOST_OPTIONS_MAX_CORES		8 ;# set_host_options -max_cores 上限
set TCL_USER_SUPPLEMENTAL_REPORTS_SCRIPT "" ;# 补充报告脚本


##########################################################################################
## Variables related to flow controls of flat PNR, hierarchical PNR and transition with DP
## 流程控制：flat / hier PNR 及与 DP 的衔接
##########################################################################################
set DESIGN_STYLE			"flat"	;# 设计风格: flat（扁平 PNR）| hier（层次化 PNR）
set PHYSICAL_HIERARCHY_LEVEL		"bottom" ;# 层次化 PNR 当前物理层级: top | intermediate | bottom
set RELEASE_DIR_DP		"" 	;# DP RM 交付库目录；INIT_DESIGN_INPUT=DP_RM_NDM 时 flat PNR 需要
set RELEASE_DIR_PNR		"" 	;# PNR RM 交付库目录；层次化 PNR 从此获取子块库

##########################################################################################
## Hierarchical PNR Variables（层次化 PNR 变量）
##########################################################################################
## For designs where the blocks are bound to abstracts（绑定 abstract 的子块）
set SUB_BLOCK_REFS                   	[list ] ;# 子块设计名列表（flattened=直接子块；nested=所有下层物理块）
set SUB_BLOCK_LIBRARIES			[list ] ;# 自顶向下 DP 建库的子块 NDM 库列表；与 SUB_BLOCK_REFS 一一对应
set USE_ABSTRACTS_FOR_BLOCKS        	[list ] ;# 下一层将绑定 abstract 的物理块设计名
set CTL_FOR_ABSTRACT_BLOCKS		[list ] ;# 顶层 compile 所需的 CTL 模型完整路径列表

## 默认使用下层 icv_in_design 之后生成的 abstract；可按阶段改用其他 label
set BLOCK_ABSTRACT_FOR_PLACE_OPT 	"$ICV_IN_DESIGN_BLOCK_NAME" ;# place_opt 使用的子块 abstract label
set BLOCK_ABSTRACT_FOR_CLOCK_OPT_CTS    "$ICV_IN_DESIGN_BLOCK_NAME" ;# clock_opt_cts 使用的子块 abstract label
set BLOCK_ABSTRACT_FOR_CLOCK_OPT_OPTO   "$ICV_IN_DESIGN_BLOCK_NAME" ;# clock_opt_opto 使用的子块 abstract label
set BLOCK_ABSTRACT_FOR_ROUTE_AUTO       "$ICV_IN_DESIGN_BLOCK_NAME" ;# route_auto 使用的子块 abstract label
set BLOCK_ABSTRACT_FOR_ROUTE_OPT        "$ICV_IN_DESIGN_BLOCK_NAME" ;# route_opt 使用的子块 abstract label
set BLOCK_ABSTRACT_FOR_CHIP_FINISH      "$ICV_IN_DESIGN_BLOCK_NAME" ;# chip_finish 使用的子块 abstract label
set BLOCK_ABSTRACT_FOR_ICV_IN_DESIGN    "$ICV_IN_DESIGN_BLOCK_NAME" ;# icv_in_design 使用的子块 abstract label

set USE_ABSTRACTS_FOR_POWER_ANALYSIS 	false ;# 是否在 abstract 子块内做功耗分析
set USE_ABSTRACTS_FOR_SIGNAL_EM_ANALYSIS false ;# 是否在 abstract 子块内做 signal EM 分析

set ABSTRACT_TYPE_FOR_MPH_BLOCKS "flattened" ;# 多级物理层次块的 abstract 类型: nested | flattened
set CHECK_HIER_TIMING_CONSTRAINTS_CONSISTENCY true ;# check_design 时是否检查顶层与子块时序约束一致性

set LIBRARY_DB_PATH        		"" ;# NDM 内 .db 不在本地时，实施工具所需的 .db 路径

########################################################################################## 
## Hierarchical PNR Variables for clock_opt_cts related settings
##########################################################################################
set PROMOTE_CLOCK_BALANCE_POINTS	false ;# 中间/顶层实现时是否从子块提升 clock balance points

########################################################################################## 
## Hierarchical PNR Variables for designs where some of the blocks are bound to ETMs
##########################################################################################
set WRITE_DATA_FOR_ETM_GENERATION       false ;# 是否写出 PrimeTime 生成 ETM 所需数据
set WRITE_DATA_FOR_ETM_BLOCK_NAME       $ICV_IN_DESIGN_BLOCK_NAME ;# write_data_for_etm 起始 block label

