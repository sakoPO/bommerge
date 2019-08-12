try:
    from components import resistor
    from components import capacitor
    from components import voltage
    from components import tolerance
except:
    from bommerge.components import resistor
    from bommerge.components import capacitor
    from bommerge.components import voltage
    from bommerge.components import tolerance
from .tme_base import _api


def show_found():
    found = find_component()

    for component in found['Data']['ProductList']:
        print(component['Symbol'] + " : " + component['OriginalSymbol'] + " : " + component['Producer'])


def decode_product_dictionary(product):
    links = {'ProductInformationPage': 'https:' + product['ProductInformationPage'],
             'Photo': 'https:' + product['Photo'], 'Thumbnail': 'https:' + product['Thumbnail']}
    description = product['Description']
    symbol = {'Symbol': product['OriginalSymbol'], 'SymbolTME': product['Symbol']}
    manufacturer = product['Producer']
    order_info = {'MinAmount': product['MinAmount'], 'Multiples': product['Multiples']}
    response = {'Links': links, 'Description': description, 'Symbol': symbol, 'OrderInfo': order_info,
                'Parameters': {'Manufacturer': manufacturer, 'Manufacturer Part Number': symbol['Symbol']}}
    return response


def split_list(l, n):
    """Yield successive n-sized chunks from l."""
    try:
        for i in xrange(0, len(l), n):
            yield l[i:i + n]
    except:
        for i in range(0, len(l), n):
            yield l[i:i + n]


def get_capacitance_id(capacitance, parameters):
    """
    :param capacitance: capacitance in Farads, type: Decimal
    :param parameters:
    :return:
    """
    for parameter in parameters:
        if parameter['Name'] == 'Capacitance':
            for value in parameter['Values']:
                if capacitor.convert_capacitance_co_farads(value['ValueName']) == capacitance:
                    return {'parameter_id': parameter['ParameterId'], 'value_ids': value['ValueId']}


def get_resistance_id(resistance, parameters):
    """
    :param resistance: resistance in Ohms, type: Decimal
    :param parameters:
    :return:
    """
    for parameter in parameters:
        if parameter['Name'] == 'Resistance':
            for value in parameter['Values']:
                param = resistor.convert_resistance_to_ohms(value['ValueName'])
                expected = resistance
                if param == None or expected == None:
                    print(value['ValueName'])
                    print(resistance)
                    raise RuntimeError("Unable to convert: " + value['ValueName'])
                if param == expected:
                    return {'parameter_id': parameter['ParameterId'], 'value_ids': value['ValueId']}


def get_tolerance_id(tolerance, parameters):
    for parameter in parameters:
        if parameter['Name'] == 'Tolerance':
            for value in parameter['Values']:
                if value['ValueName'] == tolerance:
                    return {'parameter_id': parameter['ParameterId'], 'value_ids': value['ValueId']}


def get_case_id(case, parameters):
    for parameter in parameters:
        if parameter['Name'] == 'Case - inch':
            for value in parameter['Values']:
                if value['ValueName'] == case:
                    print(str(value['ValueName']) + " " + str(value['ValueId']))
                    return {'parameter_id': parameter['ParameterId'], 'value_ids': value['ValueId']}


def get_dielectric_id(dielectric, parameters):
    for parameter in parameters:
        if parameter['Name'] == 'Dielectric':
            for value in parameter['Values']:
                if value['ValueName'] == dielectric:
                    return {'parameter_id': parameter['ParameterId'], 'value_ids': value['ValueId']}

                # -------------------------------------------------------


class TME:
    def __init__(self, token, app_secret):
        self.name = "TME"
        self.tme = _api(token, app_secret)

    def get_voltage_id(self, voltage_value, parameters):
        for parameter in parameters:
            if parameter['Name'] == 'Operating voltage':
                for value in parameter['Values']:
                    if voltage.string_to_voltage(value['ValueName']) == voltage_value:
                        return parameter['ParameterId'], value['ValueId']

    def build_products_data(self, product_list):
        def get_component_by_symbol(components, symbol):
            for component in components:
                if component['Symbol']['SymbolTME'] == symbol:
                    return component
            print("Unable to found component: " + symbol)

        components = []
        tme_symbols = []
        for product in product_list:
            part = decode_product_dictionary(product)
            tme_symbols.append(part['Symbol']['SymbolTME'])
            components.append(part)

        tme_symbols_chunks = list(split_list(tme_symbols, 50))

        for tme_symbols in tme_symbols_chunks:
            print('requesting stock and price: ' + str(tme_symbols))
            stock = self.get_stock_and_prices(tme_symbols)
            for stock_data in stock:
                component = get_component_by_symbol(components, stock_data['Symbol'])
                component['OrderInfo']['StockCount'] = stock_data['StockCount']
                component['PriceRanges'] = stock_data['PriceList']

        for tme_symbols in tme_symbols_chunks:
            print('requesting parameters for components: ' + str(tme_symbols))
            parameters = self.tme.get_parameters(tme_symbols)
            for product in parameters:
                component = get_component_by_symbol(components, product['Symbol'])
                for parameter in product['ParameterList']:
                    if parameter['ParameterName'] == 'Voltage':
                        component['Parameters'][parameter['ParameterName']] = voltage.string_to_voltage(
                            parameter["ParameterValue"])
                    elif parameter['ParameterName'] == 'Capacitance':
                        component['Parameters'][parameter['ParameterName']] = capacitor.convert_capacitance_co_farads(
                            parameter["ParameterValue"])
                    elif parameter['ParameterName'] == 'Resistance':
                        component['Parameters'][parameter['ParameterName']] = resistor.convert_resistance_to_ohms(
                            parameter["ParameterValue"])
                    elif parameter['ParameterName'] == 'Tolerance':
                        component['Parameters'][parameter['ParameterName']] = tolerance.string_to_tolerance(
                            parameter["ParameterValue"])
                    else:
                        component['Parameters'][parameter['ParameterName']] = parameter["ParameterValue"]
        return components

    def _search(self, parameters, category):
        try:
            result = self.tme.search(None, category=category, on_stock=True, parameters=parameters)
        except:
            print("exception during tme search")
            return None
        if result:
            if result['Amount'] > len(result["ProductList"]):
                pages_count = int((result['Amount'] / 20) + 1 if (result['Amount'] % 20) != 0 else 0)
                print("Pages count: " + str(pages_count))
                for page_number in range(2, pages_count + 1):
                    found = self.tme.search(None, category=category, on_stock=True, parameters=parameters,
                                            result_page=page_number)
                    result["ProductList"] = result["ProductList"] + found["ProductList"]
        return result

    def find_capacitor_by_parameters(self, capacitor):
        """
        :param capacitor: dictionary with fields:
                'Capacitance': int in Farads,
                'Case': string
                'Voltage': int in Volts
                'Dielectric Type': string ie.: X7R, NP0 etc.
        :return:
        """

        def select_filters(parameters, part):
            param = []
            if parameters:
                filters = get_capacitance_id(part['Capacitance'], parameters)
                if filters:
                    param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
                if capacitor['Case']:
                    filters = get_case_id(part['Case'], parameters)
                    if filters:
                        param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
                if capacitor['Voltage']:
                    parameterid, valueid = self.get_voltage_id(part['Voltage'], parameters)
                    if parameterid:
                        param.append({'id': parameterid, 'values': [valueid]})
                if capacitor['Dielectric Type']:
                    filters = get_dielectric_id(part['Dielectric Type'], parameters)
                    if filters:
                        param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
            return param

        capacitors_category_id = '26'
        case_id = capacitors_category_id

        parameters = self.tme.searchParameter(None, category=capacitors_category_id, on_stock=True)
        param = select_filters(parameters, capacitor)
        result = self._search(param, capacitors_category_id)
        if result and len(result) != 0:
            print(
                "Found: " + str(result['Amount']) + ", len(result['ProductList']) = " + str(len(result['ProductList'])))
            return self.build_products_data(result['ProductList'])
        else:
            print(result)

    def find_resistor_by_parameters(self, resistor):
        """
        :param resistor: dictionary with fields:
                'Resistance': Decimal in Ohms,
                'Case': string
                'Tolerance': percent as integer
        :return:
        """

        def select_filters(parameters, resistor):
            if not parameters:
                return []
            param = []
            filters = get_resistance_id(resistor['Resistance'], parameters)
            if filters:
                param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
            if resistor['Case']:
                filters = get_case_id(resistor['Case'], parameters)
                if filters:
                    param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
            if resistor['Tolerance']:
                filters = get_tolerance_id(resistor['Tolerance'], parameters)
                if filters:
                    param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
            return param

        resistors_category_id = '100299'
        parameters = self.tme.searchParameter(None, category=resistors_category_id, on_stock=True)
        param = select_filters(parameters, resistor)
        result = self._search(param, resistors_category_id)
        if result and len(result) != 0:
            print(
                "Found: " + str(result['Amount']) + ", len(result['ProductList']) = " + str(len(result['ProductList'])))
            return self.build_products_data(result['ProductList'])
        else:
            print(result)

    def find_component(self, components):
        response = None  # self.get_products([components])
        if not response:
            response = self.search(components)
        if not response:
            return

        #        if response and len(response) != 0:
        #         print("Found: " + str(response['Amount']) + ", len(result['ProductList']) = " + str(len(response)))
        #         return self.build_products_data(result['ProductList'])

        for part in response:
            stock = self.get_stock_and_prices([part['Symbol']['SymbolTME']])
            stock = stock[0]
            part['OrderInfo']['StockCount'] = stock['StockCount']
            part['PriceRanges'] = stock['PriceList']
        return response

    def get_stock_and_prices(self, components):
        response = self.tme.get_prices_and_stocks(components)
        if response:
            stock_and_price = []
            for product in response['ProductList']:
                payment_info = {'Currency': response['Currency'], 'PriceType': response['PriceType'],
                                'VatRate': product['VatRate']}
                price_list = []
                for price in product['PriceList']:
                    price_list.append({'Amount': price['Amount'], 'Price': price['PriceValue']})
                symbol = product['Symbol']
                stock_count = product['Amount']
                stock_and_price.append({'Symbol': symbol, 'StockCount': stock_count, 'PriceList': price_list})
            return stock_and_price

    def search(self, components):
        response = self.tme.search(components)
        if response and len(response) != 0:
            products = []
            for part in response['ProductList']:
                products.append(decode_product_dictionary(part))
            return products

    def get_products(self, components):
        product_list = self.tme.get_products(components)
        if product_list:
            result = []
            for product in product_list:
                result.append(decode_product_dictionary(product))
            return result

    def dump_categories(self):
        categories = self.tme.get_categories(tree=False)
        with open('categories.dump.json', 'w') as outfile:
            outfile.write(json.dumps(categories, indent=4, sort_keys=True, separators=(',', ': ')))


def do_tests():
    pass


if __name__ == '__main__':
    do_tests()
