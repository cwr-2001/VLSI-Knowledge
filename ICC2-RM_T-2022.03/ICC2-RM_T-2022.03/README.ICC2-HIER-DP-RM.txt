##########################################################################################
# Synopsys(R) IC Compiler II(TM) Hierarchical Design Planning Reference Methodology
# Version: T-2022.03
# Copyright (C) 2014-2022 Synopsys, Inc. All rights reserved.
##########################################################################################

Overview
========
A reference methodology provides a set of reference scripts that serve as a good
starting point for running a tool. These scripts are not designed to run in their
current form. You should use them as a reference and adapt them for use in your
design environment.

This RM script package contains scripts to perform the Traditional Hierarchical
Design Planning flow.  This flow takes in gates as a primary input.  It is referenced
below as the IC Compiler II Hierarchical Design Planning RM, but can also be run via
Fusion Compiler.  A separate Makefile is provided (i.e. Makefile_dp_hier_fc_traditional).

Instructions for Using the IC Compiler II Hierarchical Design Planning RM
=========================================================================
The IC Compiler II Hierarchical Design Planning Reference Methodology
consists of two major sections:

(1) Split constraints: To execute this RM step, use the following command

	IC Compiler II:
	% make -f rm_setup/Makefile_dp_hier split_constraints
	
	Fusion Compiler
	% make -f rm_setup/Makefile_dp_hier_fc_traditional split_constraints

	This RM step reads the full chip Verilog netlist, full
	chip timing constraints, full chip UPF (if specified) and
	creates the block and top constraints in the ./split directory.

(2) Design Planning: To execute the design planning flow, use the
    following command:

	IC Compiler II:
	% make -f rm_setup/Makefile_dp_hier all

	Fusion Compiler
	% make -f rm_setup/Makefile_dp_hier_fc_traditional all

	Replace "all" with any other desired step in the
	Makefile_dp_hier, such as shaping, placement, etc.

        Note: The variable CTP can be set to true/false to run/skip this flow step.

Flow Steps
==========
The IC Compiler II Hierarchical Design Planning Reference Methodology
flow includes the following steps:
(Refer to the makefile : rm_setup/Makefile_dp_hier)

* split_constraints
	- Top Chip-level SDC and UPF files are partitioned into
          top-level and block-level files.

* init_dp
	- Data preparation. Read design inputs and create the design.
	- Place I/O drivers in the design (chip level).
	- Place top-level ports of design (hier block).

* commit_blocks
	- Blocks are committed to physical hierarchy.

* expand_outline
	- Expands outline view
	- Creates placement abstracts for each block. 
	- Load top and block constraints.

* shaping
	- Shapes and places physical blocks (including power domains
          and voltage areas).

* placement
	- Performs global macro and standard cell placement.

* create_power
	- Inserts the power and ground structures for the design and
          pushes these structures into the blocks.

* clock_trunk_planning (optional)
	- Performs block and top-level clock trunk synthesis.

* place_pins
	- Performs global routing of the interface nets and block pin
          assignment.

* timing_budget
	- Performs estimated timing on the blocks and create 
	  optimized abstracts used for top level optimization.
	- Performs virtual optimization of the block and top paths.
	- Creates timing budgets for blocks.

* write_data_dp
	- Writes hierarchical design data including netlist,
          power/ground netlist, Synopsys Design Constraints (SDC), and UPF.

* all
	- Performs all of the above steps.

Notes: 1) SDC loading is delayed until needed in the high capacity mode (i.e. DP_HIGH_CAPACITY_MODE==true).
          a) You will get POW-034 warning messages until the SDC is loaded: No valid clocks are available in design......(POW-034)
          b) SDC will get loaded in placement.tcl and place_pins.tcl when timing driven capabilities are enabled.
	    i) placement.tcl ==> TIMING_DRIVEN_PLACEMENT != ""
	   ii) place_pins.tcl ==> TIMING_PIN_PLACEMENT != ""
	  c) SDC is loaded in timing_budget.tcl.
       2) SDC is loaded in expand_outline.tcl for non-high capacity mode (i.e. DP_HIGH_CAPACITY_MODE==false).

Files Included With the IC Compiler II Hierarchical Design Planning RM
======================================================================
* rm_setup/Makefile_dp_hier
* rm_setup/Makefile_dp_hier_fc_traditional
* rm_setup/fc_dp_setup.tcl
* rm_setup/design_setup.tcl
* rm_icc2_dp_hier_scripts/split_constraints.tcl
* rm_icc2_dp_hier_scripts/init_dp.tcl
* rm_icc2_dp_hier_scripts/commit_blocks.tcl
* rm_icc2_dp_hier_scripts/expand_outline.tcl
* rm_icc2_dp_hier_scripts/shaping.tcl
* rm_icc2_dp_hier_scripts/placement.tcl
* rm_icc2_dp_hier_scripts/create_power.tcl
* rm_icc2_dp_hier_scripts/clock_trunk_planning.tcl
* rm_icc2_dp_hier_scripts/place_pins.tcl
* rm_icc2_dp_hier_scripts/timing_budget.tcl
* rm_icc2_pnr_scripts/write_data.tcl
