import pytesseract
from PIL import Image
import json
import re
import os

# Función para procesar una imagen de factura y extraer los datos
def procesar_factura(imagen_path):
    imagen = Image.open(imagen_path)
    texto = pytesseract.image_to_string(imagen, lang='spa')

    datos_factura = {}
    # Extracción de datos usando expresiones regulares (regex)
    datos_factura['cliente'] = re.search(r'Cliente: (.+)', texto).group(1) if re.search(r'Cliente: (.+)', texto) else None
    datos_factura['cedula'] = re.search(r'Cédula o Nit: (\d+)', texto).group(1) if re.search(r'Cédula o Nit: (\d+)', texto) else None
    datos_factura['celular'] = re.search(r'Celular: (\d+)', texto).group(1) if re.search(r'Celular: (\d+)', texto) else None
    datos_factura['ciudad'] = re.search(r'Ciudad: (.+)', texto).group(1) if re.search(r'Ciudad: (.+)', texto) else None
    datos_factura['fecha'] = re.search(r'Fecha: (\d{2} de .+ \d{4})', texto).group(1) if re.search(r'Fecha: (\d{2} de .+ \d{4})', texto) else None
    datos_factura['tipo_cliente'] = re.search(r'Tipo de Cliente: (.+)', texto).group(1) if re.search(r'Tipo de Cliente: (.+)', texto) else None

    # Extracción de los productos
    productos = re.findall(r'([A-Z]+\d+)\s+(.+?)\s+(\d+)\s+(.+?)\s+([\d,.]+)\s+([\d,.]+)', texto)
    productos_lista = []
    for producto in productos:
        precio_venta = producto[4]  # Mantener formato original
        total = producto[5]  # Mantener formato original

        productos_lista.append({
            'ref': producto[0],
            'producto': producto[1],
            'cantidad': int(producto[2]),
            'especificacion': producto[3],
            'precio_venta': precio_venta,
            'total': total
        })

    datos_factura['productos'] = productos_lista

    # Extraer el total general manteniendo el formato de miles y decimales
    total_general = re.search(r'TOTAL\s+([\d,.]+)', texto)
    datos_factura['total'] = total_general.group(1) if total_general else None

    return datos_factura

# Función para procesar todas las imágenes dentro de una carpeta (mes específico)
def procesar_facturas_mes(carpeta_mes, mes):
    todas_facturas = []
    
    # Iterar sobre todos los archivos en la carpeta del mes
    for nombre_archivo in os.listdir(carpeta_mes):
        if nombre_archivo.endswith(('.png', '.jpg', '.jpeg')):  # Filtrar solo las imágenes
            ruta_imagen = os.path.join(carpeta_mes, nombre_archivo)
            datos_factura = procesar_factura(ruta_imagen)
            todas_facturas.append(datos_factura)

    # Guardar los datos en un archivo JSON nombrado por el mes
    nombre_json = f'facturas_{mes}.json'
    with open(nombre_json, 'w', encoding='utf-8') as f:
        json.dump(todas_facturas, f, ensure_ascii=False, indent=4)

    print(f"Se ha generado el archivo {nombre_json} con {len(todas_facturas)} facturas.")

# Función para recorrer todas las carpetas de los meses y procesar las facturas
def procesar_facturas_por_meses(carpeta_principal):
    # Iterar sobre las carpetas dentro de 'images' (cada mes)
    for nombre_carpeta in os.listdir(carpeta_principal):
        ruta_carpeta_mes = os.path.join(carpeta_principal, nombre_carpeta)
        if os.path.isdir(ruta_carpeta_mes):  # Solo procesar carpetas
            print(f"Procesando facturas del mes: {nombre_carpeta}")
            procesar_facturas_mes(ruta_carpeta_mes, nombre_carpeta)

# Ruta a la carpeta principal que contiene los meses
carpeta_principal = './images'  # Aquí se encuentran las carpetas ABRIL, MAYO, etc. CREAR LA CARPETA Y SUBIR LAS IMAGENES EN SUS SUBCARPETAS AHÍ

# Procesar todas las carpetas de meses
procesar_facturas_por_meses(carpeta_principal)