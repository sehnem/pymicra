#!/usr/bin/python
"""
Defines some useful constants
"""
from . import algs
units={}    # creates units dictionary so it can be updated everytime a constant is added

#---------------------------------------
# Gas constants
#---------------------------------------
molar_mass={'dry' : 28.9645,
            'o3'  : 47.99820,
            'h2o' : 18.0153,
            'co2' : 44.0095,
            'co'  : 28.0101,
            'ch4' : 16.0425,
            'n2o' : 44.01280,
            'o' : 15.99940,
            'n' : 14.00670}
units.update({'molar_mass' : 'g/mol'})
   
R=8.3144621    # universal gas constant J/(mol.K)
units.update({'R' : 'J/(mol * K)'})

R_spec={}
for key, val in molar_mass.items():
    R_spec.update( {key : R/val} )
del key, val
units.update({'R_spec' : 'J/(g * K)'})

units.update({'mu':'dimensionless'})

cp_dry=1.0035  # specific heat of dry air at constant pressure
units.update({'cp_dry' : 'J/(g * K)'})

cp_h2o=4.1813  # specific heat of water vapor at constant pressure
units.update({'cp_water' : 'J/(g * K)'})

from .physics import latent_heat_water
units.update({'latent_heat_water' : 'J/g'})

from .physics import satWaterPressure
units['satWaterPressure'] = 'kPa'


#---------------------------------------
# physical constants
#---------------------------------------
gravity=9.80665      # gravity
units.update({'gravity':'m/(s**2)'})

omega = 7.29212E-5  # angular velocity of the earth
units.update({'omega' : '1/s'})

earth_radius=6378140.0 # meters
units.update({'earth_radius' :'m'})

standard_pressure = 101325.00 # pascals
units.update({'standard_pressure':'Pa'})

standard_temperature = 288.15 # kelvin
units.update({'standard_temperature':'K'})

temperature_lapse_rate = -0.0065 # change in temperature with height, kelvin/metre
units.update({'temperature_lapse_rate' : 'K/m'})

earth_atmosphere_molar_mass =28.9644 # g/mol
units.update({'earth_atmosphere_molar_mass' : 'g/mol' })


#---------------------------------------
# OTHER CONSTANTS
#---------------------------------------
mole = 6.022140857e23

kappa=0.4

greek_alphabet = {
    '\u0391': 'Alpha',
    '\u0392': 'Beta',
    '\u0393': 'Gamma',
    '\u0394': 'Delta',
    '\u0395': 'Epsilon',
    '\u0396': 'Zeta',
    '\u0397': 'Eta',
    '\u0398': 'Theta',
    '\u0399': 'Iota',
    '\u039A': 'Kappa',
    '\u039B': 'Lamda',
    '\u039C': 'Mu',
    '\u039D': 'Nu',
    '\u039E': 'Xi',
    '\u039F': 'Omicron',
    '\u03A0': 'Pi',
    '\u03A1': 'Rho',
    '\u03A3': 'Sigma',
    '\u03A4': 'Tau',
    '\u03A5': 'Upsilon',
    '\u03A6': 'Phi',
    '\u03A7': 'Chi',
    '\u03A8': 'Psi',
    '\u03A9': 'Omega',
    '\u03B1': 'alpha',
    '\u03B2': 'beta',
    '\u03B3': 'gamma',
    '\u03B4': 'delta',
    '\u03B5': 'epsilon',
    '\u03B6': 'zeta',
    '\u03B7': 'eta',
    '\u03B8': 'theta',
    '\u03B9': 'iota',
    '\u03BA': 'kappa',
    '\u03BB': 'lamda',
    '\u03BC': 'mu',
    '\u03BD': 'nu',
    '\u03BE': 'xi',
    '\u03BF': 'omicron',
    '\u03C0': 'pi',
    '\u03C1': 'rho',
    '\u03C3': 'sigma',
    '\u03C4': 'tau',
    '\u03C5': 'upsilon',
    '\u03C6': 'phi',
    '\u03C7': 'chi',
    '\u03C8': 'psi',
    '\u03C9': 'omega',
}

from datetime import datetime
sumsolstice={
2010:'21 11:28',
2011:'21 17:16',
2012:'20 23:09',
2013:'21 05:04',
2014:'21 10:51',
2015:'21 16:38',
2016:'20 22:34',
2017:'21 04:24'
}
sumsolstice={ key : datetime.strptime('{0}-06-{1}'.format(key, val), '%Y-%m-%d %H:%M') for key, val in sumsolstice.items() }

 
#--------------------------------------
# CLEAN DUMMY VARIABLES
#--------------------------------------
try:
    del val, key
except:
    pass

#---------------
# Parse units to pint!
units = algs.parseUnits(units)
#---------------
