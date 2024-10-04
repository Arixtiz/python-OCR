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
        productos_lista.append({
            'ref': producto[0],
            'producto': producto[1],
            'cantidad': int(producto[2]),
            'especificacion': producto[3],
            'precio_venta': float(producto[4].replace(',', '.')),
            'total': float(producto[5].replace(',', '.'))
        })

    datos_factura['productos'] = productos_lista
    datos_factura['total'] = float(re.search(r'TOTAL\s+([\d,.]+)', texto).group(1).replace(',', '.')) if re.search(r'TOTAL\s+([\d,.]+)', texto) else None

    return datos_factura

# Función para procesar varias facturas de una carpeta y guardar los datos en un JSON
def procesar_varias_facturas(carpeta_imagenes):
    todas_facturas = []
    
    # Iterar sobre todos los archivos en la carpeta especificada
    for nombre_archivo in os.listdir(carpeta_imagenes):
        if nombre_archivo.endswith(('.png', '.jpg', '.jpeg')): 
            ruta_imagen = os.path.join(carpeta_imagenes, nombre_archivo)
            datos_factura = procesar_factura(ruta_imagen)
            todas_facturas.append(datos_factura)

    # Guardar los datos procesados en un archivo JSON
    with open('facturas.json', 'w', encoding='utf-8') as f:
        json.dump(todas_facturas, f, ensure_ascii=False, indent=4)

# Ruta a la carpeta de imágenes
carpeta_imagenes = './imagenes_facturas'  

# Procesar todas las facturas en la carpeta
procesar_varias_facturas(carpeta_imagenes)