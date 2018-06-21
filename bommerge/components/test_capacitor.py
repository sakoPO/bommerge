import unittest
import capacitor
from decimal import *


class TestCapacitor(unittest.TestCase):
    def test_conversion_str_to_decimal(self):
        self.assertEqual(capacitor.convert_capacitance_co_farads('1fF'), Decimal('0.000000000000001'))

        self.assertEqual(capacitor.convert_capacitance_co_farads('1pF'), Decimal('0.000000000001'))

        self.assertEqual(capacitor.convert_capacitance_co_farads('1nF'), Decimal('0.000000001'))
        self.assertEqual(capacitor.convert_capacitance_co_farads('100nF'), Decimal('0.0000001'))

        self.assertEqual(capacitor.convert_capacitance_co_farads('1uF'), Decimal('0.000001'))

        self.assertEqual(capacitor.convert_capacitance_co_farads('1mF'), Decimal('0.001'))

        self.assertEqual(capacitor.convert_capacitance_co_farads('0'), 0)
        self.assertEqual(capacitor.convert_capacitance_co_farads('1'), 1)
    
        self.assertEqual(capacitor.convert_capacitance_co_farads('1fF1'), Decimal('0.0000000000000011'))

        self.assertEqual(capacitor.convert_capacitance_co_farads('1pF1'), Decimal('0.0000000000011'))

        self.assertEqual(capacitor.convert_capacitance_co_farads('1nF1'), Decimal('0.0000000011'))

        self.assertEqual(capacitor.convert_capacitance_co_farads('1uF1'), Decimal('0.0000011'))

        self.assertEqual(capacitor.convert_capacitance_co_farads('1mF1'), Decimal('0.0011'))


    def test_conversion_decimal_to_str(self):
        self.assertEqual(capacitor.farads_to_string(Decimal('0.0000000001')), '100pF')
        self.assertEqual(capacitor.farads_to_string(Decimal('0.0000001')), '100nF')
        self.assertEqual(capacitor.farads_to_string(Decimal('0.0001')), '100uF')
        self.assertEqual(capacitor.farads_to_string(Decimal('0.1')), '100mF')
        self.assertEqual(capacitor.farads_to_string(Decimal('1')), '1F')
        self.assertEqual(capacitor.farads_to_string(Decimal('1000')), '1kF')


if __name__ == "__main__":
    unittest.main()

