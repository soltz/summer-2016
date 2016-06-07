
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
slowJet = pythia8.SlowJet( -1, radius, pTjetMin, etaMax, nSel, 1);

for i in range(len(mult)): 

    pT = []
    phi = []
    eta = []

#   empty lists for pythia particle info
    pjet_eta = []
    pjet_phi = []
    pjet_pT = []
    pjet_eT = []
        
    pbg_eta = []
    pbg_phi = []
    pbg_pT = []
    pbg_eT = []

#   empty lists for trento particle info
    tjet_eta = []
    tjet_phi = []
    tjet_pT = []
    tjet_eT = []
        
    tbg_eta = []
    tbg_phi = []
    tbg_pT = []
    tbg_eT = []
    
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

    slowJet.analyze(pythia.event)

#   Extract constituents and convert nested list for ease of manipulation
    slowJetPrtList = [[] for j in range(slowJet.sizeJet())]
    for j in range(slowJet.sizeJet()):
        slowJetPrtList[j] = list(slowJet.constituents(j))

    if slowJet.sizeJet() > 0:
        totJetPrtList = np.concatenate(slowJetPrtList)
    else: totJetPrtList = [0]

#   Loop over pythia particles
    for j in range(pythia.event.size() - mult[i]):
        prt = pythia.event[j]
        if prt.isFinal():
            prt_eta = prt.eta()
            prt_phi = prt.phi()
            prt_pT = prt.pT()
            prt_eT = prt.eT()
            if j in totJetPrtList:
                pjet_eta.append(prt_eta)
                pjet_phi.append(prt_phi)
                pjet_pT.append(prt_pT)
                pjet_eT.append(prt_eT)
            else:
                pbg_eta.append(prt_eta)
                pbg_phi.append(prt_phi)
                pbg_pT.append(prt_pT)
                pbg_eT.append(prt_eT)

#   Loop over trento particles
    for j in range(pythia.event.size() - mult[i], pythia.event.size()):
        prt = pythia.event[j]
        if prt.isFinal():
            prt_eta = prt.eta()
            prt_phi = prt.phi()
            prt_pT = prt.pT()
            prt_eT = prt.eT()
            if j in totJetPrtList:
                tjet_eta.append(prt_eta)
                tjet_phi.append(prt_phi)
                tjet_pT.append(prt_pT)
                tjet_eT.append(prt_eT)
            else:
                tbg_eta.append(prt_eta)
                tbg_phi.append(prt_phi)
                tbg_pT.append(prt_pT)
                tbg_eT.append(prt_eT)
        
#   Create bins using np.histogram2d(), the number of bins produced is the square of the value "b"
    b = 20
    tot_bins = b**2

#   Data from trento background is binned
    tbg_h, xedges, yedges = np.histogram2d(tbg_eta,tbg_phi,bins=b,range=[[-2,2], [-(np.pi), np.pi]],weights=tbg_eT)
    tbg_h = np.concatenate(tbg_h)

#   Data from trento particles identified as jets is binned    
    tjet_h, tjet_xedges, tjet_yedges = np.histogram2d(tjet_eta,tjet_phi,bins=[xedges,yedges],weights=tjet_eT)
    tjet_h = np.concatenate(tjet_h)

#   Data from pythia background is binned
    pbg_h, pbg_xedges, pbg_yedges = np.histogram2d(pbg_eta,pbg_phi,bins=[xedges,yedges],weights=pbg_eT)
    pbg_h = np.concatenate(pbg_h)

#   Data from pythia particles identified as jets is binned
    pjet_h, pjet_xedges, pjet_yedges = np.histogram2d(pjet_eta,pjet_phi,bins=[xedges,yedges],weights=pjet_eT)
    pjet_h = np.concatenate(pjet_h)

#   x and y coordinates for bincenters are created using bin edges
    xcenters = 0.5*(xedges[1:]+xedges[:-1])
    xcenters = np.repeat(xcenters,b)
    ycenters = 0.5*(yedges[1:]+yedges[:-1])
    ycenters = np.tile(ycenters,b)

#   arrays of bin centers are extended to match the length of the data sets
    xcenters = list(xcenters)
    ycenters = list(ycenters)
    xcenters.extend(xcenters)
    ycenters.extend(ycenters)
    xcenters.extend(xcenters)
    ycenters.extend(ycenters)
        
#   Bars associated with jets will sit on top of bars associated with background
#   the order bars will be stacked is trento bg, pythia bg, trento jet, pythia jet     

#   the base for trento bg will be all zeroes
    tbg_base = np.zeros(len(tjet_h))
    tbg_base = list(tbg_base)

#   the base for pythia bg will be the top of the trento bg
    pbg_base = tbg_h
    pbg_base = list(pbg_base)
    tbg_base.extend(pbg_base)
    pbg_base = np.array(pbg_base)

#   the base for trento jets will be the top of trento bg and pythia bg
    tjet_base = pbg_base + pbg_h
    tjet_base = list(tjet_base)
    tbg_base.extend(tjet_base)
    tjet_base = np.array(tjet_base)

#   the base for pythia jets will be on top of trento bg, pythia bg, and trento jets
    pjet_base = tjet_base + tjet_h
    pjet_base = list(pjet_base)
    tbg_base.extend(pjet_base)

    base = tbg_base
        
    tbg_h = list(tbg_h)
    pbg_h = list(pbg_h)
    tjet_h = list(tjet_h)
    pjet_h = list(pjet_h)
    tbg_h.extend(pbg_h)
    tbg_h.extend(tjet_h)
    tbg_h.extend(pjet_h)

    h = tbg_h
        
#   Set size of bars in plot
    d_eta = (xedges[1]-xedges[0])
    d_phi = (yedges[1]-yedges[0])

#   Create an array of colors where bars associated with jet particles are red
#   Background bars are blue and bars with no value are white
    jet_colors=[]
    
    tbg_col = 'skyblue'
    pbg_col = 'blue'
    tjet_col = 'yellow'
    pjet_col = 'red'
    
    for j in h[0:tot_bins]:
        if j > 0:
            jet_colors.append(tbg_col)
        else:
            jet_colors.append('w')
    for j in range(len(pbg_h)):
        if pbg_h[j] > 0:
            jet_colors.append(pbg_col)
        elif h[j] > 0:
            jet_colors.append(tbg_col)
        else:
            jet_colors.append('w')
    for j in range(len(tjet_h)):
        if tjet_h[j] > 0:
            jet_colors.append(tjet_col)
        elif pbg_h[j] > 0:
            jet_colors.append(pbg_col)
        elif h[j] > 0:
            jet_colors.append(tbg_col)
        else:
            jet_colors.append('w')
    for j in range(len(pjet_h)):
        if pjet_h[j] > 0:
            jet_colors.append(pjet_col)
        elif tjet_h[j] > 0:
            jet_colors.append(tjet_col)
        elif pbg_h[j] > 0:
            jet_colors.append(pbg_col)
        elif h[j] > 0:
            jet_colors.append(tbg_col)
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

#    for i in range(slowJet.sizeJet()):
#        pT_jet = slowJet.pT(i)
#        pT_label = 'slowJet pT = %.2f' % pT_jet
#        ax.text(slowJet.y(i),slowJet.phi(i),max(h)+0.1,pT_label,horizontalalignment='center')

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

    
