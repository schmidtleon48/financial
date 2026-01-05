#! /usr/bin/env python3

'''
Topic: Fremdkapitalhebel
Description: Script untersucht die Wirkung des Fremdkapitalhebels beid drei der häufigsten Kreditformen
Author: Leon Schmidt
'''

import numpy as np
import matplotlib.pyplot as plt

#### Annuitätendarlehen ####
# Allgemeine Parameter
kreditsumme_euro = 100e3
gebuehren = 10e3
annuittaet_monatlich_euro = 500
zins_jaerlich_prcnt = 3
rendite_asset_jaerlich_prcnt = 6

# Modell: Fremdkapital
investitionskapital = kreditsumme_euro - gebuehren
zins_monatlich_prcnt = ((1 + zins_jaerlich_prcnt / 100)**(1/12) - 1) * 100
laenge_monaten = 0
kreditsumme_euro_list = []
kreditsumme_euro_list.append(kreditsumme_euro)
while kreditsumme_euro > 0:
    laenge_monaten += 1
    kreditsumme_euro *= (1 + zins_monatlich_prcnt / 100)
    kreditsumme_euro -= annuittaet_monatlich_euro
    kreditsumme_euro_list.append(kreditsumme_euro)

# Modell: Direkt Investitionen
rendite_asset_monatlich_prcnt = ((1 + rendite_asset_jaerlich_prcnt / 100)**(1/12) - 1) * 100
investitionskapital_direkt = 0
investitionskapital_direkt_list = []
for _ in range(laenge_monaten):
    investitionskapital_direkt *= (1 + rendite_asset_monatlich_prcnt / 100)
    investitionskapital_direkt += annuittaet_monatlich_euro
    investitionskapital_direkt_list.append(investitionskapital_direkt)

# Erstellen der Plots 
plt.plot(kreditsumme_euro_list, label = "Kreditsumme")
plt.plot(np.ones(laenge_monaten) * annuittaet_monatlich_euro, label = "Monatliche Investitionen")
plt.plot(investitionskapital * (1 + rendite_asset_monatlich_prcnt / 100)**np.arange(laenge_monaten), label = "Investitionskapital mit Fremdkapital")
plt.plot(investitionskapital_direkt_list, label = "Investitionskapital direkt")
plt.legend()
plt.title("Annuitätsdarlehen")
plt.xlabel("Zeit in Monaten")
plt.ylabel("Betrag in €")
plt.show()

##### Tilgungsdarlehen ####
# Allgemeine Parameter
kreditsumme_euro = 100e3
gebuehren = 10e3
tilgung_monatlich_euro = 500
zins_jaerlich_prcnt = 3
rendite_asset_jaerlich_prcnt = 2

# Modell: Fremdkapital
investitionskapital = kreditsumme_euro - gebuehren
zins_monatlich_prcnt = ((1 + zins_jaerlich_prcnt / 100)**(1/12) - 1) * 100
laenge_monaten = int(kreditsumme_euro / tilgung_monatlich_euro)
kreditsumme_euro_list = []
kreditsumme_euro_list.append(kreditsumme_euro)
investition_monatlich_list = []
for _ in range(laenge_monaten):
    betrag_zins = kreditsumme_euro * (zins_monatlich_prcnt / 100)
    investition_monatlich_list.append(tilgung_monatlich_euro + betrag_zins)
    kreditsumme_euro -= tilgung_monatlich_euro
    kreditsumme_euro_list.append(kreditsumme_euro)

# Modell: Direkt Investitionen
rendite_asset_monatlich_prcnt = ((1 + rendite_asset_jaerlich_prcnt / 100)**(1/12) - 1) * 100
investitionskapital_direkt = 0
investitionskapital_direkt_list = []
for i in range(laenge_monaten):
    investitionskapital_direkt *= (1 + rendite_asset_monatlich_prcnt / 100)
    investitionskapital_direkt += investition_monatlich_list[i]
    investitionskapital_direkt_list.append(investitionskapital_direkt)

# Erstellen der Plots 
plt.plot(kreditsumme_euro_list, label = "Kreditsumme")
plt.plot(investition_monatlich_list, label = "Monatliche Investitionen")
plt.plot(investitionskapital * (1 + rendite_asset_monatlich_prcnt / 100)**np.arange(laenge_monaten), label = "Investitionskapital mit Fremdkapital")
plt.plot(investitionskapital_direkt_list, label = "Investitionskapital direkt")
plt.legend()
plt.title("Tilgungsdarlehen")
plt.xlabel("Zeit in Monaten")
plt.ylabel("Betrag in €")
plt.show()

##### Endfälliges Darlehen ####


