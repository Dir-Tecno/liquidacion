# Aplicación de Generación de Archivos HAB

Esta aplicación Streamlit permite convertir archivos Excel con información de liquidaciones a un formato de texto plano específico (archivo HAB) para su procesamiento posterior.

## Requisitos

- Python 3.6 o superior
- Bibliotecas requeridas:
  - streamlit
  - pandas
  - openpyxl

Para instalar las dependencias:

```bash
pip install streamlit pandas openpyxl
```

## Cómo usar la aplicación

1. Ejecute la aplicación con el siguiente comando:

```bash
streamlit run app_liquidacion.py
```

2. La aplicación se abrirá en su navegador web predeterminado.

3. Siga estos pasos para generar un archivo HAB:

   a. **Cargar archivo Excel**: Haga clic en "Browse files" y seleccione un archivo Excel (.xlsx o .xls) que contenga las siguientes columnas:
      - USUARIO
      - NRO CTA
      - SUCURSAL
      - IMPORTE

   b. **Seleccionar fecha**: Elija la fecha que desea incluir en el archivo HAB utilizando el selector de fecha.
   
   c. **Generar archivo**: Haga clic en el botón "Generar archivo HAB" para procesar el archivo.

   d. **Descargar resultado**: Una vez procesado, haga clic en "Descargar archivo HAB" para guardar el archivo generado.

## Estructura del archivo de entrada

El archivo Excel de entrada debe contener al menos las siguientes columnas:
- **USUARIO**: Identificador del usuario
- **NRO CTA**: Número de cuenta
- **SUCURSAL**: Código de sucursal
- **IMPORTE**: Monto a liquidar

## Valores por defecto

La aplicación utiliza los siguientes valores por defecto para los campos no incluidos en el archivo de entrada:

- TIPO DE CONVENIO: 13
- MONEDA: 1
- SISTEMA: 3
- NRO CONVENIO CON LA EMPRESA: 1137
- NRO COMPROBANTE: Autonumérico (se incrementa para cada registro, comenzando desde el valor inicial especificado)
- CBU: 0
- CUOTA: 0

## Formato del archivo de salida

El archivo de salida es un archivo de texto plano con extensión .hab, codificado en ANSI y con saltos de línea CRLF. Cada línea contiene los campos especificados con longitudes fijas según la estructura definida.

## Notas importantes

- Para el campo **IMPORTE**, si el valor no contiene una coma decimal, se añadirán "00" a la derecha para representar los centavos.
- Todos los campos numéricos se rellenan con ceros a la izquierda hasta alcanzar la longitud especificada.
- La aplicación verifica que cada línea tenga la longitud total esperada y muestra una advertencia si hay discrepancias.

## Solución de problemas

Si encuentra algún problema al cargar o procesar el archivo:

1. Verifique que el archivo Excel contenga todas las columnas requeridas.
2. Asegúrese de que los valores en las columnas tengan el formato correcto.
3. Si hay errores en la generación del archivo, revise las advertencias mostradas en la aplicación.

## Estructura de campos

| Campo | Longitud | Tipo | Valor por defecto |
|-------|----------|------|------------------|
| TIPO DE CONVENIO | 3 | N | 13 |
| SUCURSAL | 5 | N | - |
| MONEDA | 2 | N | 1 |
| SISTEMA | 1 | N | 3 |
| NRO CTA | 9 | N | - |
| IMPORTE | 18 | N | - |
| FECHA | 8 | N | Seleccionada en la interfaz |
| NRO CONVENIO CON LA EMPRESA | 5 | N | 1137 |
| NRO COMPROBANTE | 6 | N | Autonumérico |
| CBU | 22 | N | 0 |
| CUOTA | 2 | N | 0 |
| USUARIO | 22 | N | - |
