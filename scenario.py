

class Scenario(object):
    
    def __init__(self, house, panel, tank):
        self.house=house
        self.panel=panel
        self.tank=tank
        self._panel_power=[]
        self._consumed_tank_power=[]
        self._heat_losses_power=[]
        self._tank_heat=[]
        self._time_list=[]
        self._tank_temp = []
        self.d_time=None
        self.produced_heat_tot =0.
        self.heat_losses_tot =0.
        self.consumed_tank_heat_tot =0.
        self.house_heat_losses_tot =0.0
        
    def loop(self, simulation_time, time_step=1.0):
        
        time=0.0
        d_time=time_step*3.6e3
        self.d_time=d_time
        
        while time<simulation_time:
            
            panel_power =self.panel.compute_power(time+0.5*time_step)
            self._panel_power.append(panel_power)
            heat_prod=panel_power*d_time
            self.produced_heat_tot+=heat_prod
            
            self.tank.store_heat(heat_prod)
            
            loss_power = self.house.compute_heat_power(time, time_step)
            self.house_heat_losses_tot+=loss_power*d_time
            tank_losses = self.tank.compute_losses_power()
            self.tank.take_heat(- tank_losses * d_time)
            
            heat_loss = loss_power *d_time
            self._heat_losses_power.append(loss_power + tank_losses)
            self.heat_losses_tot += min(heat_loss+ tank_losses,0.)
        
            if heat_loss < 0:
                # dont take the tank losses here because total 
                # losses may be >0 while the tank may still loose heat
                taken_heat=self.tank.take_heat(-heat_loss)
                self.consumed_tank_heat_tot +=taken_heat
                
                if heat_loss>taken_heat:
                    print "could not take sufficient heat, missing %s kWh "%((taken_heat-heat_loss)/3.6e6)
                self._consumed_tank_power.append(taken_heat/d_time)
            else:
                self._consumed_tank_power.append(0.)
            self._time_list.append(time)
            time+=time_step
            
            self._tank_heat.append(self.tank.heat)
            self._tank_temp.append(self.tank.temp)
            
        self._simulation_time = simulation_time
        
    def post(self, sim_dir):
        
        print "-----------------------"
        print ". scenario statistics ."
        print ""
        n_days=self._simulation_time/24.
        produced_heat_kwh = self.produced_heat_tot/3.6e6
        print "Total produced heat = %1.1f kWh"%produced_heat_kwh
        savings = produced_heat_kwh*0.15*30.5/n_days
        print "Equivalent for a month = %1.1f Eur"%savings
        heat_losses_kwh =self.house_heat_losses_tot/3.6e6
        external_heat_kwh =-( self.house_heat_losses_tot + self.consumed_tank_heat_tot )/3.6e6

        print "Total consumed tank heat = %1.1f kWh"%(self.consumed_tank_heat_tot/3.6e6)
        print "Total heat losses = %1.1f kWh"%-heat_losses_kwh
        costs= -heat_losses_kwh*0.15*30.5/n_days
        print "Equivalent for a month = %1.1f Eur"%costs
        
        costs= external_heat_kwh*0.15*30.5/n_days
        print "Required external heat source = %1.1f kWh "%external_heat_kwh
        print "Equivalent for a month = %1.1f Eur"%costs
     
        print "Percentage of heat needs covered by solar panels = %1.1f "%(-100.*self.consumed_tank_heat_tot/self.heat_losses_tot)
        
        print "-----------------------"
        
        from matplotlib import pyplot as plt
        from numpy import array
        
        fig, ax1 = plt.subplots() 
        ax1.plot(self._time_list, array(self._panel_power)/1e3, label="panel power (kW)", color="g")
        ax1.plot(self._time_list, array(self._consumed_tank_power)/1e3, label="tank taken power(kW)", color='orange')
        ax1.plot(self._time_list, -array(self._heat_losses_power)/1e3, label="heat losses (kW)", color='blue', ls='--')
        ax2 = ax1.twinx()
        ax2.plot(self._time_list, array(self._tank_heat)/3.6e6, label="tank heat (kWh)", color='red')

        ax1.set_ylabel('Power sources and losses (kW)')
        ax2.set_ylabel('Tank cumulated heat (kWh)', color='r')
        
        # ax2.set_xlabel("Time (Hours)")
        plt.title("Heat balance vs time (Hours)")
        ax1.legend()
        #ax2.legend()
        fig.tight_layout()
        plt.savefig(sim_dir+"solar_stat.pdf")
       
        plt.close()
        fig, ax3 = plt.subplots()
        ax3.plot(self._time_list, array( self._tank_temp) -273.15, label="Tank temperature (deg C)", color="g")
        ax3.set_xlabel('Time (hours)')
        plt.title("Tank temperature (deg C)")
        plt.savefig(sim_dir+"tank_temp.pdf")
        plt.close()
        
        
        
        
        