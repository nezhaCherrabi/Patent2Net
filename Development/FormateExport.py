# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import sys
import os
import pickle
import bs4
from bs4.dammit import EntitySubstitution
import OPS2NetUtils2

ndf = sys.argv[1]

rep = ndf

#if ndf.count('Families')>0:
#    clesRef = ['label',  'titre', 'date', 'citations','family lenght', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior']
#else:
clesRef = ['label', 'titre', 'date', 'citations', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'IPCR4', 'IPCR7']


ListBiblioPath = '..//DONNEES//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//PatentLists'#List
ResultPathContent = '..//DONNEES//PatentContentsHTML'
temporPath = 'tempo'


try:
    os.makedirs(ResultPathContent + '//' + ndf)
except: 
    pass

with open(ListBiblioPath+'//'+ndf, 'r') as data:
    LstBrevet = pickle.load(data)
with open(ListPatentPath+'//'+ndf, 'r') as data:
    DataBrevet = pickle.load(data)
#
#    
#def Check(lstDicos):
#    assert isinstance(lstDicos, list)
#    Res = []
#    
#    for ind in range(len(lstDicos)):
#        notUnic = False
#        for dico2 in lstDicos[ind+1:]:
#            if lstDicos[ind] == dico2:
#                notUnic = True
#                break
#        if not notUnic:
#            Res.append(lstDicos[ind])
#    return Res
#we filter data for exporting most significant values

    
LstExp = [] 
LstExp2 = [] 
for brev in LstBrevet:
    
    
    tempo = dict() # this one for DataTable
    tempo2 = dict() #the one for pitable
    for cle in clesRef:
        if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
            if isinstance(brev[cle], list) and cle == 'classification':
                for classif in brev['classification']:
                    tempoClass = OPS2NetUtils2.ExtractClassificationSimple2(classif)
                    for cle2 in tempoClass.keys():
                        if cle2 == 'classification':
                            if tempo.has_key(cle2) and not isinstance(tempo[cle2], list) and tempoClass[cle2] != tempo[cle]:
                                tempo[cle2] = [tempo[cle2]].append(tempoClass[cle2])
                            elif tempo.has_key(cle2) and isinstance(tempo[cle2], list) and tempoClass[cle2] not in tempo[cle]:
                                tempo[cle2].append(tempoClass[cle2])
                            else:
                                tempo[cle2] = tempoClass[cle2]
                        elif cle2 in tempo.keys() and tempoClass[cle2] not in tempo[cle2]:
                                #tempo[cle] = []
                                tempo[cle2].append(tempoClass[cle2])
                                tempo2[cle2].append(tempoClass[cle2])
                        
                        else:
                            tempo[cle2] = []
                            tempo2[cle2] = []
                            tempo[cle2].append(tempoClass[cle2])
                            tempo2[cle2].append(tempoClass[cle2])
            elif isinstance(brev[cle], list):
                temp = unicode(' '.join(brev[cle]))
                tempo[cle] = temp
                tempo2[cle] = brev[cle]
            elif cle =='titre':
                             
                temp = unicode(brev[cle]).replace('[','').replace(']', '').lower().capitalize()
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                #tempo2[cle] = temp  #we do not need titles in pivotable
            elif cle =='date':
                tempo[cle] = str(brev['date'].year) +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
                tempo2[cle] = str(brev['date'].year) # just the year in Pivottable
            elif cle =='classification' and brev['classification'] != '':
                    tempoClass = OPS2NetUtils2.ExtractClassificationSimple2(brev['classification'])
                    for cle in tempoClass.keys():
                        if cle in tempo.keys() and tempoClass[cle] not in tempo[cle]:
                            tempo[cle].append(tempoClass[cle])
                            tempo2[cle].append(tempoClass[cle])
                        else:
                            tempo[cle] = []
                            tempo2[cle] = []
                            tempo[cle].append(tempoClass[cle])
                            tempo2[cle].append(tempoClass[cle])
                
            else:
                temp = unicode(brev[cle]).replace('[','').replace(']', '')
                
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                tempo2[cle] = brev[cle]
                
        else:
            tempo[cle] = ''
            tempo2[cle] = ''
            
    LstExp.append(tempo)
    
    tempoBrev = OPS2NetUtils2.Decoupe(tempo2)
#    tempoBrev = Check(tempoBrev) # doublons enlevés
    clesRef2 = ['label', 'date', 'citations', 'priority-active-indicator', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'IPCR4', 'IPCR7']

    for brev2 in tempoBrev:
        tempo2 = dict() #the one for pitable
        for cle in clesRef2:
            if brev2[cle] is not None and brev2[cle] != 'N/A' and brev2[cle] != 'UNKNOWN':
                if isinstance(brev2[cle], list):
                    tempo2[cle] = [bs4.BeautifulSoup(unit).text for unit in brev2[cle]]
#                                    
                if cle =='titre':
                    pass # no need of titles
                if cle == 'applicant' or cle == 'inventeur':
                    temp = unicode(brev2[cle])
                    if temp.count('[')>0:
                        tempo2 [cle] = temp.split('[')[0]
                    else:
                        tempo2 [cle] = temp
                else:
                    temp = unicode(brev2[cle])
                    
                    formate = EntitySubstitution()
                    soup = bs4.BeautifulSoup(temp)
                    temp = soup.text
                    tempo2 [cle] = temp
                    
            else:
                tempo2[cle] = ''
        if tempo2 not in LstExp2:
            LstExp2.append(tempo2)
    print len(LstExp2),
    
Exclude = []
print "entering formating html process"
dicoRes = dict()
dicoRes['data'] = LstExp
contenu = json.dumps(dicoRes, ensure_ascii=True, indent = 3)
contenu2 = json.dumps(LstExp2, ensure_ascii=True, indent = 3)

import codecs
#if rep != ndf:
#    if ndf.lower() == 'families'+rep.lower():
#        #ndf = 'Families'+ ndf
#        Modele = "ModeleFamille.html"
#else:
#    
Modele = "Modele.html"
with codecs.open(ResultPathContent + '//' + rep+ '//' +ndf+'.csv', 'w', 'utf-8') as resFic:
    entete = ''.join([u +';' for u in clesRef]) +'\n'
    resFic.write(entete)
    for brev in LstBrevet:
        ligne = ''
        for cle in clesRef:
            if isinstance(brev[cle], list):
                temp=''
                for k in brev[cle]:
                    temp += k + ' '
                try:
                    ligne += unicode(temp, 'utf8', 'replace') +';'
                except:
                    try:
                        ligne += unicode(temp, 'cp1252', 'replace') +';' 
                    except:
                        try:
                            ligne += unicode(temp, 'latin1', 'replace') +';'
                        except:
                            try:
                                ligne += unicode(temp) +';'
                            except:
                                print 'paté'
            else:
                try:
                    ligne += unicode(brev[cle], 'utf8', 'replace') +';'
                except:
                    ligne += unicode(brev[cle]) +';'
                    
        ligne += '\n'
        resFic.write(ligne)

with open(ResultPathContent + '//' + rep+ '//' +ndf+'.json', 'w') as resFic:
    resFic.write(contenu)

with open(ResultPathContent + '//' + rep+ '//' +ndf+'Pivot.json', 'w') as resFic:
    resFic.write(contenu2)
with open(Modele, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'.json' )  
    
    html = html.replace('**fichierHtmlFamille**', 'Families'+ndf+'.html' )
    html = html.replace('**fichierPivot**', ndf+'Pivot.html' )

    html = html.replace('**requete**', DataBrevet['requete'])
    with open(ResultPathContent + '//' + rep+ '//' +ndf+'.html', 'w') as resFic:
        resFic.write(html)

FichierHtml=ndf+'.html'
ModelePivot = "Pivot.html"
with open(ModelePivot, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'Pivot.json' )  
    html = html.replace('**requete**', DataBrevet['requete'])
    html = html.replace('**FichierHtml**', FichierHtml)
    html = html.replace('**FichierHtmlFamille**', 'Families'+FichierHtml)
    with open(ResultPathContent + '//' + rep+ '//' +ndf+'Pivot.html', 'w') as resFic:
        resFic.write(html)
