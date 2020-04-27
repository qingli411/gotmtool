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

    def _is_updated(self):
        """Check if the executable is updated with the source code

        :returns: (bool) True if the GOTM executable is updated, False otherwise

        """
        return True

    def build(self):
        """Build GOTM source code

        """
        if self._is_built() and self._is_updated():
            print('GOTM is already built and updated')
        else:
            cmd = ['cmake']
            cmd.append(self.environ['gotmdir_code'])
            cmd.append('-DCMAKE_INSTALL_PREFIX:PATH='+self.environ['gotmdir_exe'])
            cmd.append('-DGOTM_USE_FABM=false')
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

    def run(self):
        """TODO: Docstring for run.
        :returns: TODO

        """
        pass

