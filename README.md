# PyMicrA - Python Micrometeorological Analysis tool

This package was designed at Lemma, at the Federal University of Parana (UFPR), to make it easier to work with micrometeorological data. Pymicra is currently fully writen in python and it's aimed towards agregating all of the functionality commonly needed to process, read, and extract fluxes and etc from micrometeorological data. This leaves Pandas in charge of the optimization. In a near future we will also focus on our own kinds of optimization.


*This package is still under construction. More will come soon.*

## Required Packages
* Pandas
* Numpy

## License
This package is licensed under GNU General Public License V3.0 (http://choosealicense.com/licenses/gpl-3.0/)

## Main Features
Currently, this is what pymicra does:

  - Reading and understanding micrometeorological data in virtually any column-separated ASCII format (thanks to pandas).
  - Quality control methods (max and min values check, spikes, reverse-arrangement test and etc).
  - Rotation of coordinates (2D).
  - Detrending of data in the most common ways (block averages, moving averages and polynominal detrending).
  - Calculation of spectra and cross-spectra.
  - Calculation fluxes and characteristic scales.
  - Plus all native features of Pandas (interpolation, resampling, grouping, statistical tests, slicing, handling of missing data and etc.)

## Notation to be implemented soon
The next lines describe some general quantities, followed by the name that should be used inside straight brackets, followed by the units that compose it. The names provided are the default names and will be subjected to change by the user.
 - concentration [conc] - (mass of substance)/(mass of air)
 - density [rho] - (mass of substance)/(volume of air)
 - molar density [mrho] - (molar mass of substance)/(volume of air)
 - mixing ratio [r] - (mass of substance)/(mass of dry air)

We take humidity as the only exception to the rule above, following instead for the concentration of h2o:
 - specific humidty [q] - (mass of h2o)/(mass of air)

We also assume that the reynolds decomposition of any variable "a" takes the form
    
    a = a_mean + a_fluctuation

where the suffixes "\_mean" and "\_fluctuation", as well as other suffixes, are writen within the variables' names as
 - mean [\_mean] - indicates that the mean was taken on the variable whose name precedes this
 - fluctuation ['] - indicates that this is the fluctuation of the variable: a' = a - a\_mean
 - star/asterisc [\_star] - indicates a turbulence scale of the variable: a\_star = mean(u'\*a')

The standard notation for commo variables is 
 - thermodynamic temperature: [theta] 
 - virtual temperature: [theta\_v]
 - pressure: [p]

Some examples of names of variables following the standard notation are (description - [variable name in pymicra]):
 - u fluctuations: [u']
 - turbulence scale for virtual temperature: [theta\_v\_star]
 - fluctuations of water density on air: [rho\_h2o']
 - mean mixing ratio for carbon dioxide: [r\_co2\_mean]
