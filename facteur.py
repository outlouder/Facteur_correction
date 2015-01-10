﻿# -*- coding: utf-8 -*-
# Outlouder

import csv
from decimal import Decimal
import os
import os.path
    
# definition of list class
class list():

    def __init__(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        
        # issue cumulation of all files .lst data and Output filename => last file
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
        self.fo = open(self.filename,'wb')
                
    def write(self,freq,att):
        self.fo.write(freq+';'+"%.1f" % att+'\n')

    def __exit__(self):
        self.fo.close()

class matos():
    
    def __init__(self,filename):
        self.Data = []
        self.name = filename
        f=open(filename, 'rb')
        reader = csv.reader(f, delimiter='\t')
            
        for row in reader:
            self.Data.append([row[0],row[1]])
            
        f.close()
        
    def Find_type(self):
        pass
        
    def Calc_Atten(self,freq):
        i = 0
        for check in self.Data:
            
            if (float(self.Data[i][0]) <= float(freq)) and (float(self.Data[i+1][0] ) > float(freq)):
                self.pente = (float(self.Data[i+1][1]) - float(self.Data[i][1])) / (float(self.Data[i+1][0])-float(self.Data[i][0]))
                
                self.Atten = float(self.Data[i+1][1]) - float(self.pente)*(float(self.Data[i+1][0])-float(freq))  
                if "amp" in self.name.lower():
                    self.Atten = 0 - self.Atten
                elif "cab" in self.name.lower():
                    self.Atten = 0 - self.Atten
                
                print self.name," :"+ self.Data[i][0],"MHz"+"/ "+self.Data[i][1],"dB"," ",self.Data[i+1][0],"MHz"+"/ "+self.Data[i+1][1],"dB"," Attenuation: ","%.1f" % self.Atten+"dB"      
            i += 1
           
print "----- CHOIX SETUP ------"

setup_choice = []
for root,dirs, files in os.walk("./Setup"):
    for i,l in enumerate(dirs):
        print "choix %d"%(i+1)," :",l
        setup_choice.append(l)

print ""
dirchoice = "./Setup/"+setup_choice[int(raw_input("choix :"))-1]+"/"
print "------------------------"

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
    print "l'attenuation a " + "%.3fMHz " % float(frequest) + "est de " + "%.1fdB" % Atten

elif processchoice == 'l':
    # Calculation of multiple frequency inside .lst files
    ll = list()
    for frequest in ll.data:
        Atten = 0
        for i in xrange(len(simplelist)):
            simplelist[i].Calc_Atten(float(frequest))
            Atten += simplelist[i].Atten
        ll.write(frequest,Atten)
        print "l'attenuation a " + "%.3fMHz " % float(frequest) + "est de " + "%.1fdB" % Atten
