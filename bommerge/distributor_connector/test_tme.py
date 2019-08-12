from bommerge.utils import files
from bommerge.distributor_connector.tme import TME
from decimal import *


def read_configuration():
    user_dir = files.get_user_home_directory()
    configuration_file = user_dir + '/.bommerge/configuration.json'
    if files.file_exist(configuration_file):
        configuration = files.load_json_file(configuration_file)
        token = str(configuration['Distributors']['TME']['token'])
        app_secret = str(configuration['Distributors']['TME']['app_secret'])
        tme_config = {'token': token, 'app_secret': app_secret}
        return tme_config
    else:
        print("Unable to read bommerge configuration file. " + str(configuration_file))


tme_config = read_configuration()
distributor = TME(tme_config['token'], tme_config['app_secret'])

# parts = distributor.find_component("SMAJ6.0A")
# print(parts)

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
