
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import pythia8

#   load trento data for 100,000 Au Au events
data = np.loadtxt('AuAu_200GeV_100k.txt')

#   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]
#   create a list for the initial entropy of the events
mult = data[:,3]
e2 = data[:,4]

#   apply proportionality constanst to convert initial entropy to charged multiplicity
#   constant was calculated by fitting the trento data to phenix data
mult = 4.65905256 * mult

#   change the constituents of mult to int values
for i in range(len(mult)):
    mult[i] = round(mult[i])
mult = mult.astype(np.int64)

T = 0.15 # temperature in GeV
deta = 4
# set pion mass to 0.14 GeV
mpi = 0.14

# rho_0 scaling parameter for radial flow
# from Retiere and Lisa, PRC70.044907 (2004), table 2
rho_0 = 0.85

# e2 scaling parameter for elliptic flow
# from Alver and Roland, PRC81.054905 (2010), fig 4
rho_2 = 0.15

# pythia settings
eCM  = 200.0
pTHatMin  = 20.0
seed  = -1
QCD = 'on'
QED = 'off'

#   Initialize Pythia
pythia = pythia8.Pythia()
    
eCM = str(eCM)
set_eCM = "Beams:eCM = " + eCM
pythia.readString(set_eCM)

set_QCD = "HardQCD:all = " + QCD
pythia.readString(set_QCD)

set_QED = "PromptPhoton:all = " + QED
pythia.readString(set_QED)

pTHatMin = str(pTHatMin)
set_pTHatMin = "PhaseSpace:pTHatMin = " + pTHatMin
pythia.readString(set_pTHatMin)

pythia.readString("Random:setseed = on")
    
seed = str(seed)
set_seed = "Random:seed = " + seed
pythia.readString(set_seed)

pythia.init()

#   Initialize SlowJet
etaMax = 4.
nSel = 2    

radius = 0.4
pTjetMin = 18
var_radius = np.arange(0,1.2,0.1)
var_pTjetMin = np.arange(5,40,1)
pTjetMin_list = []
radius_list = []
jets_found_pT = []
jets_found_rad = []

tot_radius = []
tot_pTjetMin = []
tot_jets_found = []

for i in range(100):

    pT = []
    phi = []
    eta = []

    pythia.event.reset()
    pythia.next()
    pythia.event.size()
    
    for j in range(mult[i]):
        r1, r2, r3, r4 = np.random.random(4)

        # pT = transverse momentum
        pT_r1 = T*(math.sqrt(-2*math.log(r1)))

        # phi = azimuthal angle
        phi_r2 = 2*(math.pi)*(r2 - 0.5)

        # eta = pseudo-rapidity
        eta_r3 = deta*(r3 - 0.5)

        # rho = normalized radial distance 
        rho_r4 = r4**0.5

        # calculate initial transverse rapidity (yT)
        eT = (mpi*mpi+pT_r1*pT_r1)**0.5
        yT = 0.5 * np.log((eT+pT_r1)/(eT-pT_r1))
        pT_initial = pT_r1
        yT_initial = yT

        # apply flow as additive boost to transverse rapidity
        yBoost = rho_r4*rho_0 + rho_2*e2[i]*np.cos(2*phi_r2)
        yT = yT_initial + yBoost

        # convert back to pT
        pT_wflow = mpi*np.cosh(yT)

        pT.append(pT_wflow)
        phi.append(phi_r2)
        eta.append(eta_r3)

        # add particles to the event list
        px = pT_wflow * math.cos(phi_r2)
        py = pT_wflow * math.sin(phi_r2)
        pz = pT_wflow * math.sinh(eta_r3)
        E = (pT_wflow**2 + pz**2 + mpi**2)**0.5
        pythia.event.append(211, 91, 0, 0, px, py, pz, E, mpi, 0., 9.)
    for pTjet in var_pTjetMin:
        slowJet = pythia8.SlowJet( -1, radius, pTjet, etaMax, nSel, 1)
        slowJet.analyze(pythia.event)
        jets_found = slowJet.sizeJet()
        
        jets_found_pT.append(jets_found)
        pTjetMin_list.append(pTjet)

    for rad in var_radius:
        slowJet = pythia8.SlowJet( -1, rad, pTjetMin, etaMax, nSel, 1)
        slowJet.analyze(pythia.event)
        jets_found = slowJet.sizeJet()

        jets_found_rad.append(jets_found)
        radius_list.append(rad)

    for pTjet in var_pTjetMin:
        for rad in var_radius:
            slowJet = pythia8.SlowJet( -1, rad, pTjet, etaMax, nSel, 1)
            slowJet.analyze(pythia.event)
            jets_found = slowJet.sizeJet()

            tot_radius.append(rad)
            tot_pTjetMin.append(pTjet)
            tot_jets_found.append(jets_found)

#   Create bins using np.histogram2d(), the number of bins produced is the square of the value "b"
b = 10
tot_bins = b**2
bin_counts, xedges, yedges = np.histogram2d(tot_pTjetMin,tot_radius,bins=b)
height, xedges, yedges = np.histogram2d(tot_pTjetMin,tot_radius,bins=[xedges,yedges],weights=tot_jets_found)
bin_counts = np.concatenate(bin_counts)
height = np.concatenate(height)

#   The bins are normalized by dividing each bin by the sample size within that bin
av_jets_found = height/bin_counts

xcenters = 0.5*(xedges[1:]+xedges[:-1])
xcenters = np.repeat(xcenters,b)
ycenters = 0.5*(yedges[1:]+yedges[:-1])
ycenters = np.tile(ycenters,b)

#   dx and dy define the thickness of the histogram bars
dx = (xedges[1]-xedges[0])
dy = (yedges[1]-yedges[0])

base = np.zeros(len(height))

#   2d histogram is plotted showing average jets_found for differing values of pTjetMin and radius
fig = plt.figure(2)
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(xcenters,ycenters,base,dx,dy,av_jets_found,color='b',alpha=1)

ax.set_xlabel('pTjetMin',fontsize=20)
ax.set_ylabel('radius',fontsize=20)
ax.set_zlabel('average jets_found/event')

#   separate 1d plots are made for both pTjetMin and radius       
plt.figure(1)
plt.subplot(211)
plt.plot(pTjetMin_list,jets_found_pT,'o', alpha = 0.2)
title = 'pTjetMin optimization: radius = ' + str(radius)
plt.title(title)
plt.xlabel('pTjetMin')
plt.ylabel('jets_found/event')

plt.subplot(212)
plt.plot(radius_list,jets_found_rad,'o', alpha = 0.2)
title = 'radius optimization: pTjetMin = ' + str(pTjetMin)
plt.title(title)
plt.xlabel('radius')
plt.ylabel('jets_found/event')

plt.show()
