#! /usr/bin/env python3

'''
Topic: Fremdkapitalhebel
Description: Script untersucht die Wirkung des Fremdkapitalhebels beid drei der häufigsten Kreditformen
Author: Leon Schmidt
'''

import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

#### Annuitätendarlehen ####
# Allgemeine Parameter
kreditsumme_euro = 100e3
gebuehren = 10e3
annuittaet_monatlich_euro = 500
zins_jaerlich_prcnt = 3
rendite_asset_jaerlich_prcnt = 3

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

# Zeige IRR
eigenkapital = laenge_monaten * annuittaet_monatlich_euro
eigenkapital_end_direkt = investitionskapital_direkt_list[-1]
kapital_fremd = investitionskapital * (1 + rendite_asset_monatlich_prcnt / 100)**np.arange(laenge_monaten)
eigenkapital_end_fremd = kapital_fremd[-1]
laenge_jahre = laenge_monaten / 12
print("Internal Rate of Revenue (IRR) in %:")
print("\tAnnuitätsdarlehen:")
cashflows = [-annuittaet_monatlich_euro] * laenge_monaten
cashflows[-1] += eigenkapital_end_direkt
irr_monthly = npf.irr(cashflows)
irr_annual = (1 + irr_monthly)**12 - 1
print("\t\tDirekt investiertes Kapital: " + str(round(irr_annual * 100, 1)) + "%")
cashflows = [-annuittaet_monatlich_euro] * laenge_monaten
cashflows[-1] += eigenkapital_end_fremd
irr_monthly = npf.irr(cashflows)
irr_annual = (1 + irr_monthly)**12 - 1
print("\t\tDarlehen: " + str(round(irr_annual * 100 ,1))  + "%")

# Erstellen der Plots 
plt.plot(kreditsumme_euro_list, label = "Kreditsumme")
plt.plot(np.ones(laenge_monaten) * annuittaet_monatlich_euro, label = "Monatliche Investitionen")
plt.plot(kapital_fremd, label = "Investitionskapital mit Fremdkapital")
plt.plot(investitionskapital_direkt_list, label = "Investitionskapital direkt")
plt.axhline(y=eigenkapital, color='red', linestyle='--', label='Gesamt investiertes Kapital')
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
rendite_asset_jaerlich_prcnt = 3

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

# Zeige IRR
eigenkapital = np.sum(np.array(investition_monatlich_list))
eigenkapital_end_direkt = investitionskapital_direkt_list[-1]
kapital_fremd = investitionskapital * (1 + rendite_asset_monatlich_prcnt / 100)**np.arange(laenge_monaten)
eigenkapital_end_fremd = kapital_fremd[-1]
laenge_jahre = laenge_monaten / 12
print("\tTilgungsdarlehendarlehen:")
cashflows = -np.array(investition_monatlich_list)
cashflows[-1] += eigenkapital_end_direkt
irr_monthly = npf.irr(cashflows)
irr_annual = (1 + irr_monthly)**12 - 1
print("\t\tDirekt investiertes Kapital: " + str(round(irr_annual * 100, 1)) + "%")
cashflows = -np.array(investition_monatlich_list)
cashflows[-1] += eigenkapital_end_fremd
irr_monthly = npf.irr(cashflows)
irr_annual = (1 + irr_monthly)**12 - 1
print("\t\tDarlehen: " + str(round(irr_annual * 100 ,1))  + "%")

# Erstellen der Plots 
plt.plot(kreditsumme_euro_list, label = "Kreditsumme")
plt.plot(investition_monatlich_list, label = "Monatliche Investitionen")
plt.plot(kapital_fremd, label = "Investitionskapital mit Fremdkapital")
plt.plot(investitionskapital_direkt_list, label = "Investitionskapital direkt")
plt.axhline(y=np.sum(np.array(investition_monatlich_list)), color='red', linestyle='--', label='Gesamt investiertes Kapital')
plt.legend()
plt.title("Tilgungsdarlehen")
plt.xlabel("Zeit in Monaten")
plt.ylabel("Betrag in €")
plt.show()

#### Endfälliges Darlehen mit konstanten Investitionen ####
# Allgemeine Parameter
kreditsumme_euro = 100e3
laufzeit_monaten = 250
gebuehren = 10e3
investitionen_monatlich_euro = 500
zins_jaerlich_prcnt = 3
rendite_asset_jaerlich_prcnt = 3

# Modell: Fremdkapital
investitionskapital = kreditsumme_euro - gebuehren
zins_monatlich_prcnt = ((1 + zins_jaerlich_prcnt / 100)**(1/12) - 1) * 100
kreditsumme_euro_list = []
kreditsumme_euro_list.append(kreditsumme_euro)
for _ in range(laufzeit_monaten):
    kreditsumme_euro *= (1 + zins_monatlich_prcnt / 100)
    kreditsumme_euro_list.append(kreditsumme_euro)

# Modell: Direkt Investitionen
rendite_asset_monatlich_prcnt = ((1 + rendite_asset_jaerlich_prcnt / 100)**(1/12) - 1) * 100
investitionskapital_direkt = 0
investitionskapital_direkt_list = []
for _ in range(laufzeit_monaten):
    investitionskapital_direkt *= (1 + rendite_asset_monatlich_prcnt / 100)
    investitionskapital_direkt += investitionen_monatlich_euro
    investitionskapital_direkt_list.append(investitionskapital_direkt)

# Zeige IRR
kapital_fremd = investitionskapital * (1 + rendite_asset_monatlich_prcnt / 100)**np.arange(laufzeit_monaten) + investitionskapital_direkt_list
eigenkapital_end_direkt = investitionskapital_direkt_list[-1]
eigenkapital_end_fremd = kapital_fremd[-1] - kreditsumme_euro_list [-1]
laenge_jahre = laufzeit_monaten / 12
print("\tEndfälliges Darlehen:")
cashflows = -np.ones(laufzeit_monaten) * investitionen_monatlich_euro
cashflows[-1] += eigenkapital_end_direkt
irr_monthly = npf.irr(cashflows)
irr_annual = (1 + irr_monthly)**12 - 1
print("\t\tDirekt investiertes Kapital: " + str(round(irr_annual * 100, 1)) + "%")
cashflows = -np.ones(laufzeit_monaten) * investitionen_monatlich_euro
cashflows[-1] += eigenkapital_end_fremd
irr_monthly = npf.irr(cashflows)
irr_annual = (1 + irr_monthly)**12 - 1
print("\t\tDarlehen: " + str(round(irr_annual * 100 ,1))  + "%")

# Erstellen der Plots 
plt.plot(kreditsumme_euro_list, label = "Kreditsumme")
plt.plot(np.ones(laufzeit_monaten) * investitionen_monatlich_euro, label = "Monatliche Investitionen")
plt.plot(kapital_fremd, label = "Investitionskapital mit Fremdkapital und direkt Investitionen", color='orange')
plt.plot(investitionskapital_direkt_list, label = "Investitionskapital direkt", color='green')
plt.axhline(y=kapital_fremd[-1] - kreditsumme_euro_list [-1], color='orange', linestyle='--', label='Investitionskapital mit Fremdkapital nach Tilgung')
plt.axhline(y=investitionskapital_direkt_list[-1], color='green', linestyle='--', label='Endwert von Investitionskapital direkt')
plt.axhline(y=laufzeit_monaten * investitionen_monatlich_euro, color='red', linestyle='--', label='Gesamt investiertes Kapital')
plt.legend()
plt.title("Endfälliges Darlehen mit konstanten Investitionen")
plt.xlabel("Zeit in Monaten")
plt.ylabel("Betrag in €")
plt.show()

