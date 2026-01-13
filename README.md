Este proyecto analiza más de 1,000 productos del mercado de mascotas en México específicamente en 
el estado de Oaxacapara identificar oportunidades de negocio, tendencias de precios y segmentos rentables (Matriz BCG).

-------- Hallazgos Principales ----------
1. Concentración de Valor (Ley de Potencia): El segmento "Estrella" (Precio > $319 MXN + Alto Volumen) 
es el motor del mercado, generando más del 90% de los ingresos totales, superando masivamente a las estrategias de 
bajo costo.

2. Techo del Mercado Masivo: Existe una barrera psicológica de precio en los $1,300 MXN. 
Los productos que superan este umbral sufren una caída drástica en el volumen de ventas,
limitándose a nichos muy específicos.

3. Polarización de Categorías: Mientras que Accesorios domina en cantidad de oferta (mercado saturado),
las categorías de Alimento y Suplementos dominan en volumen de ventas y retención, demostrando ser el
modelo de negocio más escalable por su recurrencia.

----- Tecnologías Utilizadas ------
Python 3.13**
Pandas & NumPy:** Limpieza y manipulación de datos.
Seaborn & Matplotlib:** Visualización de datos y storytelling.
BeautifulSoup & Requests:** Web Scraping ético para obtención de datos.

-------- Estructura del Proyecto ----------
├── data/               # Datasets crudos y procesados
├── notebooks/          # Análisis exploratorio y gráficas (Jupyter)
├── src/                # Código fuente (ETL y Scraping)
│   ├── scraper.py      # Script de extracción de datos
│   ├── data_cleaning.py# Limpieza y segmentación de negocio
│   └── categorization.py # Lógica de clasificación de productos
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación

---- Cómo ejecutar este proyecto ----
1. Clonar el repositorio.
2. Instalar dependencias:
     ```bash
  pip install -r requirements.txt
   

