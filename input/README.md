# Export from EAGLE to Gerber

This guide should cover the process to go from eagle _*.brd_ file to the catalog of Gerber input files for stage 1.

## Steps:
* Open _*.brd_ and _*.sch_ files in Eagle
* Choose assembly variant in dropdown menu then resave both _*.brd_ and _*.sch_ files
* in Eagle go to **File -> CAM Processor**, then in the newly opened window **File -> Open -> Job**
* Choose the **oshpark-4layer.cam** file from this directory
* Click **Process Job** - the files will be written to the same directory where the _*.brd_ file resides
