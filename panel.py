from math import sin, pi

class Panel():
    
    
    def __init__(self, surface, number, efficiency, irradiance):
        self.surface=surface*number
        self.efficiency=efficiency
        self.irradiance=irradiance
        
    def _compute_sun_flux(self, hour_of_day):
        """
        Computes the heat flux
        unit : Watts
        Now : constant light 
        1day= 4.2 kWh/m2
    
        """
        h_min, h_max = 8.,18.
        sun_hours = h_max - h_min
        t_abs = (hour_of_day%24 - h_min)/sun_hours
        if t_abs<= 0. or t_abs >=1.:
            return 0.
        # typical sun radiation in february in toulouse
        # 2.9kW/m2.day for an angle of 30 deg
        # and ground albedo of 0.2 (trees)
        
        cos_fact = sin(pi*t_abs)
        ampl = self.irradiance*self.surface*pi/(sun_hours*2)
        #2.5*1000*self.surface/sun_hours
        
        return cos_fact*ampl
        
    def compute_power(self, hour_of_day):
        """
        heat coming out of the colector
        """
        return self.efficiency*self._compute_sun_flux(hour_of_day)
    
