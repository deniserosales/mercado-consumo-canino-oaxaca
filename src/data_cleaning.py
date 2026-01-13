import pandas as pd
import os

def cargar_y_limpiar_datos(ruta_archivo):

    # Detección de formato
    if ruta_archivo.endswith('.csv'):
        df = pd.read_csv(ruta_archivo)
    else:
        df = pd.read_excel(ruta_archivo)
    
    # Validación de duplicados
    conteo_duplicados = df.duplicated().sum()
    print(f"Filas duplicadas detectadas: {conteo_duplicados}")
    
    if conteo_duplicados > 0: 
       df = df.drop_duplicates()
       
    # Limpieza de nulos
    total_filas_inicial = len(df) 
    df = df.dropna(subset=['precio', 'vendidos_estimados'])
    total_filas_final = len(df)
    
    filas_eliminadas = total_filas_inicial - total_filas_final
    
    print(f"Filas eliminadas por datos faltantes: {filas_eliminadas}")
    print(f"Total de registros final: {total_filas_final}")

    return df

def generar_matriz_rentabilidad(df):
    
    # Cálculo de Ingresos Brutos
    if 'ingresos_estimados' not in df.columns:
        df['ingresos_estimados'] = df['precio'] * df['vendidos_estimados']

    # Definición de Puntos de Corte para analizar mejor el Mercado
    mediana_precio = df['precio'].median()
    mediana_ventas = df['vendidos_estimados'].median()
    
    print(f"Media del precio: ${mediana_precio:,.2f}")
    print(f"Media de la cantidad vendida: {mediana_ventas:,.0f} unidades")

    # Clasificación de Precios
    def clasificar_producto(fila):
        es_precio_alto = fila['precio'] >= mediana_precio
        es_venta_alta = fila['vendidos_estimados'] >= mediana_ventas
        
        if es_precio_alto and es_venta_alta:
            return '(Alto Valor / Alto Volumen)'
        elif not es_precio_alto and es_venta_alta:
            return '(Bajo Valor / Alto Volumen)'
        elif es_precio_alto and not es_venta_alta:
            return '(Alto Valor / Bajo Volumen)'
        else:
            return '(Bajo Valor / Bajo Volumen)'

    df['segmento_estrategico'] = df.apply(clasificar_producto, axis=1)
    
    print("\n--- Distribución de Productos por Segmento ---")
    print(df['segmento_estrategico'].value_counts())
    
    print("\n--- Generación de Ingresos por Segmento ---")
    ingresos_por_segmento = df.groupby('segmento_estrategico')['ingresos_estimados'].sum().sort_values(ascending=False)
    print(ingresos_por_segmento.apply(lambda x: f"${x:,.2f}"))

    return df

def detectar_outliers_precio(df):
    #Separamos el mercado dominante de los valores atípicos mediante el método IQR
   
    print("\n--- Análisis de Distribución de Precios ---")
    print(df['precio'].describe())

    # Cálculo de cuartiles
    q1 = df['precio'].quantile(0.25)
    q3 = df['precio'].quantile(0.75)
    iqr = q3 - q1

    limite_superior = q3 + 1.5 * iqr

    # Segmentación
    df_mercado_masivo = df[df['precio'] <= limite_superior].copy()
    df_mercado_atipico = df[df['precio'] > limite_superior].copy()

    print(f"\n--- Segmentación por Rango de Precios ---")
    print(f"Mercado Dominante (<= ${limite_superior:,.2f}): {len(df_mercado_masivo)} productos | Precio Máx: ${df_mercado_masivo['precio'].max():,.2f}")
    print(f"Mercado Atípico (> ${limite_superior:,.2f}): {len(df_mercado_atipico)} productos | Precio Mín: ${df_mercado_atipico['precio'].min():,.2f}")

    return df_mercado_masivo, df_mercado_atipico

# Ejecución Principal
if __name__ == "__main__":
    ruta_archivo = 'data/raw/dataset_perros_mx_1000.csv' 
    
    if os.path.exists(ruta_archivo):
        print("Iniciando pipeline de procesamiento de datos...\n")
        
        # 1. Carga
        df_principal = cargar_y_limpiar_datos(ruta_archivo)
        
        # 2. Matriz Estratégica (BCG)
        df_principal = generar_matriz_rentabilidad(df_principal)
        
        # 3. Detección de Outliers
        df_masivo, df_premium = detectar_outliers_precio(df_principal)
        
        print("\nProcesamiento finalizado exitosamente.")
    else:
        print(f"Error: No se encontró el archivo en: {ruta_archivo}")