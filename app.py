from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# 🔑 Ahora la API Key se lee desde las variables de entorno
API_KEY = os.getenv("API_KEY")

CIUDADES = [
    "Goudge, AR",
    "San Rafael, AR",
    "Monte Comán, AR",
    "Cuadro Nacional, AR",
    "Salto de las Rosas, AR",
    "Villa Atuel, AR",
    "El Nihuil, AR",
    "Los Compartos, AR",
    "Los Molles, AR",
    "La Consulta, AR",
    "Rama Caída, AR",
    "Real Del Padre, AR",
    "Las Paredes, AR",
    "Los Reyunos, AR",
    "Villa Atuel Norte, AR",
]

CIUDADES_ID = {
    "Goudge, AR": 3854916,
    "San Rafael, AR": 3836669,
    "Monte Comán, AR": 3832803,
    "Cuadro Nacional, AR": 3836669,
    "Salto de las Rosas, AR": 3836669,
    "Villa Atuel, AR": 3832803,
    "El Nihuil, AR": 3839456,
    "Los Compartos, AR": 3832803,
    "La Consulta, AR": 3851913,
    "Rama Caída, AR": 3839456,
    "Real Del Padre, AR": 3839288,
    "Las Paredes, AR": 3847935,
    "Los Reyunos, AR": 3836669,
    "Villa Atuel Norte, AR": 3836669,
}

@app.route("/", methods=["GET"])
def clima():
    ciudad = request.args.get("ciudad", "San Rafael, AR")
    ciudad_id = CIUDADES_ID.get(ciudad, "")

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    respuesta = requests.get(url)
    datos = respuesta.json()

    hoy = datetime.today().date()
    fin_periodo = hoy + timedelta(days=5)
    dias_info = {}

    if "list" in datos:
        for pronostico in datos["list"]:
            fecha_pronostico = datetime.strptime(pronostico["dt_txt"], "%Y-%m-%d %H:%M:%S").date()
            if hoy <= fecha_pronostico < fin_periodo:
                temp = pronostico["main"]["temp_min"]
                humedad = pronostico["main"]["humidity"]
                if fecha_pronostico not in dias_info:
                    dias_info[fecha_pronostico] = {"temp_min": temp, "humedad_alta": humedad >= 80}
                else:
                    dias_info[fecha_pronostico]["temp_min"] = min(dias_info[fecha_pronostico]["temp_min"], temp)
                    if humedad >= 80:
                        dias_info[fecha_pronostico]["humedad_alta"] = True

    return render_template("index.html",
                           ciudad=ciudad,
                           ciudades=CIUDADES,
                           dias_info=dias_info,
                           ciudad_id=ciudad_id)

if __name__ == "__main__":
    app.run(debug=True)
