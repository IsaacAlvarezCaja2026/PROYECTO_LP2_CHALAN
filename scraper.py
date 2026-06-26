import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime, timedelta

# Desactivar advertencias de seguridad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ScraperAgricola:
    """
    Clase encargada de realizar el web scraping a la plataforma de EMMSA.
    Extrae precios diarios de productos agrícolas en un rango de fechas.
    """
    
    def __init__(self, fecha_inicio, fecha_fin):
        """Inicializa el scraper con un rango de fechas."""
        self.inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
        self.fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        self.url = "https://old.emmsa.com.pe/emmsa_spv/app/reportes/ajax/rpt07_gettable_new_web.php"
        self.datos_totales = []

    def obtener_datos_emmsa(self):
        """Itera por cada fecha, solicita los datos al servidor y los consolida."""
        fecha_actual = self.inicio
        while fecha_actual <= self.fin:
            fecha_str = fecha_actual.strftime("%d/%m/%Y")
            print(f"Extrayendo datos para: {fecha_str}")
            
            payload = {
                'vid_tipo': '1',
                'vprod': '81,73,12,38',
                'vvari': '8105,8106,8107,8111,8115,8118,7301,7302,7303,7305,1201,1202,1203,1204,3801,3802,3803,3804,3805,3806,3807,3808,3809,3810,3811,3812,3813,3814,3815,3816,3817,3818',
                'vfecha': fecha_str
            }
            
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            respuesta = requests.post(self.url, data=payload, headers=headers, verify=False)
            
            if respuesta.status_code == 200:
                self._procesar_tabla(respuesta.text, fecha_str)
            
            fecha_actual += timedelta(days=1)
            
        df = pd.DataFrame(self.datos_totales)
        df.to_csv('precios_semana_emmsa.csv', index=False)
        print("¡Proceso terminado! Archivo 'precios_semana_emmsa.csv' creado.")

    def _procesar_tabla(self, html, fecha):
        """Limpia el HTML recibido y extrae los datos de la tabla."""
        soup = BeautifulSoup(html, 'html.parser')
        tabla = soup.find('table', {'class': 'timecard'})
        if tabla:
            filas = tabla.find_all('tr')
            for fila in filas[1:]:
                celdas = fila.find_all('td')
                if len(celdas) >= 5:
                    self.datos_totales.append({
                        'Fecha': fecha,
                        'Producto': celdas[0].text.strip(),
                        'Variedad': celdas[1].text.strip(),
                        'Min': celdas[2].text.strip(),
                        'Max': celdas[3].text.strip(),
                        'Prom': celdas[4].text.strip()
                    })
    def obtener_datos_midagri(self):
        """Extrae datos de MIDAGRI (Precios Minoristas) iterando por el rango de fechas."""
        self.datos_midagri = []
        
        fecha_actual = self.inicio
        
        while fecha_actual <= self.fin:
            fecha_str = fecha_actual.strftime("%d/%m/%Y")
            print(f"Extrayendo datos de MIDAGRI para: {fecha_str}")
            
            # URL actualizada con 'min_precio_prom' y 'periodicidad=dia'
            url_ajax = f"http://sistemas.midagri.gob.pe/sisap/portal2/ciudades/resumenes/filtrar?&region=*&&variables[]=min_precio_prom&&fecha={fecha_str}&desde=17/06/2026&&hasta=24/06/2026&&anios[]=2026&&meses[]=06&&&productos[]=010101&productos[]=010103&productos[]=061701&productos[]=061703&productos[]=062607&&periodicidad=dia&&&&&&&&&&__ajax_carga_final=consulta&ajax=true"
            
            try:
                respuesta = requests.get(url_ajax, verify=False)
                
                if respuesta.status_code == 200:
                    soup = BeautifulSoup(respuesta.text, 'html.parser')
                    tabla = soup.find('table') 
                    
                    if tabla:
                        filas = tabla.find_all('tr')
                        for fila in filas[3:]: 
                            celdas = fila.find_all('td')
                            
                            # Validamos que haya al menos 4 celdas (Producto, Unidad, Equiv, Precio)
                            if len(celdas) >= 4:
                                self.datos_midagri.append({
                                    'Fecha': fecha_str,  
                                    'Producto': celdas[0].text.strip(),                         
                                    'Prom': celdas[3].text.strip()      
                                })
            except Exception as e:
                print(f"Error en MIDAGRI para la fecha {fecha_str}: {e}")
                
            fecha_actual += timedelta(days=1)
            
        print(f"¡Se extrajeron {len(self.datos_midagri)} registros totales de MIDAGRI!")
    
    def exportar_a_csv(self):

        """Modifica/crea el método para recibir los datos de ambas fuentes 

        (EMMSA + MIDAGRI) y usa pd.concat para unirlos en un solo CSV.

        """
        try:

            df_emmsa = pd.read_csv('precios_semana_emmsa.csv')

            df_midagri = pd.read_csv('precios_semana_midagri.csv')

            if 'Min' not in df_midagri.columns:

                df_midagri['Min'] = ""

            if 'Max' not in df_midagri.columns:

                df_midagri['Max'] = ""

            df_final = pd.concat([df_emmsa, df_midagri], ignore_index=True)


            df_final.to_csv('precios_agricolas_consolidado.csv', index=False)

            print("¡Archivo 'precios_agricolas_consolidado.csv' generado con éxito!")

            

        except FileNotFoundError as e:

            print(f"Error: Faltan archivos previos para consolidar. Detalle: {e}")
        
        if self.datos_midagri:
            df_midagri = pd.DataFrame(self.datos_midagri)
            df_midagri.to_csv('precios_semana_midagri.csv', index=False)
            print("Archivo 'precios_semana_midagri.csv' creado.")
                
      


if __name__ == "__main__":
    scraper = ScraperAgricola("17/06/2026", "24/06/2026")
    scraper.obtener_datos_emmsa()
    scraper.obtener_datos_midagri()
    scraper.exportar_a_csv()