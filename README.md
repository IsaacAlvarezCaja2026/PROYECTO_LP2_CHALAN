# UNIVERSIDAD NACIONAL AGRARIA LA MOLINA

## DEPARTAMENTO ACADÉMICO DE ESTADÍSTICA E INFORMÁTICA

<p align="center">
  <img src="https://seeklogo.com/images/U/universidad-nacional-agraria-la-molina-logo-5BF0B8D973-seeklogo.com.png" alt="Universidad Nacional Agraria La Molina Logo" width="200">
</p>

### Práctica Dirigida 3: Sistema de Monitoreo de Precios Agrícolas del Perú 🥔🥑

---

## 📋 Descripción del Proyecto
Este proyecto es un sistema integral de extracción, procesamiento y visualización de datos desarrollado en Python. Su objetivo es monitorear, consolidar y analizar los precios diarios de productos agrícolas en el Perú, contrastando dos fuentes oficiales:
* **EMMSA (Mercado Mayorista):** Precios base de comercialización en Lima.
* **MIDAGRI / SISAP (Mercado Minorista):** Precios de venta al consumidor final.

El proyecto está construido bajo el paradigma de **Programación Orientada a Objetos (POO)** y cumple con todo el ciclo de vida del dato: desde la extracción en la web hasta la presentación de reportes gerenciales.

---

## 🚀 Arquitectura y Fases del Sistema

El sistema está dividido en módulos independientes para garantizar un código limpio y escalable:

1. **Módulo de Extracción (`scraper.py`):**  Se conecta mediante solicitudes HTTP (`requests`) a las plataformas de EMMSA (POST) y MIDAGRI (GET).
   * Utiliza `BeautifulSoup` para analizar el HTML y extraer las tablas de precios de toda una semana.
   * Implementa validación y limpieza de cadenas mediante **Expresiones Regulares (Regex)** para asegurar que los precios sean numéricos.

2. **Módulo de Procesamiento (`procesamiento_pandas.py` y `Analisis_estadisticos.py`):**
   * Utiliza la librería `pandas` para consolidar ambas fuentes en un único Dataset.
   * Realiza limpieza de datos nulos (`dropna`), eliminación de duplicados y transformación de tipos de datos.
   * Genera alertas de volatilidad y análisis temporal de precios.

3. **Módulo de Visualización (`visualizador.py` y `graficos_adicionales.ipynb`):**
   * Emplea `matplotlib` y `seaborn` para generar reportes visuales de alta calidad.
   * Gráficos implementados: Análisis comparativo de Tubérculos, Evolución de Frutas (Barras), Evolución temporal (Líneas) y Distribución de precios (Boxplot).

---

## 🛠️ Tecnologías y Librerías Utilizadas
* **Lenguaje:** Python 3.x
* **Control de Versiones:** Git & GitHub
* **Librerías principales:** * `requests` y `urllib3` (Redes y APIs)
  * `beautifulsoup4` (Web Scraping)
  * `re` (Expresiones Regulares)
  * `pandas` (Manipulación de Datos)
  * `matplotlib` y `seaborn` (Visualización)

---

## ⚙️ Instrucciones de Ejecución (Guía de Clonación y Uso)

Para que el proyecto funcione correctamente en un entorno local, sigue esta guía paso a paso:

**1. Clonar el repositorio:**
Primero, descarga el código desde la nube a tu computadora. Abre tu terminal (Git Bash o la terminal de tu sistema) y ejecuta:
```bash
git clone https://github.com/IsaacAlvarezCaja2026/PROYECTO_LP2_CHALAN.git
cd PROYECTO_LP2_CHALAN

**2. Instalación de dependencias:**
Una vez dentro de la carpeta del proyecto, instala las librerías necesarias ejecutando:

```bash
pip install -r Requerimientos.txt
```

**3. Extracción y validación de datos:**
Ejecuta el script principal de scraping. Esto descargará los datos en vivo de internet y generará el archivo consolidado y validado de forma automática:

```Bash
python scraper.py
```

**4. Análisis y estadísticas:**
Ejecuta los motores de procesamiento para que Pandas limpie la data y genere los CSVs con los resúmenes estadísticos (alertas_precio.csv, resumen_productos.csv, variedades_por_producto.csv, productos_volatiles.csv):
```Bash
python procesamiento_pandas.py
python Analisis_estadisticos.py
```

**5. Generación de Reportes Visuales:**
Finalmente, ejecuta el visualizador para renderizar los datos y guardar los gráficos PNG gerenciales en alta resolución:
```Bash
python visualizador.py
```

---

## 👥 Integrantes del Equipo

Nicole Alva Aquino - **Nalva19** - 2021388

Isaac Alvarez Caja - **IsaacAlvarezCaja2026** - 20221389

César Huarac Vega - **notmecj0** - 20231495

Junior Jesus Mena Mamani - **haksito** - 20241389

Sergio Mendoza Chavez - **290803S** - 20231499

Andy Mayta Quintana - **andykmq** - 20190234
