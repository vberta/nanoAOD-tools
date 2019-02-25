import os
import copy
import math

# corrected = Rochester
muon = '_corrected'

# nom = MET w/ jet smearing
met = '_nom'

selections = {

    'W' : {
        'mc' : {
            'cut': 'Vtype==0 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Muon_idx1]>25. && ' % muon) \
                #('Muon%s_MET%s_mt[Muon_idx1]>40.' % (muon, met)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : 'TMath::Abs(LHEWeight_originalXWGTUP)/LHEWeight_originalXWGTUP*' \
                'puWeight*' \
                'Muon_effSF[Muon_idx1]',
            },
        'data' : {
            'cut': 'Vtype==0 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Muon_idx1]>25. && ' % muon_pt) \
                #('Muon%s_MET%s_mt[Muon_idx1]>40. ' % (muon, met)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : '',
            },
        },

    'Fake' : {
        'mc' : {
            'cut': 'Vtype==1 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Muon_idx1]>25. && ' % muon_pt) \
                #('Muon%s_MET%s_mt[Muon_idx1]<40. ' % (muon, met)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : 'TMath::Abs(LHEWeight_originalXWGTUP)/LHEWeight_originalXWGTUP*' \
                'puWeight*' \
                'Muon_effSF[Muon_idx1]',
            },
        'data' : {
            'cut': 'Vtype==0 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Muon_idx1]>25. && ' % muon_pt) \
                #('Muon%s_MET%s_mt[Muon_idx1]<40.' % (muon, met)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : '',
            },
        },

    'Z' : {
        'mc' : {
            'cut': 'Vtype==2 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Muon_idx1]>25. && Muon_pt%s[Muon_idx2]>20.' % (muon_pt, muon_pt)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : 'TMath::Abs(LHEWeight_originalXWGTUP)/LHEWeight_originalXWGTUP*' \
                'puWeight*' \
                'Muon_effSF[Muon_idx1]*Muon_effSF[Muon_idx2]',
            },
        'data' : {
            'cut': 'Vtype==2 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Muon_idx1]>25. && Muon_pt%s[Muon_idx2]>20.' % (muon_pt, muon_pt)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : '',
            },
        },
    }

selections['Wplus'] = copy.deepcopy(selections['W'])
selections['Wminus'] = copy.deepcopy(selections['W'])
selections['Wplus']['mc']['cut']  += ' && Muon_charge[Muon_idx1]>0'
selections['Wminus']['mc']['cut'] += ' && Muon_charge[Muon_idx1]<0'

selections['Fakeplus'] = copy.deepcopy(selections['Fake'])
selections['Fakeminus'] = copy.deepcopy(selections['Fake'])
selections['Fakeplus']['mc']['cut']  += ' && Muon_charge[Muon_idx1]>0'
selections['Fakeminus']['mc']['cut'] += ' && Muon_charge[Muon_idx1]<0'


def HistoDict(self,name_,title_,Nbin_,min_,max_):
    self.dictOut = {
    'name' : name_,
    'title' : title_,
    'Nbin' : Nbin_,
    'min' : min_,
    'max' : max_
    }
    return self.dictOut

variables =  {
    # 'W' : [ 'pt' : {
    #             'name' : "P_T [GeV]"
    #             'Nbin' : 100,
    #             'min' : 0
    #             'max' : 100
    #             }
    'W' : [
        'Muon_pt' : HistoDict(('Muon%s_pt[Muon_idx1]' % muon),"$P_T$ [GeV]",100,1,-1), #TEMPORARY
        'Muon_eta' : HistoDict(('Muon%s_eta[Muon_idx1]' % muon),"$\eta$",100,1,-1), #TEMPORARY
        'Muon_phi' : HistoDict(('Muon%s_phi[Muon_idx1]' % muon),"$\phi$",100,-math.pi,math.pi),
        'Muon_pfRelIso04' : HistoDict(('Muon%s_pfRelIso04_all[Muon_idx1]' % muon),"relIso ",100,1,-1), #TEMPORARY
        'Muon_dxy' : HistoDict(('Muon%s_dxy[Muon_idx1]' % muon),,"$d_{xy}$ [cm]",100,1,-1),#TEMPORARY
        'dz' : HistoDict(('Muon%s_dz[Muon_idx1]' % muon),"$d_z$ [cm]",100,1,-1),#TEMPORARY
        'Muon_MET_mt' : HistoDict(('Muon%s_MET%s_mt[Muon_idx1]' % (muon, met)),"$M_T$ [GeV]",100,1,-1), #TEMPORARY
        'Muon_MET_h_pt' : HistoDict(('Muon%s_MET%s_h_pt[Muon_idx1]' % (muon, met)),"$P_T$ [GeV]",100,1,-1), #TEMPORARY
        'GenMuon_bare_GenMET_mt' : HistoDict(('GenMuon_bare_GenMET_mt[Muon_idx1]'),"P_T [GeV]",100,1,-1), #TEMPORARY
        'GenMuon_bare_GenMET_h_pt' : HistoDict(('GenMuon_bare_GenMET_h_pt[Muon_idx1]'),"P_T [GeV]",100,1,-1), #TEMPORARY
        'MET_pt' : HistoDict(('MET%s_pt' % met),"P_T [GeV]",100,1,-1), #TEMPORARY
        'Muon_MET_uPar' : HistoDict(('Muon_MET%s_uPar' % met),"P_T [GeV]",100,1,-1), #TEMPORARY
        'Muon_MET_uPer' : HistoDict(('Muon_MET%s_uPer' % met),"P_T [GeV]",100,1,-1), #TEMPORARY
        'PV_npvsGood' : HistoDict('PV_npvsGood',"N",100,1,-1), #TEMPORARY
    ],

    'Z' : [
        'Muon_pt_1' : HistoDict(('Muon%s_pt[Muon_idx1]' % muon),"$P_T$ [GeV]",100,1,-1), #TEMPORARY
        'Muon_eta_1' : HistoDict(('Muon%s_eta[Muon_idx1]' % muon),"$\eta$",100,1,-1), #TEMPORARY
        'Muon_phi_1' : HistoDict(('Muon%s_phi[Muon_idx1]' % muon),"$\phi$",100,-math.pi,math.pi),
        'Muon_pfRelIso04_1' : HistoDict(('Muon%s_pfRelIso04_all[Muon_idx1]' % muon),"relIso ",100,1,-1), #TEMPORARY
        'Muon_dxy_1' : HistoDict(('Muon%s_dxy[Muon_idx1]' % muon),,"$d_{xy}$ [cm]",100,1,-1),#TEMPORARY
        'dz_1' : HistoDict(('Muon%s_dz[Muon_idx1]' % muon),"$d_z$ [cm]",100,1,-1),#TEMPORARY
        'Muon_pt_2' : HistoDict(('Muon%s_pt[Muon_idx2]' % muon),"$P_T$ [GeV]",100,1,-1), #TEMPORARY
        'Muon_eta_2' : HistoDict(('Muon%s_eta[Muon_idx2]' % muon),"$\eta$",100,1,-1), #TEMPORARY
        'Muon_phi_2' : HistoDict(('Muon%s_phi[Muon_idx2]' % muon),"$\phi$",100,-math.pi,math.pi),
        'Muon_pfRelIso04_2' : HistoDict(('Muon%s_pfRelIso04_all[Muon_idx2]' % muon),"relIso ",100,1,-1), #TEMPORARY
        'Muon_dxy_2' : HistoDict(('Muon%s_dxy[Muon_idx2]' % muon),,"$d_{xy}$ [cm]",100,1,-1),#TEMPORARY
        'dz_2' : HistoDict(('Muon%s_dz[Muon_idx2]' % muon),"$d_z$ [cm]",100,1,-1),#TEMPORARY
        'RecoZ_mass': HistoDict(('RecoZ%s_mass' % muon),"M [GeV]",100,1,-1) #TEMPORARY
        'RecoZ_y': HistoDict(('RecoZ%s_y' % muon),"y",100,1,-1) #TEMPORARY
        'RecoZ_pt': HistoDict(('RecoZ%s_pt' % muon),"P_T [GeV]",100,1,-1) #TEMPORARY
        'RecoZ_CStheta': HistoDict(('RecoZ%s_CStheta' % muon),"$\theta$",100,-math.pi,math.pi)
        'RecoZ_CSphi': HistoDict(('RecoZ%s_CSphi' % muon),"$\phi$",100,-math.pi,math.pi)
        'GenZ_mass' : HistoDict(('GenZ%s_mass' % muon),"M [GeV]",100,1,-1) #TEMPORARY
        'GenZ_y': HistoDict(('GenZ%s_y' % muon),"y",100,1,-1) #TEMPORARY
        'GenZ_pt' : HistoDict(('GenZ%s_pt' % muon),"P_T [GeV]",100,1,-1) #TEMPORARY
        'GenZ_CStheta' : HistoDict(('GenZ%s_CStheta' % muon),"$\theta$",100,-math.pi,math.pi) #TEMPORARY
        'GenZ_CSphi'  : HistoDict(('GenZ%s_CSphi' % muon),"$\phi$",100,-math.pi,math.pi) #TEMPORARY
        'RecoZ_MET_uPar' : HistoDict(('RecoZ_MET%s_uPar' % met),"P_T [GeV]",100,1,-1), #TEMPORARY
        'RecoZ_MET_uPer' : HistoDict(('RecoZ_MET%s_uPer' % met),"P_T [GeV]",100,1,-1), #TEMPORARY
        'PV_npvsGood' : HistoDict('PV_npvsGood',"N",100,1,-1), #TEMPORARY

    ],
}
variables['Fake'] = copy.deepcopy(variables['W'])
