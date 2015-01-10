﻿# -*- coding: utf-8 -*-
import csv
from decimal import Decimal
import os

"""class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    GREY = '\033[90m'
    BLACK = '\033[90m'"""

class bcolors:
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    CYAN = ''
    WHITE = ''
    YELLOW = ''
    MAGENTA = ''
    GREY = ''
    BLACK = ''

class list():

    def __init__(self):
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
                
                '''print bcolors.FAIL + self.name," :"+ bcolors.ENDC ,bcolors.CYAN,self.Data[i][0],"MHz",bcolors.ENDC+"/ "+bcolors.YELLOW+self.Data[i][1],"dB",bcolors.ENDC," ",bcolors.CYAN,self.Data[i+1][0],"MHz",bcolors.ENDC+"/ "+bcolors.YELLOW+self.Data[i+1][1],"dB",bcolors.ENDC," Attenuation: ",bcolors.OKGREEN,"%.1f" % self.Atten,bcolors.ENDC+"dB"'''
                    
            i += 1
            

# Chargement des fichiers attenuation

simplelist = []

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:    
    if f[-3:] == "txt":
        x = matos(f)    
        simplelist.append(x)            

ll = list()
for frequest in ll.data:
    Atten = 0
    for i in xrange(len(simplelist)):
        simplelist[i].Calc_Atten(float(frequest))
        Atten += simplelist[i].Atten
    ll.write(frequest,Atten)
    print "l'attenuation a " + bcolors.OKGREEN + "%.3fMHz " % float(frequest) + bcolors.ENDC + "est de " + bcolors.OKGREEN + "%.1fdB" % Atten +  bcolors.ENDC