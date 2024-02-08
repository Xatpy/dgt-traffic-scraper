import requests
import json
import csv
from datetime import datetime

class TrafficIncident:
    def __init__(self, precision, poblacion, fecha, alias, suceso, sentido, descripcion,
                 fechaFin, lng, pkFinal, provincia, codEle, causa, carretera, hora,
                 estado, autonomia, pkIni, icono, tipo, horaFin, lat, nivel):
        self.precision = precision
        self.poblacion = poblacion
        self.fecha = fecha
        self.alias = alias
        self.suceso = suceso
        self.sentido = sentido
        self.descripcion = descripcion
        self.fechaFin = fechaFin
        self.lng = lng
        self.pkFinal = pkFinal
        self.provincia = provincia
        self.codEle = codEle
        self.causa = causa
        self.carretera = carretera
        self.hora = hora
        self.estado = estado
        self.autonomia = autonomia
        self.pkIni = pkIni
        self.icono = icono
        self.tipo = tipo
        self.horaFin = horaFin
        self.lat = lat
        self.nivel = nivel

    def __repr__(self):
        return f"TrafficIncident({self.alias}, {self.fecha}, {self.carretera}, {self.sentido}, {self.nivel})"

def get_traffic_info():
    url = "https://infocar.dgt.es/etraffic/BuscarElementos?latNS=44&longNS=5&latSW=27&longSW=-19&zoom=5&accion=getElementos&Camaras=false&SensoresTrafico=false&SensoresMeteorologico=false&Paneles=false&Radares=false&IncidenciasRETENCION=true&IncidenciasOBRAS=false&IncidenciasMETEOROLOGICA=false&IncidenciasPUERTOS=false&IncidenciasOTROS=false&IncidenciasEVENTOS=true&IncidenciasRESTRICCIONES=false&niveles=false&caracter=acontecimiento"

    try:
        response = requests.get(url)
        response.raise_for_status()  
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def export_to_csv(traffic_incidents, csv_filename=None):
    if not traffic_incidents:
        print("No traffic incidents to export.")
        return

    if csv_filename is None:
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M")
        csv_filename = f"out/{current_datetime}_traffic_incidents.csv"

    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['codEle', 'alias', 'provincia'] + [key for key in traffic_incidents[0].__dict__ if key not in ['codEle', 'alias', 'provincia']]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for incident in traffic_incidents:
            writer.writerow(incident.__dict__)

if __name__ == "__main__":
    traffic_info = get_traffic_info()

    traffic_incidents = [TrafficIncident(**incident) for incident in sorted(traffic_info, key=lambda x: x.get('provincia', '')) if 'MANIFESTACIÓN' in incident.get('descripcion', '')]

    if len(traffic_incidents) > 0:
        export_to_csv(traffic_incidents)

    print(f"Data exported to CSV file with filename based on the current date and time. - " + str(len(traffic_incidents)))