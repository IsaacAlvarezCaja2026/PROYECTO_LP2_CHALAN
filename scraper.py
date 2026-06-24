import requests
from bs4 import BeautifulSoup
import pandas as pd

class ScraperAgricola:
    def __init__(self, fecha_inicio, fecha_fin):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.datos_recolectados = [] 

    def obtener_datos_emmsa(self):
        print("Iniciando extracción de EMMSA...")
        url_emmsa = "https://www.emmsa.com.pe/index.php/precios-diarios/"
        
        # Conexión a la red
        respuesta = requests.get(url_emmsa)
        
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            print("¡Conexión a EMMSA exitosa! Código 200 OK.")
        else:
            print(f"Error al conectar con EMMSA: {respuesta.status_code}")

    def obtener_datos_midagri(self):
        pass

    def exportar_a_csv(self):
        pass

# --- ZONA DE PRUEBAS ---
if __name__ == "__main__":
    mi_scraper = ScraperAgricola("17/06/2026", "24/06/2026")
    mi_scraper.obtener_datos_emmsa()