# SEC-SAXS
# This branch is configured to be run on the coSAXS jupyterhub

Utilities for manipulating SEC-SAXS data - aims to be more streamlined and flexible for basic analysis and processing of SEC-SAXS.
Functions:
- Has a basic stitching function which joins data from two detectors so that the entire q range can be evaluated at the same type
- Allows for average intensity vs frame (linked to elution time) plots at different q-values, and saving of these plots
- Solvent subtraction by specifying start and end frames of solvent and sample peak, and saving of these data
- Separate plot module for comparison of saved data

Intended first time run order is stitch -> main -> plots

All files should be executable on default MAX IV / CoSAXS jupyterhub settings


