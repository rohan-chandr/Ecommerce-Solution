"""
Author : Rohan Chandra

Python script to define and test a generator function that reads a file line by line and returns the values in the line
as a tuple for each line in the file.

"""

import sys
import string 
import unittest
sys.tracebacklimit = 0


def file_reader(path, fields, sep = ',', header = False) :
  
    """
    Generator function to read the lines one by one from the file 'path' , and return all the values on each line as a tuple
    on each call to next. 

    """
    try :   
        fp = open(path,'r')                 # Read lines from file.
    
    except FileNotFoundError :              
        print ("Can't open", path)          # If file not found.
        
    except IOError as err:
        print ('Error reading the file {0}: {1}'.format(fp.name, err))      # Handle access errors.
    
    else :
        with fp :
            for num, line in enumerate(fp) :        # iterate over each line in fp.
                if header == True :
                    header = False                  # Handle the case where the file has a header.    
                    continue   
                               
                line = line.strip('\r\n')            
                
                if line.find('"') :                # Handle values being enclosed in double quotes. 
                    line = line.split('"')      
                    
                    for offset,word in enumerate(line) :
                       if offset % 2 != 0 : 
                            line[offset] = word.translate(word.maketrans('', '', ','))
                    
                    line = "".join(line)    

                line = line.split(sep)                # Split line into fields
                line = [s.strip(' ') for s in line]   # Strip leading and trailing whitespaces for each field
                
                if len(line) == fields :              # If the line has 'field' no of fields
                    yield tuple(line)                 # yield the values for each line as a tuple

                else :
                    raise ValueError(f"{fp.name} has {len(line)} fields on line {num+1} but expected {fields}") 
                    
                    




class FileReaderTest(unittest.TestCase):
     
    """ Testcases to determine if the file_reader function works properly """
    
    def test_file_reader(self):
        
        result = ()
        
        expect = ('Rohan Chandra', '10443608', 'SE', 'Ram Chander', '10443690', 'CS')
        
        for name, cwid, major in file_reader('C:/Users/Rohan/Desktop/python/studentlog(for Part2).txt', 3, sep = '|', header = True):
            
            result += (name,cwid,major)
        
        self.assertEqual(result, expect)

        
        result = ()
        
        expect = ('Apple', 'Red', '2', 'Banana', 'Yellow', '3')
        
        for name, cwid, major in file_reader('C:/Users/Rohan/Desktop/python/fruits(for Part 2).txt', 3, sep = ',', header = True):
            
            result += (name,cwid,major)
        
        self.assertEqual(result,expect)


def main():
    """
    main routine.
    """

    main()

if __name__ == '__main__' :

    unittest.main(exit=False, verbosity=2)
