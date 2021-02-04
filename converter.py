import ROOT

from samples import *
from variables import *

nEvents_max = -1
nVariables = set()

print("argv = ", argv)
filename, sampleName, index = argv                     # "vbfHmm_powheg", "DYToLL_madgraphMLM"
index = int(index, 10)

InvariantMass_code ='''
float InvariantMass (float pt1, float eta1, float phi1, float mass1, float pt2, float eta2, float phi2, float mass2)
{
   TLorentzVector mu1, mu2;
   mu1.SetPtEtaPhiM( pt1, eta1, phi1, mass1);
   mu2.SetPtEtaPhiM( pt2, eta2, phi2, mass2);
   float mass = (mu1+mu2).M();
   return mass;
}
'''

print("Running sample: %s"%sampleName)

for dataset_ in samples[sampleName]:
    dataset = dataset_%index
    print("Running dataset: %s"%dataset)
    df = ROOT.RDataFrame("Delphes", dataset)

    if nEvents_max>0:
        print("I'm running on %d events"%nEvents_max)
        df = df.Range(0, nEvents_max)

    df_out = df.Define("sum_size", "MuonTight_size+Jet_size")

for oldVariable in newVariables:
    df_out = df_out.Define(newVariables[oldVariable], oldVariable)
    nVariables.add(newVariables[oldVariable])	

    ## Define DiMuon mass ##
ROOT.gInterpreter.Declare(InvariantMass_code) ## compile invariant mass code
df_out = df_out.Define("DiMuon_mass", "InvariantMass( MuonTight_pt[0], MuonTight_eta[0], MuonTight_phi[0], 0.106,  MuonTight_pt[1], MuonTight_eta[1], MuonTight_phi[1], 0.106)") ## define DiMuon_mass variable (0.106 GeV is the muon mass)
    ###
df_out = df_out.Define("DiJet_mass", "InvariantMass( Jet_pt[0], Jet_eta[0], Jet_phi[0], Jet_mass[0],  Jet_pt[1], Jet_eta[1], Jet_phi[1], Jet_mass[1] )")


counter = df_out.Histo1D(("processedEvents", "processedEvents", 1, -100000,100000), "MuonTight_size")

    ## Cuts ##
df_out = df_out.Filter("MuonTight_size >= 2") #require at least two muon
counter_1 = df_out.Histo1D(("filteredEvents", "filteredEvents", 1, -100000,100000), "MuonTight_size")
 
df_out = df_out.Filter("MuonTight_pt[0] > 20 && MuonTight_pt[1] > 20")
df_out = df_out.Filter("abs(MuonTight_eta[0]) < 2.8 && abs(MuonTight_eta[1]) < 2.8") #require the first muon to have pt>50 GeV
df_out = df_out.Filter("DiMuon_mass > 110 && DiMuon_mass < 150") #require at least two muon

    #df_out = df_out.Filter("Jet_size >= 2")
df_out = df_out.Filter("Jet_pt[0] > 35 && Jet_pt[1] > 25")
df_out = df_out.Filter("abs(Jet_eta[0]) < 4.7 && abs(Jet_eta[1]) < 4.7")
df_out = df_out.Filter("abs(Jet_eta[0] - Jet_eta[1]) < 2.5 ")
df_out = df_out.Filter("DiJet_mass > 400")

hist = df_out.Histo1D("MuonTight_pt")
print("Launch Snapshot")
df_out.Snapshot("Events", "%s_%d.root"%(sampleName, index), nVariables)

file = ROOT.TFile("%s_%d.root"%(sampleName, index),"update")
counter.Write()
counter_1.Write()
file.Close()


print("Finished dataset %s"%dataset)
print("Finished sample %s"%sampleName)
