import datetime as dt
import pandas as pd
from abc import ABC, abstractmethod

from .flows import Flows

class Fiscalite(ABC):
    # Fiscalité sur revenus immobiliers:
    # - IR : impôts sur le revenu (barême progressif)
    # - PS : prélèvements sociaux (17.2% en 2024)
    # Impôts collectés en année N+1 au mois d'octobre
    
    def __init__(self, ir=30, ps=17.2):
        self.ir = ir
        self.ps = ps
        
    @abstractmethod
    def calculer_benefices(self):
        pass
        
class LocationNue(Fiscalite):
    @abstractmethod
    def calculer_benefices(self):
        pass
        
    def calculer_benefices(self, loyers, emprunts=[], charges=[]):
        cfs = []
        
        # Extraire les interets d'emprunts
        interets = Flows()
        if len(emprunts) == 1:
                interets.add_series("Intêrets", emprunts[0].cash_flows["Interest"])
        else:
            for i, emprunt in enumerate(emprunts):
                interets_i = emprunt.cash_flows["Interest"]
                interets.add_series(f"Intêrets {i+1}", interets_i)

        # Créer un tableau pour le résultat comptable
        flux = [loyers, -interets] + charges
        df = Flows(flux).annual_flows()
        
    def calcul_deficit_foncier(df, TMI, PS):
        df["Resultat"] = df.sum(axis=1)
        df["Deficit reporté"] = 0
        
        deficits = []
        
        for i, idx in enumerate(df.index):
            R = df.at[idx, "Resultat"]

            if R < 0:
                deficits.append(-R)
                df.at[idx, "Deficit reporté"] = -R
                df.at[idx, "Resultat"] = 0
            else:
                for j, d in enumerate(deficits):
                    assert(d>=0)
                    
                    if d >= R:
                        deficits[j] -= R
                        R = 0
                        break
                    elif d:
                        R -= d
                        deficits[j] = 0
                        
                df.at[idx, "Resultat"] = R
                deficits.append(0)
                
            if i>=10:
                deficits.pop(0)

        # Ajouter colonnes
        df["IR"] = -df.Resultat * TMI / 100
        df["PS"] = -df.Resultat * PS / 100
        df["Total"] = df[["IR","PS"]].sum(axis=1)
        df["Pression fiscale"] = round(100 * abs((df["Total"] + df["Taxe fonciere"]) / df["Loyer"]), 2)
        return df
    
if __name__ == "__main__":
    from .rent import ILoyer as Loyer
    from .loan import Loan
    from .flows import Flows

    simulation_stop = dt.date(2060, 1, 1)
    
    rent = Loyer(350, inflation=1.5, garantie_loyers_impayes=3, stop=simulation_stop)
#    rent.add_single_flow(-10000, "Travaux", dt.datetime(2024,11,1))
#    rent.add_single_flow(-5000, "Travaux", dt.datetime(2030,11,1))
    
    loan = Loan(100e3, annual_rate=3.5, duration=25, start=dt.datetime.today())
    pret_travaux = Loan(5000, annual_rate=10, duration=5, start=dt.datetime(2030, 3, 1))
    
    taxe_fonciere = Flows()
    taxe_fonciere.add_regular_flow(-500, "Taxe Foncière", start=dt.datetime(2024, 10, 15), end=simulation_stop, freq="Y")
    print(taxe_fonciere)
    taxes = LocationNue()
    taxes.calculer_benefices(rent, [loan], [taxe_fonciere])
