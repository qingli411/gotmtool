#--------------------------------
# Stokes drift
#--------------------------------

import numpy as np
from scipy import special
from .constants import gravity

def stokes_drift_dhh85(
        z,
        wind_speed,
        wave_age,
        omega_min=0.1,
        omega_max=20.,
        n_omega=1000,
        ):
    """Compute Stokes drift from Donelan et al., 1985 spectrum

    :z:           (array-like) depth < 0 (m)
    :wind_speed:  (float) 10-meter wind speed (m/s)
    :wave_age:    (float) wave age (unitless)
    :omega_min:   (float) minimum frequency (2*pi*f) for integration
    :omega_max:   (float) maximum frequency (2*pi*f) for integration
    :n_omega:     (int) number of frequency bins for integration
    :returns:     (array-like) Stokes drift at z

    """
    omega = np.linspace(omega_min, omega_max, n_omega)
    domega = omega[1]-omega[0]
    z = np.array(z)
    dz, _ = _get_grid(z)
    us = np.zeros_like(z)
    for i in np.arange(n_omega):
        us += domega * _stokes_drift_kernel_dhh85(omega[i],z,dz,wind_speed,wave_age)
    return us

def _stokes_drift_kernel_dhh85(
        omega,
        z,
        dz,
        wind_speed,
        wave_age,
        ):
    """Kernel of the Stokese

    :omega:       (float) frequency (2*pi*f)
    :z:           (array-like) depth < 0 (m)
    :dz:          (array-like) layer thickness (m)
    :wind_speed:  (float) 10-meter wind speed (m/s)
    :wave_age:    (float) wave age (unitless)
    :return:      (array-like) Stokes drift kernel at omega and z

    """
    iwa = 1./wave_age
    omega_p = gravity * iwa / wind_speed
    alpha = 0.006 * iwa**(0.55)
    sigma = 0.08 * (1. + 4. * wave_age**3)
    if iwa <= 1.:
        gamma1 = 1.7
    else:
        gamma1 = 1.7 + 6. * np.log10(iwa)
    gamma2 = np.exp(-0.5 * (omega - omega_p)**2 / sigma**2 / omega_p**2)
    spec = alpha * gravity**2 / (omega_p * omega**4) * np.exp(-(omega_p/omega)**4) * gamma1**gamma2
    kdz = omega**2 * dz / gravity
    zfilter = np.where(kdz < 10., np.sinh(kdz)/kdz, 1.)
    return 2. * (spec * omega**3) * zfilter * np.exp(2. * omega**2 * z / gravity) / gravity

def stokes_drift_spec(
        z,
        spec,
        xcmp,
        ycmp,
        freq,
        dfreq,
        tail_fm5=False,
        ):
    """Compute Stokes drift profile from wave spectrum

    :z:           (array-like) depth < 0 (m)
    :spec:        (array-like) band wave energy density (m^2 s)
    :xcmp:        (array-like) fraction of x-component (0-1)
    :ycmp:        (array-like) fraction of y-component (0-1)
    :freq:        (array-like) band center wave frequency (Hz)
    :dfreq:       (array-like) band width of wave frequency (Hz)
    :tail_fm5:    (bool, optional) add contribution from a f^-5 tail
    :returns:     (array-like) Stokes drift at z (x- and y-components)

    """
    z     = np.array(z)
    spec  = np.array(spec)
    xcmp  = np.array(xcmp)
    ycmp  = np.array(ycmp)
    freq  = np.array(freq)
    dfreq = np.array(dfreq)
    us    = np.zeros_like(z)
    vs    = np.zeros_like(z)
    nfreq = freq.size
    nz    = z.size
    const = 8. * np.pi**2 / gravity
    factor2 = const * freq**2
    factor = 2. * np.pi * freq *factor2 * dfreq
    # cutoff frequency
    freqc = freq[-1] + 0.5 * dfreq[-1]
    dfreqc = dfreq[-1]
    # get vertical grid
    dz, zi = _get_grid(z)
    # Stokes drift averaged over the grid cell
    for i in np.arange(nz):
        for j in np.arange(nfreq):
            kdz = factor2[j] * dz[i] / 2.
            if kdz < 100.:
                tmp = np.sinh(kdz) / kdz * factor[j] * spec[j] * np.exp(factor2[j]*z[i])
            else:
                tmp = factor[j] * spec[j] * np.exp(factor2[j]*z[i])
            us[i] += tmp * xcmp[j]
            vs[i] += tmp * ycmp[j]
    # contribution from a f^-5 tail
    if tail_fm5:
        us_t, vs_t = stokes_drift_tail_fm5(z, spec[-1], xcmp[-1], ycmp[-1], freqc)
        us += us_t
        vs += vs_t
    return us, vs

def stokes_drift_tail_fm5(
        z,
        spec,
        xcmp,
        ycmp,
        freq,
        ):
    """Contribution of a f^-5 spectral tail to Stokes drift
       see Apppendix B of Harcourt and D'Asaro 2008

    :z:           (array-like) depth < 0 (m)
    :spec:        (float)
    :xcmp:        (float) fraction of x-component (0-1)
    :ycmp:        (float) fraction of y-component (0-1)
    :freq:        (float) cutoff frequency
    :returns:     (array-like) Stokes drift at z (x- and y-components)

    """
    # initialize arrays
    nz    = z.size
    us    = np.zeros_like(z)
    vs    = np.zeros_like(z)
    # constants
    const = 8. * np.pi**2 / gravity
    # get vertical grid
    dz, zi = _get_grid(z)
    for i in np.arange(nz):
        aplus = np.maximum(1.e-8, -const * freq**2 * zi[i])
        aminus = -const * freq**2 * zi[i+1]
        iplus = 2. * aplus / 3. * (np.sqrt(np.pi * aplus) * special.erfc(np.sqrt(aplus)) - (1. - 0.5 / aplus) * np.exp(-aplus))
        iminus = 2. * aminus / 3. * (np.sqrt(np.pi * aminus) * special.erfc(np.sqrt(aminus)) - (1. - 0.5 / aminus) * np.exp(-aminus))
        tmp = 2. * np.pi * freq**2 / dz[i] * spec * (iplus - iminus)
        us[i] = tmp * xcmp
        vs[i] = tmp * ycmp
    return us, vs

def _get_grid(z):
    # get vertical grid thickness
    z     = np.array(z)
    nz    = z.size
    if nz == 1:
        dz = np.ones(1)*1.e6 # an arbitrarily large number
        zi = z
    else:
        dz = np.zeros_like(z)
        zi = np.zeros(nz+1)
        dz[1:-1] = 0.5 * (z[0:-2] - z[2:])
        dz[0] = -z[0] + 0.5 * (z[0] - z[1])
        dz[-1] = dz[-2]
        zi[1:] = -np.cumsum(dz)
    return dz, zi

def stokes_drift_usp(
        z,
        freq,
        ussp,
        vssp,
        ):
    """Compute Stokes drift profile from partitioned Stokes drift

    :z:           (array-like) depth < 0 (m)
    :freq:        (array-like) band center wave frequency (Hz)
    :ussp:        (array-like) x-component of partitioned Stokes drift (m/s)
    :vssp:        (array-like) y-component of partitioned Stokes drift (m/s)
    :returns:     (array-like) Stokes drift at z (x- and y-components)

    """
    z     = np.array(z)
    freq  = np.array(freq)
    ussp  = np.array(ussp)
    vssp  = np.array(vssp)
    us    = np.zeros_like(z)
    vs    = np.zeros_like(z)
    nfreq = freq.size
    nz    = z.size
    const = 8. * np.pi**2 / gravity
    factor = const * freq**2
    # get vertical grid
    dz, _ = _get_grid(z)
    # Stokes drift averaged over the grid cell
    for i in np.arange(nz):
        for j in np.arange(nfreq):
            kdz = factor[j] * dz[i] / 2.
            if kdz < 100.:
                tmp = np.sinh(kdz) / kdz * np.exp(factor[j]*z[i])
            else:
                tmp = np.exp(factor[j]*z[i])
            us[i] += tmp * ussp[j]
            vs[i] += tmp * vssp[j]
    return us, vs

