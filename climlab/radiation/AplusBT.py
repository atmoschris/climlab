'''Simple linear radiation module.
Usage example:

import climlab
sfc, atm = climlab.domain.single_column()  # creates a column atmosphere and scalar surface
# Create a state variable
Ts = climlab.Field(15., domain=sfc)
# Make a dictionary of state variables
s = {'Ts': Ts}
olr = climlab.radiation.AplusBT(state=s)
print olr
#  OR, we can pass a single state variable
olr = climlab.radiation.AplusBT(state=Ts)
print olr
# to compute tendencies and diagnostics
olr.compute()
#  or to actually update the temperature
olr.step_forward()
print olr.state


New prototype usage for xray version:

import numpy as np
import xray
import climlab
latarray = np.arange(-90,90.)
Tarray = np.ones_like(latarray)
da = xray.DataArray(data=Tarray, coords={'lat':latarray})
da.attrs['var_type'] = 'state'
model = climlab.radiation.AplusBT(variables={'Ts':da})
model['heat_capacity'] = xray.DataArray(model.Ts) *400
model.compute()

'''
from climlab.process.energy_budget import EnergyBudget


class AplusBT(EnergyBudget):
    '''The simplest linear longwave radiation module.
    Should be invoked with a single temperature state variable.'''
    def __init__(self, A=200., B=2., **kwargs):
        super(AplusBT, self).__init__(**kwargs)
        self.attrs['A'] = A
        self.attrs['B'] = B
#
#    @property
#    def A(self):
#        return self._A
#    @A.setter
#    def A(self, value):
#        self._A = value
#        self.param['A'] = value
#    @property
#    def B(self):
#        return self._B
#    @B.setter
#    def B(self, value):
#        self._B = value
#        self.param['B'] = value
#    
#    def emission(self):
#        for varname, value in self.state.iteritems():
#            flux = self.A + self.B * value
#            self.OLR = flux
#            self.diagnostics['OLR'] = self.OLR
    
    def _compute_heating_rates(self):
        '''Compute energy flux convergences to get heating rates in W / m**2.'''
        flux = self.A + self.B * self.Ts
        flux.attrs['var_type'] = 'diag'
        self['OLR'] = flux
        heating_rates = -flux
        return heating_rates
