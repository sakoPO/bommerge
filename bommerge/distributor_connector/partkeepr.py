try:
    from components import resistor
    from components import capacitor
    from components import voltage
except:
    from bommerge.components import resistor
    from bommerge.components import capacitor
    from bommerge.components import voltage
from decimal import *
import sys
import json
import requests
from requests.auth import HTTPBasicAuth


class Partkeepr:
    def __init__(self, url, user, password):
        self.name = "PartKeepr"
        self.url = url
        self.user = user
        self.password = password
        self.parameter_skip_list = ['']

    def find_component(self, component):
        """
        :param component: Manufacturer Part Number as string
        :return:
        """
        response = self.__find_by_MPN(component)
        return response

    def find_resistor_by_parameters(self, part):
        """
        :param part: dictionary with fields:
                'Resistance': Decimal in Ohms ,
                'Case': string
                'Tolerance': percent as integer
        :return:
        """
        params = {
            'filter':
                '''[
                    {{"subfilters": [
                        {{"subfilters": [
                            {{"subfilters": [], "property": "description", "value": "%{0}%", "operator": "like"}}
                            ], "type": "OR"}},
                        {{"subfilters": [
                            {{"subfilters": [], "property": "description", "value": "%{1}%", "operator": "like"}}
                            ], "type": "OR"}}                       
                        ], "type": "AND"}},
                    {{"subfilters": [], "property": "category", "operator": "IN",
                            "value": ["/api/part_categories/2", "/api/part_categories/3", "/api/part_categories/4"]}}
                   ]'''.format(resistor.ohms_to_string(part['Resistance']).replace("\u03a9", ""),
                               part['Case']).replace("\n", "").replace(" ", "")
        }
        print(params)
        response = self.__partkeepr_api_call('get', '/api/parts', params=params)
        response = response.json()
        print(response)
        if len(response["hydra:member"]) > 0:
            found = []
            for component in response["hydra:member"]:
                decoded_part = self.decode_product_dictionary(component)
                if "Tolerance" in decoded_part['Parameters'] and part['Tolerance'] is not None:
                    if decoded_part['Parameters']['Tolerance'] <= part['Tolerance']:
                        found.append(decoded_part)
                else:
                    found.append(decoded_part)
            return found

    def find_capacitor_by_parameters(self, part):
        """
        :param part: dictionary with fields:
                'Capacitance': int in Farads,
                'Case': string
                'Voltage': int in Volts
                'Dielectric Type': string ie.: X7R, NP0 etc.
        :return:
        """
        params = {
            'filter':
                '''[
                    {{"subfilters": [
                        {{"subfilters": [
                            {{"subfilters": [], "property": "description", "value": "%{0}%", "operator": "like"}}
                            ], "type": "OR"}},
                        {{"subfilters": [
                            {{"subfilters": [], "property": "description", "value": "%{1}%", "operator": "like"}}
                            ], "type": "OR"}}                       
                        ], "type": "AND"}},
                    {{"subfilters": [], "property": "category", "operator": "IN",
                            "value": ["/api/part_categories/9", "/api/part_categories/37",
                            "/api/part_categories/10", "/api/part_categories/12",
                            "/api/part_categories/11"]}}
                   ]'''.format(capacitor.farads_to_string(part['Capacitance']),
                               part['Dielectric Type']).replace("\n", "").replace(" ", "")
        }
        # print(params)
        response = self.__partkeepr_api_call('get', '/api/parts', params=params)
        response = response.json()
        if len(response["hydra:member"]) > 0:
            found = []
            for component in response["hydra:member"]:
                decoded_part = self.decode_product_dictionary(component)
                if "Voltage" in decoded_part['Parameters'] and part['Voltage'] is not None:
                    if decoded_part['Parameters']['Voltage'] >= part['Voltage']:
                        found.append(decoded_part)
                else:
                    found.append(decoded_part)
            return found

    def __find_by_MPN(self, manufacturer_part_number):
        params = {
            'filter':
                '{{"property":"name","operator":"like","value":"%{}%"}}'.format(manufacturer_part_number)
        }
        response = self.__partkeepr_api_call('get', '/api/parts', params=params)
        response = response.json()
        #print(json.dumps(response, indent=4))
        if len(response["hydra:member"]) > 0:
            parts = []
            for component in response["hydra:member"]:
                parts.append(self.decode_product_dictionary(component))
            return parts

    def decode_product_dictionary(self, product):
        links = {'ProductInformationPage': 'https:',
                 'Photo': 'https:', 'Thumbnail': 'https:'}
        description = product['description']
        try:
            manufacturer = product['manufacturers'][0]
            #print(json.dumps(manufacturer, indent=4))
            manufacturer_name = manufacturer['manufacturer']['name']
            manufacturer_part_number = manufacturer['partNumber']
        except (TypeError, IndexError):
            manufacturer_name = "Unknown"
            manufacturer_part_number = "Unknown"

        parameters = self.decode_part_parameters(product['parameters'])
        parameters['Manufacturer'] = manufacturer_name
        parameters['Manufacturer Part Number'] = manufacturer_part_number
        parameters['Storage Location'] = self.__extract_part_location(product)
        symbol = {'Name': product['name']}
        # MinAmount and Multiples fields in order info are present for compatibility with other distributors
        order_info = {'MinAmount': 1, 'Multiples': 1, 'StockCount': product['stockLevel']}
        price_list = [{'Amount': 1, 'Price': self.__extract_part_price(product)}]
        response = {'Links': links, 'Description': description, 'Symbol': symbol, 'OrderInfo': order_info,
                    'Parameters': parameters, 'PriceRanges': price_list}
        return response

    def decode_part_parameters(self, parameters):
        encoded_parameters = {}
        for parameter in parameters:
            name = parameter['name']
            if name not in ["Altium PcbLib", "Altium SchLib", "Invoice Number"]:
                if name == "Voltage":
                    encoded_parameters[name] = self.__extract_part_parameter_voltage(parameter)
                elif name == "Capacitance":
                    encoded_parameters[name] = self.__decode_part_numeric_parameter(parameter)
                elif name == "Tolerance":
                    encoded_parameters[name] = self.__decode_part_numeric_parameter(parameter)
                elif name == "Resistance":
                    encoded_parameters[name] = self.__decode_part_numeric_parameter(parameter)
                else:
                    if parameter["valueType"] == "string":
                        encoded_parameters[name] = parameter["stringValue"]
                    else:
                        encoded_parameters[name] = self.__decode_part_numeric_parameter_to_string(parameter)
        return encoded_parameters

    def __extract_part_price(self, part):
        """
        :param part: PartKeepr API response, content of ["hydra:member"] for particular part
        :return: int price if is available in other case 0
        """
        try:
            distributor = part["distributors"]
            if len(distributor) == 1:
                distributor = distributor[0]
                price = distributor['price']
                if price is None:
                    return 0
                else:
                    return price
        except IndexError:
            return 0

    def __extract_part_location(self, part):
        """
        :param part: PartKeepr API response, content of ["hydra:member"] for particular part
        :return: string representing part location
        """
        return part['storageLocation']['name']

    def __extract_part_parameter_voltage(self, parameter):
        """
        :param part: PartKeepr API response, content of 'parameter' field for particular part
        :return:
        """
        if parameter['name'] != "Voltage":
            raise
        voltage = self.__decode_part_numeric_parameter(parameter)
        return voltage

    def __decode_part_numeric_parameter(self, parameter):
        if parameter['valueType'] != 'numeric':
            raise
        if parameter['value'] is not None:
            value = Decimal(parameter['value'])
            if parameter['siPrefix'] is not None:
                base = Decimal(parameter['siPrefix']['base'])
                exponent = Decimal(parameter['siPrefix']['exponent'])
                multiplier = base ** exponent
                value = value * multiplier
            return value

    def __decode_part_numeric_parameter_to_string(self, parameter):
        if parameter['valueType'] != 'numeric':
            raise
        value = str(parameter['value'])
        if parameter['siPrefix'] is not None:
            value = value + parameter['siPrefix']['symbol'] + parameter['unit']['symbol']
        return value

    def __partkeepr_api_call(self, method, url, **kwargs):
        """calls Partkeepr API

        :method: request method
        :url: part of the url to call (without base)
        :data: data to pass to the request if any
        :returns: requests object

        """
        try:
            r = requests.request(
                method,
                self.url + url,
                **kwargs,
                auth=HTTPBasicAuth(self.user, self.password),
                verify=False
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        return r
