import collections, urllib, base64, hmac, hashlib,  json
try:
    from urllib import urlencode
    from urllib import quote
    import urllib2 as urlrequest
    from urllib2 import urlopen as urlopen
except:
    from urllib.parse import urlencode, quote
    import urllib.request as urlrequest
    from urllib.request import urlopen

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def cmp(a, b):
    return (a > b) - (a < b)

def api_call(action, params, token, app_secret, show_header=False):   
    def cmp_key (a,b):
        if 'SymbolList[' in a[0] and 'SymbolList[' in b[0]:        
            return cmp(int(a[0][11:len(a[0])-1]), int(b[0][11:len(b[0])-1]))
        elif 'SearchParameter[' in a[0] and 'SearchParameter[' in b[0]:
            return cmp(int(a[0][16:len(a[0])-4]), int(b[0][16:len(b[0])-4]))
        else:
            return (a[0].lower() > b[0].lower()) - (a[0].lower() < b[0].lower())
        
    api_url = 'https://api.tme.eu/' + action + '.json';
    params['Token'] = token;

    params = collections.OrderedDict(sorted(params.items(), key=cmp_to_key(cmp_key)))
    print(params)
    encoded_params = urlencode(params, '')
    
    signature_base = 'POST' + '&' + quote(api_url, '') + '&' + quote(encoded_params, '')
    
    api_signature = base64.encodestring(hmac.new(app_secret.encode('ascii'), signature_base.encode('ascii'), hashlib.sha1).digest()).rstrip();
    params['ApiSignature'] = api_signature;

    opts = {
        'http': {
            'method' : 'POST',
            'header' : 'Content-type: application/x-www-form-urlencoded',
            'content' : urlencode(params)
        }
    };

    http_header = {
        "Content-type": "application/x-www-form-urlencoded",
    };

    # create your HTTP request
    req = urlrequest.Request(api_url, urlencode(params).encode('ascii'), http_header);

    # submit your request
    res = urlopen(req);
    html = res.read();

    return html.decode('utf-8');


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
        if len(components) > 50:
            raise RuntimeError("Components count to big. get_parameters function can read parameters up to 50 components, requested " + str(len(components)))
        params = {
            'Country': self.country,
            'Currency': 'PLN',
            'Language': self.language,
        }
        result = self._encode_symbol_list(components)
        for key in result.keys():
            params[key] = result[key]
        response = self._api_call('Products/GetParameters', params, True)
        response = json.loads(response)
        if response['Status'] == "OK":
            return response['Data']['ProductList']


    def get_prices_and_stocks(self, components):
        if len(components) > 50:
            raise RuntimeError("Components count to big. get_prices_and_stocks function can read stock data up to 50 components, requested " + str(len(components)))
        params = {         
            'Country': self.country,
            'Currency': 'PLN',
            'Language': self.language,
        }
        result = self._encode_symbol_list(components)
        for key in result.keys():
            params[key] = result[key]
            
        response = self._api_call('Products/GetPricesAndStocks', params, True)
        response = json.loads(response)
        if response['Status'] == "OK":
            return response['Data']


    def get_products(self, components):
        if len(components) > 50:
            raise RuntimeError("Components count to big. get_products function can get up to 50 components, requested " + str(len(components)))        
        params = {
            'Country': self.country,          
            'Language': self.language
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
            'Country': self.country,          
            'Language': self.language,
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
            #print parameters
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

                  

    
