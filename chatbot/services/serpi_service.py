from serpapi import GoogleSearch
import os
SERPI_TOKEN = os.environ.get('SERPAPI')

# Update the params to use the environment variable
""""
params = {
    "api_key": SERPI_TOKEN,
    "engine": "google_hotels",
    "q": "madrid",
    "hl": "en",
    "gl": "us",
    "check_in_date": "2025-09-08",
    "check_out_date": "2025-09-14",
    "currency": "EUR",
    "sort_by": "3",
    "adults": "2"
}
"""


def hotel_query(params):
  try:
    params["api_key"] = SERPI_TOKEN
    search = GoogleSearch(params)
    results = search.get_dict()

    if "error" in results:
      return f"Ocurrió un error en la API: {results['error']}"

    if "properties" not in results:
      return "No se encontraron hoteles para la búsqueda especificada."

    lista_hoteles = results.get("properties", [])

    if not lista_hoteles:
      return "No se encontraron hoteles para la búsqueda especificada."

    # Build the formatted string
    hotel_info_string = f"Se encontraron {len(lista_hoteles)} hoteles:\n\n"

    for i, hotel in enumerate(lista_hoteles, 1):
      nombre = hotel.get("name", "Nombre no disponible")
      precio = hotel.get("rate_per_night", {}).get(
        "lowest", "N/A"
      )
  
      puntuacion = hotel.get("overall_rating", "N/A")
      total_opiniones = hotel.get("reviews", "N/A")
      descripcion = hotel.get("description", "Descripción no disponible")
      enlace = hotel.get("link", "Enlace no disponible")

      # Format price display

      hotel_info_string += f"""🏨 Hotel #{i}: {nombre}
💰 Precio: {precio}
⭐ Puntuación: {puntuacion} ({total_opiniones} opiniones)
📝 Descripción: {descripcion}
🔗 Enlace: {enlace}

{"="*50}

"""

    return hotel_info_string.strip()

  except Exception as e:
    return f"Ha ocurrido una excepción: {str(e)}"
