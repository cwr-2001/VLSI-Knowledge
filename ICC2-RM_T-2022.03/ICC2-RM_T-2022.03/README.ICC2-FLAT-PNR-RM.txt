###############################################################################
# Synopsys(R) IC Compiler(TM) II Flat Place and Route Reference Methodology
# Version: T-2022.03
# Copyright (C) 2014-2022 Synopsys, Inc. All rights reserved.
###############################################################################

Overview
========
A reference methodology (RM) provides a set of reference scripts that serve 
as a starting point for running a tool. These scripts are not designed 
to run in their current form. You should use them as a reference and adapt 
them for use in your design environment.

This RM can optionally be run directly in LYNX.
See ./rm_in_lynx/README.running_RM_in_Lynx_RTM.txt for more details.

Features
========
* Supports UPF-prime and golden UPF flows.
* Supports advanced node designs with settings specific to established and advanced nodes.
* Supports Design Compiler to the IC Compiler II ASCII and physical guidance flows.
* Supports design library hand-off from the ICC2-DP-RM.
* Supports the multicorner-multimode flow.
* Supports advanced on-chip variation (AOCV) and parametric on-chip variation 
  (POCV).
* Identifies settings specific to power, performance, and area-focused (PPA) 
  flows in the generated scripts.
* Supports low-power placement, leakage-power optimizations, total-power 
  optimizations, multibit banking, and multibit debanking.
* Includes integrated clock-gating (ICG) optimization features in place_opt.
* Includes concurrent clock and data optimization (CCD) for pre-route and 
  post-route optimizations.
* Supports non-default clock routing rules, such as double spacing, double 
  width, and shielding.
* Supports clock tree optimization after clock routing and after signal routing.
* Includes antenna fixing, redundant via insertion, shielding, and 
  crosstalk reduction.
* Includes signal electromigration analysis and fixing.
* Includes metal and non-metal filler cell insertion.
* Includes IC Validator In-Design signoff design rule checking and automatic 
  design rule fixing.
* Includes IC Validator In-Design pattern-based or track-based metal fill 
  insertion.
* Includes a consolidated reporting step at the end of each stage.
* Includes a write_data step to write out Verilog, UPF, DEF, Tcl, SPEF, 
  GDSII, and OASIS files.
* Supports Formality formal verification.
* Supports RedHawk Fusion Flows.
* Supports Verification Compiler low power static signoff analysis.
* Supports design fusion, which performs logic restructuring using the synthesis analysis to improve area, 
  power, and timing.
* Supports ECO fusion, which blends IC Compiler II, StarRC, and PrimeTime features in a single native 
  invocation system. 
* Supports a standalone timing_eco step, which can either run ECO Fusion or source user provided PT change file.

Instructions for Using the IC Compiler II Flat Reference Methodology
====================================================================
To run the standard reference methodology flow, use the following command:

   % make -f rm_setup/Makefile_pnr all

You can replace "all" with any other step, such as place_opt or clock_opt_cts,in the Makefile_pnr file.

Flow Steps
==========
The IC Compiler II Flat Reference Methodology flow includes the following 
steps (see the makefile: rm_setup/Makefile_pnr):

The following list includes the default steps with brief descriptions:
1. init_design 
  * Data preparation
  * Reads design inputs
  * Creates the design
  * Reads floorplan files
  * Check floorplan
  * Load timing and design constraints
 
2. place_opt
  * Placement and optimization
  * By default, concurrent clock and data (CCD) optimization is on
 
3. clock_opt_cts
  * Clock tree synthesis and clock routing
  * By default, concurrent clock and data (CCD) optimization is on
 
4. clock_opt_opto
  * Data path optimization based on propagated clock latencies and clock route patching
  * By default, concurrent clock and data (CCD) optimization is on
  
5. route_auto
  * Global routing, track assignment, detail routing for signal nets, and shield creation.
  
6. route_opt
  * Post-route optimization
  * By default, concurrent clock and data (CCD) optimization is on
  
7. chip_finish
  * Decouping capacitance cell insertion, regular filler cell insertion, and signal electromigration analysis and fixing.
  
8. icv_in_design
  * Signoff design rule checking, automatic design rule fixing, and metal fill creation with IC Validator In-Design.
  
9. (Optional) write_data
  * Runs the change_names command and writes out Verilog, DEF, GDSII, OASIS, 
  * UPF, UPF supplemental file, write_script, and parasitics output with write_data.tcl

10. (Optional) timing_eco
  * Timing ECO with timing_eco.tcl

11. (Optional) functional_eco
  Timing ECO with functional_eco.tcl

12. (Optional) redhawk_in_design or rhsc_in_design_pnr
  RedHawk Fusion flows with the redhawk_in_design_pnr.tcl or RedHawk-SC with the rhsc_in_design_pnr.tcl

13. (Optional) fm
  Formality formal verification with the fm.tcl script

* (Optional) vc_lp
  Verification Compiler low-power static signoff analysis with the vc_lp.tcl script

* (Optional) summary
  Summary report (in the table format) across the flow with summary.tcl

Files Included with the IC Compiler II Flat Reference Methodology
=================================================================
## Makefile and setup scripts are all in the rm_setup

* rm_setup/Makefile_pnr
  - Makefile for running the IC Compiler II Flat Place and Route Reference Methodology scripts

* rm_setup/design_setup.tcl          
  - Defines majority of variables used by the RM scripts
     - Variables specific to design inputs (refer to "# Variables for design prep which are used by init_design.tcl" section)  
     - Variables for user plugins (refer to "## Variables for pre and post plugins" section)
       These are hooks which you can use to insert your customizations to the flow without making script changes.
       The plugins are available per task. The naming convention is TCL_USER_<TASK NAME>_PRE_SCRIPT and TCL_USER_<TASK NAME>_POST_SCRIPT, etc.
       For example, 
	TCL_USER_INIT_DESIGN_PRE_SCRIPT
	TCL_USER_INIT_DESIGN_POST_SCRIPT
	TCL_USER_PLACE_OPT_PRE_SCRIPT
	TCL_USER_PLACE_OPT_POST_SCRIPT
     - Variables for other optional features

* rm_setup/header_icc2_pnr.tcl
  - None-variable related setup, such as : search_path, set_host_options, suppress_message, set_message_info, and creates necessary outputs and reports dir 
  - Not intended to be edited

* rm_setup/icc2_pnr_setp.tcl
  - Defines variables for controlling special features
    Most of the special features have tight integration with set_stage command for ease of use, where set_stage applies appropriate app options 
    or additional sanity checks. Here is the list of special features :

	SET_QOR_STRATEGY_METRIC :	Specify one metric for the set_qor_strategy -metric option and the settings will be configured to optimize the specified target metric
	
	SET_QOR_STRATEGY_MODE :		Specify one mode for set_qor_strategy -mode option and the settings will be configured for the target mode

 	ENABLE_REDUCED_EFFORT :		enables set_qor_strategy -reduced_effort

 	CTS_STYLE :			controls the CTS style. You can set it to MSCTS to enable MSCTS in the flow; take effect in place_opt.tcl
 
 	ENABLE_SPG :			enables SPG flow (physical guidance flow); takes effect in place_opt.tcl

 	ENABLE_PERFORMANCE_VIA_LADDER :	enables set_stage command to enable performance via ladder settings for applicable technology nodes; takes effect in place_opt.tcl

 	ENABLE_DPS :			enables set_stage command to enable DPS (dynamic power shaping) settings; takes effect in place_opt.tcl

	ENABLE_IRDP :			enables set_stage command to enable IR-aware placement (IRDP); takes effect in clock_opt_opto.tcl

 	ENABLE_MULTIBIT :		enables multibit banking and debanking if SET_QOR_STRATEGY_METRIC is set to timing or leakage_power
 	      				if SET_QOR_STRATEGY_METRIC is set to total_power, multibit banking and debanking is configured by set_qor_strategy automatically
	
 	ENABLE_HIGH_UTILIZATION_FLOW : 	enables extra commands to address high utilization

* sidefile_setup.tcl
  - The script sets pointers for technology specific sidefiles and settings
    For mature nodes, sidefile_setup.tcl under rm_setup/ is pre-configured.
    For advanced nodes, sidefile_setup.tcl under rm_setup/ is a template for reference only; 
    the actual sidefile_setup.tcl with pre-configured values will be available as part of the technology bundle (sidefile tar ball) from a separate download,
    which will be included under rm_tech_scripts/ along with rest of the sidefiles.
  - sidefile_setup.tcl will be sourced by each implementation script

## Implementation scripts are all in the rm_icc2_pnr_scripts directory

* For the init_design step: rm_icc2_pnr_scripts/init_design.tcl

  1. This script reads or creates the design, depending on the setting of INIT_DESIGN_INPUT :

     - If INIT_DESIGN_INPUT is set to NDM :
		The script opens $DESIGN_LIBRARY and copies block specified by $INIT_DESIGN_INPUT_BLOCK_NAME to ${DESIGN_NAME}/${INIT_DESIGN_BLOCK_NAME}

     - If INIT_DESIGN_INPUT is set to DC_ASCII : 
		The script creates $DESIGN_LIBRARY, sources the script generated by the write_icc2_scripts command in Design Compiler 
		to re-creates the design, and then commits the UPF.

		The script generated by the write_icc2_scripts command in Design Compiler is assumed to be in this location :
		${DCRM_RESULTS_DIR}/${DCRM_FINAL_DESIGN_ICC2}/${DESIGN_NAME}.icc2_script.tcl
		Edit the variables to choose a different path.
 
     - If INIT_DESIGN_INPUT is set to ASCII : 
		The script creates $DESIGN_LIBRARY, reads the Verilog netlist, loads the UPF file, commits the UPF,
		reads the floorplan specified by $TCL_FLOORPLAN_FILE or $DEF_FLOORPLAN_FILES, and then reads $DEF_SCAN_FILE

  2. The script then :
     - Sources $TCL_ADDITIONAL_FLOORPLAN_FILE for additional floorplan constraints (if specified)
     - Resets incoming app options if RESET_CHECK_STAGE_SETTINGS is set to all (optional)
     - Runs set_technology (for applicable nodes, TECHNOLOGY_NODE will be preconfigured by sidefile_setup.tcl to trigger set_technology command)
     - Sources technolgoy sidefile $SIDEFILE_INIT_DESIGN for applicable nodes (preconfigured by sidefile_setup.tcl)
     - Sources $TCL_USER_CONNECT_PG_NET_SCRIPT (if specified) or runs connect_pg_net
     - Sources $TCL_VIA_LADDER_DEFINITION_FILE and $TCL_SET_VIA_LADDER_CANDIDATE_FILE (if specified)		
     - Runs basic floorplan checks, such as missing site rows/signal terminals/tracks, unplaced macros, and unplaced boundary or tap cells etc.
       if any, script prints RM-error to the log, sets RM_FAILURE, and skips creation of the touch file init_design at the end of script, 
       which will prevent Makefile_pnr from proceeding to next target.
     - Loads timing and design constraints, such as :
	$TCL_PARASITIC_SETUP_FILE
	$TCL_MCMM_SETUP_FILE
	$TCL_POCV_SETUP_FILE
	$TCL_PLACEMENT_CONSTRAINT_FILE_LIST
	$TCL_CTS_NDR_RULE_FILE
	$TCL_LIB_CELL_PURPOSE_FILE
	$SAIF_FILE_LIST

* For the place_opt step: rm_icc2_pnr_scripts/place_opt.tcl
  This script runs the set_qor_strategy, set_stage -step placement, MSCTS setup, and 2-pass place_opt commands.

* For the clock_opt_cts step: rm_icc2_pnr_scripts/clock_opt_cts.tcl
  This script runs set_stage -step cts, performs CCD clock tree synthesis, routing, and reporting.

* For the clock_opt_opto step: rm_icc2_pnr_scripts/clock_opt_opto.tcl
  
  This script runs the set_stage -step post_cts_opto and clock_opt -from final_opto command, which performs CCD optimizations.
  ENABLE_IRAP enables IRAP (IR-aware placement) if a configuration file is provided through TCL_IRAP_CONFIG_FILE.

* For the route_opt step: rm_icc2_pnr_scripts/route_opt.tcl
  
  This script runs the set_stage -step post_route, and hyper_route_opt command for post-route optimization.
  If ENABLE_IRDCCD is set to true in rm_setup/icc2_pnr_setup.tcl, the script falls back to classic 3 route_opt command flow. 

* For the chip_finish step: rm_icc2_pnr_scripts/chip_finish.tcl

  This script runs the create_stdcell_fillers command for metal and non-metal filler cell insertion; 
  it also runs signal electromigration analysis and fixing. 

* For the icv_in_design step: rm_icc2_pnr_scripts/icv_in_design.tcl

  This script runs the IC Validator In-Design signoff_check_drc command for 
  design rule checking, signoff_fix_drc command for automatic design rule fixing,
  and signoff_create_metal_fill command for metal fill creation.

* For the write_data step: rm_icc2_pnr_scripts/write_data.tcl

  This script generates output files for the design. It runs the 
  write_verilog, save_upf, write_def, write_script, write_parasitics, write_routing_scripts,
  write_gds, and write_gds commands.

* For the timing_eco step: rm_icc2_pnr_scripts/timing_eco.tcl
  
  Supports either ECO Fusion (if PT_ECO_CHANGE_FILE is unspecified) or user-provided PT change file (if PT_ECO_CHANGE_FILE is specified). 

* For the functional_eco step: rm_icc2_pnr_scripts/functional_eco.tcl
  
  FUNCTIONAL_ECO_MODE controls either to performs MPI mode or freeze silicon mode. 

* For formal verification: rm_icc2_pnr_scripts/fm.tcl

  This script runs in Formality and checks the files going into the IC Compiler II tool against the resulting Verilog netlist from the
  IC Compiler II tool.

* For Verification Compiler low power static signoff: 
  rm_icc2_pnr_scripts/vc_lp.tcl    

  This script runs in VC-LP and checks the Verilog and UPF files generated by the 
  IC Compiler II tool with the check_lp and report_lp commands. 

* For RedHawk Fusion flows:
  
  rm_icc2_pnr_scripts/redhawk_in_design_pnr.tcl (Redhawk) or rhsc_in_design_pnr.tcl (Redhawk-SC)

  The script performs the following analyses on the power grid structure:
    - Rail Integrity Check (including the Missing Via Check)
    - Missing Via Insertion
    - Static
    - Vectorless Dynamic
    - Vector-Based Dynamic
    - Electromigration
    - Minimum Path Resistance
    - Effective Resistance
    - Power Grid Augmentation (PGA)

  Before performing any of the previous analyses, you must
  - Set the REDHAWK_* variables in rm_setup/design.tcl
  - Ensure that the RedHawk executable can be found by setting the variable REDHAWK_DIR (Redhawk) or REDHAWK_SC_DIR (Redhawk-SC) in rm_setup/design_setup.tcl,
    otherwise script will attempt to find the executible from unix seach path.

## Supporting scripts

* rm_icc2_pnr_scripts/report_qor.tcl

  The script is called by each of the implementation scripts to run the reporting commands, such as : 
  report_mode, report_scenarios, report_pvt, report_constraint, report_qor, 
  report_timing, analyze_design_violations, report_threshold_voltage_group, 
  report_power, report_mv_path, report_clock_qor, report_design, report_congestion 
  check_design, check_netlist, report_app_options, and report_user_units, etc
 
  The reports are written to the $REPORTS_DIR/$REPORTS_PREFIX directory.
  REPORTS_PREFIX is set to the name of each task, such as place_opt, clock_opt_cts, etc.
  For example, reports for the place_opt task would be located under rpts_icc2/place_opt/   

* examples/

  This directory includes many examples as referred to by the main scripts.
  These examples show typical usage of the commands and features. Once customized for your design, can be plugged into RM.
  
  Most of the example files are named with the associated variable name as the prefix.
  For example, TCL_AOCV_SETUP_FILE.tcl is an example for $TCL_AOCV_SETUP_FILE; 
  TCL_VIA_LADDER_DEFINITION_FILE.txt is an example for $TCL_VIA_LADDER_DEFINITION_FILE
  These example files will need to be customized for your design before use.

* rm_icc2_pnr_scripts/init_design.tech_setup.tcl
  
  This script includes technology-related settings, such as routing direction, 
  offset, site default, and the site symmetry list.

  If you use a technology file (TECH_FILE is defined), the init_design.tcl
  script sources the technology setup script before the read_def or
  initialize_floorplan command.

  If you use a technology library (TECH_LIB is defined), by default, the
  init_design.tcl script assumes that the technology information is already 
  loaded and does not source the technology setup script. To source the 
  technology setup script, set the TECH_LIB_INCLUDES_TECH_SETUP_INFO variable 
  to false.

* rm_icc2_pnr_scripts/set_lib_cell_purpose.tcl
  
  This script includes the following library cell purpose restrictions, and is sourced 
  by rm_icc2_pnr_scripts/place_opt.tcl:
  - Do not use, which is controlled by the TCL_LIB_CELL_DONT_USE_FILE variable
  - Hold fixing, which is controlled by the HOLD_FIX_LIB_CELL_PATTERN_LIST
    variable
  - Clock tree synthesis, which is controlled by the CTS_LIB_CELL_PATTERN_LIST variable
  - Clock tree synthesis only, which is controlled by the CTS_ONLY_LIB_CELL_PATTERN_LIST 
    variable

* rm_icc2_pnr_scripts/summary.tcl
  
  This script is sourced when you choose the summary target. It generates 
  a summary report (summary.rpt) in the $REPORTS_DIR directory for all steps 
  completed in the flow. The summary data is presented in the table format.

