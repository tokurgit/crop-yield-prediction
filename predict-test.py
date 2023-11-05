
import requests


# URL and Port where Flask "crop-yield" app is running at the moment
url = "http://0.0.0.0:9696/predict"

area = "kenya"
crop = "maize"
field_data = {
    "area": area,
    "item": crop,
    "year": 1996,
    "average_rain_fall_mm_per_year": 630.0,
    "pesticides_tonnes": 6344.0,
    "avg_temp": 16.44
}

response = requests.post(url, json=field_data)
res = response.json()

assert response.status_code == 200

hg_ha_yield = res["predicted_yield"]["hectograms_per_hectare"]

print(f"The expected {crop=} yield in {area.capitalize()} is {hg_ha_yield} hg/ha.")
