# OCR Processor for Invoices

This project uses Tesseract OCR to extract text from images of invoices and organizes the data in a JSON format. The script processes multiple invoice images and outputs structured data that includes client information, product details, and totals.

## Requirements

- macOS (or any Unix-based system)
- Python 3.x
- Homebrew (for installing Tesseract)
- Python libraries: `pytesseract`, `Pillow`

## Installation Guide

### Step 1: Install Homebrew (if not installed)

Homebrew is a package manager for macOS. To install it, open the Terminal and run the following command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the instructions on the screen to complete the installation.

### Step 2: Install Tesseract

Once Homebrew is installed, you can install Tesseract by running the following command in your Terminal:

```bash
brew install tesseract
```

To verify the installation, you can run:

```bash
tesseract --version
```

### Step 3: Install Language Data (Optional)

By default, Tesseract supports multiple languages. If you're working with Spanish invoices, you can install the Spanish language model with the following command:

```bash
brew install tesseract-lang/spa.traineddata
```

### Step 4: Install Python Libraries

In your Python environment, install the required libraries:

```bash
pip install pytesseract Pillow
```

These libraries allow us to interact with Tesseract and manipulate images in Python.

## Usage

### Python OCR Script

The provided Python script extracts information from invoice images and converts it to structured JSON format. Here’s how the script works:

1. **Tesseract OCR** is used to extract text from images.
2. **Regular expressions (regex)** are used to identify and extract specific data fields such as client name, ID, city, product details, and totals.
3. The processed data from multiple invoices is saved in a JSON file.

### Running the Script

1. Place your invoice images in a folder.
2. Modify the list of images in the script to include the path to your images.
3. Run the script with:

```bash
python ocr_invoice_processor.py
```

### Example Code

Here’s a simplified version of the script:

```python
import pytesseract
from PIL import Image
import json
import re

# Function to process an invoice image and extract data
def procesar_factura(imagen_path):
    imagen = Image.open(imagen_path)
    texto = pytesseract.image_to_string(imagen, lang='spa')

    datos_factura = {}
    datos_factura['cliente'] = re.search(r'Cliente: (.+)', texto).group(1)
    datos_factura['cedula'] = re.search(r'Cédula o Nit: (\d+)', texto).group(1)
    datos_factura['celular'] = re.search(r'Celular: (\d+)', texto).group(1)
    datos_factura['ciudad'] = re.search(r'Ciudad: (.+)', texto).group(1)
    datos_factura['fecha'] = re.search(r'Fecha: (\d{2} de .+ \d{4})', texto).group(1)
    datos_factura['tipo_cliente'] = re.search(r'Tipo de Cliente: (.+)', texto).group(1)

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
    datos_factura['total'] = float(re.search(r'TOTAL\s+([\d,.]+)', texto).group(1).replace(',', '.'))

    return datos_factura

# Function to process multiple invoices and save them as JSON
def procesar_varias_facturas(imagenes):
    todas_facturas = []
    for imagen in imagenes:
        datos_factura = procesar_factura(imagen)
        todas_facturas.append(datos_factura)

    # Save the data to a JSON file
    with open('facturas.json', 'w') as f:
        json.dump(todas_facturas, f, ensure_ascii=False, indent=4)

# List of invoice images
imagenes_facturas = ['invoice1.png', 'invoice2.png']  # Add your image paths here

# Process the invoices
procesar_varias_facturas(imagenes_facturas)
```

### Output

The script will generate a `facturas.json` file that contains the structured data for each invoice. Example output:

```json
[
    {
        "cliente": "Mariana Vásquez Echavarría",
        "cedula": "1020488334",
        "celular": "3005089165",
        "ciudad": "Bello, Antioquia",
        "fecha": "22 de Mayo de 2024",
        "tipo_cliente": "Mayorista",
        "productos": [
            {
                "ref": "A074",
                "producto": "ANILLO ARIADNA",
                "cantidad": 1,
                "especificacion": "",
                "precio_venta": 9000.0,
                "total": 9000.0
            },
            ...
        ],
        "total": 180900.0
    }
]
```

## Contribution

Feel free to fork this repository and submit pull requests to improve the code or add new features.

## License

This project is licensed under the MIT License.
```