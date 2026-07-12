##########################################################################################
# Tool: IC Compiler II 
# Script: init_dp_fc.tcl
# Version: T-2022.03
# Copyright (C) 2014-2022 Synopsys, Inc. All rights reserved.
##########################################################################################

source ./rm_utilities/procs_global.tcl 
source ./rm_utilities/procs_icc2.tcl 
rm_source -file ./rm_setup/design_setup.tcl
rm_source -file ./rm_setup/icc2_dp_setup.tcl
rm_source -file ./rm_setup/header_icc2_dp.tcl
rm_source -file sidefile_setup.tcl -after_file sidefile_setup_override.tcl

set REPORT_PREFIX ${INIT_DP_BLOCK_NAME}
file mkdir ${REPORTS_DIR}/${REPORT_PREFIX}

################################################################################
## Pre-init_dp User Customizations
################################################################################
rm_source -file $TCL_USER_INIT_DP_PRE_SCRIPT -optional -print "TCL_USER_INIT_DP_PRE_SCRIPT"

################################################################################
# Create and read the design	
################################################################################

if {[file exists ${WORK_DIR}/${DESIGN_LIBRARY}]} {
   file delete -force ${WORK_DIR}/${DESIGN_LIBRARY}
}

set create_lib_cmd "create_lib ${WORK_DIR}/${DESIGN_LIBRARY}" ;

if {[file exists [which $TECH_FILE]]} {
   lappend create_lib_cmd -tech $TECH_FILE ;# recommended
} elseif {$TECH_LIB != ""} {
   lappend create_lib_cmd -use_technology_lib $TECH_LIB ;# optional
}
lappend create_lib_cmd -ref_libs $REFERENCE_LIBRARY
puts "RM-info : $create_lib_cmd"
eval $create_lib_cmd

if {$DP_HIGH_CAPACITY_MODE} {
   ## Read in the DESIGN_NAME outline.  This will create the outline view in the database.
   ## - Running high capacity mode when block views are abstracts.
   puts "RM-info : Reading verilog outline (${VERILOG_NETLIST_FILES})"
   read_verilog_outline -design ${DESIGN_NAME}/${INIT_DP_BLOCK_NAME} -top ${DESIGN_NAME} ${VERILOG_NETLIST_FILES}
} else {
   ## Read in the full DESIGN_NAME.  This will create the DESIGN_NAME view in the database
   puts "RM-info : Reading full chip verilog (${VERILOG_NETLIST_FILES})"
   read_verilog -design ${DESIGN_NAME}/${INIT_DP_BLOCK_NAME} -top ${DESIGN_NAME} ${VERILOG_NETLIST_FILES}
}

## Design check manager
if {$EARLY_DATA_CHECK_POLICY != "none"} {set_early_data_check_policy -policy $EARLY_DATA_CHECK_POLICY -if_not_exist}

## Set Design Planning Flow Strategy
rm_set_dp_flow_strategy -dp_stage $DP_STAGE -dp_flow hierarchical -hier_fp_style $FLOORPLAN_STYLE

## Set technology mega switch
if {$TECHNOLOGY_NODE != "" && !$SET_TECHNOLOGY_AFTER_FLOORPLAN} {
   set_technology -node $TECHNOLOGY_NODE
}

## Technology setup for routing layer direction, offset, site default, and site symmetry.
#  If TECH_FILE is specified, they should be properly set.
#  If TECH_LIB is used and it does not contain such information, then they should be set here as well.
if {$TECH_FILE != "" || ($TECH_LIB != "" && !$TECH_LIB_INCLUDES_TECH_SETUP_INFO)} {
   rm_source -file $TCL_TECH_SETUP_FILE
}

# Specify a Tcl script to read in your TLU+ files by using the read_parasitic_tech command
#  Refer to examples/TCL_PARASITIC_SETUP_FILE.tcl for sample commands
rm_source -file $TCL_PARASITIC_SETUP_FILE -optional -print "TCL_PARASITIC_SETUP_FILE"

rm_source -file $TCL_TIMING_RULER_SETUP_FILE -optional -print "Warning: TCL_TIMING_RULER_SETUP_FILE not specified. Timing ruler will not work accurately if it is not defined."

##################################################################################################
## 				Routing settings						##
##################################################################################################
## Set max routing layer
if {$MAX_ROUTING_LAYER != ""} {set_ignored_layers -max_routing_layer $MAX_ROUTING_LAYER}
## Set min routing layer
if {$MIN_ROUTING_LAYER != ""} {set_ignored_layers -min_routing_layer $MIN_ROUTING_LAYER}

####################################
# Check Design: Pre-Floorplanning
####################################
if {$CHECK_DESIGN} {
   redirect -file ${REPORTS_DIR}/${REPORT_PREFIX}/check_design.pre_floorplan \
    {check_design -ems_database check_design.pre_floorplan.ems -checks dp_pre_floorplan}
}

####################################
# Floorplanning
####################################
## Floorplanning by reading $DEF_FLOORPLAN_FILES_DP (supports multiple DEF files)
#  Script firstly checks if all the specified DEF files are valid, if not, read_def is skipped
if {$DEF_FLOORPLAN_FILES_DP != ""} {
   set RM_DEF_FLOORPLAN_FILE_is_not_found FALSE
   foreach def_file $DEF_FLOORPLAN_FILES_DP {
      if {![file exists [which $def_file]]} {
         puts "RM-error : DEF floorplan file ($def_file) is invalid."
         set RM_DEF_FLOORPLAN_FILE_is_not_found TRUE
      }
   }

   if {!$RM_DEF_FLOORPLAN_FILE_is_not_found} {
      set read_def_cmd "read_def $DEF_READ_OPTIONS [list $DEF_FLOORPLAN_FILES_DP]"
      ## if {$DEF_SITE_NAME_PAIRS != ""} {lappend read_def_cmd -convert $DEF_SITE_NAME_PAIRS}
      puts "RM-info : Creating floorplan from DEF file DEF_FLOORPLAN_FILES_DP ($DEF_FLOORPLAN_FILES_DP)"
      puts "RM-info: $read_def_cmd"
      eval ${read_def_cmd}
   } else {
      puts "RM-error : At least one of the DEF_FLOORPLAN_FILES_DP specified is invalid. Pls correct it."
      puts "RM-info: Skipped reading of DEF_FLOORPLAN_FILES_DP"
   }
} elseif {[file exists [which $TCL_FLOORPLAN_FILE_DP]]} {
   rm_source -file $TCL_FLOORPLAN_FILE_DP
} else {
   ## Floorplan initialization (node specific file)
   rm_source -file $SIDEFILE_INIT_DP_FLOORPLANNING

   rm_source -file $TCL_TRACK_CREATION_FILE -optional -print "TCL_TRACK_CREATION_FILE"
}

###########################################
## General process node specific settings
###########################################

## set_technology for nodes requiring set_technology to be done after floorplanning or incoming designs without set_technology 
if {$TECHNOLOGY_NODE != "" && ($SET_TECHNOLOGY_AFTER_FLOORPLAN || [get_attribute [current_block] technology_node -quiet] == "")} {
	set_technology -node $TECHNOLOGY_NODE
}

## Technology settings (node specific file)
rm_source -file $SIDEFILE_INIT_DP_TECH_SETTINGS -optional -print "SIDEFILE_INIT_DP_TECH_SETTINGS"

## Placement spacing labels, spacing rules, and abutment rules 
if {$TCL_PLACEMENT_CONSTRAINT_FILE_LIST != ""} {
  foreach file $TCL_PLACEMENT_CONSTRAINT_FILE_LIST {
    rm_source -file $file
  }
}

## Lib cell usage restrictions (set_lib_cell_purpose)
## By default, RM sources set_lib_cell_purpose.tcl for dont use, tie cell, hold fixing, CTS and CTS-exclusive cell restrictions. 
## For advanced nodes, set_lib_cell_purpose.tcl sources node specific dont use sidefile for the corresponding node.
## You can replace it with your own script by specifying the TCL_LIB_CELL_PURPOSE_FILE variable.  
rm_source -file $TCL_LIB_CELL_PURPOSE_FILE -optional -print "TCL_LIB_CELL_PURPOSE_FILE"

################################################################################
## Post-init_dp User Customizations
################################################################################
rm_source -file $TCL_USER_INIT_DP_POST_SCRIPT -optional -print "TCL_USER_INIT_DP_POST_SCRIPT"

if {$COMPRESS_LIBS} {
  save_lib -all -compress
} else {
  save_lib -all
}


print_message_info -ids * -summary
echo [date] > init_dp

exit 
