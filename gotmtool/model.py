#--------------------------------
# GOTM Model object
#--------------------------------

import os
import subprocess as sp
from .io import *
from .utils import *

class Model:

    """A GOTM model

    """

    def __init__(
            self,
            name = 'GOTM test',
            config = None,
            environ = os.environ['HOME']+'/.gotm_env.yaml'
            ):
        """Initialization

        :name:    (str) name of the model
        :config:  (str or dict-like) path of a YAML file or a dictionary containing the GOTM configurations
        :environ: (str or dict-like) path of a YAML file or a dictionary containing the GOTM environment variables

        """
        if config is None:
            print_error('GOTM configuration required')
            print_hints('A GOTM configuration can either be a dictionary-like object or a YAML file containing all the configurations')
        if not os.path.exists(environ):
            print_error('GOTM environment file \'{}\' not found'.format(environ))
            print_hints('Please run gotm_env_init.py to set it up')
        self.name = name
        self.config = config_loader(config)
        self.environ = config_loader(environ)
        self._exe = self.environ['gotmdir_exe']+'/bin/gotm'

    def _is_built(self):
        """Check if the model has been built

        :returns: (bool) True if a GOTM executable has been built, False otherwise

        """
        return os.path.isfile(self._exe) and os.access(self._exe, os.X_OK)

    def _is_clean(self):
        """Check if the source code directory is clean

        :returns: (bool) True if the source code directory is clean, False otherwise

        """
        # check if the source code directory is clean, return False if dirty
        cmd = ['git', 'status', '--short']
        clean_info = sp.run(cmd, cwd=self.environ['gotmdir_code'], check=True, stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
        return clean_info.stdout == ''

    def _is_updated(self):
        """Check if the executable is updated with the source code

        :returns: (bool) True if the GOTM executable is updated, False otherwise

        """
        # return False if not built
        if not self._is_built():
            return False
        if not self._is_clean():
            return False
        # get the version of the compiled GOTM executable
        cmd = [self._exe, '--version']
        version_info = sp.run(cmd, check=True, stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
        # get the hash tag of the source code
        cmd = ['git', 'show', '-s', '--format=%h']
        hash_info = sp.run(cmd, cwd=self.environ['gotmdir_code'], check=True, stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
        # return False if the hash tag does not match the GOTM version
        return hash_info.stdout.strip() in version_info.stdout

    def build(
            self,
            force = False,
            use_cvmix = True,
            use_fabm = False,
            use_stim = False,
            use_netcdf = True,
            extra_output = False,
            ):
        """Build GOTM source code

        :force:        (bool) flag to force the build
        :use_cvmix:    (bool) flag to compile GOTM with CVMix
        :use_fabm:     (bool) flag to compile GOTM with FABM
        :use_stim:     (bool) flag to compile GOTM with STIM
        :use_netcdf:   (bool) flag to compile GOTM with NetCDF
        :extra_output: (bool) flag to output additional turbulence diagnostics

        """
        if not self._is_updated() or force:
            # clean up
            cleanup_dir(self.environ['gotmdir_build'])
            cleanup_dir(self.environ['gotmdir_exe'])
            # build the source code
            cmd = ['cmake']
            cmd.append(self.environ['gotmdir_code'])
            cmd.append('-DCMAKE_INSTALL_PREFIX:PATH='+self.environ['gotmdir_exe'])
            cmd.append('-DGOTM_USE_CVMIX='+str(use_cvmix).lower())
            cmd.append('-DGOTM_USE_FABM='+str(use_fabm).lower())
            cmd.append('-DGOTM_USE_STIM='+str(use_stim).lower())
            cmd.append('-DGOTM_USE_NetCDF='+str(use_netcdf).lower())
            cmd.append('-DGOTM_EXTRA_OUTPUT='+str(extra_output).lower())
            print('-'*64)
            print('Building GOTM...')
            print('-'*64+'\n')
            print(' '.join(cmd))
            proc = sp.run(cmd, cwd=self.environ['gotmdir_build'], check=True, stdout=sp.PIPE, text=True)
            print('\n'+proc.stdout+'\n')
            print('make install')
            proc = sp.run(['make','install'], cwd=self.environ['gotmdir_build'], check=True, stdout=sp.PIPE, text=True)
            print('\n'+proc.stdout+'\n')
            if proc.returncode == 0:
                print_ok('Done!')
        else:
            print_warning('GOTM is updated. Skipping the build step. Use \'force=True\' to rebuild')

    def run(self):
        """TODO: Docstring for run.
        :returns: TODO

        """
        pass

