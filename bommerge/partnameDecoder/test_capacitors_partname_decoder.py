import unittest
from partnameDecoder import capacitors

class TestCapacitorPartnameResolver(unittest.TestCase):
    def test_murata_GRT(self):
        part = capacitors.resolve('GRT0335C1E120JA02')
        component = {}
        component['Series'] = 'GRT'
        component['Note'] = 'AEC-Q200 Compliant Chip Multilayer Ceramic Capacitors for Infotainment'
        component['Case'] = '0201'
        component['Height'] = '0.3mm'
        component['Dielectric Type'] = 'C0G'
        component['Voltage'] = '25VDC'
        component['Capacitance'] = '12pF'
        component['Tolerance'] = '5%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)
        

    def test_murata_GCM(self):
        part = capacitors.resolve('GCM155R71C104KA55D')
        component = {}
        component['Series'] = 'GCM'
        component['Note'] = 'Chip Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '0402'
        component['Height'] = '0.5mm'
        component['Dielectric Type'] = 'X7R'
        component['Voltage'] = '16VDC'
        component['Capacitance'] = '100nF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)
        #-------------
        part = capacitors.resolve('GCM21BR71E105KA56L')
        component = {}
        component['Series'] = 'GCM'
        component['Note'] = 'Chip Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '0805'
        component['Height'] = '1.25mm'
        component['Dielectric Type'] = 'X7R'
        component['Voltage'] = '25VDC'
        component['Capacitance'] = '1uF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)


    def test_murata_GC3(self):
        part = capacitors.resolve('GC331AD72W153KX01')
        component = {}
        component['Series'] = 'GC3'
        component['Note'] = 'High Effective Capacitance & High Ripple Current Chip Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '1206'
        component['Height'] = '1mm'
        component['Dielectric Type'] = 'X7T'
        component['Voltage'] = '450VDC'
        component['Capacitance'] = '15nF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)


    def test_murata_GCJ(self):
        part = capacitors.resolve('GCJ188R92A152KA01')
        component = {}
        component['Series'] = 'GCJ'
        component['Note'] = 'Soft Termination Chip Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '0603'
        component['Height'] = '0.8mm'
        component['Dielectric Type'] = 'X8R'
        component['Voltage'] = '100VDC'
        component['Capacitance'] = '1.5nF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)


    def test_murata_GCD(self):
        part = capacitors.resolve('GCD188R71H153KA01')
        component = {}
        component['Series'] = 'GCD'
        component['Note'] = 'MLSC Design Chip Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '0603'
        component['Height'] = '0.8mm'
        component['Dielectric Type'] = 'X7R'
        component['Voltage'] = '50VDC'
        component['Capacitance'] = '15nF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)


    def test_murata_GCE(self):
        part = capacitors.resolve('GCE188R71H682KA01')
        component = {}
        component['Series'] = 'GCE'
        component['Note'] = 'Soft Termination MLSC Design Chip Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '0603'
        component['Height'] = '0.8mm'
        component['Dielectric Type'] = 'X7R'
        component['Voltage'] = '50VDC'
        component['Capacitance'] = '6.8nF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)


    def test_murata_NFM(self):
        pass

    def test_murata_KCM(self):
        part = capacitors.resolve('KCM55LR71H106KH01')
        component = {}
        component['Series'] = 'KCM'
        component['Note'] = 'Metal Terminal Type Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '2220'
        component['Height'] = '2.8mm'
        component['Dielectric Type'] = 'X7R'
        component['Voltage'] = '50VDC'
        component['Capacitance'] = '10uF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)

    def test_murata_KC3(self):
        part = capacitors.resolve('KC355LD72J154KH01')
        component = {}
        component['Series'] = 'KC3'
        component['Note'] = 'High Effective Capacitance & High Allowable Ripple Current Metal Terminal Type Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '2220'
        component['Height'] = '2.8mm'
        component['Dielectric Type'] = 'X7T'
        component['Voltage'] = '630VDC'
        component['Capacitance'] = '150nF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)

    def test_murata_KCA(self):
        part = capacitors.resolve('KCA55L7UMF102KH01')
        component = {}
        component['Series'] = 'KCA'
        component['Note'] = 'Safety Standard Certified Metal Terminal Type Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '2220'
        component['Height'] = '2.8mm'
        component['Dielectric Type'] = 'U2J'
        component['Voltage'] = '250VAC'
        component['Capacitance'] = '1nF'
        component['Tolerance'] = '10%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)

    def test_murata_GCG(self):
        part = capacitors.resolve('GCG1555G1H121JA01')
        component = {}
        component['Series'] = 'GCG'
        component['Note'] = 'AgPd Termination Conductive Glue Mounting Chip Multilayer Ceramic Capacitors for Automotive'
        component['Case'] = '0402'
        component['Height'] = '0.5mm'
        component['Dielectric Type'] = 'X8G'
        component['Voltage'] = '50VDC'
        component['Capacitance'] = '120pF'
        component['Tolerance'] = '5%'
        component['Manufacturer'] = 'Murata'
        self.assertEqual(part, component)


if __name__ == "__main__":
    unittest.main()
