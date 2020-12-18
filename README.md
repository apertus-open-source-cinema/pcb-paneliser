# pcb-paneliser
Creating panels from individual PCBs in an as automated way as possible.

## Setup
These scripts were built for python3.

  * Execute ```pip3 install -r requirements.txt``` to install required modules
  * Run ```python3 stage1_generate_mixed_beta_panel.py``` to generate mixed PCB panel
  * Run ```python3 stage2_generate_multi_mixed_beta_panel.py``` to generate a big panel consisting of multiple mixed PCB panels
  * Run ```python3 stage3_generate_stage1_stencils.py``` to generate stencils for mixed PCB panel

## Extracting impedance relevant layers

  * Update the filenames to extract in ```extract_impedance_stage1.py``` and then execute ```python3 extract_impedance_stage1.py``` - this extracts all traces with a specific netclass from the *.brd files and creates a new output file called <boardname>_impedance.brd inside output_impedance_filtered/
  * Extract gerber layers throught Eagles oshpark-4layer.cam into output_impedance_filtered/gerber_export and use rotate_90_ccw.sh on them if required.
  * Update output_impedance_filtered/stage1_generate_mixed_beta_impedance_panel.py again withe the correct board names and run ```python3 stage1_generate_mixed_beta_impedance_panel.py```

