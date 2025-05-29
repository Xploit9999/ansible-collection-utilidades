# Módulo Ansible: `mod_excel`

Este módulo permite modificar archivos de Excel en formato `.xlsx`, escribiendo datos horizontalmente a partir de una celda inicial.
El módulo también permite reemplazar un delimitador en una celda con datos específicos y mover dicho delimitador a la siguiente fila.

## Requisitos

- Ansible
- Python 3.x
- `openpyxl` (instalable con `pip install openpyxl`)

## Parámetros

| Parámetro    | Tipo   | Requerido | Descripción                                                                    |
|--------------|--------|-----------|--------------------------------------------------------------------------------|
| `ruta`       | `str`  | Sí        | Ruta del archivo Excel a modificar.                                            |
| `hoja`       | `str`  | No        | Nombre de la hoja de cálculo. Si no se especifica, se usa la hoja activa.      |
| `delimitador`| `str`  | No        | Texto que indica el punto de inicio de la escritura y se coloca al final.      |
| `celda_inicial` | `str` | No      | Celda de inicio para escribir los datos. Requiere `celda_final`.               |
| `celda_final` | `str` | No        | Celda final del rango donde se escribirán los datos. Requiere `celda_inicial`. |
| `data`       | `list` | Sí        | Lista de datos que se escribirán en la fila donde se encuentra el delimitador. |

## Uso

Ejemplo de un playbook que usa el módulo:

```yaml
- name: Modificar Excel con `mod_excel`
  mod_excel:
    ruta: "test.xlsx"
    hoja: "Hoja1"
    delimitador: "*/"
    data: 
      - "Valor 1"
      - "Valor 2"
      - "Valor 3"

- name: Escribir una fila en el siguiente espacio vacío del rango
  mod_excel:
    ruta: "/ruta/archivo.xlsx"
    celda_inicial: "A34"
    celda_final: "J34"
    data:
      - ["dato1", "dato2", "dato3"]

- name: Escribir varias filas en el siguiente espacio vacío del rango
  mod_excel:
    ruta: "/ruta/archivo.xlsx"
    celda_inicial: "A34"
    celda_final: "J37"
    data:
      - ["dato1", "dato2", "dato3"]
      - ["dato4", "dato5", "dato6"]
      - ["dato7", "dato8", "dato9"]
```

## Funcionamiento
### Si se utiliza el delimitador:
1. Se busca el `delimitador` en la hoja de cálculo.
2. Se sobrescribe el delimitador con el primer dato de la lista.
3. Se escriben los datos en la fila encontrada, en distintas columnas (horizontalmente).
4. El delimitador se coloca en la siguiente fila, en la misma columna donde fue encontrado.

### Si se utilizan `celda_inicial` y `celda_final`:
1. Se calcula el rango definido por ambas celdas.
2. Se escriben los datos proporcionados dentro de ese rango.

## Notas

- Si no se encuentra el `delimitador`, el módulo fallará.
- Si se usan `celda_inicial` y `celda_final`, se ignora el `delimitador`.
- El módulo requiere que `openpyxl` esté instalado en el entorno Python de ejecución.
- Se recomienda respaldar el archivo antes de modificarlo.
  
## Author

- **John Freidman** - [@Xploit9999](https://github.com/Xploit9999)
