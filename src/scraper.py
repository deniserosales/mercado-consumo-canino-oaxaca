# #Módulo de Web Scraping para Mercado Libre.
# -------------------------------------------------------------------
# Este script extrae datos de productos (Título, Precio, Ventas, Links)
# simulando navegación humana para evitar bloqueos básicos.

# NOTA IMPORTANTE:
# Las estructuras HTML de sitios como Mercado Libre cambian constantemente.
# Este script fue funcional al momento de la extracción de los datos originales 
# (Diciembre 2025). Si se ejecuta hoy, es posible que requiera ajustes en los 
# selectores CSS (BeautifulSoup) para adaptarse al diseño actual del sitio.

# Dataset generado: data/raw/dataset_perros_mx_1000.csv

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

# --- CONFIGURACIÓN DE ALTO VOLUMEN ---
ESTADO = 'oaxaca'

PAGINAS_A_BUSCAR = 12 
BASE_URL = f"https://listado.mercadolibre.com.mx/{ESTADO}/perros"

def obtener_html(url):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15'
    ]
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'es-MX,es;q=0.9',
        'Referer': 'https://www.google.com/'
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            return r.text
        return None
    except Exception as e:
        print(f" Error red: {e}")
        return None

def limpiar_precio(texto):
    if not texto: return 0
    try:
        limpio = re.sub(r'[^\d.]', '', texto)
        return float(limpio)
    except:
        return 0

def extraer_vendidos(item_node):
    texto_vendidos = "0"
    
    # ESTRATEGIA 1: Diseño Nuevo (Poly) - Suele estar en reviews
    # Busca etiquetas que contengan la palabra "vendidos"
    etiquetas = item_node.find_all(['span', 'div', 'p'])
    
    for tag in etiquetas:
        texto = tag.get_text().lower()
        if 'vendido' in texto:
            # Extraer solo los números (ej: "+100 vendidos" -> 100)
            # Usamos Regex para sacar números
            numeros = re.findall(r'\d+', texto.replace(',', '').replace('.', ''))
            if numeros:
                # A veces el primer número es el rating (4.5), tomamos el mayor por si acaso
                # o el último que suele ser la cantidad
                texto_vendidos = numeros[-1]
                break
    
    # ESTRATEGIA 2: Diseño Clásico
    if texto_vendidos == "0":
        ui_text = item_node.find('div', class_='ui-search-item__group__element')
        if ui_text and 'vendido' in ui_text.text.lower():
             numeros = re.findall(r'\d+', ui_text.text.replace(',', ''))
             if numeros:
                 texto_vendidos = numeros[0]

    return int(texto_vendidos)

def extraer_visual(html):
    soup = BeautifulSoup(html, 'html.parser')
    productos = []
    
    # Detectar contenedores (Busca ambos tipos)
    items = soup.find_all('li', class_='ui-search-layout__item')
    if not items:
        items = soup.find_all('div', class_='poly-card__content')
        if not items:
             # Último intento: buscar divs genéricos de resultados
             items = soup.find_all('div', class_='ui-search-result__wrapper')

    for item in items:
        try:
            # 1. TÍTULO
            titulo_tag = item.find('h2', class_='ui-search-item__title') or \
                         item.find('a', class_='poly-component__title') or \
                         item.find('h2', class_='poly-box')
            
            titulo = titulo_tag.text.strip() if titulo_tag else "Sin Título"
            
            # 2. PRECIO
            # Buscamos cualquier cosa que parezca precio actual
            precio_tag = item.find('span', class_='andes-money-amount__fraction')
            precio = limpiar_precio(precio_tag.text) if precio_tag else 0
            
            # 3. VENDIDOS 
            vendidos = extraer_vendidos(item)
            
            # 4. LINK
            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else ""

            # Filtro de calidad: Solo guardar si tiene precio
            if precio > 0:
                productos.append({
                    'titulo': titulo,
                    'precio': precio,
                    'vendidos_estimados': vendidos,
                    'link': link,
                    'estado': ESTADO.capitalize()
                })
                
        except Exception:
            continue

    return productos

def main():
    print(f" INICIANDO SCRAPER (META: 550 PRODUCTOS)")
    print(f" Estado: {ESTADO.upper()}")
    
    datos_totales = []
    
    for pagina in range(1, PAGINAS_A_BUSCAR + 1):
        # Paginación 1, 51, 101...
        inicio = 1 + (pagina - 1) * 50
        
        if pagina == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}_Desde_{inicio}"
            
        print(f"\n Escaneando página {pagina} ({len(datos_totales)} acumulados)...")
        
        html = obtener_html(url)
        
        if html:
            # Verificación de bloqueo
            if "captcha" in html.lower():
                print(" CAPTCHA DETECTADO. Deteniendo para salvar los datos actuales.")
                break
                
            items = extraer_visual(html)
            
            if items:
                print(f" {len(items)} productos encontrados.")
                datos_totales.extend(items)
            else:
                print(" Página vacía. Es posible que se acabaron los productos en Oaxaca.")
                print(" Terminando escaneo anticipadamente.")
                break
        else:
            print(" Error de red en esta página.")
        
        # Pausa ética (clave para llegar a 550 sin bloqueo)
        time.sleep(random.uniform(3, 5))

    # --- GUARDADO Y RESULTADOS ---
    if datos_totales:
        df = pd.DataFrame(datos_totales)
        
        # Eliminar duplicados (importante en scrapeos largos)
        df.drop_duplicates(subset=['link'], inplace=True)
        
        # Convertir vendidos a numérico para el análisis
        df['vendidos_estimados'] = pd.to_numeric(df['vendidos_estimados'])
        
        nombre_archivo = f"dataset_{ESTADO}_final_vendidos.csv"
        df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
        
        print(f"   Total Final: {len(df)} productos únicos.")
        print(f"   Archivo: {nombre_archivo}")
        print("\n   TOP 5 MÁS VENDIDOS ENCONTRADOS:")
        print(df.nlargest(5, 'vendidos_estimados')[['titulo', 'precio', 'vendidos_estimados']])
    else:
        print("\nAlgo salió mal. No se recolectaron datos.")

if __name__ == "__main__":
    main()