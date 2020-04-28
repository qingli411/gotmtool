#!/usr/bin/env python3
#
# Initialize GOTM environment
#
# Qing Li, 20200423

import os
from ruamel.yaml import YAML
from gotmtool.utils import *

def main():
    """Set up GOTM environment variables

    """
    # print some instructions
    print_help()
    # inquire GOTM environment file
    while True:
        envfile = inquire(
                'GOTM environment configuration file',
                os.environ['HOME']+'/.gotm_env.yaml',
                )
        envfile = os.path.expanduser(envfile)
        if check_file(envfile):
            break
    # set gotm root directory
    base = os.path.basename(envfile)
    envname = os.path.splitext(base)[0].replace('.','')
    if envname == 'gotm_env':
        gotmdir = os.path.dirname(os.getcwd())+'/gotm'
    else:
        gotmdir = os.path.dirname(envfile)+'/'+envname
    # inquire GOTM directories
    messages = {
            'code': 'Directory of the GOTM source code',
            'data': 'Directory of the GOTM input data',
            'build': 'Directory to build GOTM',
            'exe': 'Directory to install the GOTM executable',
            'run': 'Directory to run GOTM cases',
            'figure': 'Directory to save figures of standard diagnostics',
            }
    dirs = {}
    for name in messages.keys():
        while True:
            tmpdir = inquire(messages[name], gotmdir+'/'+name)
            # check if input directory is valid
            if check_dir(tmpdir):
                break
        dirs['gotmdir_'+name] = tmpdir

    # create the GOTM environment file
    print('-'*64)
    print('Writting GOTM environment to \'{:s}\':'.format(envfile))
    for name in dirs.keys():
        print('  {:s}: {:s}'.format(name, dirs[name]))
    print('-'*64)
    yaml=YAML()
    with open(envfile, 'w') as f:
        yaml.dump(dirs, f)

    # done
    print_ok('Done!')

def print_help():
    """Print help information

    """
    print('-'*64)
    print('Setting up GOTM environment')
    print('-'*64)
    print('\nPlease type in the full path of the file or directory.')
    print('Leave it empty to use the default value in parentheses.\n')

def check_file(filename):
    """Check if the file name is valid.

    :filename: (str) full path of the file
    :returns:  (bool) if file is valid

    """
    # expand user's home directory
    filename = os.path.expanduser(filename)
    # check if is a full path
    if filename[0] != '/':
        print_error('Please use the full path')
        return False
    if os.path.exists(filename):
        print_warning('File \'{:s}\' exists'.format(filename))
        yn = inquire(
                'Overwrite? Type in \'y\' to confirm and \'n\' to use a different file name',
                'y',
                )
        if yn == 'y':
            return True
        else:
            return False
    elif os.access(os.path.dirname(filename), os.W_OK):
        return True
    else:
        print_error('Cannot create the file \'{:s}\' -- no write privilege'.format(filename))
        print('Please try again')
        return False

def check_dir(dirname):
    """Check if the directory is valid. If so, make the directory and
       return True. If not, return False

    :dirname: (str) directory name
    :returns: (bool) if directory is valid

    """
    # expand user's home directory
    filename = os.path.expanduser(dirname)
    # check if is a full path
    if dirname[0] != '/':
        print_error('Please use the full path')
        return False
    # check if exists
    if os.path.exists(dirname):
        print_warning('Directory \'{:s}\' exists'.format(dirname))
        yn = inquire(
                'Continue? Type in \'y\' to confirm and \'n\' to use a differnet directory',
                'y',
                )
        if yn == 'y':
            return True
        else:
            return False
    else: # check if make directory is success
        try:
            os.makedirs(dirname, 0o750)
            return True
        except OSError as e:
            print_error(e.__str__())
            print('Please try again')
            return False

if __name__ == "__main__":
    main()
