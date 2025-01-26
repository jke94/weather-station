import requests
import os

def obtener_datos_meteorologicos(station_id, api_key):
    url = f"https://api.weather.com/v2/pws/dailysummary/3day?apiKey={api_key}&stationId={station_id}&numericPrecision=decimal&format=json&units=m"

    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()

            # Obtenemos los datos
            tempHigh = data['summaries'][1]['metric']['tempHigh']
            tempLow = data['summaries'][1]['metric']['tempLow']
            precipTotal = data['summaries'][1]['metric']['precipTotal']
            pressureMax = data['summaries'][1]['metric']['pressureMax']
            pressureMin = data['summaries'][1]['metric']['pressureMin']
            windspeedAvg = data['summaries'][1]['metric']['windspeedAvg']
            windgustHigh = data['summaries'][1]['metric']['windgustHigh']
            uvHigh = data['summaries'][0]['uvHigh']
            winddirAvg = data['summaries'][0]['winddirAvg']
            
            # Calculamos direccion del viento
            if 0 <= winddirAvg <= 22.5 or 337.5 <= winddirAvg <= 360:
                WindDirec = "N"
            elif 22.5 <= winddirAvg < 67.5:
                WindDirec = "NE"
            elif 67.5 <= winddirAvg < 112.5:
                WindDirec = "E" 
            elif 112.5 <= winddirAvg < 157.5:
                WindDirec = "SE"
            elif 157.5 <= winddirAvg < 202.5:
                WindDirec = "S"
            elif 202.5 <= winddirAvg < 247.5:
                WindDirec = "SW"
            elif 247.5 <= winddirAvg < 292.5:
                WindDirec = "W"
            elif 292.5 <= winddirAvg < 337.5:
                WindDirec = "NW"

            # Calculamos indice UV
            if 0 <= uvHigh <= 2:
                uvHighLetter = "Bajo"
            elif 3 <= uvHigh <= 5:
                uvHighLetter = "Moderado"
            elif 6 <= uvHigh <= 7:
                uvHighLetter = "Alto"
            elif 8 <= uvHigh <= 10:
                uvHighLetter = "Muy alto"
            elif 11 <= uvHigh <= 100:
                uvHighLetter = "Extremo"

            # Salida de datos
            output = {
                "tempHigh": tempHigh,
                "tempLow": tempLow,
                "precipTotal": precipTotal,
                "pressureMax": pressureMax,
                "pressureMin": pressureMin,
                "windspeedAvg": windspeedAvg,
                "windgustHigh": windgustHigh,
                "winddirAvg": winddirAvg,
                "uvHigh": uvHigh,
                "WindDirec": WindDirec,
                "uvHighLetter": uvHighLetter
            }

            return output

        except ValueError:
            return {"error": "Error al procesar los datos JSON."}
    else:
        return {"error": f"Error al obtener los datos: {response.status_code}"}

if __name__ == "__main__":

    station_id = os.getenv("STATION_ID")
    api_key = os.getenv("API_KEY")

    if not station_id or not api_key:
        print("Error: Las variables de entorno STATION_ID y API_KEY deben estar definidas.")
    else:
        resultado = obtener_datos_meteorologicos(station_id, api_key)
        print(resultado)
