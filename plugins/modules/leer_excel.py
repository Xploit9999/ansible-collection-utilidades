#/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: leer_excel
short_description: Lee datos de un archivo Excel desde una celda inicial, hasta un delimitador o rango.
version_added: "1.0"
description:
  - Este módulo lee datos desde una hoja de Excel (.xlsx), comenzando en una celda específica.
  - Se puede detener la lectura al encontrar un delimitador o definir un rango con celda inicial y final.
  - El número de columnas a leer puede definirse manualmente si no se proporciona una celda final.
options:
  ruta:
    description:
      - Ruta absoluta al archivo de Excel (.xlsx) a leer.
    required: true
    type: str
  hoja:
    description:
      - Nombre de la hoja desde donde se leerán los datos.
    required: true
    type: str
  celda_inicial:
    description:
      - Celda inicial para comenzar la lectura (por ejemplo, A34).
    required: true
    type: str
  num_columnas:
    description:
      - Número de columnas a leer horizontalmente desde la celda inicial.
      - Requerido si no se proporciona C(celda_final).
    required: false
    type: int
    default: null
  celda_final:
    description:
      - Celda final que define el límite del rango de lectura.
      - No se puede usar junto con C(delimitador).
    required: false
    type: str
    default: null
  delimitador:
    description:
      - Cadena usada como marcador para detener la lectura cuando se encuentra en alguna celda.
      - No se puede usar junto con C(celda_final).
    required: false
    type: str
    default: null
author:
  - John (@Xploit9999)
'''

EXAMPLES = r'''
# Leer desde A34 hasta encontrar el delimitador "*/"
- name: Leer con delimitador
  leer_excel:
    ruta: "/ruta/al/archivo.xlsx"
    hoja: "Datos"
    celda_inicial: "A34"
    num_columnas: 10
    delimitador: "*/"

# Leer desde A34 hasta J40
- name: Leer rango definido
  leer_excel:
    ruta: "/ruta/al/archivo.xlsx"
    hoja: "Datos"
    celda_inicial: "A34"
    celda_final: "J40"
'''

RETURN = r'''
datos:
  description: Lista de filas leídas desde la hoja de Excel.
  type: list
  elements: list
  returned: success
  sample: [["dato1", "dato2"], ["dato3", "dato4"]]
changed:
  description: Siempre es False porque no se modifica ningún archivo.
  type: bool
  returned: always
'''

import openpyxl
from ansible.module_utils.basic import AnsibleModule

def leer_excel(ruta, hoja_nombre, celda_inicial, num_columnas, delimitador=None, celda_final=None):

    if delimitador and celda_final:
        raise ValueError("No se puede usar 'delimitador' y 'celda_final' juntos.")
    if not delimitador and not celda_final:
        raise ValueError("Debe especificarse 'delimitador' o 'celda_final'.")

    columna_inicial = ord(celda_inicial[0].upper()) - ord('A') + 1
    fila_inicial = int(celda_inicial[1:])

    if celda_final:
        columna_final = ord(celda_final[0].upper()) - ord('A') + 1
        fila_final = int(celda_final[1:])
        max_col = columna_final  
    elif num_columnas is not None:
        max_col = columna_inicial + num_columnas - 1
        fila_final = fila_inicial + 1000  
    else:
        raise ValueError("Debe especificarse 'num_columnas' cuando no se usa 'celda_final'.")

    wb = openpyxl.load_workbook(ruta, data_only=True)
    hoja = wb[hoja_nombre]
    datos = []

    for fila in hoja.iter_rows(min_row=fila_inicial, max_row=fila_final, min_col=columna_inicial, max_col=max_col):
        datos_fila = [str(celda.value).strip() if celda.value is not None else "" for celda in fila]

        if delimitador and any(delimitador.strip() == valor for valor in datos_fila):  
            break  

        datos.append(datos_fila)

    return datos

def iniciar_proceso():
    module_args = dict(
        ruta=dict(type='str', required=True),
        hoja=dict(type='str', required=True),
        celda_inicial=dict(type='str', required=True),
        num_columnas=dict(type='int', required=False, default=None),
        delimitador=dict(type='str', required=False, default=None),
        celda_final=dict(type='str', required=False, default=None)
    )

    resultado = dict(
        changed=False,
        datos=None
    )

    try:
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

        resultado['datos'] = leer_excel(
            module.params['ruta'],
            module.params['hoja'],
            module.params['celda_inicial'],
            module.params['num_columnas'],
            module.params.get('delimitador'),
            module.params.get('celda_final')
        )

        module.exit_json(**resultado)

    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    iniciar_proceso()

