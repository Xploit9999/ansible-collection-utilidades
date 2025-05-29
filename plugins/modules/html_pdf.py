#!/usr/bin/python

DOCUMENTATION = r'''
---
module: html_pdf
short_description: Convierte un archivo HTML a PDF usando Pyppeteer.
version_added: "1.0"
description:
  - Este módulo convierte un archivo HTML local en un archivo PDF.
  - Permite configurar el formato de hoja y la orientación del PDF generado.
options:
  origen:
    description:
      - Ruta del archivo HTML de entrada que se desea convertir.
    required: true
    type: str
  destino:
    description:
      - Ruta donde se guardará el archivo PDF generado.
    required: true
    type: str
  formato_hoja:
    description:
      - Formato del papel para el PDF.
      - Consultar todos los formato en https://github.com/Xploit9999/Ansible_modulos/blob/devel/html_pdf/README.md#-formatos-de-hoja-disponibles
    required: false
    type: str
    default: "A4"
  orientacion:
    description:
      - Orientación de la página en el PDF.
      - Puede ser "vertical" o "horizontal".
    required: false
    type: str
    choices:
      - vertical
      - horizontal
    default: "vertical"
author:
  - John (@Xploit9999)
requirements:
  - pyppeteer
  - Dependencias de S.O consultar el README https://github.com/Xploit9999/Ansible_modulos/tree/devel/html_pdf/README.md 
notes:
  - Se requiere que pyppeteer y sus dependencias estén instaladas en el entorno Python.
  - Este módulo usa un navegador Chromium sin interfaz gráfica para la conversión.
'''

EXAMPLES = r'''
# Convertir un archivo HTML a PDF con configuración por defecto (A4 vertical)
- name: Convertir HTML a PDF
  html_pdf:
    origen: "/tmp/ejemplo.html"
    destino: "/tmp/ejemplo.pdf"

# Convertir HTML a PDF en formato Letter y orientación horizontal
- name: Convertir HTML a PDF con formato Letter y horizontal
  html_pdf:
    origen: "/var/www/index.html"
    destino: "/var/www/index.pdf"
    formato_hoja: "Letter"
    orientacion: "horizontal"
'''

RETURN = r'''
changed:
  description: Indica si el PDF fue generado correctamente.
  type: bool
  returned: always
msg:
  description: Mensaje de estado del módulo.
  type: str
  returned: always
destino:
  description: Ruta absoluta del archivo PDF generado.
  type: str
  returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import asyncio
import os
from pyppeteer import launch

async def convertir_html_a_pdf(ruta_html, ruta_pdf, formato_hoja, orientacion):

    navegador = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    pagina = await navegador.newPage()
    await pagina.setViewport({'width': 1200, 'height': 800})

    url_archivo = 'file://' + os.path.abspath(ruta_html)
    await pagina.goto(url_archivo, waitUntil='load', timeout=0)
    await asyncio.sleep(1) 

    await pagina.pdf({
        'path': ruta_pdf,
        'format': formato_hoja,
        'landscape': orientacion == 'horizontal',
        'printBackground': True,
        'margin': {
            'top': '20px',
            'right': '20px',
            'bottom': '20px',
            'left': '20px'
        }
    })

    await navegador.close()

def main():

    modulo = AnsibleModule(
        argument_spec=dict(
            origen=dict(type='path', required=True),
            destino=dict(type='path', required=True),
            formato_hoja=dict(type='str', required=False, default='A4'),
            orientacion=dict(type='str', required=False, choices=['vertical', 'horizontal'], default='vertical')
        )
    )

    ruta_html = os.path.abspath(modulo.params['origen'])
    ruta_pdf = os.path.abspath(modulo.params['destino'])
    formato_hoja = modulo.params['formato_hoja']
    orientacion = modulo.params['orientacion']

    if not os.path.exists(ruta_html):
        modulo.fail_json(msg=f"El archivo HTML no existe en la ruta: {ruta_html}")

    try:
        asyncio.run(convertir_html_a_pdf(ruta_html, ruta_pdf, formato_hoja, orientacion))
        modulo.exit_json(changed=True, msg="PDF generado correctamente", destino=ruta_pdf)
    except Exception as error:
        modulo.fail_json(msg=f"Error al generar el PDF: {str(error)}")

if __name__ == '__main__':
    main()
