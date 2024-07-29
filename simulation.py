import time
import random
import matplotlib.pyplot as plt
import numpy as np

class SolarPanel:
    def __init__(self, efficiency=0.2, area=1.0):
        self.efficiency = efficiency
        self.area = area
    
    def generate_power(self, sunlight):
        # Simulate power generation based on sunlight intensity (0 to 1)
        power = sunlight * self.efficiency * self.area * 1000  # kW to W
        return power

class Battery:
    def __init__(self, capacity=10000, efficiency=0.9, discharge_rate=0.05):
        self.capacity = capacity  # Wh
        self.charge_level = 0  # Wh
        self.efficiency = efficiency
        self.discharge_rate = discharge_rate
    
    def charge(self, power, time_period):
        # Charge the battery with the provided power over the given time period (in hours)
        effective_power = power * self.efficiency
        self.charge_level += effective_power * time_period
        if self.charge_level > self.capacity:
            self.charge_level = self.capacity

    def discharge(self, time_period):
        # Simulate battery discharge over the given time period (in hours)
        self.charge_level -= self.charge_level * self.discharge_rate * time_period
        if self.charge_level < 0:
            self.charge_level = 0

    def get_charge_level(self):
        return self.charge_level

class ChargeController:
    def __init__(self, battery):
        self.battery = battery
    
    def manage_charging(self, power):
        # Charge the battery using the power from solar panels
        self.battery.charge(power, 1)  # 1 hour time period

class MonitoringSystem:
    def __init__(self, solar_panel, battery):
        self.solar_panel = solar_panel
        self.battery = battery
        self.logs = []

    def log_status(self, hour, sunlight, power_generated):
        # Log the current status of the system
        charge_level = self.battery.get_charge_level()
        self.logs.append((hour, sunlight, power_generated, charge_level))
        print(f"Hour: {hour}, Sunlight: {sunlight:.2f}, Power Generated: {power_generated:.2f} W, Battery Charge Level: {charge_level:.2f} Wh")

    def plot_logs(self):
        # Plot the logged data
        hours, sunlight, power_generated, charge_level = zip(*self.logs)
        fig, ax1 = plt.subplots()

        ax1.set_xlabel('Hour')
        ax1.set_ylabel('Power (W)', color='tab:blue')
        ax1.plot(hours, power_generated, label='Power Generated', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Charge Level (Wh)', color='tab:green')
        ax2.plot(hours, charge_level, label='Battery Charge Level', color='tab:green')
        ax2.tick_params(axis='y', labelcolor='tab:green')

        fig.tight_layout()
        plt.title('Solar Charging Station Performance')
        plt.show()

def lunar_sunlight_cycle(hour):
    # Simulate lunar daylight cycle
    # Simple model: 14 days of daylight followed by 14 days of darkness
    day_period = 14 * 24  # hours
    cycle_period = day_period * 2
    cycle_position = hour % cycle_period
    if cycle_position < day_period:
        return 1  # Full daylight
    else:
        return 0  # Full darkness

def simulate_solar_charging():
    # Create system components
    solar_panel = SolarPanel(efficiency=0.2, area=2.0)
    battery = Battery(capacity=5000)
    charge_controller = ChargeController(battery)
    monitoring_system = MonitoringSystem(solar_panel, battery)

    # Simulate charging over a lunar day (14 days) and night (14 days)
    total_hours = 28 * 24  # 28 days
    for hour in range(total_hours):
        sunlight = lunar_sunlight_cycle(hour)  # Realistic lunar sunlight cycle
        power_generated = solar_panel.generate_power(sunlight)
        charge_controller.manage_charging(power_generated)
        battery.discharge(1)  # Discharge battery every hour
        monitoring_system.log_status(hour, sunlight, power_generated)
        time.sleep(0.1)  # Simulate real-time logging (optional)

    # Plot the results
    monitoring_system.plot_logs()

if __name__ == "__main__":
    simulate_solar_charging()
