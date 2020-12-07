#--------------------------------
# Diagnostics
#--------------------------------
import numpy as np
import xarray as xr

def get_mld_deltaT(Temp, deltaT=0.2, zRef=-10):
    """Find the mixed layer depth defined as the depth where
       the temperature difference from the reference level first exceeds
       a threshold value

    :Temp: (xarray.DataArray) temperature in degree C
    :deltaT: (float, optional) temperature threshold in degree C
    :zRef: (float, optional) depth of the reference level
    :returns: (xarray.DataArray) mixed layer depth in m

    """
    t = Temp.values
    z = Temp.z.values
    nt = Temp.time.shape[0]
    mld_val = np.zeros(nt)
    for i in np.arange(nt):
        idx_zref = np.argmin(np.abs(z-zRef))
        dT = t[:,i]-t[idx_zref,i]
        # ignore the points above the reference level
        dT[idx_zref:] = 0.
        # ignore nan
        dT[np.isnan(dT)] = 0.
        # find the maximum index (closest to the surface) where the temperature
        # difference is greater than the threshold value
        idxlist = np.where(np.abs(dT)>=deltaT)
        if idxlist[0].size>0:
            idx_min = np.max(idxlist)
            mld_val[i] = z[idx_min]
        else:
            mld_val[i] = np.min(z)
    mld = xr.DataArray(np.abs(mld_val), dims=['time'], coords={'time': Temp.time},
                      attrs={'long_name': 'mixed layer depth (T threshold)',
                            'units': 'm'})
    return mld

def get_mld_deltaR(Rho, deltaR=0.03, zRef=-10):
    """Find the mixed layer depth defined as the depth where
       the potential density difference from the reference level first exceeds
       a threshold value

    :Rho: (xarray.DataArray) potential density in kg/m^3
    :deltaR: (float, optional) potential density threshold in kg/m^3
    :zRef: (float, optional) depth of the reference level
    :returns: (numpy array) mixed layer depth

    """
    r = Rho.values
    z = Rho.z.values
    nt = Rho.time.shape[0]
    mld_val = np.zeros(nt)
    for i in np.arange(nt):
        idx_zref = np.argmin(np.abs(z-zRef))
        dRho = r[:,i]-r[idx_zref,i]
        # ignore the points above the reference level
        dRho[idx_zref:] = -99.
        # ignore nan
        dRho[np.isnan(dRho)] = -99.
        # find the maximum index (closest to the surface) where the density
        # difference is greater than the threshold value
        idxlist = np.where(dRho>=deltaR)
        if idxlist[0].size>0:
            idx_min = np.max(idxlist)
            mld_val[i] = z[idx_min]
        else:
            mld_val[i] = np.min(z)
    mld = xr.DataArray(np.abs(mld_val), dims=['time'], coords={'time': Rho.time},
                      attrs={'long_name': 'mixed layer depth (rho threshold)',
                            'units': 'm'})
    return mld

def get_bld_maxNN(NN):
    """Find the boundary layer depth defined as the depth where
       the stratification N^2 reaches its maximum

    :NN: (xarray.DataArray) stratification
    :returns: (xarray.DataArray) boundary layer depth in m

    """
    Nsqr = NN.values
    z = NN.zi.values
    nz = z.size
    nt = NN.time.shape[0]
    bld_val = np.zeros(nt)
    # find the indices where N^2 reaches its maximum
    # add small noise that increase with depth to find the shallowest
    # occurrence when N^2 is constant
    noise = np.array(np.arange(nz))*1e-15
    for i in np.arange(nt):
        idx_max = np.argmax(Nsqr[:,i]+noise)
        bld_val[i] = z[idx_max]
    bld = xr.DataArray(np.abs(bld_val), dims=['time'], coords={'time': NN.time},
                      attrs={'long_name': 'boundary layer depth (Max N^2)',
                            'units': 'm'})
    return bld

def get_bld_nuh(nuh, nuh_bg=1e-5):
    """Find the boundary layer depth defined as the depth where
       the turbulent diffusivity first drops to a background value

    :nuh: (xarray.DataArray) turbulent diffusivity in m^2/s
    :nuh_bg: (float, optional) background diffusivity in m^2/s
    :returns: (xarray.DataArray) boundary layer depth in m

    """
    nu = nuh.values
    z = nuh.zi.values
    nz = z.size
    nt = nuh.time.shape[0]
    bld_val = np.zeros(nt)
    for i in np.arange(nt):
        idxlist = np.where(nuh[:,i]<nuh_bg)[0]
        idxlist = idxlist[idxlist<nz-1]
        if idxlist.size==0:
            bld[i] = z[0]
        elif np.max(idxlist)<nz-2:
            idx1 = np.max(idxlist)
            idx0 = idx1+1
            bld_val[i] = z[idx0] - (z[idx0]-z[idx1]) * \
                     (nuh[idx0,i]-nuh_bg) / (nuh[idx0,i]-nuh[idx1,i])
        else:
            bld_val[i] = z[-1]
    bld = xr.DataArray(np.abs(bld_val), dims=['time'], coords={'time': nuh.time},
                      attrs={'long_name': 'boundary layer depth (nuh threshold)',
                            'units': 'm'})
    return bld

def get_bld_tke(tke, tke_crit=1e-7):
    """Find the boundary layer depth defined as the depth where
       the turbulent kinetic energy approaches zero (equals a small
       critical value.

    :tke: (xarray.DataArray) turbulent kenetic energy in m^2/s^2
    :tke_crit: (float, optional) critial TKE in m^2/s^2
    :returns: (xarray.DataArray) boundary layer depth in m

    """
    e = tke.values
    z = tke.zi.values
    nz = z.size
    nt = tke.time.shape[0]
    bld_val = np.zeros(nt)
    for i in np.arange(nt):
        idxlist = np.where(tke[:,i]<tke_crit)[0]
        idxlist = idxlist[idxlist<nz-1]
        if idxlist.size==0:
            bld_val[i] = z[0]
        elif np.max(idxlist)<nz-2:
            idx1 = np.max(idxlist)
            idx0 = idx1+1
            bld_val[i] = z[idx0] - (z[idx0]-z[idx1]) * \
                (tke[idx0,i]-tke_crit) / (tke[idx0,i]-tke[idx1,i])
        else:
            bld_val[i] = z[-1]
    bld = xr.DataArray(np.abs(bld_val), dims=['time'], coords={'time': tke.time},
                      attrs={'long_name': 'boundary layer depth (TKE threshold)',
                            'units': 'm'})
    return bld
