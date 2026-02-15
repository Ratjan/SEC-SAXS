# SEC-SAXS - local version
# This branch is configured to be downloaded and run locally

Utilities for manipulating SEC-SAXS data - aims to be more streamlined and flexible for basic analysis and processing of SEC-SAXS.
Functions:

Stitch:
  
- Has a basic stitching function which joins data from two detectors so that the entire q range can be evaluated at the same type

Main:

- Allows for average intensity vs frame (linked to elution time) plots at different q-values, and saving of these plots
- Solvent subtraction by specifying start and end frames of solvent and sample peak, and saving of these data

Plots:

- Separate plot module for comparison of saved data, e.g. from different runs

Intended first time run order is stitch -> main -> plots
Save folder and file paths are built relative to the path location of the .pynb files are placed.


