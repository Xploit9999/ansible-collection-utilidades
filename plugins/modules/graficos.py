#!/usr/bin/python

DOCUMENTATION = r'''
---
module: graficos
short_description: Genera gráficos de torta y barras a partir de datos en diccionario.
version_added: "1.0"
description:
  - Este módulo genera gráficos de tipo torta (pie chart) y barras horizontales usando Plotly.
  - Los datos pueden incluir colores personalizados por categoría.
  - Las imágenes se guardan en disco y opcionalmente se devuelven codificadas en base64.
options:
  distribucion:
    description:
      - Diccionario de datos para el gráfico de torta.
      - Cada clave representa una categoría.
      - El valor puede ser un número (cantidad) o un diccionario con 'cantidad' y 'color'.
    required: true
    type: dict
  titulo_torta:
    description:
      - Título del gráfico de torta.
    required: false
    type: str
    default: "Grafico de Distribucion"
  recurrencias:
    description:
      - Diccionario de datos para el gráfico de barras.
      - Si no se especifica, no se genera gráfico de barras.
    required: false
    type: dict
    default: {}
  titulo_barras:
    description:
      - Título del gráfico de barras.
    required: false
    type: str
    default: "Grafico de Medicion"
  carpeta_salida:
    description:
      - Carpeta donde se guardarán las imágenes generadas.
    required: false
    type: str
    default: "."
  incluir_base64:
    description:
      - Si es verdadero, devuelve las imágenes también codificadas en base64.
    required: false
    type: bool
    default: false
author:
  - John (@Xploit9999)
requirements:
  - plotly
  - kaleido
  - numpy
  - pandas
notes:
  - Requiere tener instalado plotly, kaleido, numpy y pandas para la generación y exportación de gráficos.
  - La carpeta de salida debe existir o el módulo fallará.
'''

EXAMPLES = r'''
# Generar gráfico de torta simple
- name: Generar gráfico de torta simple
  graficos:
    distribucion:
      CategoriaA: 10
      CategoriaB: 20
    carpeta_salida: "/tmp"

# Generar gráficos de torta y barras con colores y base64
- name: Generar gráficos de torta y barras con colores y base64
  graficos:
    distribucion:
      CategoriaA:
        cantidad: 15
        color: "#FF0000"
      CategoriaB:
        cantidad: 35
        color: "#00FF00"
    recurrencias:
      Tarea1: 5
      Tarea2: 8
    incluir_base64: true
    carpeta_salida: "/tmp"
'''


RETURN = r'''
changed:
  description: Indica si el módulo generó nuevos gráficos.
  type: bool
  returned: always
grafico_torta:
  description: Ruta del archivo generado para el gráfico de torta.
  type: str
  returned: always
grafico_barras:
  description: Ruta del archivo generado para el gráfico de barras (o null si no aplica).
  type: str
  returned: when recurrencias se proveen
leyenda_barras:
  description: Lista de diccionarios con las tareas y sus cantidades en el gráfico de barras.
  type: list
  elements: dict
  returned: when recurrencias se proveen
grafico_torta_base64:
  description: Contenido del gráfico de torta codificado en base64 (solo si incluir_base64 es true).
  type: str
  returned: when incluir_base64 == true
grafico_barras_base64:
  description: Contenido del gráfico de barras codificado en base64 (solo si incluir_base64 es true y se genera gráfico de barras).
  type: str
  returned: when incluir_base64 == true and recurrencias se proveen
'''

from ansible.module_utils.basic import AnsibleModule
import plotly.express as px
import base64
import os

def codificar_base64(ruta):
    with open(ruta, 'rb') as imagen:
        return base64.b64encode(imagen.read()).decode('utf-8')

def procesar_datos(datos):
    etiquetas = []
    cantidades = []
    colores = []

    for etiqueta, info in datos.items():
        if isinstance(info, dict):
            cantidad = info.get('cantidad', 0)
            color = info.get('color')
        else:
            cantidad = info
            color = None

        etiquetas.append(etiqueta)
        cantidades.append(cantidad)
        colores.append(color)

    return etiquetas, cantidades, colores

def main():

    modulo = AnsibleModule(
        argument_spec=dict(
            distribucion=dict(type='dict', required=True),
            titulo_torta=dict(type='str', required=False, default='Gráfico de Distribución'),
            recurrencias=dict(type='dict', required=False, default={}),
            titulo_barras=dict(type='str', required=False, default='Gráfico de Medición'),
            carpeta_salida=dict(type='str', required=False, default='.'),
            incluir_base64=dict(type='bool', required=False, default=False),
        ),
        supports_check_mode=False
    )

    distribucion = modulo.params['distribucion']
    titulo_torta = modulo.params['titulo_torta']
    recurrencias = modulo.params['recurrencias']
    titulo_barras = modulo.params['titulo_barras']
    carpeta_salida = modulo.params['carpeta_salida']
    incluir_base64 = modulo.params['incluir_base64']

    try:
        etiquetas_torta, cantidades_torta, colores_torta = procesar_datos(distribucion)
        etiquetas_con_valores = [f"{etiqueta} ({cantidad})" for etiqueta, cantidad in zip(etiquetas_torta, cantidades_torta)]

        datos_pie = {
            'Etiqueta': etiquetas_con_valores,
            'Cantidad': cantidades_torta
        }

        figura_pie = px.pie(
            datos_pie,
            names='Etiqueta',
            values='Cantidad',
            title=titulo_torta,
        )

        if any(colores_torta):
            color_map = {label: color for label, color in zip(etiquetas_con_valores, colores_torta) if color}
            figura_pie.update_traces(marker=dict(colors=[color_map.get(lbl) for lbl in etiquetas_con_valores]))

        figura_pie.update_traces(textposition='inside', textinfo='percent+label')
        ruta_pie = os.path.join(carpeta_salida, "grafico_torta.png")
        figura_pie.write_image(ruta_pie, width=400, height=400)

        leyenda_barras = []

        if recurrencias:
            etiquetas_barras, cantidades_barras, colores_barras = procesar_datos(recurrencias)

            datos_barras = list(zip(etiquetas_barras, cantidades_barras, colores_barras))
            datos_barras.sort(key=lambda x: x[1], reverse=True)
            etiquetas_barras, cantidades_barras, colores_barras = zip(*datos_barras)

            figura_barras = px.bar(
                x=cantidades_barras,
                y=etiquetas_barras,
                title=titulo_barras,
                labels={'x': 'Cantidad', 'y': 'Tarea'},
                orientation='h'
            )
            figura_barras.update_layout(yaxis=dict(autorange="reversed"))

            figura_barras.update_traces(marker_color=[
                color if color else '#C9190B' for color in colores_barras
            ], text=cantidades_barras, textposition='outside')

            alto = max(400, len(etiquetas_barras) * 40)
            ruta_barras = os.path.join(carpeta_salida, "grafico_barras.png")
            figura_barras.write_image(ruta_barras, width=600, height=alto)

            leyenda_barras = [
                {"tarea": etiqueta, "cantidad": cantidad}
                for etiqueta, cantidad in zip(etiquetas_barras, cantidades_barras)
            ]
        else:
            ruta_barras = None

        resultado = {
            'changed': True,
            'grafico_torta': ruta_pie,
            'grafico_barras': ruta_barras,
            'leyenda_barras': leyenda_barras,
            'msg': "Gráficos generados correctamente"
        }

        if incluir_base64:
            resultado['grafico_torta_base64'] = codificar_base64(ruta_pie)
            if ruta_barras:
                resultado['grafico_barras_base64'] = codificar_base64(ruta_barras)

        modulo.exit_json(**resultado)

    except Exception as e:
        modulo.fail_json(msg=f"Error generando gráficos: {e}")

if __name__ == '__main__':
    main()
