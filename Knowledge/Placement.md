# Floorplan

## Analysis Global Route Congestion in Floorplan
`route_global -floorplan true -congestion_map_only true`

## Apply "Padding" Around Macro Edges
`create_keepout_margin -type hard -outer {left bottom right top} Design/Cells`  
Keepout margin: bound to macro/cell, moves with the macro  
Placement blockage: floorplan area constraint, does not move with objects

# Placement

## Advanced Legalier
`set_technology -node 7`  
`place.legalize.enable_advanced_legalizer`  
`place.legalize.enable_advanced_prerouted_net_check`  

## Analysis Global Route Congestion in Placement
1. Use low-effort methods to quickly determine if there is any obvious congestion.  
`route_global -congestion_map_only true -effort_level low`  
2. If congestion is borderline, conduct a re-analysis with a higher level of effort to avoid erroneous optimization of placement due to the pessimistic estimation made with a lower level of effort.
`route_global -congestion_map_only true -effort_level medial | high |ultra`  

## Route Congestion Model Enhancements
1. Support for soft congestion map information to help designs that heavily use layer promotions and soft NDRs to meet QoR goals. 
2. Bidirectional cell expansion for reducing lower-layer congestion by considering the directionality (H/V) of the routing resource shortage. (Vertical expansion is general mostly expensive)

## Congestion-Driven Restructuring (CDR) 
1. Designs with complex AOI/OAI logic structures can cause many net crossings, thereby creating substantial core congestion hotspots. CDR identifies tangled nets that drive input pins of commutative and associative logic trees ((N)AND/OR/XOR trees), reorders and places them more optimally.    
`place.coarse.cong_restruct`

## Create Cell Spacing Rules
```
set_placement_spacing_label -name {X} -side both -lib_cells [get_lib_cells "*/SDFF* */AOI*"]  
set_placement_spacing_label -name {Y} -side both -lib_cells [get_lib_cells */*]
set_placement_spacing_rule -labels {X X} {0 3}   
set_placement_spacing_rule -labels {X Y} {0 1}
```

## Relative Placement
```
### rp_constraints.tcl
create_rp_group rp1 -design MY_DP -columns 4 -rows 4  

add_to_rp_group MY_DP::rp1 -leaf U0 -col 0 -row 0
add_to_rp_group MY_DP::rp1 -leaf U1 -col 1 -row 0
add_to_rp_group MY_DP::rp1 -leaf U2 -col 2 -row 0
add_to_rp_group MY_DP::rp1 -leaf U3 -col 3 -row 0
add_to_rp_group MY_DP::rp1 -leaf U4 -col 0 -row 1
... 
```
```
source rp_constraints.tcl
place_opt
```

## Cell Naming Convention
1. Cell Function_Drive Strength_Threshold Voltage (NAND2_X2_LVT)   

| Name  | Meaning |
| ----- | ------- |
| INV   | inverter |
| BUF   | buffer |
| NAND2 | 2-input NAND |
| NAND3 | 3-input NAND |
| NOR2  | 2-input NOR |
| AND2  | AND |
| OR2   | OR |
| XOR2  | XOR |
| XNOR2 | XNOR |
| AOI21 | AND-OR-INVERT |
| OAI21 | OR-AND-INVERT |
| MUX2  | 2:1 mux |
| DFF   | flip flop |
| SDFF  | scan DFF |

![Cell Naming Convention](Figure/Cell%20Naming%20Convention.png)
