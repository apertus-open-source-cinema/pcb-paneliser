This guide should cover the process to go from eagle *.brd file to the catalog of gerber input files for stage 1.

# Steps:
* Open *.brd file in Eagle
* Choose assembly variant in dropdown menu
* Download the 4 layer CAM job from oshpark corresponding to your eagle version: https://docs.oshpark.com/design-tools/eagle/generating-gerbers/
* in Eagle go to File -> CAM Processorthen in the newly opened window File ->  Open -> Job
* Choose the oshpark-4layer.cam file you just downloaded
* Click "Process Job" - the files will be written to the same directory where the *.brd file resides
