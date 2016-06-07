#!/usr/bin/python
"""
Maybe add

molecular_weight of moist air
water vapor mass density
water vapor partial pressure
water vapor partial pressure at saturation
relative humidity?
dew point temperature?
partial  pressure of dry air
dry air molar volume?
density of dry air
density of moist air
dry air heat capacity at constant pressure?
water vapor heat capacity at constant pressure?
specific humidity
refining ambient temperature?
moist air heat capacity at constant pressure?
specific evaporation heat?
water to dry air mixing ratio
"""

def preProcess(data, dataunits, notation_defs=None,
        rho_air_from="theta_v"):
    '''
    Pre-processes data by calculating moist and dry air densities, specific humidity
    mass density and other important variables

    Parameters:
    -----------
    data:
    dataunits:
    '''
    from .. import constants
    from .. import notation
    from .. import algs

    data = data.copy()
    dataunits = dataunits.copy()

    Rh2o = constants.R_spec['h2o']
    Mh2o = constants.molar_mass['h2o']

    #---------
    # Define useful notation to look for
    if notation_defs==None:
        defs=notation()
    else:
        defs=notation_defs
    #---------

    if defs.h2o_density not in data.columns:
        print("Didn't locate mass density of h2o. Will try to calculate it")

    if rho_air_from=='theta_v':
        pass
        #algs.airDensity_from_theta_v()
    else:
        pass
        #algs.airDensity_from_theta()

def eddyCov(data, wpl=True,
        notation_defs=None, solutes=[], from_fluctuations=True, from_scales=False):
    """
    Get fluxes according to characteristic lengths
    
    WARNING! If using wpl=True, be sure that all masses are consistent!
        For example, if q = [g/g], rho_h2o = [g/m3] and rho_co2 = [g/m3] and so on.
        Avoid mixing kg/m3 with g/m3 (e.g. for co2 and h2o) and mg/kg with g/g (e.g. for
        co2 and h2o).

    TODO: add support for pint units

    Parameters:
    -----------
    data: pandas.DataFrame
        dataframe with the characteristic lengths calculated
    notation_defs: pymicra.notation
        object that holds the notation used in the dataframe
    wpl: boolean
        whether or not to apply WPL correction on the latent heat flux and solutes flux
    solutes: list
        list that holds every solute considered for flux
    """
    from .. import constants
    from ..core import notation
    import pandas as pd

    if from_fluctuations:
        return eddyCov2(data, wpl=wpl, notation_defs=notation_defs, solutes=solutes)

    cp=constants.cp_dry
    lamb = constants.latent_heat_water

    #---------
    # Define useful notation to look for
    if notation_defs==None:
        defs=notation()
    else:
        defs=notation_defs
    star = defs.star
    #---------

    #---------
    # Define name of variables to look for based on the notation
    p           =   defs.pressure
    theta_mean  =   defs.mean % defs.thermodyn_temp
    theta_v     =   defs.virtual_temp
    theta_star  =   star % defs.thermodyn_temp
    theta_v_star=   star % defs.virtual_temp
    u_star      =   star % defs.u
    q_star      =   star % defs.specific_humidity
    #---------

    #---------
    # Define auxiliar variables
    rho_mean=data['rho_air_mean']
    rho_h2o_mean=data['rho_h2o_mean']
    rho_co2_mean=data['rho_co2_mean']
    rho_dry_mean=data['rho_dry_mean']
    c_stars = []
    for solute in solutes:
        c_stars.append( star % solute )
    #---------

    #---------
    # Calculate the fluxes
    out=pd.DataFrame(index=data.index)
    out[ defs.momentum_flux ]               = rho_mean* ( data[u_star]**2.)
    out[ defs.sensible_heat_flux ]          = rho_mean* cp* data[u_star] * data[theta_star]
    out[ defs.virtual_sensible_heat_flux ]  = rho_mean* cp* data[u_star] * data[theta_v_star]
    out[ defs.water_vapor_flux]             = rho_mean* data[u_star] * data[q_star]
    out[ defs.latent_heat_flux ]            = lamb( data[theta_mean] ) * rho_mean * data[u_star] * data[q_star]
    for solute, c_star in zip(solutes, c_stars):
        out[ 'F_{}'.format(solute) ] =  rho_mean* data[u_star]* data[c_star]
    #---------

    #------------------------
    # APPLY WPL CORRECTION. PAGES 34-35 OF MICRABORDA
    if wpl:
        mu=constants.R_spec['h2o']/constants.R_spec['dry']
        rv=rho_h2o_mean/rho_dry_mean
        rc=rho_co2_mean/rho_dry_mean
        out['E'] = (1. +mu*rv)*( out['E'] + rho_h2o_mean * (data[theta_star]*data[u_star]/data[theta_mean]) )
        for solute, c_star in zip(solutes, c_stars):
            out[ 'F_{}'.format(solute) ] = \
                out[ 'F_{}'.format(solute) ] + \
                rho_co2_mean*(1. + mu*rv)*(data[theta_star]*data[u_star])/data[theta_mean] + \
                mu*rc*out['E']
    #------------------------
    return out



def eddyCov2(data, wpl=True,
        notation_defs=None, solutes=[]):
    """
    Get fluxes from the turbulent fluctuations
    
    WARNING! If using wpl=True, be sure that all masses are consistent!
        For example, if q = [g/g], rho_h2o = [g/m3] and rho_co2 = [g/m3] and so on.
        Avoid mixing kg/m3 with g/m3 (e.g. for co2 and h2o) and mg/kg with g/g (e.g. for
        co2 and h2o).

    TODO: add support for pint units

    Parameters:
    -----------
    data: pandas.DataFrame
        dataframe with the characteristic lengths calculated
    notation_defs: pymicra.notation
        object that holds the notation used in the dataframe
    wpl: boolean
        whether or not to apply WPL correction on the latent heat flux and solutes flux
    solutes: list
        list that holds every solute considered for flux
    """
    from .. import constants
    from ..core import notation
    import pandas as pd

    cp = constants.cp_dry
    lamb = constants.latent_heat_water

    #---------
    # Define useful notation to look for
    if notation_defs==None:
        defs=notation()
    else:
        defs=notation_defs
    fluct = defs.fluctuation
    mean = defs.mean
    #---------

    #---------
    # Define name of variables to look for based on the notation
    u               =   fluct % defs.u
    w               =   fluct % defs.w
    q_fluc          =   fluct % defs.specific_humidity
    theta_fluc      =   fluct % defs.thermodyn_temp
    theta_v_fluc    =   fluct % defs.virtual_temp
    solutesf        = [ fluct % solute for solute in solutes ]
    #---------

    #---------
    # Now we try to calculate or identify the fluctuations of theta
    data_theta_mean = data[ defs.thermodyn_temp ].mean()
    try:
        data_theta_fluc  =   data[ fluct % defs.thermodyn_temp ]
    except:
        #---------
        # We need the mean of the specific humidity and temperature
        data_q_mean  =   data[ defs.specific_humidity ].mean()
        #---------

        data_theta_fluc  =   ( data[theta_v_fluc] - 0.61*data_theta_mean*data[q_fluc])/(1.+0.61*data_q_mean)
        data[ theta_fluc ] = data_theta_fluc
    #---------

    #---------
    # First we construct the covariance matrix
    cov = data[[u,w,theta_v_fluc, theta_fluc, q_fluc] + solutesf ].cov()
    #---------

    #---------
    # Define auxiliar variables
    mu=constants.R_spec['h2o']/constants.R_spec['dry']
    rho_air_mean    =   data[ defs.density % defs.moist_air ].mean()
    rho_h2o_mean    =   data[ defs.density % defs.h2o ].mean()
    rho_co2_mean    =   data[ defs.density % defs.co2 ].mean()
    rho_dry_mean    =   data[ defs.density % defs.dry_air ].mean()
    #---------

    #---------
    # Calculate the fluxes
    out=pd.DataFrame(index=[data.index[0]])
    out[ defs.momentum_flux ]               = -rho_air_mean * cov[u][w]
    out[ defs.sensible_heat_flux ]          = rho_air_mean * cp * cov[theta_fluc][w]
    out[ defs.virtual_sensible_heat_flux ]  = rho_air_mean * cp * cov[theta_v_fluc][w]
    out[ defs.water_vapor_flux ]            = rho_air_mean * cov[q_fluc][w]
    out[ defs.latent_heat_flux ]            = lamb( data_theta_mean ) * rho_air_mean * cov[q_fluc][w]
        #---------
        # Calculate flux for each solute
    for solute, solutef in zip(solutes, solutesf):
        out[ defs.flux_of % solute ] =  rho_air_mean * cov[solutef][w]
        #---------
    #---------

    #------------------------
    # APPLY WPL CORRECTION. PAGES 34-35 OF MICRABORDA
    if wpl:
        rv=rho_h2o_mean/rho_dry_mean
        rc=rho_co2_mean/rho_dry_mean
        out[ defs.water_vapor_flux ] = (1. +mu*rv)*( out[ defs.water_vapor_flux ] + rho_h2o_mean * (cov[theta_fluc][w]/data_theta_mean) )
        for solute in solutes:
            out[ defs.flux_of % solute ] = \
                out[ defs.flux_of % solute ] + \
                rho_co2_mean*(1. + mu*rv)*(cov[theta_fluc][w])/data_theta_mean + \
                mu*rc*out[ defs.water_vapor_flux ]
    #------------------------
    return out



