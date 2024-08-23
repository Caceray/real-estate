from django.db import models
from django import forms

import engine

import datetime as dt
from abc import abstractmethod

END = dt.date(2060, 1, 1)

class BaseModel(models.Model):
    dataframe_engine = None

    class Meta:
        abstract = True

    @abstractmethod
    def create_dataframe(self):
        raise NotImplementedError

    @abstractmethod
    def to_html(self, annual=True):
        raise NotImplementedError
    
    def to_html(self, annual=True):
        assert(not self.dataframe_engine is None)
        if annual:
            df = self.dataframe_engine.annual_flows()
        else:
            df = self.dataframe_engine.get_dataframe()
        return df.to_html()
    
    def get_dataframe(self):
        return self.dataframe_engine.get_dataframe()
    
class Rent(BaseModel):
    rent = models.fields.IntegerField(default=350)
    warranty = models.fields.FloatField(default=2.5)
    start = models.DateField(default="2024-09-01")
    broker_fees = models.fields.IntegerField(default=300)

    def create_dataframe(self):
        self.dataframe_engine = engine.Rent(self.rent, self.start, END, warranty=self.warranty, broker_fees=self.broker_fees)

class Charge(BaseModel):
    property_tax = models.fields.IntegerField(default=500)
    waste_collection_tax = models.fields.IntegerField(default=250)
    start = None
    end = None

    def create_dataframe(self):
        assert(not self.start is None)
        assert(not self.end is None)
        self.dataframe_engine = engine.Flows()

        self.dataframe_engine.add_regular_flow(self.property_tax, "Property tax", self.start, self.end, freq="Y")
        self.dataframe_engine.add_regular_flow(self.waste_collection_tax, "Waste tax", self.start, self.end, freq="Y")

class Loan(BaseModel):
    nominal = models.fields.IntegerField(default=100000)
    rate = models.fields.FloatField(default=3.9)
    duration = models.fields.IntegerField(default=25)
    start = models.DateField(default="2024-09-01")
    
    def create_dataframe(self):
        self.dataframe_engine = engine.Loan(self.nominal, self.rate, self.duration, self.start)

class Acquisition(BaseModel):
    nominal = models.fields.IntegerField(default=100000)
    fees = models.fields.IntegerField(default=10000)
    start = models.DateField(default="2024-09-01")

    def create_dataframe(self):
        self.dataframe_engine = engine.Flows()

    def to_html(self, annual=True):
        pass