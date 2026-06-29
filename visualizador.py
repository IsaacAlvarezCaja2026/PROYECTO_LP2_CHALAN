import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class VisualizadorPrecios:
    """
    Clase de nivel profesional encargada de la capa de visualización arquitectónica 
    del Sistema de Monitoreo de Precios Agrícolas.
    Satisface los requisitos de POO, segmentación categórica y presentación ejecutiva.
    """
    
    def __init__(self, archivo_datos="precios_agricolas_validado.csv"):
        """Carga el dataset y aplica estilos estéticos globales de publicación."""
        try:
            self.df = pd.read_csv(archivo_datos)
            self.df["Fecha"] = pd.to_datetime(self.df["Fecha"], format="%d/%m/%Y")
            self.df = self.df.dropna(subset=["Prom"])
            
            # Configuración de estilo estético y limpio para el trabajo final
            sns.set_theme(style="whitegrid")
            plt.rcParams["font.sans-serif"] = "Arial"
            plt.rcParams["font.family"] = "sans-serif"
            
            print(f"📈 Sistema de Visualización listo. {len(self.df)} registros procesados para exposición.")
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo '{archivo_datos}'.")

    def _agregar_etiquetas_barras(self, ax):
        """Método privado auxiliar para renderizar el valor exacto sobre cada barra."""
        for p in ax.patches:
            width = p.get_width()
            if width > 0:
                ax.annotate(
                    f"S/. {width:.2f}",
                    (width, p.get_y() + p.get_height() / 2),
                    ha="left", va="center",
                    xytext=(8, 0),
                    textcoords="offset points",
                    fontsize=10, fontweight="bold", color="#2c3e50"
                )

    def generar_grafico_tuberculos(self):
        """
        Gráfico 1: Análisis Comparativo de Tubérculos (Papas y Camotes).
        Filtra y agrupa las variedades solicitadas de manera específica.
        """
        # 1. Filtrar filas de papas y camotes por sus variedades clave
        condicion_papas = (self.df["Producto"].str.upper() == "PAPA") & (
            self.df["Variedad"].str.upper().str.contains("YUNGAY|AMARILLA|CANCHAN", na=False)
        )
        condicion_camotes = (self.df["Producto"].str.upper() == "CAMOTE") | (
            self.df["Producto"].str.lower().str.contains("camote", na=False)
        )
        
        # Corregido: usando 'condicion_camotes' en español
        df_tuberculos = self.df[condicion_papas | condicion_camotes].copy()
        
        # Estandarizar nombres para mostrar en el eje del gráfico
        def formatear_nombre(row):
            prod = str(row["Producto"]).upper()
            var = str(row["Variedad"]).upper()
            if "PAPA" in prod:
                if "AMARILLA" in var: return "Papa Amarilla"
                if "YUNGAY" in var: return "Papa Yungay"
                if "CANCHAN" in var: return "Papa Canchán"
            if "CAMOTE" in prod or "CAMOTE" in var:
                if "AMARILLO" in var or "amarillo" in str(row["Producto"]): return "Camote Amarillo"
                if "MORADO" in var or "morado" in str(row["Producto"]): return "Camote Morado"
            return "Otros Tubérculos"

        df_tuberculos["Etiqueta"] = df_tuberculos.apply(formatear_nombre, axis=1)
        df_tuberculos = df_tuberculos[df_tuberculos["Etiqueta"] != "Otros Tubérculos"]
        
        # Agrupar por el promedio histórico de la semana
        data_final = df_tuberculos.groupby("Etiqueta")["Prom"].mean().sort_values(ascending=False).reset_index()
        
        # Construcción de la figura
        fig, ax = plt.subplots(figsize=(11, 5))
        paleta_elegida = sns.color_palette("YlOrBr_r", n_colors=len(data_final))
        
        sns.barplot(data=data_final, x="Prom", y="Etiqueta", ax=ax, palette=paleta_elegida, hue="Etiqueta", legend=False)
        
        # Acabados de alta gama (Eliminar bordes innecesarios)
        sns.despine(left=True, bottom=True)
        self._agregar_etiquetas_barras(ax)
        
        # Títulos y formato de presentación
        plt.title("ANÁLISIS DE PRECIOS: TUBÉRCULOS EN EL MERCADO MAYORISTA Y MINORISTA", fontsize=13, fontweight="bold", color="#1a252f", pad=20)
        plt.xlabel("Precio Promedio Registrado (S/. por Kilogramo)", fontsize=11, color="#34495e", labelpad=10)
        plt.ylabel("", fontsize=11)
        plt.xlim(0, data_final["Prom"].max() * 1.15) # Espacio para las etiquetas de texto
        
        plt.tight_layout()
        plt.savefig("reporte_tuberculos_profesional.png", dpi=300)
        plt.show()
        print("💾 Reporte de tubérculos guardado con resolución 300 DPI.")

    def generar_grafico_frutas(self):
        """
        Gráfico 2: Análisis de Precios de Frutas y Oleaginosas (Manzanas y Paltas).
        Muestra la brecha comercial de las variedades de alta demanda.
        """
        df_frutas = self.df.copy()
        
        def formatear_nombre_frutas(row):
            prod = str(row["Producto"]).upper()
            var = str(row["Variedad"]).upper()
            
            if "MANZANA" in prod or "MANZANA" in var:
                if "DELICIA" in var or "DELICIA" in prod: 
                    return "Manzana Delicia"
                if "CORRIENTE" in var or "CTE" in prod or "CTE" in var or "AGUA" in var: 
                    return "Manzana Corriente"
                return "Manzana (Otra)"
                
            if "PALTA" in prod or "PALTA" in var:
                return "Palta Fuerte"
                
            return "Otros"

        df_frutas["Etiqueta"] = df_frutas.apply(formatear_nombre_frutas, axis=1)
        df_frutas = df_frutas[df_frutas["Etiqueta"].isin(["Manzana Delicia", "Manzana Corriente", "Palta Fuerte"])]
        
        if df_frutas.empty:
            print("⚠️ Alerta: No se encontraron registros que coincidan con los criterios de frutas.")
            return
            
        data_final = df_frutas.groupby("Etiqueta")["Prom"].mean().sort_values(ascending=False).reset_index()
        
        # Construcción gráfica profesional de alta gama
        fig, ax = plt.subplots(figsize=(11, 5))
        
        # CORREGIDO: 'crest_r' en minúsculas para evitar el ValueError
        paleta_elegida = sns.color_palette("crest_r", n_colors=len(data_final))
        
        sns.barplot(data=data_final, x="Prom", y="Etiqueta", ax=ax, palette=paleta_elegida, hue="Etiqueta", legend=False)
        
        sns.despine(left=True, bottom=True)
        self._agregar_etiquetas_barras(ax)
        
        plt.title("ANÁLISIS DE PRECIOS: FRUTAS Y OLEAGINOSAS SELECCIONADAS", fontsize=13, fontweight="bold", color="#1a252f", pad=20)
        plt.xlabel("Precio Promedio Registrado (S/. por Kilogramo)", fontsize=11, color="#34495e", labelpad=10)
        plt.ylabel("", fontsize=11)
        plt.xlim(0, data_final["Prom"].max() * 1.15)
        
        plt.tight_layout()
        plt.savefig("reporte_frutas_profesional.png", dpi=300)
        plt.show()
        print("💾 Reporte de frutas guardado exitosamente en alta resolución (300 DPI).")

if __name__ == "__main__":
    visualizador = VisualizadorPrecios()
    # Ejecución de los gráficos solicitados para el trabajo final
    visualizador.generar_grafico_tuberculos()
    visualizador.generar_grafico_frutas()