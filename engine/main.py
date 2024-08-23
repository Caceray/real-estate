from rent import Rent
from taxes import Tax
from amortization import Loan

import pandas as pd
import numpy as np
import datetime as dt

nominal = 50e3

rent = Rent(350, inflation=1)
rents = rent.get_cash_flows()
print(rent)

tax = Tax()
taxes = tax.get_cash_flows(rents)

loan = Loan(nominal, 3.5, 25, dt.datetime(2024, 9, 1))
payments = loan.get_cash_flows()

df = pd.concat([rents, taxes, payments, pd.Series(nominal, index=[dt.datetime(2051,1,1)])], axis=1).fillna(0)
CF = df.sum(axis=1)
print(CF)

r = 1
R = (1 + r/100) ** (1/12)

VAN = 0
f = R
for cf in CF:
    VAN += cf * f
    f *= R
print(VAN)
