import unittest
from partnameDecoder import capacitors

class TestCapacitorPartnameResolver(unittest.TestCase):
    def test_murata_GRT(self):
        pass
        

    def test_murata_GCM(self):
        part = capacitors.resolve('GCM155R71C104KA55D')
        component = {}
        component['Series'] = 'GCM'
        component['Case'] = '0402'
        component['Height'] = '0.5mm'
        component['Dielectric Type'] = 'X7R'
        component['Voltage'] = '16V'
        component['Capacitance'] = '100nF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)
        #-------------
        part = capacitors.resolve('GCM21BR71E105KA56L')
        component = {}
        component['Series'] = 'GCM'
        component['Case'] = '0805'
        component['Height'] = '1.25mm'
        component['Dielectric Type'] = 'X7R'
        component['Voltage'] = '25V'
        component['Capacitance'] = '1uF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)


    def test_murata_GC3(self):
        pass


    def test_murata_GCJ(self):
        part = capacitors.resolve('GCJ188R92A152KA01')
        component = {}
        component['Series'] = 'GCJ'
        component['Case'] = '0603'
        component['Height'] = '0.8mm'
        component['Dielectric Type'] = 'X8R'
        component['Voltage'] = '100V'
        component['Capacitance'] = '1.5nF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)


    def test_murata_GCD(self):
        pass

    def test_murata_GCE(self):
        pass

    def test_murata_NFM(self):
        pass

    def test_murata_KCM(self):
        pass

    def test_murata_KC3(self):
        pass

    def test_murata_KCA(self):
        pass

    def test_murata_GCG(self):
        pass


if __name__ == "__main__":
    unittest.main()
