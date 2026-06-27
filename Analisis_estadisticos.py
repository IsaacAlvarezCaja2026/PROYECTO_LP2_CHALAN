import pandas as pd

class AnalizadorPrecios:
    def __init__(self):
        self.df = pd.read_csv("precios_agricolas_consolidado.csv")
        self.df["Fecha"] = pd.to_datetime(self.df["Fecha"], format="%d/%m/%Y")
        self.df["Prom"] = pd.to_numeric(self.df["Prom"], errors="coerce")
        self.df["Min"] = pd.to_numeric(self.df["Min"], errors="coerce")
        self.df["Max"] = pd.to_numeric(self.df["Max"], errors="coerce")


