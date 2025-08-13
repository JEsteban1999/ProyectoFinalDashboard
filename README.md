
# Dashboard de Establecimientos y Turismo en Colombia

## 📌 Descripción del Proyecto

Este proyecto es un dashboard interactivo que visualiza datos sobre establecimientos turísticos y visitantes extranjeros en Colombia. La aplicación utiliza datos abiertos del gobierno colombiano para mostrar:

* Distribución geográfica de establecimientos por departamentos y municipios

* Tipos de establecimientos turísticos registrados

* Estadísticas de extranjeros no residentes por país de origen

* Integración con un dashboard de Power BI sobre turismo

## Tecnologías utilizadas

* Backend: Python con Flask

* Frontend: HTML5, CSS3, JavaScript

* Visualizaciones: Plotly.js

* Procesamiento de datos: Pandas

* APIs: Datos abiertos de Colombia

* Geocodificación: pycountry, pycountry-convert

## 🚀 Características Principales

* Visualizaciones interactivas con Plotly (mapas coropléticos, gráficos de barras y gráficos circulares)

* Integración con APIs de datos abiertos de Colombia

* Traducción y normalización de nombres de países

* Diseño responsive para diferentes dispositivos

* Integración con Power BI para visualizaciones adicionales

## Requisitos del sistema

* Python 3.7 o superior

* Pip para la instalación de dependencias


## ⚙️ Configuración e Instalación

1. Clonar el repositorio:

```bash
  git clone https://github.com/JEsteban1999/ProyectoFinalDashboard.git
  cd nombre-del-repositorio
```

## 🏗️ Estructura del Proyecto

```bash
/proyecto
├── app.py                # Aplicación principal Flask
├── static/               # Archivos estáticos (CSS, JS, imágenes)
│   └── style.css         # Estilos CSS
├── templates/            # Plantillas HTML
│   └── dashboard.html    # Plantilla principal del dashboard
├── data_extranjeros.csv  # Datos de extranjeros guardados
├── requirements.txt      # Dependencias de Python
└── README.md             # Este archivo
```

## Uso

1. Al acceder a la aplicación, se cargarán automáticamente los datos más recientes de las APIs.

2. Navega por las diferentes secciones usando el menú superior.

3. Interactúa con los gráficos:

* Zoom en los mapas

* Pasa el cursor sobre los elementos para ver detalles

* Haz clic en las leyendas para filtrar datos

## Fuentes de datos

* Datos Abiertos Colombia - Establecimientos

* Datos Abiertos Colombia - Extranjeros

* GeoJSON Departamentos de Colombia

* GeoJSON Municipios de Colombia
