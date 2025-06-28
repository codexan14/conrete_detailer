import core.materials as materials
import core.structural_sections as structural_sections
import core.geometry as geometry
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

b = 400
h = 600
fc = 28 
fy = 420 
ab = 1/4*np.pi*(25)**2

As = np.array([4, 2, 2, 4])*ab
position = np.linspace(40, 600-40, 4)
Es = 200000

print(position)

Force = []
Moment = []

phiMoment = []
phiForce = []


for c in 5*h*np.logspace(0.01, 1, 25, base=100)/100: 
    theta = 0.003/c 
    a = np.clip(0.85*c, 0, h)
    Fc = 0.85*fc*a*b 
    steel_strain_array = theta*(c - position)
    steel_stress_array = np.clip(steel_strain_array*200000, -420, 420)
    steel_force_array = steel_stress_array * As
#     print(c, steel_force_array)
    F = Fc + np.sum(steel_force_array)
    M = Fc*(h/2 - a/2) + np.sum(steel_force_array*(h/2 - position))
    # print(F,M)

    es = steel_strain_array[-1]
    phi = np.clip(0.65 + (0.90-0.65)/(0.005-0.0021)*(-es-0.0021), 0.65, 0.90)

    phiMn = M*phi 
    phiF = phi*np.clip(F , -np.sum(As)*420,0.80*(0.85*fc*(b*h - np.sum(As)) + np.sum(As)*420))

    print(a, phi, es)
    Force.append(F/1000)
    Moment.append(M/1000/1000)

    phiMoment.append(phiMn/1000/1000)
    phiForce.append(phiF/1000)



plt.plot(Moment,Force,'-o')
plt.plot(phiMoment, phiForce, '-*')

print(position)
plt.show()