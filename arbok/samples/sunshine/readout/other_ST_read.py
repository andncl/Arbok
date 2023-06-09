from arbok.core.subsequence import SubSequence
from arbok.QMv2.Readout import Readout
import numpy as np
from qm.qua import *

readJ = 0

class OtherStReadout():
    """
    Class containing parameters and sequence for mixed down up initialization
    Args:
    program_parameters (dict): Dict containing all program parameters 
    unit_amp (float): unit amplitude of all pulses
    """
    def __init__(
            self, 
            name = 'OtherStReadout',
            config = {
                'elements': ['P1', 'J1', 'P2'],
                'unit_amp': {'unit': 'V', 'value': 0.5},
                'vHome':{'value': [0, 0, 0], 'unit': 'V'},
                'vReference': {'unit': 'v', 'value': [0.0, 0.0, 0.0]},
                'tReadReferenceRamp': {'unit': 's', 'value': int(17)},
                'vPreRead': {'unit': 'v', 'value': [0.065, 0, -0.065]},
                'tPreReadRamp': {'unit': 's', 'value': int(17)},
                'vPreReadPoint': {'unit': 'v', 'value': [0.0925, readJ, -0.0925]},
                'tPreReadPoint': {'unit': 's', 'value': int(6)},
                'vRead': {'unit': 'v', 'value': [0.0925, readJ, -0.0925]},
                'tReadRamp': {'unit': 's', 'value': int(12)},
                'tPreRead': {'unit': 's', 'value': int(0.1e3/4)},
                'tPostRead': {'unit': 's', 'value': int(0.1e3/4)},
                
            },
    ):
        """
        Constructor method for 'DummyReadout' class
        
        Args:
        unit_amp (float): unit amplitude of all pulses
        """
        #self.program_parameters = program_parameters
        self.config = config
        self.add_qc_params_from_config(self.config)

        self.ref2 = Readout('ref2_')
        self.ref2.read_label =  'SDC'
        self.read = Readout('read_')
        self.read.read_label = 'SDC'
        self.diff = Readout('diff_')
        self.diff.read_label = 'SDC'
        self.diff.threshold = 0.004
        self.gettables = [self.ref2, self.read, self.diff]


    def create_qc_params_from_program_dict(self):
        pass

    def qua_declare(self):
        for gettable in self.gettables:
            gettable.init_qua_vars()

    def qua_stream(self):
        for gettable in self.gettables:
            gettable.init_qua_vars()

    def qua_sequence(self, cls = None, simulate = False):
        """QUA sequence to perform mixed down up initialization"""
        if cls == None: cls = self

        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        play('unit_ramp_20ns'*amp(cls.vReference[0] - cls.vHome[0]),
                'P1',duration=cls.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(cls.vReference[1] - cls.vHome[1]),
                'J1',duration=cls.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(cls.vReference[2] - cls.vHome[2]),
                'P2',duration=cls.tReadReferenceRamp)
        
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(cls.tPreRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        if simulate: cls.ref2.measureAndSave()
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(cls.tPostRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(-cls.vReference[0] + cls.vHome[0]),
                'P1',duration=cls.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(-cls.vReference[1] + cls.vHome[1]),
                'J1',duration=cls.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(-cls.vReference[2] + cls.vHome[2]),
                'P2',duration=cls.tReadReferenceRamp)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(cls.vPreRead[0] - cls.vHome[0]),'P1',
                duration = cls.tPreReadRamp)
        play('unit_ramp_20ns'*amp(cls.vPreRead[1] - cls.vHome[1]),'J1',
                duration = cls.tPreReadRamp)
        play('unit_ramp_20ns'*amp(cls.vPreRead[2] - cls.vHome[2]),'P2',
                duration = cls.tPreReadRamp)
        
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky'
                ,'Qoff','J1_not_sticky')
        wait(cls.tPreReadPoint)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(cls.vRead[0] - cls.vPreRead[0]),'P1',
                duration = cls.tReadRamp)
        play('unit_ramp_20ns'*amp(cls.vRead[1] - cls.vPreRead[1]),'J1',
                duration = cls.tReadRamp)
        play('unit_ramp_20ns'*amp(cls.vRead[2] - cls.vPreRead[2]),'P2',
                duration = cls.tReadRamp)
                
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(cls.tPreRead,'SDC')       
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        if simulate: self.read.measureAndSave() 
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        wait(cls.tPostRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky',
                'Qoff','J1_not_sticky')
        
        play('unit_ramp_20ns'*amp(cls.vHome[0]-cls.vRead[0]),'P1')
        play('unit_ramp_20ns'*amp(cls.vHome[1]-cls.vRead[1]),'J1')
        play('unit_ramp_20ns'*amp(cls.vHome[2]-self.vRead[2]),'P2')

        align()
                    
        #setVars.feedback_SSR(ref2.read,set_pt=SETFB_DCsetpt, fb_gate='SDC',
        #                      gain = SETFB_DCalpha)

        ramp_to_zero('P1')
        ramp_to_zero('J1')
        ramp_to_zero('P2')
        ramp_to_zero('J2')
        ramp_to_zero('P3')
        #self.diff.takeDiff(self.read, self.ref2)