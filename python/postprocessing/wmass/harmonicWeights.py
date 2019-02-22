import ROOT
import math
import numpy as np 
import os
import pickle

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

np_bins_qt_p0 = np.linspace( 0.0, 10.0, 6)
np_bins_qt_p1 = np.linspace(12.0, 20.0, 5)
np_bins_qt_p2 = np.linspace(24.0, 40.0, 5)
np_bins_qt_p3 = np.array([60, 80, 100, 150, 200]) 
np_bins_qt = np.append( np.append(np_bins_qt_p0, np_bins_qt_p1), np.append( np_bins_qt_p2, np_bins_qt_p3))
np_bins_qt_width = np.array( [np_bins_qt[i+1]-np_bins_qt[i] for i in range(np_bins_qt.size-1)] )
np_bins_qt_mid  = np.array( [(np_bins_qt[i+1]+np_bins_qt[i])*0.5 for i in range(np_bins_qt.size-1)] )

np_bins_y_p0 = np.linspace(-5.0, -2.5,  6)
np_bins_y_p1 = np.linspace(-2.0, +2.0, 21)
np_bins_y_p2 = np.linspace(+2.5, +5.0,  6)
np_bins_y    = np.append( np.append(np_bins_y_p0, np_bins_y_p1), np_bins_y_p2)
np_bins_y_width = np.array( [np_bins_y[i+1]-np_bins_y[i] for i in range(np_bins_y.size-1)] )
np_bins_y_mid = np.array( [(np_bins_y[i+1]+np_bins_y[i])*0.5 for i in range(np_bins_y.size-1)] )

def find_y_qt_bin( ps=(), verbose=False ):

    y = abs(ps[0])
    iy_low  = np.where(np_bins_y<=y)[0][-1] if np.where(np_bins_y<=y)[0].size>0 else -1
    iy_high = np.where(np_bins_y>y)[0][0]   if np.where(np_bins_y>y)[0].size>0  else -1
    bin_y='OF'
    if iy_low==-1 or iy_high==-1:
        if verbose:
            print 'y=', y, 'yields (', iy_low, iy_high, ') => return'
    else:
        bin_y = 'y{:03.2f}'.format(np_bins_y[iy_low])+'_'+'y{:03.2f}'.format(np_bins_y[iy_high])

    qt = ps[1]
    iqt_low = np.where(np_bins_qt<=qt)[0][-1] if np.where(np_bins_qt<=qt)[0].size>0 else -1
    iqt_high = np.where(np_bins_qt>qt)[0][0] if np.where(np_bins_qt>qt)[0].size>0 else -1
    bin_qt='OF'
    if iqt_low==-1 or iqt_high==-1:
        if verbose:
            print 'qt=', qt, 'yields (', iqt_low, iqt_high, ') => return'
    else:
        bin_qt = 'qt{:03.1f}'.format(np_bins_qt[iqt_low])+'_'+'qt{:03.1f}'.format(np_bins_qt[iqt_high])

    if verbose:
        print 'y=', y, 'yields bins (', iy_low, iy_high, ') => Ok'
        print 'qt=', qt, 'yields bins (', iqt_low, iqt_high, ') => Ok'
    
    return (bin_y, iy_low, bin_qt, iqt_low)


# Evaluate the angular pdf given a PS point (cos*,phi*) and the value of the 8 parameters
def angular_pdf(ps=(), coeff_vals=[], verbose=False):
    (x,y) = ps
    UL = (1.0 + x*x)
    L = 0.5*(1-3*x*x)
    T = 2.0*x*math.sqrt(1-x*x)*math.cos(y)
    I = 0.5*(1-x*x)*math.cos(2*y)
    A = math.sqrt(1-x*x)*math.cos(y)
    P = x
    p7 = (1-x*x)*math.sin(2*y)
    p8 = 2.0*x*math.sqrt(1-x*x)*math.sin(y)
    p9 = math.sqrt(1-x*x)*math.sin(y)
    if verbose:
        print ('\t pdf = 3./16./math.pi * ( UL + %s*L + %s*T + %s*I + %s*A + %s*P + %s*p7 + %s*p8 + %s*p9)' % (coeff_vals[0], coeff_vals[1], coeff_vals[2], coeff_vals[3], coeff_vals[4], coeff_vals[5], coeff_vals[6], coeff_vals[7]) )
    return 3./16./math.pi * ( UL + coeff_vals[0]*L + coeff_vals[1]*T + coeff_vals[2]*I + coeff_vals[3]*A + coeff_vals[4]*P + coeff_vals[5]*p7 + coeff_vals[6]*p8 + coeff_vals[7]*p9)


def get_coeff_vals(res={}, coeff_eval='fit', bin_y='', qt=0.0, coeff=['A0'], np_bins_template_qt_new=np.array([])):

    if np_bins_template_qt_new.size==0:
        np_bins_template_qt = np_bins_qt
    else:
        np_bins_template_qt = np_bins_template_qt_new

    coeff_vals = np.zeros(8)
    for ic,c in enumerate(coeff):
        coeff_val = 0.0
        if coeff_eval == 'fit':
            order = len(res[c+'_'+bin_y+'_fit'])
            for o in range(order):
                coeff_val += math.pow(qt,o)*res[c+'_'+bin_y+'_fit'][o]
        elif coeff_eval == 'val':
            iqt = np.where(np_bins_template_qt<=qt)[0][-1]
            coeff_val = res[c+'_'+bin_y+'_val'][iqt]
        coeff_vals[ic] = coeff_val
    return coeff_vals

def weight_coeff(res={}, coeff_eval='fit', bin_y='', qt=0.0, ps=(), coeff=['A0'], verbose=False):
    coeff_vals = get_coeff_vals(res=res, coeff_eval=coeff_eval, bin_y=bin_y, qt=qt, coeff=coeff)
    val = angular_pdf(ps=ps, coeff_vals=coeff_vals)
    if val > 0.0:        
        if verbose:
            print 'Fit type', coeff_eval, ': bin', bin_y, 'at qt =', qt, 'for ps=', ps, 'yields val = ', val
        return val
    else:
        if verbose:
            print ('Fit type', coeff_eval, ': bin', bin_y, 'at qt =', qt, 'for ps=', ps, 'yields pdf = ', val, '<=0.0. Return 1.0')
    return 1.0

class harmonicWeights(Module):
    def __init__(self, coeff=['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'], Wtypes=['bare', 'preFSR', 'dress'], coeff_eval='val'):
        self.coeff = coeff
        self.Wtypes = Wtypes
        self.coeff_eval = coeff_eval
        self.fit_result = {}
        input_dir = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing/data/angularCoeff/' % os.environ['CMSSW_BASE']
        for q in ['Wplus', 'Wminus']:
            self.fit_result[q]  = {}
            for t in Wtypes:
                file_name = 'fit_results_CC_FxFx_%s_W%s_all_A0-7.pkl' % (q,t)
                print "Loading angular coefficients file from file '%s'" % (input_dir+'/'+file_name)
                self.fit_result[q]["W"+t] = pickle.load( open(input_dir+'/'+file_name) )      
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for t in self.Wtypes:
            for c in (self.coeff+['UL']):                
                self.out.branch("Weight_"+t+"_"+c, "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if event.genVtype != 14:
            for t in self.Wtypes:
                for c in (self.coeff+['UL']):
                    self.out.fillBranch("Weight_"+t+"_"+c, 1.0)
            return True        

        for t in self.Wtypes:

            q = getattr(event, "W_"+t+"_charge")

            # W of type t not found
            if abs(q)!=13:
                for c in (self.coeff+['UL']):
                    wc = 1.0
                    self.out.fillBranch("Weight_"+t+"_"+c, wc)
                continue

            Wcharge = 'Wplus' if q==-13 else 'Wminus'             
            ps_W  = (getattr(event, "W_"+t+"_y"), getattr(event, "W_"+t+"_qt") )
            ps_CS = (getattr(event, "CS_"+t+"_theta"), getattr(event, "CS_"+t+"_phi") )

            # if (qt,y) not in the bins, use MC
            useMC = False
            (bin_y, iy_low, bin_qt, iqt_low) = find_y_qt_bin( ps=ps_W, verbose=False )
            if bin_y=='OF' or bin_qt=='OF':
                useMC = True
            pdf = weight_coeff(res=getattr(self, "fit_result")[Wcharge]["W"+t], coeff_eval=self.coeff_eval, bin_y=bin_y, qt=ps_W[1], ps=ps_CS, coeff=self.coeff) if (not useMC) else 1.0
            if pdf <= 0.0:
                print ('Fit type', coeff_eval, ': bin', bin_y, 'at qt =', qt, 'for ps=', ps_CS, 'yields pdf = ', pdf, '<=0.0. Return 1.0')
                continue
            for c in (self.coeff+['UL']):
                wc = 1.0
                coeff_vals = np.zeros(8)
                if c!='UL':
                    coeff_vals[int(c[1])] = 1.0
                wc = angular_pdf(ps=ps_CS, coeff_vals=coeff_vals)/pdf if (not useMC) else 1.0
                self.out.fillBranch("Weight_"+t+"_"+c, wc)

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

harmonicWeightsModule = lambda : harmonicWeights()
