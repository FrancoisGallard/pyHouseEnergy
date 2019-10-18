
class Tank():
    
    def __init__(self, volume, temp, max_temp, min_temp, floor_surf, tank_R):
        """
        volume in m3
        temps in kelvin
        """
        self.volume=volume
        self.temp=temp
        self.min_temp=min_temp
        self.max_temp=max_temp
        self.heat_capacity=volume*(max_temp-min_temp)*4.18e6
        self._heat_coeff=(self.max_temp-self.min_temp)/self.heat_capacity
        self.floor_surf = floor_surf
        self.height = self.volume / floor_surf
        self.tank_R = tank_R
        width = self.floor_surf**0.5
        self.total_surf = 4*width*self.height+2*self.floor_surf
        
        
    def store_heat(self, heat):
        self.temp+=heat*self._heat_coeff
        if self.temp>self.max_temp:
            self.temp=self.max_temp 
        
    def take_heat(self, heat):
        """
        Try to take heat from the tank
        returns the actual heat extracted
        """
        assert heat>=0
        if heat==0.:
            return 0.
        if self.heat<heat:
            self.temp=self.min_temp
            return self.heat
        self.temp-=heat*self._heat_coeff
        return heat
        
    def compute_losses_power(self):
        return self.total_surf*(self.min_temp-self.temp)/self.tank_R
    
    @property
    def heat(self):
        return (self.temp-self.min_temp)/self._heat_coeff
        
    def __str__(self):
        s= "Tank volume = %s m3\n"%self.volume
        s+= "max heat capacity = %s kWh\n"%(self.heat_capacity/3.6e6)
        s+= "current heat =%s kWh"%(self.heat/(3.6e6))
        
        return s