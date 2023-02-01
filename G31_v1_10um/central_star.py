import numpy as np
import matplotlib.pyplot as plt

M_sun = 1.988920e+33  # g
R_sun = 6.960000e+10  # cm
L_sun = 3.83e33  # erg s^-1

filename_hosokawa = "md3x3.dat"
filename_MIST = "MIST_ZAMS_galaxy.csv"

# importing data from the data file of accretin rate = 3*10^-3 M_solar yr^-1
lbol = np.genfromtxt(filename_hosokawa, skip_header=1, usecols=5)
M_star = np.genfromtxt(filename_hosokawa, skip_header=1, usecols=1)
R_star = np.genfromtxt(filename_hosokawa, skip_header=1, usecols=2)
L_star = np.genfromtxt(filename_hosokawa, skip_header=1, usecols=4)
t_acc = np.genfromtxt(filename_hosokawa, skip_header=1, usecols=6)

# importing data from MIST ZAMS
age = np.genfromtxt(filename_MIST, skip_header=1, usecols=1)
M_star_MIST = np.genfromtxt(filename_MIST, skip_header=1, usecols=2)
logL = np.genfromtxt(filename_MIST, skip_header=1, usecols=3)
logT = np.genfromtxt(filename_MIST, skip_header=1, usecols=4)
logR = np.genfromtxt(filename_MIST, skip_header=1, usecols=5)

# converting from log to solar normalized values
L_star_MIST = 10**logL  # solar luminosity
T_star = 10**logT
R_star_MIST = 10**logR  # solar radius

# writing noramlized values into file
f = open("MIST_normalized.txt", "w+")
f.write(" age(yr) M*(M_sun) L*(L_sun) T(K) R*(R_sun)\n")
for index in range(len(age)):
    f.write('%d %13.10e %13.10e %13.10e %13.10e %13.10e\n' % (index, age[index], M_star_MIST[index], L_star_MIST[index],
            T_star[index], R_star_MIST[index]))
f.close()

# The bolometric luminoisty of G31 (Beltran 2021; taken from Osorio 2009)
lbol_G31 = 4e4  # solar luminosity

# Getting central star information of G31
M_star_G31 = np.interp(lbol_G31, lbol, M_star)
R_star_G31 = np.interp(lbol_G31, lbol, R_star)
L_star_G31 = np.interp(lbol_G31, lbol, L_star)
t_acc_G31 = np.interp(lbol_G31, lbol, t_acc)
# using the stellar luminosity obtained to find the radius and temperatuure from MIST
# although we can already find R from Hosokawa, we can find it again here
R_star_G31_MIST = np.interp(L_star_G31, L_star_MIST, R_star_MIST)
T_star_G31 = np.interp(L_star_G31, L_star_MIST, T_star)

print("The mass of the central star is ", M_star_G31, "solar mass")
print("The radius of the central star is ", R_star_G31, "solar radius")
print("The stellar luminosity of the central star is ",
      L_star_G31, "solar lunminosity")
print("The accretion time of the central star is ", t_acc_G31, "year")
print("************")
print("The radius of central star from MIST is",
      R_star_G31_MIST, "solar radius")
print("The temperature of the central star from MIST is", T_star_G31, "K")
