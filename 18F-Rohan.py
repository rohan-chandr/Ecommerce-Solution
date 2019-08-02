"""
Author : Rohan Chandra 

Python script to create an e-commerce solution in Python to allow multiple stores to sell multiple products to multiple customers.   

"""
from prettytable import PrettyTable  
import os 
import sys
import string 
from collections import defaultdict 
import unittest 
from FileReaderRohan import file_reader

class Store :
    """ A class to provide a data structure to hold the details of a store and to provide methods to manipulate them """
    
    pt_labels = [ "Store", "Product", "Customers", "Quantity Sold" ]        # fields for PrettyTable
    
    def __init__ (self, id, name) :   
        self._id = id 
        self._name = name
        self._products = dict()                           #_products[product_name] = quantity     
        self._sales= dict()                               #_sales[product_name] = [{ customer_name : quantity }] 
                       
    
    def add_product(self, product_name, quantity) :
        """ Update store's details with a new product and quantity """ 
        
        if product_name not in self._products :
            self._products[product_name] = quantity       #add new product and quantity 
            # { product_name : quantity }
             
        else :
            print(f"Warning : product {product_name} already exists!")

    
    def add_sale(self, customer_name, product_name, quantity) :
        """ Update store's details with a new customer,the product bought and the quantity bought """ 

        if self._products[product_name] == 0 :          #don't update if there is no stock of product_name
            return 
        
        elif quantity > self._products[product_name] :  #if requested quantity > remaining stock, sell remaining stock to requestor 
            quantity = self._products[product_name]
            self._products[product_name] = 0            #update stock to 0(No stock left)    
        
        else : 
            self._products[product_name] -= quantity    #normal transaction; update stocks to reflect sold items
            
        
        if product_name in self._sales.keys() :
            self._sales[product_name].append({ customer_name : quantity })  #add to existing sales history for product_name

        else :
            self._sales[product_name] = [{ customer_name : quantity }]      #create sales history for newly encountered product_name

    
    def return_inventory(self, product_name) :
        """ Return stock for product_name when called """
         
        return self._products[product_name]    #_products[product_name] = quantity


    def pt_row(self) :
        """ return a list of values needed to add a row to display store information in the PrettyTable """
        
        for product_name in self._sales.keys() :  
            customers_list = []  
            total_sales = 0
             
            #unpack _sales[product_name] = [{ customer_name : quantity }]
            for k, v in [(k, v) for x in self._sales[product_name] for (k, v) in x.items()]:    
                if k not in customers_list :
                    customers_list.append(k) 
                total_sales += int(v)

            yield self._name, product_name, sorted(customers_list), total_sales
            
                   
class Product :
    """ A class to provide a data structure to hold the details of a product and to provide methods to manipulate them """

    def __init__(self, product_id, _product_name) :
        self._product_id = product_id
        self._product_name = _product_name
        self._inventory = dict()                       #_inventory[store_id] = quantity  


    def add_inventory(self, store_id, quantity) :
        """ Populate with initial inventory """

        if store_id in self._inventory.keys() :
            print(f"Warning: product {self._product_id} is already listed under store {store_id}.")

        else :
            self._inventory = { store_id : quantity } 

    
    def return_name(self) :
        """ Return product_name when called """
        
        return self._product_name


class Customer :
    """ A class to provide a data structure to hold the details of a customer and to provide methods to manipulate them """

    pt_labels = [ "Customer Name", "Product", "Quantity Purchased" ]        #fields for PrettyTable.
    
    def __init__(self,id,cust_name) :
        self._id = id 
        self._cust_name = cust_name
        self._purchases = dict()                                   #_purchases[product_name] = [{ store_id : quantity }]
        
    
    def add_purchase(self, store_id, product_name, quantity) :
        """ Store the product and quantity of product bought by this customer """
        

        if product_name in self._purchases.keys() :
            self._purchases[product_name].append({ store_id : quantity})   #add to existing purchase records for product_name

        else :
            self._purchases[product_name] = [{ store_id : quantity }]      #create a new purchase record for newly encountered product_name

    def return_name(self) :
        """ Return cust_name when called """
        
        return self._cust_name  
         

    def pt_row(self) :
        """ return a list of values needed to add a row to display Customer information in the PrettyTable """

        #unpack _purchases[product_name] = [{ store_id : quantity }]
        for product_name in self._purchases.keys() :
            quantity_purchased = 0
            name_list = []
            for  k, v in [(k, v) for x in self._purchases[product_name] for (k, v) in x.items()]:
                quantity_purchased += v
            if product_name not in name_list :
                name_list.append(product_name)
                yield self._cust_name, product_name, quantity_purchased
     
        
class Portal :
    """ A class that makes uses of the Store, Product and Customer classes to create a Portal that stores all this information  """

    def __init__(self,path_dir) :
        self._stores = dict()         #_stores[id] = instance of class Store
        self._products = dict()       #_products[id] = instance of class Product 
        self._customers = dict()      #_customers[id] = instance of class Customer
        
        self.read_stores(os.path.join(path_dir, "stores.txt"))   #read stores file
        self.read_products(os.path.join(path_dir, "products.txt")) #read instructors file
        self.read_customers(os.path.join(path_dir, "customers.txt"))     #read customers file
        self.read_inventory(os.path.join(path_dir, "inventory.txt"))     #read inventory file
        self.read_transactions(os.path.join(path_dir, "transactions.txt")) #read transactions file         

    def read_stores(self, path) :
        """ Read the stores file and store the data in self._stores """

        try :
            for id, name in file_reader(path, 2, sep = '*', header = True ):  #call file_reader for stores.txt
                if id in self._stores :
                    print(f"Warning: id {id} already read from file")

                else :
                    #_stores[id] = instance of class Store with id    
                    self._stores[id] = Store(id, name)    
                     
        except ValueError as err :
            print(err)

            
    def read_products(self, path) :
        """ Read the instructors file and store the data in self._instructors """

        try:
            for p_id, s_id, p_name in file_reader(path, 3, sep = '|', header = False ):  #call file_reader for products.txt
                if p_id in self._products :
                    continue
                    
                else :
                    self._products[p_id] = Product(p_id, p_name)  #_products[p_id] = instance of class Product with p_id
            
        except ValueError as err :
            print(err)
            
    
    def read_customers(self, path) :
        """ Read the customers file and store the data in self._customers"""

        try :
            for cust_id, name in file_reader(path, 2, sep = ',', header = True ):  #call file_reader for customers.txt
                if cust_id in self._customers :
                    print(f"Warning: id {cust_id} already read from file")

                else :    
                    #_customers[cust_id] = instance of class Customer with cust_id
                    self._customers[cust_id] = Customer(cust_id, name)    
                    
        except ValueError as err :
            print(err)


    def read_inventory(self, path) :
        """ Read inventory file and update initial inventory for stores and products. """

        try:   #call file_reader for inventory.txt 
            for store_id, quantity, product_id  in file_reader(path, 3, sep = '|', header = True ):
                
                #tell product about a new product and it's initial quantity
                self._products[product_id].add_inventory( store_id, int(quantity) )
                
                #tell store about a new product and it's initial quantity
                self._stores[store_id].add_product( self._products[product_id].return_name(), int(quantity) )
                  
        except ValueError as err :
            print(err)

    
    def read_transactions(self, path) :
        """ Read transactions file and update sales and purchase history for stores and customers """

        try:  #call file_reader for transactions.txt
            for cust_id, quantity, product_id, store_id in file_reader(path, 4, sep = '|', header = True ):  
                
                stock = self._stores[store_id].return_inventory(self._products[product_id].return_name())
                #get stock from stores 

                if stock == 0 :     #if no remaining stock of requested product, don't sell to customer.
                    continue 

                elif stock < int(quantity) :    
                     
                    #if stock less than requested quantity, update purchase records accordingly.
                    self._customers[cust_id].add_purchase( store_id, self._products[product_id].return_name() , stock)
                    

                else :
                    
                    #normal purchase record update 
                    self._customers[cust_id].add_purchase( store_id, self._products[product_id].return_name() , int(quantity))

                #update sales information for store 
                self._stores[store_id].add_sale( self._customers[cust_id].return_name(), 
                self._products[product_id].return_name(), int(quantity) )
                
        except ValueError as err :
            print(err)
        

    def store_prettytable(self) :
        """ Create and print a table of all the stores and their details """
        
        pt = PrettyTable(field_names = Store.pt_labels)
        for store in self._stores.keys() :
            for i in list(self._stores[store].pt_row()) :
                pt.add_row(i)
        print(pt)
    
    
    def customer_prettytable(self):
        """ Create and print a table of all the customers and their details """
        
        pt = PrettyTable(field_names = Customer.pt_labels)
        for customer in self._customers.keys():
            for i in list(self._customers[customer].pt_row()):
                pt.add_row(i)
        print(pt)

if __name__ == '__main__' :
    
    while True :
        portal_dir = input("Enter the directory")          
        if not os.path.isdir(portal_dir)   :
            print("Invalid directory!")                           #if directory does not exist              
                                                  
        else :
            portal = Portal(portal_dir)                           #create an instance of class Portal with path portal_dir
            portal.store_prettytable()                            #generate store prettytable 
            portal.customer_prettytable()                         #generate cusomter prettytable
            
        
        if input('Press "Q" to Quit or any other key to work on another directory. :').upper() == 'Q' :
            sys.exit(0)
    
    