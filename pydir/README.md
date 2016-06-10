
2d_hist_jetplot_wcol.py
 -creates a 2d histogram from pythia data
     -the x and y axes of the histogram are pseudorapidity and azimuthal angle phi
     -the bars of the histogram are weighted by eT
 -slowJet is called within the program
     -bars from particles identified as jets are colored red
     -all other particles are colored blue
 -command line options shown with -h

addflow.py
 -example program showing how to add flow to the background particles produced from trento data

pT_QEDevents.py
 -creates a histogram showing the frequency of different measurements of pT for pythia QED processes 

slowJetpT_vs_pTHatQED.py
 -compares the jet pT produced by pythia QED events to the calculated jet pT found by slowJet
 -command line options shown with -h

2d_hist_trento.py
 -creates a 2d histogram from 200 GeV Au Au trento data
     -the x and y axes of the histogram are pseudorapidity and azimuthal angle phi
     -the bars of the histogram are weighted by pT
 -e2 flow is considered
- command line options shown with -h	 

getopt_sample.py
 -example program showing how to add options to python programs

phenix_data.py
 -phenix data plotted with errorbars for various energies of Au Au collisions
 -x axis is number of participants, y axis is charged multiplicity

pythia_scanEvent.py
 -example program that prints which hard process took place for each pythia event

slowjet_trento_hist.py
 -creates a 2d histogram from 200 GeV Au Au trento data
     -the x and y axes of the histogram are pseudorapidity and azimuthal angle phi
     -the bars of the histogram are weighted by pT
 -e2 flow is considered
 -slowJet is called within the program
     -number of jets found by slowJet is listed
     -bars from particles identified as jets are colored red
     -all others are colored blue

3d_jetplot_2016.py
 -creates a 2d bar plot from pythia data
     -the x and y axes of the histogram are pseudorapidity and azimuthal angle phi
     -the bars of the histogram are weighted by eT
	 -each particle has is represented by a bar
 -slowJet is called within the program
     -bars from particles identified as jets are colored red
     -all other particles are colored blue
 -command line options shown with -h

mixedcolors_example.py
 -example program showing what happens when different colors of bars are overlayed in mpl_toolkits.mplot3d

phenix_trento_comp.py
 -fits trento data to phenix data for various energies of Au Au collisions
 -fit parameters for each energy are returned
 -an errorbar plot is produced showing how well trento matches phenix data

pythia_slowjet_trento_hist.py
 -creates a 2d histogram from both trento and pythia data
     -the x and y axes of the histogram are pseudorapidity and azimuthal angle phi
     -the bars of the histogram are weighted by eT
 -slowJet is called within the program
     -bars from pythia particles identified as jets are colored red
     -bars from trento particles identified as jets are colored yellow
     -other trento particles are lightblue and other pythia particles are blue
 -command line options shown with -h
      -pythia or trento data can be turned off
      -QED processes can be enabled
	  -various slowJet and pythia settings can be changed

xi_reconstructed_jets.py
 -creates a histogram of xi values for both trento and pythia data
 -jets are reconstructed using slowJet
 -command line options shown with -h

xi_true_jets.py
 -test program that creates a histogram of xi values for pythia jets
 -program is incomplete

trento_in_python.py
 -creates plots with trento data for the following:
     -Npart vs. impact parameter
     -mult vs. impact parameter
     -mult vs. Npart
     -e2 vs. Npart
     -e3 vs. Npart

nCh_QED.py
 -creates a histogram showing the frequency of different charged multiplicities for pythia QED processes

phi_pT_eta_trento.py
 -using multiplicities from trento data, randomly creates values for phi, pT, and eta
 -three histograms are produced showing the results

restricted_jetpT.py
 -pythia pTHat is restricted between the values of 20-25 GeV/c
 -a histogram is produced showing the frequency of calculated jet pT from slowJet
 -different values of radius for slowJet initialization are shown

Npart_bins.py
 -creates a histogram for trento data showing Npart vs multiplicity

nCh_mult_events.py
 -creates a histogram showing the frequency of different charged multiplicities for pythia QCD processes

pythia_pTjet.py
 -creates a histogram showing the frequency of different measurements of pT for pythia QCD processes

scanPythia.py
 -prints slowJet information about pythia events such as jet constituents and jet pT

optimize_slowjet.py
 -creates a 2d histogram showing how many jets slowJet finds for different values of radius and pTjetMin
 -both pythia and trento data are analyzed by slowJet

pythia_pyplot.py
 -creates a histogram showing the frequency of different charged multiplicities for pythia events

slowJetpT_vs_pTHat.py
 -compares the jet pT produced by pythia QCD events to the calculated jet pT found by slowJet
 -command line options shown with -h
