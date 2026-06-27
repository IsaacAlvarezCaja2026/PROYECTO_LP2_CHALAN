import pandas as pd

class ProcesadorPrecios:

    def __init__(self):
        self.df = pd.read_csv("precios_agricolas_consolidado.csv")
## Limpieza de datos 
    def limpiar_datos(self):
            """Limpia y transforma los datos."""
    
            # Convertir fecha
            self.df["Fecha"] = pd.to_datetime(
                self.df["Fecha"],
                format="%d/%m/%Y"
            )
    
            # Convertir columnas numéricas
            columnas = ["Min", "Max", "Prom"]
    
            self.df[columnas] = self.df[columnas].apply(
                pd.to_numeric,
                errors="coerce"
            )
    
            # Eliminar filas con datos faltantes
            self.df = self.df.dropna(subset=columnas)
    
            # Eliminar duplicados
            self.df = self.df.drop_duplicates()
    
            print("Datos limpiados correctamente.")
    
    def transformar_datos(self):
            """Crea nuevas columnas."""
    
            self.df["Rango"] = self.df["Max"] - self.df["Min"]
    
            self.df["Mes"] = self.df["Fecha"].dt.month_name()
    
            print("Transformación completada.")
## Añadimos analisis estadistico    
    def estadisticas_generales(self):
            """Muestra estadísticas descriptivas."""
    
            print(self.df.describe())
    
    def precio_promedio_producto(self):
            """Precio promedio por producto."""
    
            resultado = (
                self.df.groupby("Producto")["Prom"]
                .mean()
                .sort_values(ascending=False)
            )
    
            return resultado
    
    def resumen_productos(self):
            """Resumen estadístico por producto."""
    
            resumen = (
                self.df.groupby("Producto")
                .agg(
                    Precio_Minimo=("Min", "min"),
                    Precio_Maximo=("Max", "max"),
                    Precio_Promedio=("Prom", "mean"),
                    Desviacion=("Prom", "std"),
                    Registros=("Prom", "count")
                )
                .round(2)
            )
    
            return resumen
    
    def productos_mas_volatiles(self):
            """Productos con mayor variación."""
    
            volatilidad = (
                self.df.groupby("Producto")["Rango"]
                .mean()
                .sort_values(ascending=False)
            )
    
            return volatilidad
## Exportamos datos    
    def exportar_resultados(self):
            """Guarda los resultados."""
    
            self.resumen_productos().to_csv(
                "resumen_productos.csv"
            )
    
            self.productos_mas_volatiles().to_csv(
                "productos_volatiles.csv"
            )
    
            print("Archivos exportados correctamente.")
