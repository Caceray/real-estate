from .flows import Flows

class Rent(Flows):
    def __init__(self, nominal, start, end, warranty=0, broker_fees=0, inflation=0):
        Flows.__init__(self)
        self.nominal = nominal
        self.start = start
        self.end = end
        self.warranty = warranty
        self.broker_fees = broker_fees
        self.inflation = inflation

        self.add_regular_flow(nominal, "Loyer", start, end, inflation=inflation)

        if warranty:
            self.add_proportional_flows("Loyer", -self.warranty/100, "GLI")

        if broker_fees:
            # Adjust first cash flow by fees
            for date, cf in self.cash_flows["Loyer"].items():
                self.cash_flows["Loyer"][date] = cf - broker_fees
                break

if __name__ == "__main__":
    import datetime as dt

    rent = Rent(350, dt.date(2024, 9 , 1), dt.date(2025, 9, 1), warranty=10, broker_fees=500, inflation=1)
    print(rent.get_dataframe())