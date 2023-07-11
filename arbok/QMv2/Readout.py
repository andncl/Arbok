#\\ COMMERCIAL-IN-CONFIDENCE
#\\ DO NOT DISTRIBUTE WITHOUT PRIOR CONSENT FROM PROF ANDREW DZURAK.
#\\ Copyright Dzurak Research Group, UNSW.
"""
General readout class to manage measurements

SSR
24/06/2022
"""

from qm.qua import *
import matplotlib.pyplot as plt

class Readout():
    def __init__(self, tag='', read_label = None, threshold = 0):
        
        self.read_label = read_label
        self.threshold = threshold
                
        self.tag = tag
        
        self.read_I = None
        self.read_Q = None
        self.read = None
        self.state = None
        
        self.read_I_stream = None
        self.read_Q_stream = None
        self.read_stream = None
        self.state_stream = None
        self.chopRef_stream = None

    def measure(self):
        ### This function performs a measurement and saves the streams
        measure('measure', self.read_label, None, demod.full('x',self.read_I),
                demod.full('y',self.read_Q))
    
    def save(self):
        assign(self.read, self.read_I + self.read_Q)   
        assign(self.state, self.read > self.threshold)
        
        assign(self.chopRef, self.read)
        
        save(self.read_I, self.read_I_stream)
        save(self.read_Q, self.read_Q_stream)
        save(self.read, self.read_stream)
        save(self.chopRef, self.chopRef_stream)
        save(self.state, self.state_stream)
    
    def measureAndSave(self):
        align()
        self.measure()
        self.save()
        align()
        
    def takeDiff(self, read, ref, thr = None):
        """This functions saves streams for a Readout object that is calculated
        without a measurement. e.g., the difference between 2 readouts. """
        
        assign(self.read_I, read.read_I - ref.read_I)
        assign(self.read_Q, read.read_Q - ref.read_Q)
        assign(self.read, read.read - ref.read)
        
        save(self.read_I, self.read_I_stream)
        save(self.read_Q, self.read_Q_stream)
        save(self.read, self.read_stream)
        
        assign(self.chopRef, self.read)
        save(self.chopRef, self.chopRef_stream)
        
        if(thr == None):
            thr = self.threshold
        
        self.aboveThreshold(thr)
    
    def aboveThreshold(self, thr):
        # with if_(thr == None):
            # thr = self.threshold
            
        assign(self.state, self.read > thr)
        save(self.state, self.state_stream)
    
    def init_qua_vars(self):
        self.read_I = declare(fixed)
        self.read_Q = declare(fixed)
        self.read = declare(fixed)
        self.state = declare(bool)
        self.chopN = declare(int)
        self.chopRef = declare(fixed)
        
        self.read_I_stream = declare_stream()
        self.read_Q_stream = declare_stream()
        self.read_stream = declare_stream()
        self.chopRef_stream = declare_stream()
        self.state_stream = declare_stream()
      
    def save_streams(self):
        self.read_I_stream.save_all(self.tag+"read_I")
        self.read_Q_stream.save_all(self.tag+"read_Q")
        self.read_stream.save_all(self.tag+"read")
        self.chopRef_stream.save_all(self.tag+"chopRef")
        self.state_stream.save_all(self.tag+"state")
        
        self.read_stream.timestamps().save_all(self.tag+"TIMES")
    
    def fetch_streams(self, res):
        self.READ_I = res.get(self.tag + 'read_I').fetch_all()['value']
        self.READ_Q = res.get(self.tag + 'read_Q').fetch_all()['value']
        self.READ = res.get(self.tag + 'read').fetch_all()['value']
        self.CHOP_REF = res.get(self.tag + 'chopRef').fetch_all()['value']
        self.STATE = res.get(self.tag + 'state').fetch_all()['value']
        
        TIMES_ns = res.get(self.tag + 'TIMES').fetch_all()['value']
        self.TIMES = TIMES_ns * 1e-9
        
        
    def plot_histogram(self, title = 'Histogram', bins = 500, color = 'r'):
        data = self.READ
        plt.hist(data,bins=bins,alpha = 0.7)
        plt.xlabel(self.tag + 'READ')
        plt.ylabel('Counts')
        plt.title(title)
        plt.axvline(x=self.threshold*(tReadInt_nominal/tReadInt),color=color)
        plt.show()