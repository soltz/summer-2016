
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
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
radius = 0.7
pTjetMin = 10.
nSel = 2
massSet = 2
slowJet = pythia8.SlowJet( -1, radius, pTjetMin, etaMax, nSel, massSet);

for i in range(len(mult)): 

    pT = []
    phi = []
    eta = []

    jet_eta = []
    jet_phi = []
    jet_pT = []
    jet_eT = []
        
    bg_eta = []
    bg_phi = []
    bg_pT = []
    bg_eT = []
    

    pythia.event.reset()
    
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

    slowJet.analyze(pythia.event)

#   Extract constituents and convert nested list for ease of manipulation
    slowJetPrtList = [[] for j in range(slowJet.sizeJet())]
    for j in range(slowJet.sizeJet()):
        slowJetPrtList[j] = list(slowJet.constituents(j))

    if slowJet.sizeJet() > 0:
        totJetPrtList = np.concatenate(slowJetPrtList)
    else: totJetPrtList = [0]

#   Loop over pythia event particles
    for j in range(pythia.event.size()):
        prt = pythia.event[j]
        if prt.isFinal():
            prt_eta = prt.eta()
            prt_phi = prt.phi()
            prt_pT = prt.pT()
            prt_eT = prt.eT()
            if j in totJetPrtList:
                jet_eta.append(prt_eta)
                jet_phi.append(prt_phi)
                jet_pT.append(prt_pT)
                jet_eT.append(prt_eT)
            else:
                bg_eta.append(prt_eta)
                bg_phi.append(prt_phi)
                bg_pT.append(prt_pT)
                bg_eT.append(prt_eT)
        
#   Create bins using np.histogram2d(), the number of bins produced is the square of the value "b"
    b = 20
    tot_bins = b**2
    bg_h, xedges, yedges = np.histogram2d(bg_eta,bg_phi,bins=b,range=[[-2,2], [-(np.pi), np.pi]],weights=bg_eT)
    bg_h = np.concatenate(bg_h)
    xcenters = 0.5*(xedges[1:]+xedges[:-1])
    xcenters = np.repeat(xcenters,b)
    ycenters = 0.5*(yedges[1:]+yedges[:-1])
    ycenters = np.tile(ycenters,b)

#   Data from jet particles is binned separately        
    jet_h, jet_xedges, jet_yedges = np.histogram2d(jet_eta,jet_phi,bins=[xedges,yedges],weights=jet_eT)
    jet_h = np.concatenate(jet_h)

    xcenters = list(xcenters)
    ycenters = list(ycenters)
    xcenters.extend(xcenters)
    ycenters.extend(ycenters)
        
#   Bars associated with jets will sit on top of bars associated with background        
    bg_base = np.zeros(len(jet_h))
    bg_base = list(bg_base)
    jet_base = bg_h
    bg_base.extend(jet_base)
    base = bg_base
        
    bg_h = list(bg_h)
    jet_h = list(jet_h)
    bg_h.extend(jet_h)
    h = bg_h
        
#   Set size of bars in plot
    d_eta = (xedges[1]-xedges[0])
    d_phi = (yedges[1]-yedges[0])

#   Create an array of colors where bars associated with jet particles are red
#   Background bars are blue and bars with no value are white
    jet_colors=[]
    for j in h[0:tot_bins]:
        if j > 0:
            jet_colors.append('b')
        else:
            jet_colors.append('w')
    for j in range(len(jet_h)):
        if jet_h[j] > 0:
            jet_colors.append('r')
        elif h[j] > 0:
            jet_colors.append('b')
        else:
            jet_colors.append('w')

#   End of event loop. Statistics. Histogram. Done.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d(xcenters,ycenters,base,d_eta,d_phi,h,color=jet_colors,alpha=1)

    ax.set_xlabel('\n$\eta$',fontsize=20)
    ax.set_ylabel('\n$\phi$',fontsize=20)
    ax.set_zlabel('eT (GeV)')

    plt.title('slowJet w/ trento background')
    pi = np.pi
    plt.ylim(-pi,pi)

#    for j in range(slowJet.sizeJet()):
#        pT_jet = slowJet.pT(j)
#        pT_label = 'slowJet pT = %.2f' % pT_jet
#        ax.text(slowJet.y(j),slowJet.phi(j),max(h)+0.1,pT_label,horizontalalignment='center')

    plt.show(block = False)

    pythia.event.list()
    print "jets found: ", slowJet.sizeJet()
    print "trento multiplicity: ", mult[i]
    print "e2: ", e2[i]
    
    query = raw_input("q to quit, p to save to png,  <CR> to continue: ")
    if (query=='q'):
        break
    if (query=='p'):
        query = raw_input("name this png file (do not include extension .png): ")
        filename = query + '.png'
        plt.savefig(filename)
        query = raw_input("q to quit, <CR> to continue: ")
        if (query=='q'):
            break
    else: continue

    

