##########################################################################################
# Tool: IC Compiler II ;
# Script: split_constraints.tcl
# Version: T-2022.03
# Copyright (C) 2014-2022 Synopsys, Inc. All rights reserved.
##########################################################################################


source ./rm_utilities/procs_global.tcl 
source ./rm_utilities/procs_icc2.tcl 
rm_source -file ./rm_setup/design_setup.tcl
rm_source -file ./rm_setup/icc2_dp_setup.tcl
rm_source -file ./rm_setup/header_icc2_dp.tcl
rm_source -file sidefile_setup.tcl -after_file sidefile_setup_override.tcl

set REPORT_PREFIX ${SPLIT_CONSTRAINTS_BLOCK_NAME}
file mkdir ${REPORTS_DIR}/${REPORT_PREFIX}

################################################################################
# Create and read the design	
################################################################################
set SUFFIX "_split"

if {[file exists ${WORK_DIR}/${DESIGN_LIBRARY}${SUFFIX}]} {
   file delete -force ${WORK_DIR}/${DESIGN_LIBRARY}${SUFFIX}
}

set create_lib_cmd "create_lib ${WORK_DIR}/${DESIGN_LIBRARY}${SUFFIX}"

if {[file exists [which $TECH_FILE]]} {
   lappend create_lib_cmd -tech $TECH_FILE ;# recommended
} elseif {$TECH_LIB != ""} {
   lappend create_lib_cmd -use_technology_lib $TECH_LIB ;# optional
}
lappend create_lib_cmd -ref_libs $REFERENCE_LIBRARY
puts "RM-info : $create_lib_cmd"
eval $create_lib_cmd

puts "RM-info : Reading verilog file(s) $VERILOG_NETLIST_FILES"
read_verilog -top ${DESIGN_NAME} ${VERILOG_NETLIST_FILES}

# Load UPF file
if {[file exists [which $UPF_FILE]]} {
   puts "RM-info : Loading UPF file $UPF_FILE"
   load_upf $UPF_FILE
   if {[file exists [which $UPF_UPDATE_SUPPLY_SET_FILE]]} {
      puts "RM-info : Loading UPF update supply set file $UPF_UPDATE_SUPPLY_SET_FILE"
      load_upf $UPF_UPDATE_SUPPLY_SET_FILE
   }
} else {
   puts "RM-warning : UPF file not found"
}

## Specify a Tcl script to read in your TLU+ files by using the read_parasitic_tech command
#  Refer to examples/TCL_PARASITIC_SETUP_FILE.tcl for sample commands
rm_source -file $TCL_PARASITIC_SETUP_FILE -optional -print "TCL_PARASITIC_SETUP_FILE"

## Specify a Tcl script to create your corners, modes, scenarios and load respective constraints;
#  Two examples are provided: 
#  - examples/TCL_MCMM_SETUP_FILE.explicit.tcl: provide mode, corner, and scenario constraints; create modes, corners, 
#    and scenarios; source mode, corner, and scenario constraints, respectively 
#  - examples/TCL_MCMM_SETUP_FILE.auto_expanded.tcl: provide constraints for the scenarios; create modes, corners, 
#    and scenarios; source scenario constraints which are then expanded to associated modes and corners
rm_source -file $TCL_MCMM_SETUP_FILE

# Adjust commit_upf after mcmm setup preventing iso rename. Refer to mv.cells.rename_isolation_cell_with_formal_name for details.
if {[file exists [which $UPF_FILE]]} {
   commit_upf
}

file delete -force split

# Derive block instances from block references if not already defined.
set DP_BLOCK_INSTS ""
foreach ref "$DP_BLOCK_REFS" {
   set DP_BLOCK_INSTS "$DP_BLOCK_INSTS [get_object_name [get_cells -hier -filter ref_name==$ref]]"
}

set_budget_options -add_blocks $DP_BLOCK_INSTS

if {$DP_INTERMEDIATE_LEVEL_BLOCK_REFS != ""} {
   if {$INTERMEDIATE_BLOCK_VIEW == "abstract"} {
     puts "RM-info : splitting constraints with -hier_abstract_subblocks"
     split_constraints -force -hier_abstract_subblocks $DP_INTERMEDIATE_LEVEL_BLOCK_REFS -nosplit
   } else {
     puts "RM-info : splitting constraints using -design_subblocks"
     split_constraints -design_subblocks $DP_INTERMEDIATE_LEVEL_BLOCK_REFS -nosplit
   }
} else {
   puts "RM-info : splitting constraints"
   split_constraints -nosplit
}

if {[info exists DP_BB_BLOCK_REFS] && $DP_BB_BLOCK_REFS != ""} {
   set DP_BB_BLOCK_INSTS ""
   foreach ref $DP_BB_BLOCK_REFS {
     set DP_BB_BLOCK_INSTS "$DP_BB_BLOCK_INSTS [get_object_name [get_cells -hier -filter ref_name==$ref]]"
   }
   set cb [current_block]
   foreach bb $DP_BB_BLOCK_INSTS { create_blackbox $bb }
   foreach bb $DP_BB_BLOCK_REFS {
      # If BB UPF provided, load it
      if {[info exists DP_BB_BLOCKS(${bb},upf)] && [file exists $DP_BB_BLOCKS(${bb},upf)]} {
         current_block ${bb}.design
         load_upf $DP_BB_BLOCKS(${bb},upf)
         commit_upf
         save_upf -for_empty_blackbox ./split/$bb/top.upf
         current_block $DESIGN_NAME
      }
      # if BB timing exists put it in split directory as well
      if {[info exists DP_BB_BLOCKS(${bb},timing)] && [file exists $DP_BB_BLOCKS(${bb},timing)]} {
         exec cat $DP_BB_BLOCKS(${bb},timing) >> ./split/$bb/top.tcl
      }
   }
}

close_lib
file delete -force ${WORK_DIR}/${DESIGN_LIBRARY}${SUFFIX}

print_message_info -ids * -summary
echo [date] > split_constraints

exit 
