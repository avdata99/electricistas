import csv
import os
import requests

from bs4 import BeautifulSoup  # pip install bs4
from time import sleep

from matriculados import Matriculado


def gen_html(URL, n_page):
    # Agregar headers al request para que parezca hecho por un humano
    print(f'Revisando {URL}')

    # para evitar que cada ejecucion haga 200 request a la página,
    # grabamos los HTMLs localmente y los usamos cuando sea necesario
    # solo hacemos el request si no está descargado el HTML
    html_file = f'paginas/pagina-{n_page}.html'
    headers_val = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }
    # pregunto primero si existe la pagina dentro de la carpeta,
    # si no existe la descargo
    if not os.path.exists(html_file):
        print(f' - Descargando {URL}')
        response = requests.get(
            URL,
            headers=headers_val,
            timeout=10,
        )
        f = open(html_file, 'w', encoding='utf-8')
        f.write(response.text)
        f.close()

    # abrimos el archivo local que ya está descargado
    f = open(html_file, 'r', encoding='utf-8')
    texto_pagina = f.read()
    f.close()

    return texto_pagina


def scrape_volta():
    # preparar un archivo CSV para guardar los datos
    final_csv_file = open('final.csv', 'w', encoding='utf-8')
    fieldnames = ['numero', 'cuil', 'nombre', 'categoria', 'registro',
                  'localidad', 'barrio', 'contacto']
    writer = csv.DictWriter(final_csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Creo la carpeta donde guardare los archivos .html creados
    path = 'paginas'
    if not os.path.exists(path):
        os.makedirs(path)

    # URL con la pagina pendiente de carga para paginar
    url = 'http://volta.net.ar/registro?gd=&categoria=&nombre=&cuil=&registro=&localidad=CORDOBA&page={npage}'
    # son 201 páginas
    for page in range(1, 202):
        paginated_url = url.format(npage=page)
        text = gen_html(paginated_url, page)
        soup = BeautifulSoup(text, 'html.parser')

        # ejemplo de como ver las clases de todas las tablas del HTML
        # Sirve para ver que elementos están en el HTML y BS4 ve
        # for table in soup.find_all('table'):
        #     print(table.get('class'))

        # la pagina tiene una tabla con ID
        # eso simplifica ubicarla
        tabla_id = 'tblResultados'
        table = soup.find('table', id=tabla_id)
        for row in table.tbody.find_all('tr'):
            # mirar los rows (filas) de la tabla 
            # print(row)
            tds = row.find_all('td')
            """ Ejemplo de celdas (td) de la fila 
                #	CUIL	Nombre	Categoría	Registro	Localidad	Barrio	Contacto
                1	20338305851	AGUSTIN ANDRES DE LA COLINA	PROFESIONAL	5325/x	CORDOBA	GRANJA DE FUNES	 03543-423885
                157-913035
                agus_dlc5@hotmail.com
                """
            matriculado = Matriculado(
                nro=tds[0].text,
                cuil=tds[1].text,
                nombre=tds[2].text,
                categoria=tds[3].text,
                registro=tds[4].text,
                localidad=tds[5].text,
                barrio=tds[6].text,
                contacto=tds[7].text
            )

            # tomar solo las propiedades del matriculado que
            # se usaron como fieldnames al inicio
            row = {}
            m_dict = matriculado.__dict__
            for key, value in m_dict.items():
                if key in fieldnames:
                    row[key] = value

            writer.writerow(row)
        sleep(1)
