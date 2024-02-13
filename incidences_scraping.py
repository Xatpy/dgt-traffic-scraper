import requests
import csv
from datetime import datetime, timedelta
import re

class TrafficIncident:
    def __init__(self, **kwargs):
        self.codEle = kwargs.get('codEle')
        self.alias = kwargs.get('alias')
        self.suceso = kwargs.get('suceso')
        self.autonomia = kwargs.get('autonomia')
        self.provincia = kwargs.get('provincia')
        self.poblacion = kwargs.get('poblacion')
        self.descripcion = kwargs.get('descripcion')
        self.causa = kwargs.get('causa')
        self.tipo = kwargs.get('tipo')
        self.estado = kwargs.get('estado')
        self.carretera = kwargs.get('carretera')
        self.sentido = kwargs.get('sentido')
        self.hora = kwargs.get('hora')
        self.horaFin = kwargs.get('horaFin')
        self.fecha = kwargs.get('fecha')
        self.fechaFin = kwargs.get('fechaFin')
        self.lng = kwargs.get('lng')
        self.lat = kwargs.get('lat')
        self.pkIni = kwargs.get('pkIni')
        self.pkFinal = kwargs.get('pkFinal')
        self.icono = kwargs.get('icono')
        self.nivel = kwargs.get('nivel')
        self.precision = kwargs.get('precision')
        self._date = kwargs.get('_date')

    def __repr__(self):
        return f"TrafficIncident({self.codEle}, {self.alias}, {self.suceso}, {self.autonomia}, {self.provincia}, {self.poblacion}, {self.descripcion}, {self.causa}, {self.tipo}, {self.estado}, {self.carretera}, {self.sentido}, {self.hora}, {self.horaFin}, {self.fecha}, {self.fechaFin}, {self.lng}, {self.lat}, {self.pkIni}, {self.pkFinal}, {self.icono}, {self.nivel}, {self.precision}, {self._date})"

    def __eq__(self, other):
        if not isinstance(other, TrafficIncident):
            return False

        return self.codEle == other.codEle

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    

def convert_date_format(input_date):
    parsed_date = datetime.strptime(input_date, "%d/%m/%Y - %H:%M")

    # Set the time zone offset for Madrid (CET/CEST)
    timezone_offset = timedelta(hours=1)

    parsed_date_with_offset = parsed_date - timezone_offset
    offset_seconds = timezone_offset.total_seconds()
    offset_sign = '+' if offset_seconds >= 0 else '-'
    offset_hours = int(offset_seconds // 3600)
    formatted_date = parsed_date_with_offset.strftime(f"%Y-%m-%dT%H:%M:%S{offset_sign}{offset_hours:02d}:00")

    return formatted_date


def remove_html_tags(input_string):
    clean_text = re.sub(r'<.*?>', '', input_string)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text


def get_traffic_info():
    url = "https://infocar.dgt.es/etraffic/BuscarElementos?latNS=44&longNS=5&latSW=27&longSW=-19&zoom=5&accion=getElementos&Camaras=false&SensoresTrafico=false&SensoresMeteorologico=false&Paneles=false&Radares=false&IncidenciasRETENCION=true&IncidenciasOBRAS=true&IncidenciasMETEOROLOGICA=true&IncidenciasPUERTOS=true&IncidenciasOTROS=true&IncidenciasEVENTOS=true&IncidenciasRESTRICCIONES=true&niveles=true&caracter=acontecimiento"

    try:
        response = requests.get(url)
        response.raise_for_status()  
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def export_to_csv(traffic_incidents):
    if not traffic_incidents:
        print("No traffic incidents to export.")
        return
    
    csv_filename = f"out/incidences/dgt_incidences.csv"
    existing_incidents = load_existing_incidents(csv_filename)

    with open(csv_filename, 'a', newline='') as csvfile:
        fieldnames = ['codEle', 'alias', 'suceso', 'autonomia', 'provincia', 'poblacion', 'descripcion',
                      'causa', 'tipo', 'estado', 'carretera', 'sentido', 'hora', 'horaFin', 'fecha', 'fechaFin',
                      'lng', 'lat', 'pkIni', 'pkFinal', 'icono', 'nivel', 'precision']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if len(existing_incidents) == 0:
            writer.writeheader()  # Write header only if the file is empty

        for incident in traffic_incidents:
            if not any(inc.codEle == incident.codEle for inc in existing_incidents):
                dateToConvert = f"{incident.fecha} - {incident.hora}"
                incident._date = convert_date_format(dateToConvert)
                incident.descripcion = remove_html_tags(incident.descripcion)
                writer.writerow(incident.__dict__)


def load_existing_incidents(csv_filename):
    existing_incidents = set()
    try:
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert attributes to the correct data types
                row = {key: value if value != '' else None for key, value in row.items()}
                existing_incidents.add(TrafficIncident(**row))
    except FileNotFoundError:
        pass  # File doesn't exist, it's okay to proceed

    return existing_incidents

if __name__ == "__main__":
    traffic_info = get_traffic_info()
    traffic_incidents = [TrafficIncident(**incident) for incident in sorted(traffic_info, key=lambda x: x.get('codEle', ''))]

    if len(traffic_incidents) > 0:
        export_to_csv(traffic_incidents)

    print(f"Data exported to CSV file with filename based on the current date and time. - " + str(len(traffic_incidents)))
