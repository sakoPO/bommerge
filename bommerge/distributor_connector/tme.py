from components import resistor
import collections, urllib, base64, hmac, hashlib, urllib2, json

def api_call(action, params, token, app_secret, show_header=False):
    api_url = 'https://api.tme.eu/' + action + '.json';
    params['Token'] = token;

    params = collections.OrderedDict(sorted(params.items()));
    print params
    encoded_params = urllib.urlencode(params, '')
    
    signature_base = 'POST' + '&' + urllib.quote(api_url, '') + '&' + urllib.quote(encoded_params, '')
    
    api_signature = base64.encodestring(hmac.new(app_secret, signature_base, hashlib.sha1).digest()).rstrip();
    params['ApiSignature'] = api_signature;

    opts = {
        'http': {
            'method' : 'POST',
            'header' : 'Content-type: application/x-www-form-urlencoded',
            'content' : urllib.urlencode(params)
        }
    };

    http_header = {
        "Content-type": "application/x-www-form-urlencoded",
    };

    # create your HTTP request
    req = urllib2.Request(api_url, urllib.urlencode(params), http_header);

    # submit your request
    res = urllib2.urlopen(req);
    html = res.read();

    return html;
################################################################


def show_found():
    found = find_component()
    
    for component in found['Data']['ProductList']:
        print(component['Symbol'] + " : " + component['OriginalSymbol'] + " : " + component['Producer'])


def decode_product_dictionary(product):
    links = {'ProductInformationPage': 'https:' + product['ProductInformationPage'], 'Photo': 'https:' + product['Photo'], 'Thumbnail': 'https:' + product['Thumbnail']}
    description = product['Description']
    symbol = {'Symbol': product['OriginalSymbol'], 'SymbolTME': product['Symbol']}
    manufacturer = product['Producer']
    order_info = {'MinAmount': product['MinAmount'], 'Multiples': product['Multiples']}
    response = {'Links': links, 'Description': description, 'Symbol': symbol, 'OrderInfo': order_info, 'Parameters': {'Manufacturer': manufacturer, 'Manufacturer Part Number': symbol['Symbol']}}
    return response


class _api:
    def __init__(self, token, app_secret, language = 'EN', country = 'PL', currency = 'PLN'):
        self.token = token
        self.app_secret = app_secret
        self.language = language
        self.country = country
        self.currency = currency

    def search(self, search_text, category=None, on_stock=None, result_page=None,  parameters=None, search_order=None, search_order_type=None):
        params = self._encode_search_parameters(search_text, category, result_page, on_stock, parameters, search_order, search_order_type)
        response = self._api_call('Products/Search', params, True)
        response = json.loads(response)
        if response['Status'] == "OK" and len(response['Data']['ProductList']) != 0:
            return response['Data']


    def searchParameter(self, search_text, category=None, on_stock=None, result_page=None,  parameters=None, search_order=None, search_order_type=None):
        params = self._encode_search_parameters(search_text, category, result_page, on_stock, parameters, search_order, search_order_type)
        response = self._api_call('Products/SearchParameters', params, True)
        response = json.loads(response)
        if response['Status'] == "OK":
            return response['Data']['ParametersList']


    def autocomplete(self, component):
        params = {           
            'Country': self.country,
            'Language': self.language,
            'Phrase': component
        }
        response = self._api_call('Products/Autocomplete', params, True)
        response = json.loads(response)
        if response['Status'] == "OK":
            return response['Data']['Result']


    def get_categories(self, category_id = None, tree = None):
        params = {
            'Language': self.language,
            'Country': self.country             
        }
        if category_id:
            params['CategoryId'] = category_id
        if tree and tree == False:
            params['Tree'] = 'False'
        response = self._api_call('Products/GetCategories', params, True)
        response = json.loads(response)
        if response['Status'] == "OK":
            return response['Data']['CategoryTree']


    def get_delivery_time(self):
        raise RuntimeError('Unimplemented')


    def get_prices(self):
        raise RuntimeError('Unimplemented')


    def get_parameters(self, components):
        params = {
            'Country': 'PL',
            'Currency': 'PLN',
            'Language': 'EN',
        }
        result = self._encode_symbol_list(components)
        for key in result.keys():
            params[key] = result[key]
        response = self._api_call('Products/GetParameters', params, True)
        response = json.loads(response)
        if response['Status'] == "OK":
            return response['Data']['ProductList']


    def get_prices_and_stocks(self, components):            
        params = {         
            'Country': 'PL',
            'Currency': 'PLN',
            'Language': 'PL',
        }
        result = self._encode_symbol_list(components)
        for key in result.keys():
            params[key] = result[key]
            
        response = self._api_call('Products/GetPricesAndStocks', params, True)
        response = json.loads(response)
        if response['Status'] == "OK":
            return response['Data']


    def get_products(self, components):
        params = {
            'Country': 'PL',          
            'Language': 'EN'
        }        
        result = self._encode_symbol_list(components)
        for key in result.keys():
            params[key] = result[key]

        response = self._api_call('Products/GetProducts', params, True)
        response = json.loads(response)
        if response['Status'] == "OK":
            return response['Data']['ProductList']


    def get_product_files(self, components):
        raise RuntimeError('Unimplemented')


    def get_stocks(self, components):
        raise RuntimeError('Unimplemented')


    def get_symbols(self, category_id):
        params = {
            'Country': 'PL',          
            'Language': 'EN',
            'CategoryId' : category_id
        }        
        response = self._api_call('Products/GetSymbols', params, True)
        response = json.loads(response)
        if response['Status'] == "OK":
            return response['Data']['SymbolList']


    def get_similar_products(self):
        raise RuntimeError('Unimplemented')


    def get_related_products(self):
        raise RuntimeError('Unimplemented')


    def check_api_status(self):
        params = None
        response = self._api_call('Utils/Ping', params, True)
        response = json.loads(response);
        expected_answer = {"Status": "OK", "Data":{"PONG": "PING-PONG"}}        
        return response == expected_answer


    def _api_call(self, action, params, show_header=False):
        return api_call(action, params, self.token, self.app_secret, show_header)


    def _encode_search_parameters(self, search_text, category, result_page, on_stock, parameters, search_order, search_order_type):
        def encode(parameter_id, value_id):
            result = {}
            for i, value in enumerate(value_id):
                key = 'SearchParameter[' + str(parameter_id) + '][' + str(i) + ']'
                result[key] = value
            return result

        params = {           
            'Country': self.country,
            'Currency': self.currency,
            'Language': self.language,
        }
        
        if search_text:
            params['SearchPlain'] = search_text
        if category:
            params['SearchCategory'] = category
        if result_page:
            params['SearchPage'] = result_page
        if on_stock and on_stock == True:
            params['SearchWithStock'] = 'True'
        if parameters:
            print parameters
            for parameter in parameters:     
                result = encode(parameter['id'], parameter['values'])
                for key in result:
                    params[key] = result[key]
        if search_order:
            params['SearchOrder'] = search_order
        if search_order_type:
            params['SearchOrderType'] = search_order_type
        return params


    def _encode_symbol_list(self, components):
        result = {}
        for i, value in enumerate(components):
            key = 'SymbolList[' + str(i) + ']'
            result[key] = value
        return result

def get_capacitance_id(capacitance, parameters):
    for parameter in parameters:
        if parameter['Name'] == 'Capacitance':
            for value in parameter['Values']:
                if value['ValueName'].replace(u"\u00B5", 'u') == capacitance:
                    return {'parameter_id': parameter['ParameterId'], 'value_ids': value['ValueId']}

def get_resistance_id(resistance, parameters):
    for parameter in parameters:
        if parameter['Name'] == 'Resistance':
            for value in parameter['Values']:
                param = resistor.convertResistanceToOhms(value['ValueName'])
                expected = resistor.convertResistanceToOhms(resistance)
                if param == None or expected == None:
                    print value['ValueName']
                    print resistance
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
                    return {'parameter_id': parameter['ParameterId'], 'value_ids': value['ValueId']}                    
  
def get_dielectric_id(dielectric, parameters):
    for parameter in parameters:
        if parameter['Name'] == 'Dielectric':
            for value in parameter['Values']:
                if value['ValueName'] == dielectric:
                    return {'parameter_id': parameter['ParameterId'], 'value_ids': value['ValueId']}                    

    
#-------------------------------------------------------
class TME:
    def __init__(self, token, app_secret):
        self.tme = _api(token, app_secret)


    def get_voltage_id(self, voltage, parameters):
        for parameter in parameters:
            if parameter['Name'] == 'Operating voltage':
                for value in parameter['Values']:
                    if value['ValueName'] == voltage:
                        return parameter['ParameterId'], value['ValueId']


    def find_capacitor_by_parameters(self, capacitor):
        from time import sleep
   #     case_to_id = {'0201': '113537', '0402': '100568', '0603': '100558', '0805': '100559', '1206': '112338', '1210': '113185', '1812': '113186', '2020': '113187'}
        capacitors_category_id = '26'
   #     if capacitor['Case']:
   #         case_id = case_to_id[capacitor['Case']]
   #     else:
        case_id = capacitors_category_id

        parameters = self.tme.searchParameter(None, category=capacitors_category_id, on_stock=True)
        param = []
        if parameters:     
            filters = get_capacitance_id(capacitor['Capacitance'], parameters)
            if filters:
                param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
            if capacitor['Case']:
                filters = get_case_id(capacitor['Case'], parameters)
                if filters:
                    param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
            if capacitor['Voltage']:
                parameterid, valueid = self.get_voltage_id(capacitor['Voltage'], parameters)
                if parameterid:
                    param.append({'id': parameterid, 'values': [valueid]})
            if capacitor['Dielectric Type']:
                filters = get_dielectric_id(capacitor['Dielectric Type'], parameters)
                if filters:
                    param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
        
        result = self.tme.search(None, category=capacitors_category_id, on_stock=True, parameters=param)
        if result and len(result) != 0:
            print("Found: " + str(result['Amount']))
            tmp = []
            for product in result['ProductList']:
                part = decode_product_dictionary(product)

                stock = self.get_stock_and_prices([part['Symbol']['SymbolTME']])
                stock = stock[0]
                part['OrderInfo']['StockCount'] = stock['StockCount']
                part['PriceRanges'] = stock['PriceList']
                
                parameters = self.tme.get_parameters([part['Symbol']['SymbolTME']])
                parameters = parameters[0]
                for parameter in parameters['ParameterList']:
                    print parameter
                    part['Parameters'][parameter['ParameterName']] = parameter["ParameterValue"]

                tmp.append(part)
            return tmp
        else:
            print result
            
    def find_resistor_by_parameters(self, resistor):
        from time import sleep
        resistors_category_id = '100299'
        case_id = resistors_category_id
        
        parameters = self.tme.searchParameter(None, category=resistors_category_id, on_stock=True)
        param = []
        if parameters:     
            filters = get_resistance_id(resistor['Resistance'], parameters)
            if filters:
                param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
            if resistor['Case']:
                filters = get_case_id(resistor['Case'], parameters)
                if filters:
                    param.append({'id': filters['parameter_id'], 'values': [filters['value_ids']]})
       #     if resistor['Tolerance']:
       #         parameterid, valueid = self.get_tolerance_id(resistor['Tolerance'], parameters)
       #         if parameterid:
       #             param.append({'id': parameterid, 'values': [valueid]})
        try:           
            result = self.tme.search(None, category=resistors_category_id, on_stock=True, parameters=param)
        except:
            result = None        
        if result and len(result) != 0:
            print("Found: " + str(result['Amount']))
            tmp = []
            for product in result['ProductList']:
                part = decode_product_dictionary(product)

                stock = self.get_stock_and_prices([part['Symbol']['SymbolTME']])
                stock = stock[0]
                part['OrderInfo']['StockCount'] = stock['StockCount']
                part['PriceRanges'] = stock['PriceList']
                
                parameters = self.tme.get_parameters([part['Symbol']['SymbolTME']])
                parameters = parameters[0]
                for parameter in parameters['ParameterList']:
                    print parameter
                    part['Parameters'][parameter['ParameterName']] = parameter["ParameterValue"]

                tmp.append(part)
            return tmp
        else:
            print result


    def find_component(self, components):
        response = None#self.get_products(components)
        if not response:
            response = self.search(components)
        if not response:
            return
        
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
                payment_info = {'Currency': response['Currency'], 'PriceType': response['PriceType'], 'VatRate': product['VatRate']}
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

