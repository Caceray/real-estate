import pandas as pd
import datetime as dt

from .flows import Flows

AM = "Amortissement"
ITR = "Intérêts"
CRD = "Capital restant dû"

class Loan(Flows):
    def __init__(self, amount, annual_rate, duration, start):
        super().__init__()
        
        R = (1 + annual_rate / 100) ** (1/12) - 1
        D = duration * 12
        
        self.monthly_rate = R
        self.monthly_payment = amount * R / ( 1 - ( 1 + R ) ** (-D) )
        print(f"Mensualité = {self.monthly_payment:.2f}€")

        self.duration = duration * 12
        
        # Create DataFrame
        remaining = amount
        amortizations, outstanding_principal, interests = [], [], []
        for i in range(duration * 12):
            interest = remaining * self.monthly_rate
            amortization = self.monthly_payment - interest
            remaining -= amortization
            
            outstanding_principal.append(round(remaining, 2))
            
            I = round(interest, 2)
            amortizations.append(round(self.monthly_payment - I, 2))
            interests.append(I)
            
        index = pd.date_range(start=start, periods=self.duration, freq='MS') + pd.DateOffset(days=start.day-1)
        self.add_flows(index, amortizations, AM)
        self.add_flows(index, interests, ITR)
        self.add_flows(index, outstanding_principal, CRD)

    def __str__(self):
        df = self.get_dataframe()
        return str(df)
    
    def annual_flows(self, expanded=True):
        df = self.get_dataframe()
        df = df.groupby(pd.Grouper(freq='YE')).agg({AM: 'sum',
                                                    ITR: 'sum',
                                                    CRD: 'last'})
        return df
        
if __name__ == "__main__":
    a = Loan(100000, 1, 25, start=dt.datetime(2024, 8, 31))
    print(a)
    print(a.annual_flows())
