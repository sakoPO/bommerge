from decimal import *


class OrderInfo:
    def __init__(self):
        self.quantity = 0  # quantity to be ordered
        self.price = 0  # price for quantity
        self.distributor_name = "None"
        self.distributor_order_number = None


class Component:
    def __init__(self, parameters, quantity, distributors):
        self.parameters = parameters
        self.quantity = quantity
        self.distributors = distributors
        self.order_info = OrderInfo()
        self.combined_parameters = None

    def __getitem__(self, key):
        if key in self.parameters:
            return self.parameters[key]
        if key == "Quantity":
            return self.quantity
        raise KeyError

    def __contains__(self, item):
        if item == "Quantity":
            return True
        if item in self.parameters:
            return True
        print("Item not found: ", item)
        return False

    def __repr__(self):
        return self.parameters["Designator"]

    def update_order_info(self, quantity, distributor_name, distributor_component_index):
        if distributor_name == "None":
            self.order_info.distributor_name = "None"
            self.order_info.price = 0
            self.order_info.quantity = 0
            self.order_info.distributor_order_number = None
        else:
            self.order_info.price = self.get_price(quantity, distributor_name, distributor_component_index)
            self.order_info.quantity = quantity
            self.order_info.distributor_name = distributor_name
            if distributor_name == "TME":
                self.order_info.distributor_order_number = \
                    self.distributors[distributor_name][distributor_component_index]["Symbol"]["SymbolTME"]

    def get_price(self, quantity, distributor_name, distributor_component_index):
        price_ranges = self.distributors[distributor_name][distributor_component_index]["PriceRanges"]
        if len(price_ranges) > 0:
            for price in reversed(price_ranges):
                if quantity >= price['Amount']:
                    if price['Price'] is not None:
                        return Decimal(price['Price']) * quantity
                    else:
                        return 0
        else:
            return 0
        print(distributor_name, distributor_component_index)
        raise RuntimeError("Unable to match price range. Required quantity: " + str(quantity))
