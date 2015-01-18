# -*- coding: utf-8 -*-
# coding by Outlouder

import csv
from decimal import Decimal
import os
import os.path
    
# Toolbox Definition

# Methode whish permits to generate space in order to align atten results layout
def space_generator(str,num):
    space = ""
    for i in xrange(num-len(str)):
        space = space + " "
    return space

# definition of frequency list class
class list():

    def __init__(self,simplelist):
        
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
       
        for f in files:    
            if f[-3:] == "lst":
                self.f = f
                fi = open(f,'rb')
                g = csv.reader(fi,delimiter='\t')
                self.data = []
                for row in g:
                    self.data.append(row[0])
                fi.close()

                del self.data[0]
                del self.data[0]

                self.filename = self.f[:-3]+"csv"
                fo = open(self.filename,'wb')

                for frequest in self.data:
                    Atten = 0
                    for i in xrange(len(simplelist)):
                        simplelist[i].Calc_Atten(float(frequest))
                        Atten += simplelist[i].Atten
                    fo.write(frequest+';'+"%.1f" % Atten+'\n')
                    
                    print "attenuation at " + "%.3fMHz " % float(frequest) + "is " + "%.1fdB" % float(Atten)

                fo.close()
          
    def write(self,freq,att):
        pass

    def __exit__(self):
        pass



class matos():
    
    def __init__(self,filename):
        self.Data = []
        self.simplelist = []
        self.name = filename
        f=open(filename, 'rb')
        reader = csv.reader(f, delimiter='\t')    
        for row in reader:
            self.Data.append([row[0],row[1]])   
        f.close()
      
    #Method whish calculate attenuation from Atten file loaded in __ini__ methode    
    def Calc_Atten(self,freq):
        i = 0
        for check in self.Data:
            
            if (float(self.Data[i][0]) <= float(freq)) and (float(self.Data[i+1][0] ) > float(freq)):
                self.pente = (float(self.Data[i+1][1]) - float(self.Data[i][1])) / (float(self.Data[i+1][0])-float(self.Data[i][0]))
                
                self.Atten = float(self.Data[i+1][1]) - float(self.pente)*(float(self.Data[i+1][0])-float(freq))  
                
                #Adaptation of ampli and cable attenuation sign
                if "amp" in self.name.lower():
                    self.Atten = 0 - self.Atten
                elif "cab" in self.name.lower():
                    self.Atten = 0 - self.Atten
                
                print self.name+space_generator(self.name,32)+" :"+"%.3fMHz" % float(self.Data[i][0])+"/"+"%.1fdB"%float(self.Data[i][1])," ","%.2fMHz" % float(self.Data[i+1][0])+"/"+"%.1fdB"%float(self.Data[i+1][1])," Attenuation: ","%.1f" % self.Atten+"dB"      
            i += 1
 
#Menu selection whish allow setup batch files from ./Setup directory          
print "----- SETUP CHOICE------"
setup_choice = []
for root,dirs, files in os.walk("./Setup"):
    for i,l in enumerate(dirs):
        print "choix %d"%(i+1)," :",l
        setup_choice.append(l)

print ""
dirchoice = "./Setup/"+setup_choice[int(raw_input("choix :"))-1]+"/"
print "------------------------"

#Generate List of device object list from batch file
simplelist = []
files =  os.listdir(dirchoice)
for f in files:    
    if f[-3:] == "txt":
        x = matos(dirchoice+f)    
        simplelist.append(x)            
    Atten = 0

processchoice = raw_input("list or single (l or s) :")

if processchoice == 's' :
    # Calculation of single frequency 
    frequest = raw_input("Frequency (MHz): ")
    print " "
    
    for i in xrange(len(simplelist)):
        simplelist[i].Calc_Atten(float(frequest))
        Atten += simplelist[i].Atten

    print " "            
    print "attenuation at " + "%.3fMHz " % float(frequest) + "is " + "%.1fdB" % float(Atten)

elif processchoice == 'l':
    # Calculation of multiple frequency inside .lst files
    warning1 = raw_input("WARNING : setup choisen will be applied on All lst Files in root directory")
    ll = list(simplelist)



