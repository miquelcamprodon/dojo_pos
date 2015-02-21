import unittest
from mock import patch


class Store():
    def lock(self,cod,cant):
        pass



class POS(object):
    
    def __init__(self, prices={}):
        self.dict_cant = {}
        self.dict_prices = prices
        self.store = Store()
    
    def scan(self, codigo, cantidad):
        self.dict_cant[codigo] = self.dict_cant.get(codigo,0) + cantidad
        self.store.lock(codigo, cantidad)
         
    def list(self):
        result = []
        for code in sorted(self.dict_cant.keys()):
            price = self.dict_prices.get(code, None)
            cant = self.dict_cant[code]
            if not price:
                result.append((code, cant))
            else:
                result.append((code, cant, price, cant*price))

        return result


class Test(unittest.TestCase):
    
    @classmethod
    def setUp(self):
        self.pos = POS()
    
    def test_empty(self):
        self.assertEqual(self.pos.list(), [])

    @patch.object(Store, 'lock', return_value = None)
    def test_one_element(self, mock_store):
        self.pos.scan('1111111111', 1)
        mock_store.assert_called_with('1111111111', 1)
        self.assertEqual(self.pos.list(), [('1111111111', 1)])

    @patch.object(Store, 'lock', return_value = None)
    def test_many(self, mock_store):
        # Ojo con el orden del diccionario
        lprods = [('1234', 1), ('2345', 6), ('333', 5)]
        for p in lprods:
            #apply(self.pos.scan, p)
            self.pos.scan(*p)
            mock_store.assert_called_with(*p)
            #self.pos.scan(p[0], p[1])
            
        self.assertEqual(sorted(self.pos.list(), key=lambda x:x[0]), 
                        sorted(lprods, key=lambda x:x[0]))

    @patch.object(Store, 'lock', return_value = None)
    def test_twice(self, mock_store):
        prod = ('12345', 1)
        self.pos.scan(prod[0], prod[1])
        mock_store.assert_called_with(*prod)
        self.pos.scan(prod[0], prod[1])
        mock_store.assert_called_with(*prod)
        self.assertEqual(self.pos.list(), [('12345', 2)])
        
    @patch.object(Store, 'lock', return_value = None)        
    def test_prices(self, mock_store):
        self.pos = POS({'1': 5.25, '2': 3.18, '3': 7.14})
        prod = ('1', 10)
        self.pos.scan(*prod)
        mock_store.assert_called_with(*prod)
        self.assertEqual(self.pos.list(),[('1',10,5.25,52.5)])

    @patch.object(Store, 'lock', return_value = None)
    def test_prices_mixed(self, mock_store):
        self.pos = POS({'1': 5.25, '2': 3.18, '3': 7.14})
        prod = ('1', 10)
        self.pos.scan(*prod)
        mock_store.assert_called_with(*prod)
        prod = ('4', 7)
        self.pos.scan(*prod)
        mock_store.assert_called_with(*prod)        
        self.assertEqual(self.pos.list(),[('1',10,5.25,52.5), ('4',7)])
        
if __name__ == '__main__':
    unittest.main()
