
# Proyecto OCR en Python

Este proyecto utiliza Tesseract para realizar el reconocimiento óptico de caracteres (OCR) en imágenes de facturas. A continuación se detallan las instrucciones para instalar y ejecutar el proyecto en diferentes sistemas operativos.

## Prerequisitos

Asegúrate de tener instalados los siguientes programas:

- Python 3.x
- Pip (incluido en Python 3.x)
- Tesseract OCR

## Instalación

### 1. Clonar el repositorio

Primero, clona el repositorio a tu máquina local:

```bash
git clone https://github.com/Arixtiz/python-OCR.git
cd python-OCR
```

### 2. Instalar Tesseract

#### Para macOS

Puedes instalar Tesseract usando Homebrew. Si no tienes Homebrew, puedes instalarlo desde [aquí](https://brew.sh/).

```bash
brew install tesseract
```

#### Para Ubuntu

Ejecuta el siguiente comando en la terminal:

```bash
sudo apt-get install tesseract-ocr
```

#### Para Windows

1. Descarga el instalador de Tesseract desde [aquí](https://github.com/UB-Mannheim/tesseract/wiki).
2. Sigue las instrucciones del instalador y asegúrate de añadir la ruta de instalación de Tesseract a las variables de entorno del sistema.

### 3. Crear un entorno virtual

Es una buena práctica crear un entorno virtual para gestionar las dependencias de tu proyecto. Sigue estos pasos:

```bash
# Entra en la carpeta del proyecto
cd python-OCR

# Crear un entorno virtual (puedes cambiar 'venv' por el nombre que prefieras)
python -m venv venv

# Activar el entorno virtual
# En macOS y Linux
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 4. Instalar dependencias

Con el entorno virtual activado, instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

## Uso

Una vez que hayas configurado el entorno y las dependencias, puedes ejecutar el script:

```bash
python script.py
```

Asegúrate de tener las imágenes de las facturas en las carpetas correspondientes dentro de la carpeta `images`.

## Estructura de Carpetas

Asegúrate de que tu estructura de carpetas sea similar a la siguiente:

```
/python-OCR
|-- images
|   |-- ABRIL
|   |-- MARZO
|   |-- MAYO
|-- venv
|-- .gitignore
|-- LICENSE
|-- README.md
|-- script.py
```

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un *issue* o un *pull request*.

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.
```
