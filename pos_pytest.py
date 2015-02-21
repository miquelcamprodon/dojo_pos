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


def test_empty():
    pos = POS()
    assert pos.list() == []


def test_one_element(monkeypatch):
    pos = POS()
    monkeypatch.setattr(Store, 'lock', lambda x,y,z: None)
    pos.scan('1111111111', 1)

