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
## Detección de anomalías
    def alertas_precio(self, umbral_subida: float = 10.0, umbral_bajada: float = -10.0):
            """Detecta variaciones bruscas entre fechas consecutivas por variedad."""

            df_ord = self.df.sort_values(["Variedad", "Fecha"]).copy()

            df_ord["Cambio_%"] = (
                df_ord.groupby("Variedad")["Prom"]
                .pct_change() * 100
            ).round(2)

            alertas = df_ord[
                (df_ord["Cambio_%"] >= umbral_subida) |
                (df_ord["Cambio_%"] <= umbral_bajada)
            ]

            return alertas[["Fecha", "Producto", "Variedad", "Prom", "Cambio_%"]]
    
##Precios por fecha
    def precio_en_fecha(self, fecha: str):
            """Precios de todos los productos en una fecha específica."""

            fecha_dt = pd.to_datetime(fecha, format="%d/%m/%Y")

            resultado = (
                self.df[self.df["Fecha"] == fecha_dt]
                [["Producto", "Variedad", "Min", "Max", "Prom"]]
                .sort_values("Producto")
            )

            return resultado

## Exportamos datos
    def exportar_resultados(self):
            """Guarda los resultados de los análisis en archivos CSV."""

            self.alertas_precio().to_csv("alertas_precio.csv")

            self.variedades_por_producto().to_csv("variedades_por_producto.csv")

            print("Archivos exportados correctamente.")

