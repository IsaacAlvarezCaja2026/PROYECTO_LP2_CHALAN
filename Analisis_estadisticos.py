import pandas as pd

class AnalizadorPrecios:
    def __init__(self):
        self.df = pd.read_csv("precios_agricolas_consolidado.csv")
        self.df["Fecha"] = pd.to_datetime(self.df["Fecha"], format="%d/%m/%Y")
        self.df["Prom"] = pd.to_numeric(self.df["Prom"], errors="coerce")
        self.df["Min"] = pd.to_numeric(self.df["Min"], errors="coerce")
        self.df["Max"] = pd.to_numeric(self.df["Max"], errors="coerce")

## Análisis temporal
    
    def variedades_por_producto(self):
            """Cuántas variedades distintas tiene cada producto."""

            resultado = (
                self.df.groupby("Producto")["Variedad"]
                .nunique()
                .sort_values(ascending=False)
            )

            return resultado

