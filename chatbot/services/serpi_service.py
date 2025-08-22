from serpapi import GoogleSearch
import os
from dotenv import load_dotenv


load_dotenv()
SERPI_TOKEN = os.getenv("SERPAPI")


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
    hoteles_encontrados = []
    hotel_info_string = f"Se encontraron {len(lista_hoteles)} hoteles:\n\n"
    for hotel in lista_hoteles:
        info_hotel = {
            "nombre": hotel.get("name"),
            "precio": hotel.get("rate_per_night", {}).get("lowest"),
            "puntuacion": hotel.get("overall_rating"),
            "total_opiniones": hotel.get("reviews"),
            "descripcion": hotel.get("description"),
            "enlace_google": hotel.get("link")
        }
        hoteles_encontrados.append(info_hotel)

    return hoteles_encontrados

  except Exception as e:
    return f"Ha ocurrido una excepción: {str(e)}"
