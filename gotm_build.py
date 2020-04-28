#!/usr/bin/env python3
#
# Build GOTM
#
# Qing Li, 20200428

import os
from gotmtool.model import Model

def main():
    """Build GOTM

    """
    # create a model for build
    m = Model(
            # not used in the build step
            name='build',
            # not used in the build step, but should be a valid .yaml file
            config='./examples/gotm.yaml',
            # if necessary, change to the GOTM environment file set up
            # by gotm_env_init.py
            environ=os.environ['HOME']+'/.gotm_env.yaml',
            )
    # build the model
    print('-'*64)
    print('Building GOTM source code')
    print('-'*64)
    m.build(
            # do a clean build
            clean=True,
            # build with CVMix
            use_cvmix=True,
            # build with FABM
            use_fabm=False,
            # build with STIM
            use_stim=False,
            # build with NetCDF
            use_netcdf=True,
            # output extra output for turbulence variables
            extra_output=False,
            )

if __name__ == "__main__":
    main()
