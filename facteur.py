# -*- coding: utf-8 -*-
import csv
from decimal import Decimal
import os
import os.path
    
class matos():
    
    def __init__(self,filename):
        self.Data = []
        self.name = filename
        f=open(filename, 'rb')
        reader = csv.reader(f, delimiter='\t')
            
        for row in reader:
            self.Data.append([row[0],row[1]])
            #print row[0],row[1]		
        f.close()        
        #print self.Data
        
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
            

# Chargement des fichiers attenuation

print "----- CHOIX SETUP ------"

for root,dirs, files in os.walk(".")
    print dirs

print "------------------------"

simplelist = []

frequest = raw_input("Frequence a calculer: ")
print " "
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:    
        if f[-3:] == "txt":
            x = matos(f)    
            simplelist.append(x)            
Atten = 0

# Calculer l'Attenuation totale à la fréquence demandée
for i in xrange(len(simplelist)):
    simplelist[i].Calc_Atten(float(frequest))
    Atten += simplelist[i].Atten


print " "            
print "l'attenuation a " + "%.3fMHz " % float(frequest) + "est de " + "%.1fdB" % Atten
