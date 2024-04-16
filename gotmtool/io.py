#--------------------------------
# Functions for input/output
#--------------------------------

import os
import re
import sys
import numpy as np
from ruamel.yaml import YAML
from shutil import copy2

def config_load(config):
    """Load configuration

    :config:  (str or dict-like) configurations
    :returns: (dict) configurations in a dictionary

    """
    if isinstance(config, str):
        if os.path.exists(config):
            out = yaml_load(config)
        else:
            print_error('Configuration file {:s} not found'.format(config))
    else:
        out = config
    return out

def config_dump(config, filename):
    """Dump configuration to file

    :config:    (str or dict-like) configurations
    :filename:  (str) path of the output file

    """
    if isinstance(config, str):
        if os.path.exists(config):
            copy2(config, filename)
        else:
            print_error('Configuration file {:s} not found'.format(config))
    else:
        yaml_dump(config, filename)

def yaml_load(filename):
    """Read yaml configuration file

    :filename: (str) path of the input file
    :returns:  (dict) configurations in a dictionary

    """
    with open(filename, 'r') as f:
        fstring = f.read()
        fstring = re.sub("\*", "\'*\'", fstring)
    yaml = YAML()
    out = yaml.load(fstring)
    return out

def yaml_dump(data, filename):
    """Write yaml configuration file

    :data:      (dict-like) output data
    :filename:  (str) path of the output file

    """
    yaml = YAML()
    with open(filename, 'w') as stream_out:
        yaml.dump(data, stream_out, transform=_remove_quotes)

def _remove_quotes(s):
    return s.replace('\'', '')

def dat_dump_ts(time, data, filename, skip_value=None, scale_factor=1.):
    """Write time series in GOTM input format

    :time:         (array-like) array of time in datetime
    :data:         (list of array-like) array of variables
    :filename:     (str) filename of output file
    :skip_value:   (float, optional) value in data to skip
    :scale_factor: (float, optional) scale factor to be applied to data

    """
    nt = len(time)
    if not all(var.shape == (nt,) for var in data):
        dim_str = '['+' '.join([str(var.shape) for var in data])+']'
        raise ValueError('Dimension of data {} does not match time ({:d},)'.format(dim_str, nt))
    with open(filename, 'w') as fout:
        for i in np.arange(nt):
            if (skip_value is None) or ((not any(np.isnan(var[i]) for var in data))  and (not any(var[i] == skip_value for var in data))):
                out_str = time[i].strftime('%Y-%m-%d %H:%M:%S')
                for var in data:
                    out_str += '  {:10.6g}'.format(var[i]*scale_factor)
                out_str += '\n'
                fout.write(out_str)

def dat_dump_pfl(time, z, data, filename, skip_value=None, scale_factor=1., order=2):
    """Write time series of profile in GOTM input format.

    :time:         (array-like) array of time in datetime
    :z:            (array-like) array of depth
    :data:         (list of array-like) array of variables
    :filename:     (str) filename of output file
    :skip_value:   (float, optional) value in data to skip
    :scale_factor: (float, optional) scale factor to be applied to data
    :order:        (int) data written from bottom to top (z<0 increasing) if 1,
                       from top to bottom (z<0 decreasing) if 2

    """
    nt = len(time)
    nd = len(z)
    if not all(var.shape == (nt, nd) for var in data):
        dim_str = '['+' '.join([str(var.shape) for var in data])+']'
        raise ValueError('Dimension of data {} does not match time ({:d},) and z ({:d},)'.format(dim_str, nt, nd))
    with open(filename, 'w') as fout:
        for i in range(nt):
            fidx = []
            if skip_value is not None:
                for j in range(nd):
                    if any(np.isnan(var[i,j]) for var in data) or any(var[i,j] == skip_value for var in data):
                        fidx.append(j)
            nskip = len(fidx)
            if nd-nskip > 0:
                out_str = '{}  {}  {}\n'.format(time[i].strftime('%Y-%m-%d %H:%M:%S'), nd-nskip, order)
                fout.write(out_str)
                for j in range(nd):
                    if j not in fidx:
                        out_str = '{:8.2f}'.format(z[j])
                        for var in data:
                            out_str += '  {:10.6f}'.format(var[i,j]*scale_factor)
                        out_str += '\n'
                        fout.write(out_str)
