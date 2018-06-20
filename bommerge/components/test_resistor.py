import unittest
import resistor
from decimal import *

class TestResistor(unittest.TestCase):
    def test_conversion(self):
        self.assertEqual(resistor.convert_resistance_to_ohms('1m'), Decimal('0.001'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1m\u03a9'), Decimal('0.001'))

        self.assertEqual(resistor.convert_resistance_to_ohms('0'), Decimal('0'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1'), Decimal('1'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1R'), Decimal('1'))
        self.assertEqual(resistor.convert_resistance_to_ohms(u'1\u03a9'), Decimal('1'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1k'), Decimal('1000'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1k\u03a9'), Decimal('1000'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1M'), Decimal('1000000'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1M\u03a9'), Decimal('1000000'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1G'), Decimal('1000000000'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1G\u03a9'), Decimal('1000000000'))
        # test fractionals 
        self.assertEqual(resistor.convert_resistance_to_ohms('1m1'), Decimal('0.0011'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1m\u03a91'), Decimal('0.0011'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1R1'), Decimal('1.1'))
        self.assertEqual(resistor.convert_resistance_to_ohms(u'1\u03a91'), Decimal('1.1'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1k1'), Decimal('1100'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1k\u03a91'), Decimal('1100'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1M1'), Decimal('1100000'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1M\u03a91'), Decimal('1100000'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1G1'), Decimal('1100000000'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1G\u03a91'), Decimal('1100000000'))
        # 
        self.assertEqual(resistor.convert_resistance_to_ohms('1.1m'), Decimal('0.0011'))
        self.assertEqual(resistor.convert_resistance_to_ohms(u'1.1m\u03a9'), Decimal('0.0011'))
                
        self.assertEqual(resistor.convert_resistance_to_ohms('1.1R'), Decimal('1.1'))
        self.assertEqual(resistor.convert_resistance_to_ohms(u'1.1\u03a9'), Decimal('1.1'))        

        self.assertEqual(resistor.convert_resistance_to_ohms('1.1k'), Decimal('1100'))
        self.assertEqual(resistor.convert_resistance_to_ohms('1.1kR'), Decimal('1100'))
        self.assertEqual(resistor.convert_resistance_to_ohms(u'1.1k\u03a9'), Decimal('1100'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1.1M'), Decimal('1100000'))
        self.assertEqual(resistor.convert_resistance_to_ohms(u'1.1M\u03a9'), Decimal('1100000'))

        self.assertEqual(resistor.convert_resistance_to_ohms('1.1G'), Decimal('1100000000'))
        self.assertEqual(resistor.convert_resistance_to_ohms(u'1.1G\u03a9'), Decimal('1100000000'))

    def test_conversion_decimal_to_str(self):
        self.assertEqual(resistor.ohms_to_string(Decimal('0.0001')), u'100u\u03a9')
        self.assertEqual(resistor.ohms_to_string(Decimal('0.1')), u'100m\u03a9')
        self.assertEqual(resistor.ohms_to_string(Decimal('0')), u'0\u03a9')
        self.assertEqual(resistor.ohms_to_string(Decimal('1')), u'1\u03a9')
        self.assertEqual(resistor.ohms_to_string(Decimal('1000')), u'1k\u03a9')
        self.assertEqual(resistor.ohms_to_string(Decimal('1000000')), u'1M\u03a9')
        self.assertEqual(resistor.ohms_to_string(Decimal('1000000000')), u'1G\u03a9')


if __name__ == "__main__":
    unittest.main()

