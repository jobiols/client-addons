import xmlrpc.client 
import datetime

class Odoo():
    def __init__(self):
        self.DATA = 'SolucionSeguros'
        self.USER = 'lymtechbr@gmail.com'
        self.PASS = 'lymadmin#1'
        self.PORT= '8069'
        self.URL = 'http://216.158.237.182'
        self.URL_COMMON = "{}:{}/xmlrpc/2/common".format(self.URL, self.PORT)
        self.URL_OBJECT = "{}:{}/xmlrpc/2/object".format(self.URL, self.PORT)

    def authenticateOdoo(self):
        self.ODOO_COMMON = xmlrpc.client.ServerProxy(self.URL_COMMON)
        self.ODOO_OBJECT = xmlrpc.client.ServerProxy(self.URL_OBJECT)
        self.UID = self.ODOO_COMMON.authenticate(
            self.DATA, 
            self.USER,
            self.PASS,
            {})
    
    def partnerAdd(self, partnerRow):
        partner_id = self.ODOO_OBJECT.execute_kw(
            self.DATA,
            self.UID,
            self.PASS,
            'res.partner',
            'create',
            partnerRow)
        return partner_id
    
    def leadAdd(self, partnerRow):
        partner_id = self.ODOO_OBJECT.execute_kw(
            self.DATA,
            self.UID,
            self.PASS,
            'crm.lead',
            'create',
            partnerRow)
        return partner_id

def main():
    od = Odoo()
    od.authenticateOdoo()
    print(od.UID)
    partnerRow = [{"name":"Léo",
        "phone":"777-777-7777",
        "website": "http://leo.com",
        "country_id": "55"}]
    od.partnerAdd(partnerRow)
    print("Feito!")

def Lead():
    od = Odoo()
    od.authenticateOdoo()
    print(od.UID)
    leadRow = [{"name":"Léo",
        "contact_name":"Léo Lymtech"}]
    od.leadAdd(leadRow)
    print("Feito!")

if __name__ == '__main__':
    main()
    print("Cadastrei User")
    mainLead()
    print("Cadastrei Lead")


print("Já fiz tudo")
