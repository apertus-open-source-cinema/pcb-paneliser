# Export from EAGLE to Gerber

This guide should cover the process to go from eagle _*.brd_ file to the catalog of Gerber input files for stage 1.

## Steps:
* Open _*.brd_ and _*.sch_ files in Eagle
* Choose assembly variant in dropdown menu then resave both _*.brd_ and _*.sch_ files
  * Select base (**empty** variant) for panels and **Tele** for stencil and BOM
* in Eagle go to **File -> CAM Processor**, then in the newly opened window **File -> Open -> Job**
* Choose the **oshpark-4layer.cam** file from this directory
* Click **Process Job** - the files will be written to the same directory where the _*.brd_ file resides
  * Confirm the warning about large data with **Yes to all**

# using the rotate script
copy the **rotate_90_ccw.sh** script into a subfolder containing gerber files like the **base_variant** folder.
Run **rotate_90_ccw.sh** with the name of the board and subfolder as argument.
It will rename the source to ..._original, but you should grab the data from the new folder and paste it over the original one, delete new folder and remove _original. Bit cumbersome currently but works for now.
