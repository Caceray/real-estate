from django.db import models
from django import forms

import engine
from engine.rent import ILoyer
from engine.loan import Loan as ILoan

class Rent(models.Model):
    rent = models.fields.IntegerField(default=350)
    warranty = models.fields.FloatField(default=2.5)
    start = models.DateField(default="2024-09-01")
    broker_fees = models.fields.IntegerField(default=300)
    
    def to_html(self, annual=True):
        rents = ILoyer(self.rent, start=self.start, garantie_loyers_impayes=self.warranty)
        if annual:
            df = rents.annual_flows()
        else:
            df = rents.get_dataframe()
        return df.to_html()
    
    def get_object(self):
        return ILoyer(self.rent, start=self.start, garantie_loyers_impayes=self.warranty)
    
class Charge(models.Model):
    property_tax = models.fields.IntegerField(default=500)
    waste_collection_tax = models.fields.IntegerField(default=250)
    
    def generate_cash_flows(self):
        print("Génération des CF pour les charges locatives")

class Loan(models.Model):
    nominal = models.fields.IntegerField(default=100000)
    rate = models.fields.FloatField(default=3.9)
    duration = models.fields.IntegerField(default=25)
    start = models.DateField(default="2024-09-01")

    def to_html(self, annual=True):
        loan = ILoan(self.nominal, self.rate, self.duration, self.start)
        
        if annual:
            df = loan.annual_flows()
        else:
            df = loan.get_dataframe()

        # French labels
        df.rename(columns={"Amortization":"Amortissement",
                           "Interest":"Intérêts",
                           "Outstanding principal":"Capital restant dû"}, inplace=True)
        
        return df.to_html()
    
    def get_object(self):
        return ILoan(self.nominal, self.rate, self.duration, self.start)

class Acquisition(models.Model):
    nominal = models.fields.IntegerField(default=100000)
    fees = models.fields.IntegerField(default=10000)
    start = models.DateField(default="2024-09-01")