import pandas as pd
import datetime as dt

class Flows:
    def __init__(self, flows=[]):
        self.cash_flows = {}
        
        assert(isinstance(flows, list))
        if flows:
            for cf in flows:
                self.cash_flows.update(cf.cash_flows)
        
    def add_regular_flow(self, amount, name, start, end, periods=None, freq="MS", inflation=0):
        assert(not name in self.cash_flows.keys())
        
        index = pd.date_range(start, end, periods, freq)
        cfs = []
        for i, date in enumerate(index):
            cf = amount * (1 + inflation/100) ** (i//12)
            cfs.append(round(cf, 2))

        self.add_flows(index, cfs, name)
        
    def add_single_flow(self, amount, name, date):
        if not name in self.cash_flows.keys():
            self.cash_flows[name] = {}
            
        self.cash_flows[name][date] = amount
        
    def add_flows(self, dates, cash_flows, name):
        assert(not name in self.cash_flows.keys())
        self.cash_flows[name] = {i:cf for i,cf in zip(dates, cash_flows)}
        
    def add_series(self, name, series):
        assert(not name in self.cash_flows.keys())
        self.cash_flows[name] = series
#    def remove_flows(self, name):
#        del self.cash_flows[name]
        
    def __str__(self):
        df = self.get_dataframe()
        return str(df)
        
    def __neg__(self):
        F = self
        for cat, cfs in F.cash_flows.items():
            cfs = {k:-v for k,v in cfs.items()}
            F.cash_flows[cat] = cfs
        return F
        
    def get_dataframe(self):
        return pd.DataFrame(self.cash_flows).fillna(0).sort_index()
        
    def annual_flows(self, expanded=True):
        df = self.get_dataframe()
        
        if expanded:
            return df.groupby(pd.Grouper(freq='YE')).sum()
        else:
            return df.groupby(pd.Grouper(freq='YE')).sum().sum(axis=1)
        
        
if __name__ == "__main__":
    flows = Flows()
    
    start = dt.datetime(2024, 9, 5)
    end = dt.datetime(2026, 9, 5)
    freq = "M"
    
    flows.add_regular_flow(300, "Rent", start=start, end=end, freq=freq)
    flows.add_regular_flow(-3, "Warranty", start=start, end=end, freq=freq)
    flows.add_single_flow(dt.datetime(2024, 9, 28), -2000, "Fees")
        
        
