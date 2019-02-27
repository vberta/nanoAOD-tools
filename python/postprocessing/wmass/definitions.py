import os
import copy
import math

# corrected = Rochester
# muon = 'corrected_'
muon = ''

# nom = MET w/ jet smearing
met = '_nom'

selections = {

    'W' : {
        'mc' : {
            'cut': 'Vtype==0 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Idx_mu1]>25. && ' % muon) \
                #('Muon%s_MET%s_mt[Idx_mu1]>40.' % (muon, met)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : 'TMath::Abs(LHEWeight_originalXWGTUP)/LHEWeight_originalXWGTUP*' \
                'puWeight*' \
                'Muon_effSF[Idx_mu1]',
            },
        'data' : {
            'cut': 'Vtype==0 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Idx_mu1]>25. && ' % muon_pt) \
                #('Muon%s_MET%s_mt[Idx_mu1]>40. ' % (muon, met)) \
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
                #('Muon_pt%s[Idx_mu1]>25. && ' % muon_pt) \
                #('Muon%s_MET%s_mt[Idx_mu1]<40. ' % (muon, met)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : 'TMath::Abs(LHEWeight_originalXWGTUP)/LHEWeight_originalXWGTUP*' \
                'puWeight*' \
                'Muon_effSF[Idx_mu1]',
            },
        'data' : {
            'cut': 'Vtype==0 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Idx_mu1]>25. && ' % muon_pt) \
                #('Muon%s_MET%s_mt[Idx_mu1]<40.' % (muon, met)) \
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
                #('Muon_pt%s[Idx_mu1]>25. && Muon_pt%s[Idx_mu2]>20.' % (muon_pt, muon_pt)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : 'TMath::Abs(LHEWeight_originalXWGTUP)/LHEWeight_originalXWGTUP*' \
                'puWeight*' \
                'Muon_effSF[Idx_mu1]*Muon_effSF[Idx_mu2]',
            },
        'data' : {
            'cut': 'Vtype==2 && ' \
                #'Muon_HLT && ' \
                #('Muon_pt%s[Idx_mu1]>25. && Muon_pt%s[Idx_mu2]>20.' % (muon_pt, muon_pt)) \
                #'MET_filters==1 && ' \
                #'nVetoElectrons==0 && ', \
                '1',
            'weight' : '',
            },
        },
    }

selections['Wplus'] = copy.deepcopy(selections['W'])
selections['Wminus'] = copy.deepcopy(selections['W'])
selections['Wplus']['mc']['cut']  += ' && Muon_charge[Idx_mu1]>0'
selections['Wminus']['mc']['cut'] += ' && Muon_charge[Idx_mu1]<0'

selections['Fakeplus'] = copy.deepcopy(selections['Fake'])
selections['Fakeminus'] = copy.deepcopy(selections['Fake'])
selections['Fakeplus']['mc']['cut']  += ' && Muon_charge[Idx_mu1]>0'
selections['Fakeminus']['mc']['cut'] += ' && Muon_charge[Idx_mu1]<0'


def HistoDict(name_,title_,Nbin_,min_,max_):
    dictOut = {
    'name' : name_,
    'title' : title_,
    'Nbin' : Nbin_,
    'min' : min_,
    'max' : max_
    }
    return dictOut

variables =  {
    # 'W' : [ 'pt' : {
    #             'name' : "P_T [GeV]"
    #             'Nbin' : 100,
    #             'min' : 0
    #             'max' : 100
    #             }
    'W' : {
        'Muon_pt' : HistoDict(('Muon%s_pt[Idx_mu1]' % muon),"$P_{T}$ [GeV]",100,0,200), #TEMPORARY
        'Muon_eta' : HistoDict(('Muon%s_eta[Idx_mu1]' % muon),"$\eta$",100,-4,4), #TEMPORARY
        'Muon_phi' : HistoDict(('Muon%s_phi[Idx_mu1]' % muon),"$\phi$",100,-math.pi,math.pi),
        'Muon_pfRelIso04' : HistoDict(('Muon%s_pfRelIso04_all[Idx_mu1]' % muon),"relIso ",100,0,0.4), #TEMPORARY
        'Muon_dxy' : HistoDict(('Muon%s_dxy[Idx_mu1]' % muon),"d_{xy} [cm]",100,-0.01,0.01),#TEMPORARY
        'dz' : HistoDict(('Muon%s_dz[Idx_mu1]' % muon),"$d_z$ [cm]",100,-0.1,0.1),#TEMPORARY
        'Muon_MET_mt' : HistoDict(('Muon%s_MET%s_mt[Idx_mu1]' % (muon, met)),"$M_{T}$ [GeV]",100,0,200), #TEMPORARY
        'Muon_MET_h_pt' : HistoDict(('Muon%s_MET%s_h_pt[Idx_mu1]' % (muon, met)),"$P_{T}$ [GeV]",100,0,200), #TEMPORARY
        'GenMuon_bare_GenMET_mt' : HistoDict(('GenMuon_bare_GenMET_mt[Idx_mu1]'),"P_{T} [GeV]",100,0,200), #TEMPORARY
        'GenMuon_bare_GenMET_h_pt' : HistoDict(('GenMuon_bare_GenMET_h_pt[Idx_mu1]'),"P_{T} [GeV]",100,0,200), #TEMPORARY
        'MET_pt' : HistoDict(('MET%s_pt' % met),"P_{T} [GeV]",100,0,200), #TEMPORARY
        'Muon_MET_uPar' : HistoDict(('Muon_MET%s_uPar' % met),"P_{T} [GeV]",100,-200,200), #TEMPORARY
        'Muon_MET_uPer' : HistoDict(('Muon_MET%s_uPer' % met),"P_{T} [GeV]",100,-200,200), #TEMPORARY
        'PV_npvsGood' : HistoDict('PV_npvsGood',"N",100,0,100), #TEMPORARY
    },

    'Z' : {
        'Muon_pt_1' : HistoDict(('Muon%s_pt[Idx_mu1]' % muon),"$P_{T}$ [GeV]",100,0,200), #TEMPORARY
        'Muon_eta_1' : HistoDict(('Muon%s_eta[Idx_mu1]' % muon),"$\eta$",100,-4,4), #TEMPORARY
        'Muon_phi_1' : HistoDict(('Muon%s_phi[Idx_mu1]' % muon),"$\phi$",100,-math.pi,math.pi),
        'Muon_pfRelIso04_1' : HistoDict(('Muon%s_pfRelIso04_all[Idx_mu1]' % muon),"relIso ",100,0,0.4), #TEMPORARY
        'Muon_dxy_1' : HistoDict(('Muon%s_dxy[Idx_mu1]' % muon),"d_{xy} [cm]",100,-0.01,0.01),#TEMPORARY
        'dz_1' : HistoDict(('Muon%s_dz[Idx_mu1]' % muon),"$d_z$ [cm]",100,-0.1,0.1),#TEMPORARY
        'Muon_pt_2' : HistoDict(('Muon%s_pt[Idx_mu2]' % muon),"$P_{T}$ [GeV]",100,0,200), #TEMPORARY
        'Muon_eta_2' : HistoDict(('Muon%s_eta[Idx_mu2]' % muon),"$\eta$",100,-4,4), #TEMPORARY
        'Muon_phi_2' : HistoDict(('Muon%s_phi[Idx_mu2]' % muon),"$\phi$",100,-math.pi,math.pi),
        'Muon_pfRelIso04_2' : HistoDict(('Muon%s_pfRelIso04_all[Idx_mu2]' % muon),"relIso ",100,0,0.4), #TEMPORARY
        'Muon_dxy_2' : HistoDict(('Muon%s_dxy[Idx_mu2]' % muon),"d_{xy} [cm]",100,-0.01,0.01),#TEMPORARY
        'dz_2' : HistoDict(('Muon%s_dz[Idx_mu2]' % muon),"$d_z$ [cm]",100,-0.1,0.1),#TEMPORARY
        'RecoZ_mass': HistoDict(('RecoZ%s_mass' % muon),"M [GeV]",100,0,200), #TEMPORARY
        'RecoZ_y': HistoDict(('RecoZ%s_y' % muon),"y",100,-10,10), #TEMPORARY
        'RecoZ_pt': HistoDict(('RecoZ%s_pt' % muon),"P_{T} [GeV]",100,0,200), #TEMPORARY
        'RecoZ_CStheta': HistoDict(('RecoZ%s_CStheta' % muon),"$\Theta$",100,-math.pi,math.pi),
        'RecoZ_CSphi': HistoDict(('RecoZ%s_CSphi' % muon),"$\phi$",100,0,2*math.pi),
        'GenZ_mass' : HistoDict(('GenZ%s_mass' % muon),"M [GeV]",100,0,200), #TEMPORARY
        'GenZ_y': HistoDict(('GenZ%s_y' % muon),"y",100,-200,200), #TEMPORARY
        'GenZ_pt' : HistoDict(('GenZ%s_pt' % muon),"P_{T} [GeV]",100,-200,200), #TEMPORARY
        'GenZ_CStheta' : HistoDict(('GenZ%s_CStheta' % muon),"$\Theta$",100,-math.pi,math.pi), #TEMPORARY
        'GenZ_CSphi'  : HistoDict(('GenZ%s_CSphi' % muon),"$\phi$",100,0,2*math.pi), #TEMPORARY
        'RecoZ_MET_uPar' : HistoDict(('RecoZ_MET%s_uPar' % met),"P_{T} [GeV]",100,-200,200), #TEMPORARY
        'RecoZ_MET_uPer' : HistoDict(('RecoZ_MET%s_uPer' % met),"P_{T} [GeV]",100,-200,200), #TEMPORARY
        'PV_npvsGood' : HistoDict('PV_npvsGood',"N",100,0,100), #TEMPORARY

    },
}
variables['Fake'] = copy.deepcopy(variables['W'])
