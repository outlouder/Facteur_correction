# -*- coding: utf-8 -*-
# Outlouder

import csv
from decimal import Decimal
import os
import os.path
    
# Toolbox def

# methode whish permits to generate space in order to align atten results layout
def space_generator(str,num):
    space = ""
    for i in xrange(num-len(str)):
        space = space + " "
    return space


# definition of list class
class list():

    def __init__(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        self.file_found = 0
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
                self.file_found = 1
        
        if self.file_found == 1:
	        self.filename = self.f[:-3]+"csv"
	        self.fo = open(self.filename,'wb')
                
    def write(self,freq,att):
        if self.file_found == 1:
	        self.fo.write(freq+';'+"%.1f" % att+'\n')

    def __exit__(self):
        if self.file_found == 1:
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
           
print "----- SETUP CHOICE------"

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
    print "attenuation at " + "%.3fMHz " % float(frequest) + "is " + "%.1fdB" % float(Atten)

elif processchoice == 'l':
    # Calculation of multiple frequency inside .lst files 
    ll = list()
    if ll.file_found == 1:
        for frequest in ll.data:
            Atten = 0
            for i in xrange(len(simplelist)):
                simplelist[i].Calc_Atten(float(frequest))
                Atten += simplelist[i].Atten
            ll.write(frequest,Atten)
            print "attenuation at " + "%.3fMHz " % float(frequest) + "is " + "%.1fdB" % float(Atten)
    else:
        print "No Lst file found in root directory"
