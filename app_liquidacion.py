import streamlit as st
import pandas as pd
import os
from datetime import datetime
import tempfile

# Configuración de la página
st.set_page_config(
    page_title="Generador de Archivo HAB",
    page_icon="💰",
    layout="wide"
)

# Título y descripción
st.title("Generador de Archivo HAB")
st.markdown("""
Esta aplicación permite convertir un archivo Excel con información de liquidaciones a un archivo de texto plano
con formato específico para su procesamiento.
""")

# Definir la estructura de campos según la tabla
campos = [
    {'nombre': 'TIPO DE CONVENIO', 'longitud': 3, 'tipo': 'N', 'default': '13'},
    {'nombre': 'SUCURSAL', 'longitud': 5, 'tipo': 'N', 'default': ''},
    {'nombre': 'MONEDA', 'longitud': 2, 'tipo': 'N', 'default': '1'},
    {'nombre': 'SISTEMA', 'longitud': 1, 'tipo': 'N', 'default': '3'},
    {'nombre': 'NRO CTA', 'longitud': 9, 'tipo': 'N', 'default': ''},
    {'nombre': 'IMPORTE', 'longitud': 18, 'tipo': 'N', 'default': ''},
    {'nombre': 'FECHA', 'longitud': 8, 'tipo': 'N', 'default': ''},
    {'nombre': 'NRO CONVENIO CON LA EMPRESA', 'longitud': 5, 'tipo': 'N', 'default': '1137'},
    {'nombre': 'NRO COMPROBANTE', 'longitud': 6, 'tipo': 'N', 'default': 1},  # Valor por defecto como entero
    {'nombre': 'CBU', 'longitud': 22, 'tipo': 'N', 'default': '0'},
    {'nombre': 'CUOTA', 'longitud': 2, 'tipo': 'N', 'default': '0'},
    {'nombre': 'USUARIO', 'longitud': 22, 'tipo': 'N', 'default': ''}
]

# Calcular la longitud total esperada
longitud_total = sum(campo['longitud'] for campo in campos)
st.info(f"Longitud total esperada del archivo: {longitud_total} caracteres por línea")

# Función para convertir valores a enteros sin decimales
def convertir_a_entero(valor):
    if pd.isna(valor):
        return ""
    
    # Si es un número, convertirlo a entero
    try:
        if isinstance(valor, (int, float)):
            # Redondear a 0 decimales
            return int(round(valor))
    except:
        pass
    
    # Si es un string, eliminar puntos y convertir a entero si es posible
    if isinstance(valor, str):
        valor_limpio = valor.replace('.', '')
        try:
            return int(valor_limpio)
        except:
            return valor_limpio
    
    return valor

# Función para procesar el archivo
def procesar_archivo(df, fecha, nro_comprobante_inicial):
    # Crear una copia del DataFrame original para preservar los valores originales
    df_original = df.copy()
    
    # Procesar el DataFrame para eliminar puntos y comas
    for columna in df.columns:
        # Eliminar puntos y comas que puedan existir en los valores
        df[columna] = df[columna].str.replace('.', '')
        df[columna] = df[columna].str.replace(',', '')
        df[columna] = df[columna].str.replace(r'\.0$', '', regex=True)
    
    # Crear un archivo temporal para guardar el resultado
    with tempfile.NamedTemporaryFile(delete=False, suffix='.hab', mode='w', encoding='ansi', newline='\r\n') as temp_file:
        archivo_salida = temp_file.name
        
        # Contador para líneas con longitud incorrecta
        lineas_incorrectas = 0
        
        # Inicializar el contador para el NRO COMPROBANTE
        nro_comprobante = nro_comprobante_inicial
        
        for idx, fila in df.iterrows():
            linea = ""
            
            # Procesar cada campo según su definición
            for campo in campos:
                nombre = campo['nombre']
                longitud = campo['longitud']
                default = campo['default']
                
                # Obtener el valor del DataFrame o usar el valor por defecto
                if nombre in df.columns:
                    valor = str(fila.get(nombre, default)).strip()
                else:
                    valor = default
                
                # Para el campo FECHA, usar la fecha proporcionada
                if nombre == 'FECHA':
                    valor = fecha
                
                # Para el campo NRO COMPROBANTE, usar el contador
                if nombre == 'NRO COMPROBANTE':
                    valor = str(nro_comprobante).zfill(longitud)
                    nro_comprobante += 1
                
                # Para el campo IMPORTE, manejar los decimales correctamente
                if nombre == 'IMPORTE' and nombre in df_original.columns:
                    valor_original = str(df_original.iloc[idx][nombre])
                    
                    # Verificar si el valor tiene decimal (punto o coma)
                    tiene_decimal = ',' in valor_original or '.' in valor_original
                    
                    if not tiene_decimal:
                        # Si no tiene decimal, añadir "00" para representar centavos
                        valor = valor + "00"
                    else:
                        # Si ya tiene decimal, asegurarse de que tenga 2 dígitos después del decimal
                        # El valor en 'valor' ya tiene los puntos y comas eliminados
                        pass
                
                # Rellenar con ceros a la izquierda
                valor_formateado = valor.zfill(longitud)
                
                # Asegurar que la longitud sea exactamente la especificada
                valor_formateado = valor_formateado[:longitud]
                
                # Agregar a la línea
                linea += valor_formateado
            
            # Verificar la longitud total
            if len(linea) != longitud_total:
                lineas_incorrectas += 1
            
            # Escribir la línea al archivo
            temp_file.write(linea + '\n')
    
    return archivo_salida, lineas_incorrectas

# Interfaz para cargar el archivo
st.header("Cargar archivo Excel")
st.markdown("""
El archivo debe contener las siguientes columnas:
- USUARIO
- NRO CTA
- SUCURSAL
- IMPORTE
""")

uploaded_file = st.file_uploader("Seleccione el archivo Excel", type=["xlsx", "xls"])

# Seleccionar fecha
fecha = st.date_input(
    "Seleccione la fecha para el archivo HAB",
    datetime.today()
)
# Convertir la fecha al formato YYYYMMDD
fecha_formateada = fecha.strftime("%Y%m%d")

# Número inicial de comprobante
st.text("Número de comprobante: 1")
nro_comprobante_inicial = 1  # Valor fijo que no puede ser modificado por el usuario

# Mostrar vista previa si se cargó un archivo
if uploaded_file is not None:
    try:
        # Leer el Excel tratando todas las columnas como strings y usando openpyxl como motor
        df = pd.read_excel(uploaded_file, dtype=str, engine='openpyxl')
        
        # Verificar las columnas requeridas
        columnas_requeridas = ['USUARIO', 'NRO CTA', 'SUCURSAL', 'IMPORTE']
        columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
        
        if columnas_faltantes:
            st.error(f"El archivo no contiene las siguientes columnas requeridas: {', '.join(columnas_faltantes)}")
        else:
            st.success("Archivo cargado correctamente")
            
            # Mostrar vista previa
            st.subheader("Vista previa del archivo")
            st.dataframe(df.head())
            
            # Información del archivo
            st.info(f"El archivo contiene {len(df)} registros.")
            
            # Botón para procesar
            if st.button("Generar archivo HAB"):
                with st.spinner("Procesando archivo..."):
                    archivo_salida, lineas_incorrectas = procesar_archivo(df, fecha_formateada, nro_comprobante_inicial)
                    
                    # Leer el archivo generado para mostrar vista previa
                    with open(archivo_salida, 'r', encoding='ansi') as f:
                        contenido = f.readlines()[:5]  # Mostrar solo las primeras 5 líneas
                    
                    st.success(f"Procesamiento completado. Se procesaron {len(df)} registros.")
                    
                    if lineas_incorrectas > 0:
                        st.warning(f"Se encontraron {lineas_incorrectas} líneas con longitud incorrecta.")
                    
                    # Mostrar vista previa del archivo generado
                    st.subheader("Vista previa del archivo generado")
                    for i, linea in enumerate(contenido):
                        st.code(linea.strip(), language=None)
                    
                    # Botón para descargar el archivo
                    with open(archivo_salida, 'rb') as f:
                        archivo_bytes = f.read()
                        
                    st.download_button(
                        label="Descargar archivo HAB",
                        data=archivo_bytes,
                        file_name=f"liquidacion_{fecha_formateada}.hab",
                        mime="text/plain"
                    )
                    
                    # Eliminar el archivo temporal después de la descarga
                    os.unlink(archivo_salida)
    
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")

# Información adicional
st.sidebar.header("Información")
st.sidebar.markdown("""
### Valores por defecto
- TIPO DE CONVENIO: 13
- MONEDA: 1
- SISTEMA: 3
- NRO CONVENIO CON LA EMPRESA: 1137
- NRO COMPROBANTE: Autonumérico
- CBU: 0
- CUOTA: 0
""")

st.sidebar.markdown("""
### Instrucciones
1. Cargue un archivo Excel con las columnas requeridas
2. Seleccione la fecha para el archivo HAB
3. Haga clic en "Generar archivo HAB"
4. Descargue el archivo generado
""")
