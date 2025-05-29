# Módulo Ansible: `html_pdf`

Este módulo permite convertir archivos HTML en archivos PDF utilizando la biblioteca `pyppeteer` (automatización de Chromium). Es útil para generar reportes automatizados desde documentos HTML renderizados.

## Requisitos

- Python 3.7+
- Ansible
- pyppeteer (Instalable con `pip install pyppeteer`)

## Parámetros 

| Parámetro    | Tipo | Requerido | Descripción                                  | Valor por defecto |
|--------------|-----|------|----------------------------------------------------|-------------------|
| `origen`     | str | Sí | Ruta al archivo HTML de entrada                      | -                 |
| `destino`     | str | Sí | Ruta de salida para el PDF generado                 | -                 |
| `formato_hoja`| str | No | Formato del papel del PDF (Ej: `A4`, `Letter`)      | `A4`              |
| `orientacion` | str | No | Orientación del papel (`horizontal` o `vertical`)   | `horizontal`      |

## Uso

Ejemplo de un playbook que usa el módulo:

```yaml
- name: Convertir documento HTML en tamaño letter (carta) con orientación horizontal. 
  html_pdf:
    origen: /home/usuario/reporte.html
    destino: /home/usuario/reporte.pdf
    formato_hoja: Letter
    orientacion: horizontal

- name: Convertir documento HTML sin especificar formato_hoja, por defecto (A4), con orientación vertical.
  html_pdf:
    origen: /home/usuario/reporte.html
    destino: /home/usuario/reporte.pdf
    orientacion: vertical
```

### 📄 Formatos de hoja disponibles

| Nombre   | Dimensiones (pulgadas) | Dimensiones (milímetros) | Notas                     |
|----------|------------------------|--------------------------|---------------------------|
| A0       | 33.1 × 46.8            | 841 × 1189               | Tamaño ISO                |
| A1       | 23.4 × 33.1            | 594 × 841                | Tamaño ISO                |
| A2       | 16.5 × 23.4            | 420 × 594                | Tamaño ISO                |
| A3       | 11.7 × 16.5            | 297 × 420                | Tamaño ISO                |
| A4       | 8.3 × 11.7             | 210 × 297                | Tamaño ISO, **por defecto** |
| A5       | 5.8 × 8.3              | 148 × 210                | Tamaño ISO                |
| Letter   | 8.5 × 11               | 216 × 279                | Estándar en EE.UU.        |
| Legal    | 8.5 × 14               | 216 × 356                |                           |
| Tabloid  | 11 × 17                | 279 × 432                |                           |
| Ledger   | 17 × 11                | 432 × 279                |                           |

---

### ↔️ Opciones de orientación

| Valor       | Descripción                 | Efecto en el módulo            |
|-------------|-----------------------------|-------------------------------|
| "vertical"   | Orientación vertical (portrait)   | landscape: false (por defecto) |
| "horizontal" | Orientación horizontal (landscape) | landscape: true                |


## Nota

> *Este módulo solo convierte archivos HTML.*

---

## Author

- [@Xploit9999](https://github.com/Xploit9999)
