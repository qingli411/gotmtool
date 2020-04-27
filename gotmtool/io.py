#--------------------------------
# Functions for input/output
#--------------------------------

import os
import re
import sys
from ruamel.yaml import YAML

def config_loader(config):
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

def yaml_load(filename):
    """Read yaml configuration file

    :filename: (str) path of the input file

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

