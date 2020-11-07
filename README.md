# pcb-paneliser
Creating panels from individual PCBs in an as automated way as possible.

## Setup
These scripts were built for python3.

  * Execute ```pip3 install -r requirements.txt``` to install required modules
  * Run ```python3 stage1_generate_mixed_beta_panel.py``` to generate mixed PCB panel
  * Run ```python3 stage2_generate_multi_mixed_beta_panel.py``` to generate a big panel consisting of multiple mixed PCB panels
  * Run ```python3 stage3_generate_stage1_stencils.py``` to generate stencils for mixed PCB panel
