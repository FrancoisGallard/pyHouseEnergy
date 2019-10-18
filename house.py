
class House(object):
    
    def __init__(self, in_temp, out_temp,
    	            walls_surf, windows_surf, ground_surf, 
                	ground_R, walls_R, windows_R, roof_R, 
                 dtemp_roof, dtemp_ground,
                 vent_mass_flow_rate, hot_water_mass,
                 hot_water_temp, double_flux_vent=False):
       self.in_temp=in_temp
       self.out_temp=out_temp
       self.walls_surf=walls_surf
       self.windows_surf=windows_surf
       self.ground_surf=ground_surf
       self.ground_R=ground_R
       self.walls_R=walls_R
       self.windows_R=windows_R
       self.roof_R=roof_R
       self.dtemp_roof=dtemp_roof
       self.dtemp_ground=dtemp_ground
       self.vent_mass_flow_rate=vent_mass_flow_rate
       self.hot_water_mass=hot_water_mass
       self.hot_water_temp=hot_water_temp
       self.double_flux_vent=double_flux_vent
       
       self.total_surf=walls_surf+windows_surf+2*ground_surf
       
       self._times = []
       self._heat_windows = []
       self._heat_ground = []
       self._heat_roof = []
       self._heat_walls = []
       self._heat_vent = []
       self._heat_water =[]
       
       
    def _compute_roof_power(self):
        return (self.out_temp-(self.in_temp+self.dtemp_roof))*\
              self.ground_surf/self.roof_R
       
    def _compute_windows_power(self):
        return (self.out_temp-self.in_temp)*\
              self.windows_surf/self.windows_R
       
    def _compute_walls_power(self):
        return (self.out_temp-self.in_temp)*\
              self.walls_surf/self.walls_R
        
    def _compute_ground_power(self):
        return (self.out_temp-(self.in_temp+self.dtemp_ground))*\
              self.ground_surf/self.ground_R
        
    def _compute_vent_power(self):
        vent_flux=self.vent_mass_flow_rate*(self.out_temp-self.in_temp)*1256.
        print "vent flux", vent_flux
        if not self.double_flux_vent:
        #air thermal capacity =1256 J/m3/K
            return vent_flux
        return vent_flux*0.3
        
    def _compute_hot_water_power(self, time):
        h_min=7.
        h_max=22.
        if time%24<=h_max and time%24>=h_min:
            return self.hot_water_mass*(288.-self.hot_water_temp)*4.18e3/((h_max-h_min)*3600.)
        return 0.0
        
    def compute_heat_power(self, time, time_step):
        flux_windows =self._compute_windows_power()
        flux_ground =self._compute_ground_power()
        flux_roof =self._compute_roof_power()
        flux_walls =self._compute_walls_power()
        flux_vent =self._compute_vent_power()
        flux_water = self._compute_hot_water_power(time)
        
        # print "power vent %1.3g kW"%(flux_vent/1.e3)
        self._times.append(time)
        self._heat_windows.append(flux_windows*time_step *3.6e3 )
        self._heat_ground.append(flux_ground*time_step*3.6e3)
        self._heat_roof.append(flux_roof*time_step *3.6e3)
        self._heat_walls.append(flux_walls*time_step *3.6e3)
        self._heat_vent.append(flux_vent*time_step *3.6e3)
        self._heat_water.append(flux_water*time_step *3.6e3)
        
        flux_conduction =flux_windows+ flux_ground + flux_roof + flux_walls
        dtemp= (self.out_temp-self.in_temp)
        r_eq= self.total_surf*dtemp/(flux_conduction)
        flux = flux_conduction + flux_vent + flux_water
        #print "power conduction = %1.3g kW"%(flux_conduction/1e3)
        #print "power water = %1.3g kW"%(flux_water/1e3)
        #print "power ventillation = %1.3g kW"%(flux_vent/1e3)
        #print "total power = %1.3g kW"%(flux/1e3)
        
        #print "R equiv house for dtemp %1.2g K =%1.2g"%(dtemp, r_eq)
        return flux
        
        
        
    def post(self, sim_dir):
        from matplotlib import pyplot as plt
        
        self._times = []
        tot_heat_windows = sum(self._heat_windows)
        tot_heat_ground = sum(self._heat_ground)
        tot_heat_roof =sum(self._heat_roof)
        tot_heat_walls =sum(self._heat_walls)
        tot_heat_vent =sum(self._heat_vent)
        tot_heat_water =sum(self._heat_water)
        
        consumed_heat_tot= tot_heat_windows+ tot_heat_ground + tot_heat_roof
        consumed_heat_tot+=tot_heat_walls + tot_heat_vent + tot_heat_water
        
        labels = 'Walls', 'Roof', 'Hot water','Windows','Ground','Ventilation'
        sizes = [tot_heat_walls/consumed_heat_tot,
                 tot_heat_roof/consumed_heat_tot,
                 tot_heat_water/consumed_heat_tot,
                 tot_heat_windows/consumed_heat_tot,
                 tot_heat_ground/consumed_heat_tot,
                 tot_heat_vent/consumed_heat_tot,] 
       
        plt.pie(sizes, labels=labels, 
        	       shadow=True, startangle=90,
        	       autopct=lambda(p): '{:.1f}'.format(-p *consumed_heat_tot/ 3.6e8)) 
        plt.axis('equal')
        plt.title("Heat consumption per category (kWh)")
        plt.savefig(sim_dir+"heat_stat.png")
        plt.close()