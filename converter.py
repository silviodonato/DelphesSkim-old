import ROOT

sampleName = "vbfHmm_powheg"

index = 0
#for i in range(0, 38):
#    print(i)
	
	
samples = {"vbfHmm_powheg":
"root://eoscms.cern.ch//store/group/upgrade/delphes_output/YR_Delphes/Delphes342pre14/VBFHToMuMu_M125_14TeV_powheg_pythia8_200PU/VBFHToMuMu_M125_14TeV_powheg_pythia8_*%d.root"%index
}


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

mqq_code ='''
float mqq (float pt1, float eta1, float phi1, float mass1, float pt2, float eta2, float phi2, float mass2)
{
        TLorentzVector j1, j2;
        j1.SetPtEtaPhiM( pt1, eta1, phi1, mass1);
        j2.SetPtEtaPhiM( pt2, eta2, phi2, mass2);
        float mass = (j1+j2).M();
        return mass;
}
'''
########################

df = ROOT.RDataFrame("Delphes", samples[sampleName])

#sum = df.Filter("MuonTight_size > 0").Sum("Jet_size")
#print(sum.GetValue())

df_out = df.Define("sum_size", "MuonTight_size+Jet_size")


df_out = df_out.Define("MuonTight_pt", "MuonTight.PT")
df_out = df_out.Define("MuonTight_eta", "MuonTight.Eta")
df_out = df_out.Define("MuonTight_phi", "MuonTight.Phi")
df_out = df_out.Define("MuonTight_t", "MuonTight.T")
df_out = df_out.Define("MuonTight_charge", "MuonTight.Charge")
#df_out = df_out.Define("MuonTight_particle", "MuonTight.Particle")
df_out = df_out.Define("MuonTight_isolationvar", "MuonTight.IsolationVar")
df_out = df_out.Define("MuonTight_isolationvarrhocorr", "MuonTight.IsolationVarRhoCorr")
df_out = df_out.Define("MuonTight_sumptcharged", "MuonTight.SumPtCharged")
df_out = df_out.Define("MuonTight_sumptneutral", "MuonTight.SumPtNeutral")
df_out = df_out.Define("MuonTight_sumptchargedPU", "MuonTight.SumPtChargedPU")
df_out = df_out.Define("MuonTight_sumpt", "MuonTight.SumPt")

df_out = df_out.Define("Jet_pt", "Jet.PT")
df_out = df_out.Define("Jet_eta", "Jet.Eta")
df_out = df_out.Define("Jet_phi", "Jet.Phi")
df_out = df_out.Define("Jet_mass", "Jet.Mass")


## Define DiMuon mass ##
ROOT.gInterpreter.Declare(InvariantMass_code) ## compile invariant mass code
df_out = df_out.Define("DiMuon_mass", "InvariantMass( MuonTight_pt[0], MuonTight_eta[0], MuonTight_phi[0], 0.106,  MuonTight_pt[1], MuonTight_eta[1], MuonTight_phi[1], 0.106)") ## define DiMuon_mass variable (0.106 GeV is the muon mass)
###

ROOT.gInterpreter.Declare(mqq_code) ## compile invariant mass code
df_out = df_out.Define("DiJet_mass", "mqq( Jet_pt[0], Jet_eta[0], Jet_phi[0], Jet_mass[0],  Jet_pt[1], Jet_eta[1], Jet_phi[1], Jet_mass[1] )")


## Cuts ##
df_out = df_out.Filter("MuonTight_size >= 2") #require at least two muon
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

df_out.Snapshot("Events", "%s_%d.root"%(sampleName, index), {'MuonTight_pt', 'MuonTight_eta', 'MuonTight_phi', 'MuonTight_t', 'MuonTight_charge', 'MuonTight_isolationvar', 'MuonTight_isolationvarrhocorr', 'MuonTight_sumptcharged', 'MuonTight_sumptneutral', 'MuonTight_sumptchargedPU', 'MuonTight_sumpt', 'Jet_pt', 'Jet_eta', 'Jet_phi', 'Jet_mass','DiMuon_mass', 'DiJet_mass'});

print("Finished")
