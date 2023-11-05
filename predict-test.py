
import requests


# URL and Port where Flask "crop-yield" app is running at the moment
url = "http://localhost:9696/predict"

field_data = {
    "area": "kenya",
    "item": "kek",
    "year": 1996,
    "average_rain_fall_mm_per_year": 630.0,
    "pesticides_tonnes": 6344.0,
    "avg_temp": 16.44
}

response = requests.post(url, json=field_data)
assert response.status_code == 200

res = response.json()
hg_ha_yield = res["predicted_yield"]["hectograms_per_hectare"]

print(f"The expected crop yield is {hg_ha_yield} hg/ha.")
