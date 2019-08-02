"""
Author : Rohan Chandra

Python script to define and run unittest testcases for an Ecommerce Portal Creator

"""

import unittest 
from importlib import import_module
import os
module = import_module('18F-Rohan')

class PortalTest(unittest.TestCase):
    """ Testcases to demonstrate that the Portal creator works properly """
    
    def test_TestUni(self) :
        """ Testcase definition for instance of class Portal """
        
        portal = module.Portal("Test-Store")
        
        stores, customers, products = [], [], []
        
        for store in portal._stores.values():  
            for s in list(store.pt_row()):
                stores += [s]                         #extract relevant store data from portal
        
        for customer in portal._customers.values():
            for c in list(customer.pt_row()):
                customers += [c]                      #extract relevant customer data from portal
        
        for product in portal._products.values():
            products.append(product.return_name())    #extract relevant product data from portal
        
        expect_stores = [('Dunkin Donuts', 'Chocolate Donuts', ['Architect Armin'], 10), ('Dunkin Donuts', 'Coffee', ['Hacker Rohan'], 3),
         ('Valve Productions', 'Dota 2', ['Pilot Dave'], 100)]
                
        expect_customers = [('Architect Armin', 'Chocolate Donuts', 10), ('Hacker Rohan', 'Coffee', 3), ('Pilot Dave', 'Dota 2', 100)] 
        
        expect_products = ['Chocolate Donuts', 'Coffee', 'Dota 2']

        self.assertEqual(stores, expect_stores)
        self.assertEqual(customers, expect_customers)
        self.assertEqual(products, expect_products)

if __name__ == '__main__' :

    unittest.main(exit=False, verbosity=2)
