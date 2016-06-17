
2d_pythia_slowjet.py:
   -displays Pythia events and colors particles identified as jets by SlowJet red

2d_pythia_slowjet_truejet.py:
   -displays Pythia events and tests to see which particles are part of true jets

2d_pythia_trento_slowjet.py:	
   -displays Pythia events with trento background. SlowJet is called and jets are colored

2d_pythia_trento_slowjet_truejet.py	
   -displays Pythia events with trento background. SlowJet is tested against true jets.

2d_trento.py:							
   -displays trento background with flow and scaled multiplicity to PHENIX data

2d_trento_slowjet.py						
   -displays trento background (no jets) with SlowJet called, identified jets are colored red

3d_pythia_slowjet.py						
   -displays Pythia events showing each particle individually, SlowJet jets are red

phenix_data.py				
   -phenix data plotted with errorbars for various energies of Au Au collisions
   -charged multiplicity vs. number of participants

phenix_trento_comp.py
   -fits trento data to phenix data for various energies of Au Au collisions. Errorbar plot

pythia_mult_process.py
   -creates a histogram showing the frequency of different charged multiplicities for pythia QCD/QED events

pythia_pT_process.py:
   -creates a histogram for pT of pythia QED/QCD hard processes 

pythia_scanEvent.py
   -example program that prints which hard process took place for each pythia event

scanPythia.py
   -prints slowJet information about pythia events such as jet constituents and jet pT

slowJetpT_vs_pTHat.py
   -compares the jet pT produced by pythia QCD/QED events to the calculated jet pT found by slowJet

slowjet_pTmin_radius.py
   -creates a 2d histogram showing how many jets slowJet finds for different values of radius and pTjetMin

slowjet_pTrange_radius.py
   -Tests various values of SlowJet radius while the Pythia jets are in a restricted pT range

test_addflow.py:
   -example program showing how to add flow to the background particles produced from trento data

test_getopt.py
   -example program showing how to add options to python programs

test_mixed_colors.py
   -example program showing what happens when different colors of bars are overlayed in mpl_toolkits.mplot3d

trento_mult_npart.py
   -Plots initial entropy (mult) vs. number of participants (Npart) for trento data

trento_phi_pT_eta.py
   -Plots the values of phi, pT, and eta that are created for the trento backgrounds

trento_plot_values.py
   -creates plots with trento data for the following:
      -Npart vs. impact parameter
      -mult vs. impact parameter
      -mult vs. Npart
      -e2 vs. Npart
      -e3 vs. Npart

xi_slowjet.py
   -creates a histogram of xi values for SlowJet jets

xi_slowjet_truejet.py
   -compares xi for true and reconstructed jets

xi_truejet.py
   -creates a histogram of xi values for true jets
