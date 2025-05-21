import requests
import pandas as pd
import plotly.express as px
from flask import Flask, render_template
import datetime
import os
import pycountry
from pycountry_convert import country_name_to_country_alpha2
import json

app = Flask(__name__)

traducciones = {
    'es': {
        'SPM': 'San Pedro y Miquelón',
        'BLM': 'San Bartolomé',
        'NCL': 'Nueva Caledonia',
        'PYF': 'Polinesia Francesa',
        'WLF': 'Wallis y Futuna',
        'ATF': 'Tierras Australes y Antárticas Francesas',
        'NER': 'Níger',
        'AZE': 'Azerbaiyán',
        'GRD': 'Granada',
        'PER': 'Perú',
        'RWA': 'Ruanda',
        'BDI': 'Burundi',
        'LBY': 'Libia',
        'NGA': 'Nigeria',
        'DNK': 'Dinamarca',
        'USA': 'Estados Unidos',
        'SWE': 'Suecia',
        'MAF': 'San Martin',
        'SXN': 'San Martín',
        'ESP': 'España',
        'FRA': 'Francia',
        'GRC': 'Grecia',
        'DEU': 'Alemania',
        'BRA': 'Brasil',
        'HRV': 'Croacia',
        'CMR': 'Camerún',
        'CUW': 'Curazao',
        'BEL': 'Bélgica',
        'ROU': 'Rumania',
        'RUS': 'Rusia',
        'BES': 'Bonaire, San Eustaquio y Saba',
        'NLD': 'Países Bajos',
        'PSE': 'Palestina',
        'GBR': 'Reino Unido',
        'DOM': 'República Dominicana',
        # Nuevas traducciones añadidas
        'AFG': 'Afganistán',
        'AIA': 'Anguila',
        'ATG': 'Antigua y Barbuda',
        'ANT': 'Antillas Neerlandesas',  # Código obsoleto (ahora son BES, CUW, SXM)
        'SAU': 'Arabia Saudita',
        'DZA': 'Argelia',
        'AZE': 'Azerbaiyán',
        'BHR': 'Bahréin',
        'BLZ': 'Belice',
        'BMU': 'Bermudas',
        'BLR': 'Bielorrusia',
        'BES': 'Bonaire-San Esustaquio y Saba',  # Mismo que Bonaire, San Eustaquio y Saba
        'BWA': 'Botsuana',
        'KHM': 'Camboya',
        'CYP': 'Chipre',
        'VAT': 'Ciudad del Vaticano',
        'COM': 'Comoras',
        'KOR': 'Corea del Sur',
        'PRK': 'Corea del Norte',
        'CIV': 'Costa de Marfil',
        'EGY': 'Egipto',
        'ARE': 'Emiratos Árabes Unidos',
        'SVK': 'Eslovaquia',
        'SVN': 'Eslovenia',
        'ETH': 'Etiopía',
        'PHL': 'Filipinas',
        'FIN': 'Finlandia',
        'FJI': 'Fiyi',
        'GUF': 'Guayana Francesa',
        'HUN': 'Hungría',
        'IRL': 'Irlanda',
        'ALA': 'Isla Aland',
        'ISL': 'Islandia',
        'CYM': 'Islas Caimán',
        'TCA': 'Islas Turcas y Caicos',
        'UMI': 'Islas Ultramarinas Menores de Estados Unidos',
        'VGB': 'Islas Vírgenes Británicas',
        'VIR': 'Islas Vírgenes Estadounidenses',
        'JPN': 'Japón',
        'JOR': 'Jordania',
        'KAZ': 'Kazajistán',
        'KEN': 'Kenia',
        'KGZ': 'Kirguistán',
        'LSO': 'Lesoto',
        'LVA': 'Letonia',
        'LBN': 'Líbano',
        'LTU': 'Lituania',
        'LUX': 'Luxemburgo',
        'MYS': 'Malasia',
        'MAR': 'Marruecos',
        'MTQ': 'Martinica',
        'MUS': 'Mauricio',
        'MDA': 'Moldavia',
        'NOR': 'Noruega',
        'NCL': 'Nueva Caledonia',
        'NZL': 'Nueva Zelanda',
        'PNG': 'Papua Nueva Guinea',
        'PYF': 'Polinesia Francesa',
        'POL': 'Polonia',
        'CAF': 'República Centroafricana',
        'CZE': 'República Checa',
        'XKX': 'República de Kosovo',  # Código no oficial (Kosovo no es miembro de la ONU)
        'MKD': 'República de Macedonia',
        'COD': 'República Democratica del Congo',
        'RWA': 'Ruanda',
        'ESH': 'Sáhara Occidental',
        'KNA': 'San Cristóbal y Nieves',
        'VCT': 'San Vicente y las Granadinas',
        'LCA': 'Santa Lucia',
        'SLE': 'Sierra Leona',
        'SGP': 'Singapur',
        'SYR': 'Siria',
        'SWZ': 'Suazilandia',
        'ZAF': 'Sudáfrica',
        'SSD': 'Sudan del Sur',
        'CHE': 'Suiza',
        'THA': 'Tailandia',
        'TTO': 'Trinidad y Tobago',
        'TUN': 'Túnez',
        'TUR': 'Turquía',
        'UKR': 'Ucrania',
        'ZWE': 'Zimbabue',
        'GLP': 'Guadalupe',
        'GNQ': 'Guinea Ecuatorial',
        'IMN': 'Isla de Man',
        'NFK': 'Isla Norfolk',
        'BLM': 'San Bartolomé',
        'IOT': 'Terr. Britanico del Oceano Indico',
        'BTN': 'Bután',
        'GNB': 'Guinea-Bisáu',
        'ASM': 'Samoa Americana',
        'STP': 'Santo Tomé y Principe',
        'ATA': 'Terr. Británico en Antártida',
        'XX1': 'Organismos internacionales',  # No es un código ISO real
    }
}


def obtener_codigo_pais(nombre_pais):
    # Primero aplicar correcciones específicas
    nombre_limpio = nombre_pais.strip().lower()

    try:
        # Buscar en nuestras traducciones inversas
        codigo = next(
            code for code, name in traducciones['es'].items()
            if name.lower() == nombre_limpio
        )
        return codigo
    except StopIteration:
        # Si no está en nuestro diccionario, intentar con pycountry
        try:
            pais = pycountry.countries.search_fuzzy(nombre_limpio)
            return pais[0].alpha_3
        except:
            # Como último recurso, intentar con pycountry-convert
            try:
                alpha2 = country_name_to_country_alpha2(nombre_limpio)
                return pycountry.countries.get(alpha_2=alpha2).alpha_3
            except:
                print(f"No se pudo encontrar código para: {nombre_pais}")
                return None


def obtener_datos_establecimientos():
    API_URL = "https://www.datos.gov.co/resource/thwd-ivmp.json"
    APP_TOKEN = "6drZ6YrTri9FeH1zhG3QdyHHk"
    LIMIT = 10000
    offset = 0
    dataframes = []

    # Columnas que SI necesitas
    columnas_necesarias = [
        'mes', 'cod_mun', 'cod_dpto', 'razon_social_establecimiento', 'departamento', 'municipio', 'categoria', 'sub_categoria',
        'habitaciones', 'camas', 'num_emp1'
    ]

    headers = {"X-App-Token": APP_TOKEN}

    while True:
        params = {
            "$limit": LIMIT,
            "$offset": offset,
            "$order": "departamento",
            # Solo solicita estas columnas
            "$select": ",".join(columnas_necesarias)
        }

        response = requests.get(API_URL, headers=headers,
                                params=params, timeout=60)
        response.raise_for_status()

        data = response.json()
        if not data:
            break

        df = pd.DataFrame(data)
        dataframes.append(df)
        offset += LIMIT
        print(f"Registros obtenidos: {offset}")

    return pd.concat(dataframes, ignore_index=True)


def obtener_datos_extranjeros():
    API_URL = "https://www.datos.gov.co/resource/7wm8-w5ad.json"
    APP_TOKEN = "TcCv2IlEtCLd3emS8QABwNVTb"  # Usando el mismo token
    LIMIT = 10000
    offset = 0
    dataframes = []

    columnas_necesarias = [
        'a_o', 'mes', 'departamento', 'ciudad', 'paisoeeresidencia', 'cant_extranjeros_no_residentes'
    ]

    headers = {"X-App-Token": APP_TOKEN}

    while True:
        params = {
            "$limit": LIMIT,
            "$offset": offset,
            "$where": "a_o == 2025",
            "$select": ",".join(columnas_necesarias)
        }

        try:
            response = requests.get(
                API_URL, headers=headers, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            if not data:
                break

            df = pd.DataFrame(data)
            dataframes.append(df)
            offset += LIMIT
            print(f"Registros de extranjeros obtenidos: {offset}")

        except Exception as e:
            print(f"Error al obtener datos: {str(e)}")
            break

    if dataframes:
        df_extranjeros = pd.concat(dataframes, ignore_index=True)

        # Convertir cantidad a numérico
        df_extranjeros['cant_extranjeros_no_residentes'] = pd.to_numeric(
            df_extranjeros['cant_extranjeros_no_residentes'], errors='coerce').fillna(0)

        # Obtener códigos ISO para los países
        df_extranjeros['codigo_pais'] = df_extranjeros['paisoeeresidencia'].apply(
            obtener_codigo_pais)
        
        # Verificar países sin código para diagnóstico
        paises_sin_codigo = df_extranjeros[df_extranjeros['codigo_pais'].isna()]['paisoeeresidencia'].unique()
        if len(paises_sin_codigo) > 0:
            print("Países sin código encontrados:", paises_sin_codigo)
        
        return df_extranjeros
    else:
        return pd.DataFrame(columns=columnas_necesarias + ['codigo_pais'])


def crear_mapa_extranjeros(data):
    # Descargar el GeoJSON una vez y guardarlo localmente
    local_geojson_path = "static/custom.geo.json"
    
    # Si no existe el archivo local, descargarlo
    if not os.path.exists(local_geojson_path):
        url_geojson_mundial = "https://raw.githubusercontent.com/JEsteban1999/GeoJson-Mapa-Municipios-Colombia/refs/heads/main/custom.geo.json"
        response = requests.get(url_geojson_mundial)
        with open(local_geojson_path, 'wb') as f:
            f.write(response.content)
    
    # Usar el archivo local
    with open(local_geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    # Agrupar por país de residencia
    por_pais = data.groupby(['paisoeeresidencia', 'codigo_pais'])[
        'cant_extranjeros_no_residentes'].sum().reset_index()
    por_pais = por_pais[por_pais['codigo_pais'].notna()]

    # Crear el mapa mundial
    fig = px.choropleth(
        por_pais,
        geojson=geojson_data,
        featureidkey="properties.iso_a3",
        locations='codigo_pais',
        color='cant_extranjeros_no_residentes',
        hover_name='paisoeeresidencia',
        hover_data=['cant_extranjeros_no_residentes'],
        color_continuous_scale="Viridis",
        projection="natural earth",
        title="Extranjeros no residentes por país de origen"
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=650,
        paper_bgcolor='rgba(34,34,34,1)',
        plot_bgcolor='rgba(34,34,34,1)',
        font=dict(color='white'),
        coloraxis_colorbar=dict(
            title="Cantidad de extranjeros",
            tickfont=dict(color='white'),
        )
    )

    return fig.to_json()


def crear_grafico_top_paises(data):
    # Agrupar por país y sumar
    por_pais = data.groupby(['paisoeeresidencia'])[
        'cant_extranjeros_no_residentes'].sum().reset_index()
    por_pais = por_pais.sort_values(
        'cant_extranjeros_no_residentes', ascending=False)

    # Tomar top 15
    top_paises = por_pais.head(15).sort_values(
        'cant_extranjeros_no_residentes', ascending=True)

    # Crear gráfico de barras
    fig = px.bar(
        top_paises,
        x='cant_extranjeros_no_residentes',
        y='paisoeeresidencia',
        orientation='h',
        color='cant_extranjeros_no_residentes',
        color_continuous_scale='Viridis',
        labels={
            'cant_extranjeros_no_residentes': 'Cantidad de extranjeros',
            'paisoeeresidencia': 'País de residencia'
        }
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1a2e44'),
        margin=dict(l=100, r=50, t=50, b=50),
        height=650,
        xaxis_title='Cantidad de Extranjeros',
        yaxis_title=''
    )

    return fig.to_json()


def crear_mapa_departamentos(data):
    # Procesamiento de datos
    cantidad_establecimientos_por_departamento = data.groupby(
        ['departamento', 'cod_dpto'])['razon_social_establecimiento'].count().reset_index()
    cantidad_establecimientos_por_departamento.columns = [
        'departamento', 'codigo_dpto', 'cantidad_establecimientos']
    cantidad_establecimientos_por_departamento.sort_values(
        by='cantidad_establecimientos', ascending=False, inplace=True)
    cantidad_establecimientos_por_departamento["codigo_dpto"] = cantidad_establecimientos_por_departamento["codigo_dpto"].astype(
        str).str.zfill(2)

    # Crear el mapa
    url_geojson_departamento = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json"
    fig = px.choropleth_map(
        cantidad_establecimientos_por_departamento,
        geojson=url_geojson_departamento,
        featureidkey="properties.DPTO",
        locations='codigo_dpto',
        color='cantidad_establecimientos',
        hover_name='departamento',
        hover_data='cantidad_establecimientos',
        color_continuous_scale="Viridis",
        map_style="carto-darkmatter",
        zoom=4.5,
        center={"lat": 4.5709, "lon": -74.2973},
        opacity=0.9,
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Ajustar el layout
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=650,
        paper_bgcolor='rgba(34,34,34,1)',
        plot_bgcolor='rgba(34,34,34,1)',
        font=dict(color='white'),
        coloraxis_colorbar=dict(
            title="Cantidad de establecimientos",
            tickfont=dict(color='white'),
        )
    )

    fig.update_traces(marker_line_color='rgba(255, 255, 255, 0.7)')

    return fig.to_json()


def crear_mapa_municipios(data):
    # Procesamiento de datos
    cantidad_establecimientos_por_municipio = data.groupby(
        ['municipio', 'cod_mun'])['razon_social_establecimiento'].count().reset_index()
    cantidad_establecimientos_por_municipio.columns = [
        'municipio', 'codigo_mun', 'cantidad_establecimientos']
    cantidad_establecimientos_por_municipio.sort_values(
        by='cantidad_establecimientos', ascending=False, inplace=True)
    cantidad_establecimientos_por_municipio["codigo_mun"] = cantidad_establecimientos_por_municipio["codigo_mun"].astype(
        str).str.zfill(5)

    # Cargar el GeoJSON (asegúrate de tener el archivo en tu proyecto)
    url_geojson_municipio = "https://raw.githubusercontent.com/JEsteban1999/GeoJson-Mapa-Municipios-Colombia/refs/heads/main/MGN_ANM_MPIOS%20(1).json"

    # Crear el mapa
    fig = px.choropleth_map(
        cantidad_establecimientos_por_municipio,
        geojson=url_geojson_municipio,
        featureidkey="properties.MPIO_CDPMP",
        locations='codigo_mun',
        color='cantidad_establecimientos',
        color_continuous_scale="Viridis",
        map_style="carto-darkmatter",
        hover_name='municipio',
        hover_data={'cantidad_establecimientos': True, 'municipio': False},
        zoom=4.5,
        center={"lat": 4.5709, "lon": -74.2973},
        opacity=0.8,
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Ajustar el layout
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=650,
        paper_bgcolor='rgba(34,34,34,1)',
        plot_bgcolor='rgba(34,34,34,1)',
        font=dict(color='white'),
        coloraxis_colorbar=dict(
            title="Cantidad de establecimientos",
            tickfont=dict(color='white'),
        )
    )

    fig.update_traces(marker_line_color='rgba(255, 255, 255, 0.7)')

    return fig.to_json()


def crear_grafico_top_municipios(data):
    # Procesamiento de datos
    cantidad_establecimientos_por_municipio = data.groupby(
        ['municipio', 'cod_mun'])['razon_social_establecimiento'].count().reset_index()
    cantidad_establecimientos_por_municipio.columns = [
        'municipio', 'codigo_mun', 'cantidad_establecimientos']
    cantidad_establecimientos_por_municipio.sort_values(
        by='cantidad_establecimientos', ascending=False, inplace=True)
    cantidad_establecimientos_por_municipio["codigo_mun"] = cantidad_establecimientos_por_municipio["codigo_mun"].astype(
        str).str.zfill(5)

    # Obtener solo los top 20 municipios para el gráfico de barras
    top_municipios = cantidad_establecimientos_por_municipio.head(
        20).sort_values('cantidad_establecimientos', ascending=True)
    # Crear gráfico de barras
    fig = px.bar(
        top_municipios,
        x='cantidad_establecimientos',
        y='municipio',
        orientation='h',
        color='cantidad_establecimientos',
        color_continuous_scale='Viridis',
        labels={'cantidad_establecimientos': 'Cantidad de Establecimientos',
                'municipio': 'Municipio'}
    )

    # Ajustar el layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1a2e44'),
        margin=dict(l=100, r=50, t=50, b=50),
        height=650,
        xaxis_title='Cantidad de Establecimientos',
        yaxis_title=''
    )

    return fig.to_json()


def crear_grafico_tipos(data):
    # Procesamiento de datos
    distribucion_tipos = data['sub_categoria'].value_counts().reset_index()
    distribucion_tipos.columns = ['tipo', 'cantidad']

    # Umbral para agrupar categorías pequeñas (ej. 1% del total)
    threshold = 0.01 * distribucion_tipos['cantidad'].sum()

    # Crear nueva columna con categorías agrupadas
    distribucion_tipos['tipo_agrupado'] = distribucion_tipos.apply(
        lambda x: x['tipo'] if x['cantidad'] >= threshold else 'Otros', axis=1
    )

    # Agrupar los datos
    distribucion_agrupada = distribucion_tipos.groupby(
        'tipo_agrupado')['cantidad'].sum().reset_index()

    # Crear gráfico de pastel
    fig = px.pie(
        distribucion_agrupada,
        values='cantidad',
        names='tipo_agrupado',
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Viridis,
    )

    # Mejorar el layout y las etiquetas
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='radial',
        pull=[0.1 if t == 'Otros' else 0 for t in distribucion_agrupada['tipo_agrupado']]
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1a2e44', size=12),
        margin=dict(l=50, r=50, t=50, b=50),
        height=650,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        )
    )

    return fig.to_json()


@app.route('/')
def dashboard():
    try:
        print("Obteniendo datos de establecimientos...")
        data_establecimientos = obtener_datos_establecimientos()
        print(
            f"Datos de establecimientos obtenidos: {len(data_establecimientos)} registros")

        print("Obteniendo datos de extranjeros...")
        data_extranjeros = obtener_datos_extranjeros()
        print(
            f"Datos de extranjeros obtenidos: {len(data_extranjeros)} registros")
        # Guardar dataframe de extranjeros en CSV
        data_extranjeros.to_csv('data_extranjeros.csv', index=False)

        print("Generando visualizaciones...")
        visualizaciones = {
            'graphJSON_departamento': crear_mapa_departamentos(data_establecimientos),
            'graphJSON_municipios': crear_mapa_municipios(data_establecimientos),
            'graphJSON_top_municipios': crear_grafico_top_municipios(data_establecimientos),
            'graphJSON_tipos': crear_grafico_tipos(data_establecimientos),
            'graphJSON_mapa_extranjeros': crear_mapa_extranjeros(data_extranjeros),
            'graphJSON_top_paises': crear_grafico_top_paises(data_extranjeros)
        }

        print("Visualizaciones generadas correctamente")

        return render_template(
            'dashboard.html',
            total_registros=len(data_establecimientos),
            total_extranjeros=data_extranjeros['cant_extranjeros_no_residentes'].sum(
            ),
            **visualizaciones,
            now=datetime.datetime.now().strftime("%Y-%m-%d")
        )

    except Exception as e:
        print(f"Error en dashboard: {str(e)}", exc_info=True)
        return render_template('error.html', error=str(e)), 500


if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 10000))
    app.run(debug=True)
