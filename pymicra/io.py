#!/usr/bin/python
"""
Author: Tomas Chor
Date: 2015-08-07
-------------------------

Modifications:

"""
import pandas as pd
import algs

#-------------------------------------------
#-------------------------------------------
# INPUT OF DATA
#-------------------------------------------
#-------------------------------------------
def readDataFile(fname, varNames=None, dates_as_string=True, **kwargs):
    """
    Author: Tomas Chor

    Parameters
    ----------
    kwargs: dict
        dictionary with kwargs of pandas' read_csv function
        see http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html for more detail

    varNames: list
        list containing the names of each variable in the file.
        
    Returns
    ---------
    dataFrame: pandas.DataFrame object
    """
    if dates_as_string:
        dtypes={ i : str for i,key in enumerate(varNames) if r'%' in key }
    try:
        data=pd.read_csv(fname, dtype=dtypes, **kwargs)
    except ValueError:
        print 'WARNING: Ignoring dtypes for date columns. This may cause problems parsing dates'
        data=pd.read_csv(fname, **kwargs)
    if varNames:
        data.columns=varNames + list(data.columns[len(varNames):])
    return data


def readDataFiles(flist, verbose=0, **kwargs):
    """
    Author: Tomas Chor
    ** needs to be tested! **

    -------------------------------------

    * kwargs are readDataFile kwargs

    * returns one pandas.DataFrame
    """
    if len(flist)==0:
        raise ValueError('Passed a list of files of zero length to be read.')
    dflist=[]
    for f in flist:
        if verbose==1:
            print 'Reading',f
        subdata=readDataFile(f, **kwargs)
        dflist.append(subdata)
    if verbose==1:
        print 'Concatenating DataFrames...'
    data=pd.concat(dflist, ignore_index=True)
    if verbose==1:
        print 'Done!'
    return data

#------------------------------------
#
#------------------------------------
class dataloggerConf(object):
    """
    This class defines a specific configuration of a datalogger output file
    --------------------------

    Parameters:
    ----------

    varNames: list of strings
        should be a list of strings with the names of the variables. If the variable
        is part if the date, then it should be provided as a datetime directive,
        so if the columns is only the year, its name must be `%Y` and so forth. While
        if it is the date in YYYY/MM/DD format, it should be `%Y/%m/%d`. For more info
        see https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior

    date_cols: list of strings
        should be the subset of varNames that corresponds to the variables that compose
        the timestamp. If it is not provided the program will try to guess by getting
        all variable names that have a percentage sign (%).

    date_connector: string
        generally not really necessary. It is used to join and then parse the date_cols.

    columns_separator: string
        used to assemble the date. Should only be used if the default char creates conflict.

    header_lines: int
        up to which line of the file is a header. See pandas.read_csv header option.

    first_time_skip: int
        how many units of frequency the first line of the file is offset (generally zero)

    filename_format: string
        tells the format of the file with the standard notation for date and time and with variable
        parts as "?". E.g. if the files are 56_20150101.csv, 57_20150102.csv etc filename_format should be:
            ??_%Y%m%d.csv
        this is useful primarily for the quality control feature

    units: dictionary
        very important: a dictionary whose key are the columns of the file and whose items are
        the units in which they appear.

    description: string
        brief description of the datalogger configuration file
    """
    def __init__(self, varNames,
             date_cols=None,
             frequency=None,
             date_connector='-', 
             columns_separator=',',
             header_lines=None,
             first_time_skip=False,
             units=None,
             filename_format='CSV_?????.fluxo_??m_%Y_%j_%H%M.dat',
             description='generic datalogger configuration file'):
        #-------------------------
        # Makes sure that units is a dictionary type
        #-------------------------
        if units is not None:
            if not isinstance(units, dict):
                raise TypeError('units should be a dictionary. Ex.: {"u" : "m/s", "v" : "m/s", "theta" : "K" }')
        self.varNames=varNames
        if date_cols:
            self.date_cols=date_cols
        else:    #tries to guess the date columns by assuming that no other columns has a % sign on their name
            self.date_cols=[ el for el in varNames if '%' in el ]
        self.frequency=frequency
        self.date_connector=date_connector
        self.columns_separator=columns_separator
        self.header_lines=header_lines
        self.first_time_skip=first_time_skip
        self.units=units
        self.description=description
        self.filename_format=filename_format


def timeSeries(flist, datalogger, index_by_date=True, correct_fracs=None, complete_zeroes=False, verbose=0):
    """
    Creates a micrometeorological time series from a file or list of files.

    Parameters:
    -----------

    flist: list or string
        either list or names of files (dataFrame will be one concatenated dataframe) or the name of one file
    datalogger: pymicra.dataloggerConf object
        configuration of the datalogger which is from where all the configurations of the file will be taken
    index_by_date: bool
        whether or not to index the data by date. Note that if this is False many of the functionalities
        of pymicra will be lost.
    correct_fracs: bool
        set to True if the data is sampled at a frequency higher than the frequency of the timestamp 
        (i.d. there are repeated timestamps)
    complete_zeroes: list
        list of columns which are part of dates and need to be padded with zeroes to be correctly read
    verbose: int, bool
        verbose level
    """
    
    if isinstance(flist, str):
        flist=[flist]
    header_lines=datalogger.header_lines
    columns_separator=datalogger.columns_separator
    date_cols=datalogger.date_cols
    date_connector=datalogger.date_connector
    if columns_separator=='whitespace':
        series=readDataFiles(flist, header=header_lines, delim_whitespace=True, varNames=datalogger.varNames, verbose=verbose)
    else:
        series=readDataFiles(flist, header=header_lines, sep=columns_separator, varNames=datalogger.varNames, verbose=verbose)
    if verbose==1:
        print 'Starting to parse the dates'
    if index_by_date:
        series=algs.parseDates(series, date_cols, connector=date_connector, first_time_skip=datalogger.first_time_skip, 
                          clean=True, correct_fracs=correct_fracs, complete_zeroes=complete_zeroes)
    return series


def read_dlc(dlcfile):
    """
    Reads datalogger configuration file

    WARNING! When defining the .dlc note that by default columns that are enclosed between doublequotes
    will appear without the doublequotes. So if your file is of the form :

    "2013-04-05 00:00:00", .345, .344, ...

    Then the .dlc should have: varNames=['%Y-%m-%d %H:%M:%S','u','v']. This is the default csv format of
    CampbellSci dataloggers. To disable this feature, you should parse the file with read_csv using the kw: quoting=3.
    """
    globs={}
    dlcvars={}
    try:
        execfile(dlcfile, globs, dlcvars)
    except NameError:
        print '''This version of python does not have an execfile function. This workaround should work but is yet to be fully tested'''
        with open(dlcfile) as f:
            code=compile(f.read(), dlcfile, 'exec')
            exec(code, globs, dlcvars)
    return dataloggerConf(**dlcvars)


def readUnitsCsv(filename, names=0, units=1, **kwargs):
    """
    Reads a csv file in which the first line is the name of the variables
    and the second line contains the units

    Parameters:
    -----------
    filename: string
        path of the csv file to read
    names: int
        line number (starting from zero) that has the variables' names
    units: int
        line number (starting from zero) that has the variables' units

    Returns:
    --------
    df: pandas.DataFrame
        dataframe with the data
    unitsdic: dictionary
        dictionary with the variable names as keys and the units as values
    """
    df=pd.read_csv(filename, header=[names, units], **kwargs)
    #df=pd.read_csv(filename, header=[names, units], index_col=0, parse_dates=[0])
    cols,units=zip(*df.columns)
    unitsdic={ k:v for k,v in zip(cols,units) }
    df.columns=cols
    return df, unitsdic


#-------------------------------------------
#-------------------------------------------
# OUTPUT OF DATA
#-------------------------------------------
#-------------------------------------------

def toUnitsCsv(data, units, filename, to_tex=False, **kwargs):
    """
    Writes s csv with the units of the variables as a second line

    Parameters:
    ----------

    data: pandas.DataFrame
        dataframe of data
    units: dict
        dictionary containing { nameOfVar : unit }
    filename: string
        path of output file
    to_tex: bool
        whether or not to convert the string of the unit to TeX format (useful for printing)
    """
    if to_tex:
        from util import printUnit as pru
        units={ k : pru(v) for k,v in units.iteritems() }
    cols=data.columns
    unts=[ units[c] for c in cols ]
    columns=pd.MultiIndex.from_tuples(zip(cols, unts))
    df=data.copy()
    df.columns=columns
    df.to_csv(filename, **kwargs)
    return

def get_printable(data, units, to_tex_cols=True, to_tex_units=True):
    """
    Returns a csv that is pandas-printable. It does so changing the column names to add units to it.

    """
    if to_tex_cols==True:
        from constants import greek_alphabet
        columns=[ u'\\'+c if c in greek_alphabet.values() else c for c in data.columns ]
        units={ u'\\'+ c if c in greek_alphabet.values() else c : v for c,v in units.iteritems() }
    if to_tex_units==True:
        from util import printUnit as pru
        units={ k : pru(v) for k,v in units.iteritems() }
    columns=[ r'$\rm '+fl+r'\, \left({0}\right)$'.format(units[fl]) for fl in columns ]
    df=data.copy()
    df.columns=columns
    return df


