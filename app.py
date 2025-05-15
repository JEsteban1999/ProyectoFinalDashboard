import requests
import pandas as pd
import plotly.express as px
from flask import Flask, render_template
import datetime
import os

app = Flask(__name__)


def obtener_datos():
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
            "$select": ",".join(columnas_necesarias)  # Solo solicita estas columnas
        }
        
        response = requests.get(API_URL, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            break

        df = pd.DataFrame(data)
        dataframes.append(df)
        offset += LIMIT
        print(f"Registros obtenidos: {offset}")
    
    return pd.concat(dataframes, ignore_index=True)


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
        # Obtener datos
        data = obtener_datos()
        print(data.head(10))
        # Crear visualizaciones
        graphJSON_departamento = crear_mapa_departamentos(data)
        graphJSON_municipios = crear_mapa_municipios(
            data)  # Esta es la nueva función
        graphJSON_top_municipios = crear_grafico_top_municipios(data)
        graphJSON_tipos = crear_grafico_tipos(data)

        # Verificar que los JSON son válidos
        import json
        json.loads(graphJSON_departamento)
        json.loads(graphJSON_municipios)
        json.loads(graphJSON_top_municipios)
        json.loads(graphJSON_tipos)
        # Renderizar template con los datos
        return render_template(
            'dashboard.html',
            total_registros=len(data),
            graphJSON_departamento=graphJSON_departamento,
            graphJSON_municipios=graphJSON_municipios,
            graphJSON_top_municipios=graphJSON_top_municipios,
            graphJSON_tipos=graphJSON_tipos,
            now=datetime.datetime.now().strftime("%Y-%m-%d")
        )
    except Exception as e:
        return f"Error al generar el dashboard: {str(e)}", 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
