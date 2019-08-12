from partkeepr import Partkeepr
from decimal import *

distributor = Partkeepr("https://partkeepr.locallan", "auto", "auto")
parts = distributor.find_component("EMK212B7475KG-T")
print(parts)

parts = distributor.find_component("SMAJ6.0A")
print(parts)


capacitor_parameters = {'Capacitance': Decimal(0.0000001),
                        'Case': "0402",
                        'Voltage': Decimal(25),
                        'Dielectric Type': "X7R"}
parts = distributor.find_capacitor_by_parameters(capacitor_parameters)
print(parts)

resistor_parameters = {'Resistance': Decimal(1000),
                        'Case': "0402",
                        'Tolerance': Decimal(5)}
parts = distributor.find_resistor_by_parameters(resistor_parameters)
print(parts)
