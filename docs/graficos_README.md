# Módulo Ansible: `graficos`

Este módulo genera dos tipos de gráficos a partir de los resultados de tareas automatizadas; un gráfico de torta para éxitos y fallos, y un gráfico de barras para representar metricas agrupadas. Utiliza la biblioteca `plotly` para crear visualizaciones exportables en formato PNG. (Plotly)

## Requisitos

- Ansible
- Python 3.x
- chromium o chrome
- Dependencias Python:
  - Plotly  
  - Kaleido
  - Numpy
  - Pandas
- Dependencias S.O:
  - libX11 
  - libXcomposite 
  - libXcursor 
  - libXdamage 
  - libXext 
  - libXi 
  - libXtst 
  - libxkbcommon 
  - libXrandr 
  - libXcomposite 
  - libxshmfence 
  - libXScrnSaver 
  - libX11-xcb
  - mesa-libgbm
  - nss 
  - alsa-lib
  - cups-libs
  - pango
  - atk
  - at-spi2-atk

```bash
$ pip install <librería>
```

```bash
# Instalación de chromium manual por sí lo requieren.

$ curl -L -o chrome-linux.zip https://download-chromium.appspot.com/dl/Linux_x64?type=snapshots
$ unzip chrome-linux.zip -d /opt
$ ln -s /opt/chrome-linux/chrome /usr/local/bin/chrome
```
## Parámetros

| Parámetro              | Tipo   | Requerido | Descripción |
|---------------------|--------|-----------|-------------|
| `distribucion`            | dict    | Sí        | Diccionario que representa la distribución para el gráfico de torta. Cada clave representa una categoría, y su valor puede ser un número o un diccionario con cantidad y opcionalmente color. |
| `titulo_torta`            | str    | No        | Título para el gráfico de torta. Valor por defecto: "Gráfico de Distribución". |
| `recurrencias`      | dict   | No        | 	Diccionario con datos para el gráfico de barras (clave = nombre, valor = cantidad o diccionario con cantidad y color). |
| `titulo_barras`      | str   | No        | Título para el gráfico de barras. Valor por defecto: "Gráfico de Medición". |
| `carpeta_salida`    | str    | No        | Carpeta donde se guardarán los gráficos generados. Por defecto es el directorio actual (`.`). |
| `incluir_base64`    | bool   | No        | Si se establece en `true`, se incluirán las versiones codificadas en Base64 de los gráficos en la salida del módulo. |

## Uso 

```yaml
- name: Generar gráficos personalizados (colores y titulos personalizados) con base64
  graficos:
    distribucion:
      exitos:
        cantidad: 80
        color: '#28a745'
      fallos:
        cantidad: 20
        color: '#dc3545'
    recurrencias:
      adultos:
        cantidad: 5
        color: '#007bff'
      adolescentes:
        cantidad: 3
    titulo_torta: "Resumen de Tareas"
    titulo_barras: "Distribución por Grupo"
    carpeta_salida: "/tmp"
    incluir_base64: true

- name: Generar gráficos sin tanta personalización y sin base64
  graficos:
    distribucion: "{{ metricas }}"
    recurrencias: "{{ asistentes }}"
    carpeta_salida: "/tmp"
  vars:
    metricas:
        tasa_exito: 80
        tasa_fallo: 20
    asistentes:
        adultos: 5
        adolescentes: 3 
```

## Ejemplo de graficos generados:

#### Grafico torta

![Gráfico torta](imagenes/grafico_torta.png)

#### Gráfico de barras

![Gráfico de barras](imagenes/grafico_barras.png)

## Retorno

El módulo devuelve un diccionario con las rutas de los archivos generados y, si se solicita, sus representaciones en Base64:

```yaml
{
  "changed": true,
  "grafico_torta": "/tmp/grafico_torta.png",
  "grafico_barras": "/tmp/grafico_barras.png",
  "grafico_torta_base64": "iVBORw0K...",
  "grafico_barras_base64": "iVBORw0K...",
  "msg": "Gráficos generados correctamente"
}
```

## Notas

- Puedes usar las imágenes en reportes HTML o insertarlas directamente en documentos PDF.

## Author

- [@Xploit9999](https://github.com/Xploit9999)
