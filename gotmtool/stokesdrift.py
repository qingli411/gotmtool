#--------------------------------
# Stokes drift
#--------------------------------

import numpy as np
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

    :z:           (array-like) depth (m)
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
    if z.size == 1:
        dz = 1.e6 # an arbitrarily large number
    else:
        dz = np.zeros_like(z)
        dz[1:-1] = 0.5 * (z[0:-2]-z[2:])
        dz[0] = -z[0] + 0.5 * (z[1] - z[0])
        dz[-1] = dz[-2]
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
    :z:           (array-like) depth (m)
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

