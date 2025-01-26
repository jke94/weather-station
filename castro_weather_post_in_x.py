import requests
import argparse
import tweepy

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

def publicar_en_x(api_key, api_key_secret, access_token, access_token_secret, mensaje):
    try:
        # Autenticación con la API de X (Twitter)
        auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        # Publicar el tweet
        api.update_status(mensaje)
        print("Mensaje publicado en X correctamente.")
    except Exception as e:
        print(f"Error al publicar en X: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Obtener datos meteorológicos y publicarlos en X.")
    parser.add_argument("station_id", type=str, help="ID de la estación meteorológica.")
    parser.add_argument("api_key", type=str, help="API Key para acceder a los datos.")
    parser.add_argument("twitter_api_key", type=str, help="API Key de X (Twitter).")
    parser.add_argument("twitter_api_key_secret", type=str, help="API Key Secret de X (Twitter).")
    parser.add_argument("twitter_access_token", type=str, help="Access Token de X (Twitter).")
    parser.add_argument("twitter_access_token_secret", type=str, help="Access Token Secret de X (Twitter).")
    args = parser.parse_args()

    # Obtener datos meteorológicos
    resultado = obtener_datos_meteorologicos(args.station_id, args.api_key)

    if "error" not in resultado:
        # Crear el mensaje para publicar
        mensaje = (
            f"📊 Datos meteorológicos:\n"
            f"🌡️ Máxima: {resultado['tempHigh']}°C\n"
            f"🌡️ Mínima: {resultado['tempLow']}°C\n"
            f"💧 Precipitación: {resultado['precipTotal']}mm\n"
            f"🌬️ Viento promedio: {resultado['windspeedAvg']} km/h ({resultado['WindDirec']})\n"
            f"🔆 Índice UV: {resultado['uvHigh']} ({resultado['uvHighLetter']})"
        )

        # Publicar en X
        publicar_en_x(
            args.twitter_api_key,
            args.twitter_api_key_secret,
            args.twitter_access_token,
            args.twitter_access_token_secret,
            mensaje
        )
    else:
        print(resultado["error"])
