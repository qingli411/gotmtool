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
                '.gotm_env.yaml',
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
    # add GOTM tool directory (current directory)
    dirs['gotmdir_tool'] = os.getcwd()
    # create the GOTM environment file
    print('-'*64)
    print('Writting GOTM environment to \'{:s}\':'.format(envfile))
    for name in dirs.keys():
        print('  {:s}: {:s}'.format(name, dirs[name]))
    print('-'*64)
    yaml=YAML()
    with open(envfile, 'w') as f:
        yaml.dump(dirs, f)
    # process examples
    print('Processing examples...')
    process_examples()
    print('-'*64)
    # link examples directory to gotmdir_data
    try:
        os.symlink(os.getcwd()+'/examples', dirs['gotmdir_data']+'/examples')
    except FileExistsError:
        pass
    # check out GOTM source code
    default_repo = 'https://github.com/gotm-model/code.git'
    default_branch = 'master'
    yn = inquire('\nDownload GOTM source code from a git repository? Type in \'y\' to confirm and \'n\' to skip', 'n')
    if yn == 'y':
        gotm_repo = inquire('Repository URL', default_repo)
        gotm_branch = inquire('Branch name', default_branch)
        rc = install_gotm(gotm_repo, gotm_branch, dirs['gotmdir_code'])
    else:
        rc = 0
    # done
    if rc == 0:
        print('-'*64)
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
    # expand absolute path
    filename = os.path.abspath(filename)
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
    dirname = os.path.expanduser(dirname)
    # expand absolute path
    dirname = os.path.abspath(dirname)
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

def install_gotm(repo, branch, path):
    """Install GOTM source code

    :repo:   (str) git repository of the GOTM source code
    :branch: (str) branch name of the GOTM source code
    :path:   (str) full path of the GOTM source code directory

    """
    rc1 = os.system('git clone {:s} {:s}'.format(repo, path))
    cwd = os.getcwd()
    os.chdir(path)
    rc2 = os.system('git checkout {:s}'.format(branch))
    rc3 = os.system('git submodule update --init --recursive')
    os.chdir(cwd)
    return rc1+rc2+rc3

def process_examples():
    """Process data for examples.
    :returns: None

    """
    cwd = os.getcwd()
    path = os.path.join(cwd, 'examples')
    examples = os.listdir(path)
    exes = ['extract_data']
    for case in examples:
        casedir = os.path.join(path, case)
        print(' - {}'.format(case))
        for exe in exes:
            if os.path.isfile(os.path.join(casedir, exe)):
                os.chdir(casedir)
                rc = os.system(os.path.join('.', exe))
    os.chdir(cwd)
    return None

if __name__ == "__main__":
    main()
