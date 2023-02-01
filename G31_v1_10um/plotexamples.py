import numpy as np
import setup as p
from mpl_toolkits.mplot3d import axes3d
from matplotlib import pyplot as plt
from matplotlib import cm
from radmc3dPy.image import *
from radmc3dPy.analyze import *

#
# View a 2-D slice of the 3-D array of the setup
#
xx = p.xx[:, :, 16]
yy = p.yy[:, :, 16]
data = p.rhod[:, :, 16]
fig1 = plt.figure()
ax = fig1.gca(projection='3d')
#ax.plot_wireframe(xx, yy, data, rstride=1, cstride=1)
ax.plot_surface(xx, yy, data, rstride=1, cstride=1,
                cmap=cm.coolwarm, linewidth=0, antialiased=False)

#
# Plot the opacity table
#
o = readOpac(ext='sg-a10um')
plt.figure()
plt.loglog(o.wav[0], o.kabs[0],
           label=r'$\kappa_\nu^{\mathrm{abs}}$ (absorption)')
plt.loglog(o.wav[0], o.ksca[0], ':',
           label=r'$\kappa_\nu^{\mathrm{scat}}$ (scattering)')
plt.ylim((1e-2, 1e5))
plt.xlabel(r'$\lambda\;[\mu\mathrm{m}]$')
plt.ylabel(r'$\kappa_\nu\;[\mathrm{cm}^2/\mathrm{g}]$')
plt.title(r'Dust opacity ($a_{max}=10\,\mu\mathrm{m}$)')
plt.legend()
#
# Make and plot an example image
#
makeImage(npix=50, incl=60., phi=30., lambdarange=[
          1300., 7000.], nlam=2, sizeau=45)   # This calls radmc3d
fig2 = plt.figure()
a = readImage()
plotImage(a, log=True, au=True, maxlog=6, bunit='inu', cmap='hot', ifreq=0)
#plotImage(a, log=True, au=True, maxlog=6, cmap='hot', ifreq=0)
plotImage(a, log=True, au=True, maxlog=6, bunit='inu', cmap='hot', ifreq=1)
#plotImage(a, log=True, au=True, maxlog=6, cmap='hot', ifreq=1)
a.writeFits('image_scat_01_300.fits', dpc=100., ifreq=0)
a.writeFits('image_scat_01_1300.fits', dpc=100., ifreq=1)
#
# Make the SED, by calling RADMC-3D
# radmc3d performs ray tracing computation to compute the specral energy distribution (SED)
#
os.system("radmc3d sed incl 60 phi 30")

#
# Plotting it "by hand", the SED as seen at 1 pc distance
#
fig3 = plt.figure()
s = readSpectrum()
lam = s[:, 0]
nu = 1e4*cc/lam
fnu = s[:, 1]
nufnu = nu*fnu
plt.plot(lam, nufnu)
plt.xscale('log')
plt.yscale('log')
plt.xlim(1e-1, 1e4)
plt.xlabel('$\lambda\; [\mu \mathrm{m}$]')
plt.ylabel(
    '$\\nu F_\\nu \; [\mathrm{erg}\,\mathrm{cm}^{-2}\,\mathrm{s}^{-1}]$')

# #
# # Use the radmc3dPy.analyze tool set for plotting the SED,
# # this time let's plot nuLnu in units of Lsun
# #
# fig4 = plt.figure()
# plotSpectrum(s, nulnu=True, lsun=True, xlg=True, ylg=False, micron=True)
# plt.xlim(1e-1, 1e4)

#
# Use the radmc3dPy.analyze tool set to read in the dust temperatures
# calculated by the command-line command "radmc3d mctherm"
#
q = readData()
fig5 = plt.figure()
fig6 = plt.figure()
ay5 = fig5.gca(projection='3d')
ay6 = fig6.gca()
qq = np.meshgrid(q.grid.x, q.grid.y, q.grid.z, indexing='ij')
xx = qq[0][:, :, 16]
yy = qq[1][:, :, 16]
# The extra "0" is because of possible multiple dust species; here only 1 dust species
dd = q.dusttemp[:, :, 16, 0]
ay5.plot_surface(xx, yy, dd, rstride=1, cstride=1,
                 cmap=cm.coolwarm, linewidth=1)
c = ay6.pcolor(xx, yy, dd, cmap=cm.coolwarm, linewidth=1, shading='auto')
fig6.colorbar(c, label='[K]')


plt.show()
