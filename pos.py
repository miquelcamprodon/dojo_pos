import unittest

class POS(dict):
    def __init__(self):
        dict.__init__(self)


    def scan(self, codigo, cantidad):
        self[codigo] = self.get(codigo,0) + cantidad
        
    def list(self):
        return self.items()


class Test(unittest.TestCase):
    
    @classmethod
    def setUp(self):
        self.pos = POS()
    
    def test_empty(self):
        self.assertEqual(self.pos.list(), [])
        
    def test_one_element(self):
        self.pos.scan('1111111111', 1)
        self.assertEqual(self.pos.list(), [('1111111111', 1)])

    def test_many(self):
        # Ojo con el orden del diccionario
        lprods = [('1234', 1), ('2345', 6), ('333', 5)]
        for p in lprods:
            #apply(self.pos.scan, p)
            self.pos.scan(*p)
            #self.pos.scan(p[0], p[1])
            
        self.assertEqual(sorted(self.pos.list(), key=lambda x:x[0]), 
                        sorted(lprods, key=lambda x:x[0]))

    def test_twice(self):
        prod = ('12345', 1)
        self.pos.scan(prod[0], prod[1])
        self.pos.scan(prod[0], prod[1])
        self.assertEqual(self.pos.list(), [('12345', 2)])
        
        
        
if __name__ == '__main__':
    unittest.main()
