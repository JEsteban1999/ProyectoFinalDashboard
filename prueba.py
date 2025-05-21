import pycountry
from pycountry_convert import country_name_to_country_alpha2

# Diccionario de traducción personalizado
traducciones = {
    'es': {
        'COL': 'Colombia',
        'USA': 'Estados Unidos',
        'ESP': 'España',
        'MEX': 'México',
        'FRA': 'Francia',
        # Añadir todas las traducciones necesarias
    }
}

def obtener_codigo_desde_espanol(nombre_espanol):
    try:
        # Buscar en nuestras traducciones inversas
        codigo = next(
            code for code, name in traducciones['es'].items() 
            if name.lower() == nombre_espanol.lower()
        )
        return codigo
    except StopIteration:
        # Si no está en nuestro diccionario, intentar con pycountry
        try:
            pais = pycountry.countries.search_fuzzy(nombre_espanol)
            return pais[0].alpha_3
        except:
            return None

pais = obtener_codigo_desde_espanol("France")
print(pais)