[![Traffic Scraper](https://github.com/Xatpy/dgt-traffic-scraper/actions/workflows/traffic_scraper.yml/badge.svg)](https://github.com/Xatpy/dgt-traffic-scraper/actions/workflows/traffic-scraper.yml)

## Description

Script que "scrapea" la web https://infocar.dgt.es/etraffic/ para almacenar un histórico de todos los cortes de tráfico (fecha y lugar) por _manifestación_ en toda España.

La web da información en tiempo real, pero el problema es que no hay una forma fácil de acceder a un histórico de datos de cuándo fueron los anteriores cortes de tráfico. Con este script descargamos esos datos filtrados cada 20 minutos.
