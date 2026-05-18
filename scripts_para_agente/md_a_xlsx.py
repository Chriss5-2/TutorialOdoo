import pandas as pd
import io
import re

# CONFIGURACIÓN: Cambia esto por la ruta de tu archivo
archivo_md = 'bm_ctl_produccion_descripciones.md' 
archivo_xlsx = 'bm_ctl_produccion_descripciones.xlsx'

def convertir_md_a_excel(ruta_origen, ruta_destino):
    try:
        with open(ruta_origen, 'r', encoding='utf-8') as f:
            contenido = f.read()

        # Extraer bloques que parecen tablas de Markdown
        tablas_raw = re.findall(r'((?:\|.+?\|(?:\n|$))+)', contenido)

        if not tablas_raw:
            print(f"No se encontraron tablas en {ruta_origen}")
            return

        with pd.ExcelWriter(ruta_destino, engine='openpyxl') as writer:
            for i, tabla_str in enumerate(tablas_raw):
                # Limpiar líneas de separación (---)
                lineas = [l for l in tabla_str.strip().split('\n') if not re.match(r'^\|?[\s\-:|]+$', l)]
                
                # Leer como CSV usando el pipe | como separador
                df = pd.read_csv(io.StringIO('\n'.join(lineas)), sep='|', skipinitialspace=True)
                
                # Eliminar columnas vacías que se crean por los pipes de los extremos
                df = df.dropna(axis=1, how='all')
                
                # Limpiar espacios en nombres de columnas y datos
                df.columns = [c.strip() for c in df.columns]
                df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
                
                nombre_hoja = f"Tabla_{i+1}"
                df.to_excel(writer, sheet_name=nombre_hoja, index=False)
                
        print(f"Conversión exitosa: {ruta_destino}")

    except Exception as e:
        print(f"❌ Error: {e}")

# Ejecutar
convertir_md_a_excel(archivo_md, archivo_xlsx)