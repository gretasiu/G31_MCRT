#
# Importing files and packages
#
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import central_star as cs
#
# Some natural constants
#
au = 1.49598e13     # Astronomical Unit       [cm]
pc = 3.08572e18     # Parsec                  [cm]
ms = 1.98892e33     # Solar mass              [g]
Ts = 5.78e3         # Solar temperature       [K]
Ls = 3.8525e33      # Solar luminosity        [erg/s]
Rs = 6.96e10        # Solar radius            [cm]
#
# Number of photons
#
nphot = 1e6
nphot_scat = 1e6
#
# Grid parameters
#
nx = 32  # number of cell on x axis
ny = 32
nz = 32
sizex = 8500*au
sizey = 8500*au
sizez = 8500*au

#
# Density model parameters (taken from Beltran 2021 0r 2019)
#
rhoc = 9e-18  # g cm^-3
rc = 8500*au
n = 2
#
# Star parameters
#
mstar = cs.M_star_G31*ms
rstar = cs.R_star_G31*Rs
tstar = cs.T_star_G31
pstar = np.array([0., 0., 0.])  # posiiton of the star inside the grid; center
#
# Make the coordinates for density profile
#
xi = np.linspace(-sizex, sizex, nx+1)  # finding all the walls of the cells
yi = np.linspace(-sizey, sizey, nx+1)
zi = np.linspace(-sizez, sizez, nx+1)
# finding the midpoints of each cell by adding up walls from both sides and dividing by 2
xc = 0.5 * (xi[0:nx] + xi[1:nx+1])
yc = 0.5 * (yi[0:ny] + yi[1:ny+1])
zc = 0.5 * (zi[0:nz] + zi[1:nz+1])
#
# Dust density model
#
qq = np.meshgrid(xc, yc, zc, indexing='ij')
xx = qq[0]
yy = qq[1]
zz = qq[2]
rr = np.sqrt(xx**2+yy**2+zz**2)
rhod = rhoc*(rr/rc)**(-n)
#
# wavelength which I want to calculate over
#
lammin = 1e-10
lammax = 1e4
steplam = 1000
lam = np.linspace(lammin, lammax+steplam, steplam)
nlam = lam.size
#
# Write the wavelength_micron.inp file
#
with open('wavelength_micron.inp', 'w+') as f:
    f.write('%d\n' % (nlam))
    for value in lam:
        f.write('%13.6e\n' % (value))
#
# write the star.inp file
#
with open('stars.inp', 'w+') as f:
    f.write('2\n')
    f.write('1 %d\n\n' % (nlam))
    f.write('%13.6e %13.6e %13.6e %13.6e %13.6e\n\n' %
            (rstar, mstar, pstar[0], pstar[1], pstar[2]))
    for value in lam:
        f.write('%13.6e\n' % (value))
    f.write('\n%13.6e\n' % (-tstar))
#
# Write the grid file
#
with open('amr_grid.inp', 'w+') as f:
    f.write('1\n')                       # iformat
    # AMR grid style  (0=regular grid, no AMR)
    f.write('0\n')
    f.write('0\n')                       # Coordinate system
    f.write('0\n')                       # gridinfo
    f.write('1 1 1\n')                   # Include x,y,z coordinate
    f.write('%d %d %d\n' % (nx, ny, nz))     # Size of grid
    for value in xi:
        f.write('%13.6e\n' % (value))      # X coordinates (cell walls)
    for value in yi:
        f.write('%13.6e\n' % (value))      # Y coordinates (cell walls)
    for value in zi:
        f.write('%13.6e\n' % (value))      # Z coordinates (cell walls)
#
# Write the density file
#
with open('dust_density.inp', 'w+') as f:
    f.write('1\n')                       # Format number
    f.write('%d\n' % (nx*ny*nz))           # Nr of cells
    f.write('1\n')                       # Nr of dust species
    # Create a 1-D view, fortran-style indexing
    data = rhod.ravel(order='F')
    data.tofile(f, sep='\n', format="%13.6e")
    f.write('\n')
#
# Dust opacity control file
#
with open('dustopac.inp', 'w+') as f:
    f.write('2               Format number of this file\n')
    f.write('1               Nr of dust species\n')
    f.write(
        '============================================================================\n')
    f.write('1               Way in which this dust species is read\n')
    f.write('0               0=Thermal grain\n')
    f.write('sg-a10um        Extension of name of dustkappa_***.inp file\n')
    f.write(
        '----------------------------------------------------------------------------\n')
#
# Write the radmc3d.inp control file
#
with open('radmc3d.inp', 'w+') as f:
    f.write('nphot = %d\n' % (nphot))
    f.write('nphot_scat = %d\n' % (nphot_scat))
    f.write('scattering_mode_max = 2\n')
    #f.write('iranfreqmode = 1\n')
    f.write('setthreads = 40\n')
    f.write('istar_sphere = 0\n')
#

