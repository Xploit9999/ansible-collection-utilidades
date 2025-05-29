# Módulo Ansible: leer_excel

## Descripción
El módulo `leer_excel` permite leer datos desde un archivo Excel (.xlsx), comenzando desde una celda especificada y tomando un número determinado de columnas. La lectura se detendrá cuando se encuentre un delimitador definido por el usuario. Los datos leídos se retornan como una lista de listas, donde cada sublista corresponde a una fila del archivo Excel.

## Opciones
El módulo requiere los siguientes parámetros:

### `ruta`
- **Descripción**: Ruta del archivo Excel a leer.
- **Tipo**: `str`
- **Requerido**: Sí

### `hoja`
- **Descripción**: Nombre de la hoja dentro del archivo Excel de la cual leer los datos.
- **Tipo**: `str`
- **Requerido**: Sí

### `celda_inicial`
- **Descripción**: La celda inicial desde la cual comenzar a leer los datos (por ejemplo, "B53").
- **Tipo**: `str`
- **Requerido**: Sí

### `celda_final`
- **Descripción**: Celda de finalización de lectura. Si se especifica, la lectura se detendrá en esa celda. 
- **Tipo**: `str`
- **Requerido**: No


### `num_columnas`
- **Descripción**: Número de columnas a leer, a partir de la celda inicial. (No aplica si celda_final tiene parametro definido).
- **Tipo**: `int`
- **Requerido**: No

### `delimitador`
- **Descripción**: Delimitador que indica el final de la lectura. Cuando se encuentra este valor, la lectura se detiene.
- **Tipo**: `str`
- **Requerido**: No

## Ejemplos

### Leer datos desde un archivo Excel
```yaml
  - name: Leer datos desde un archivo Excel
    leer_excel:
      ruta: "/path/to/file.xlsx"
      hoja: "testing"
      celda_inicial: "B53"
      num_columnas: 15
      delimitador: "*/"
    register: datos

  - name: Mostrar los datos leídos
    debug:
      var: datos

  - name: Leer una celda en especifico
    leer_excel:
      ruta: "/path/to/file.xlsx"
      hoja: "testing"
      celda_inicial: "A2"
      num_columnas: 1
      delimitador: "*/"
    register: datos

  - name: Mostrar dato de la celda en especifico a consultar.
    debug:
      var: "{{ datos[0][0] }}"

  - name: Leer archivo Excel con rango de celda final
    leer_excel:
      ruta: "/path/to/test.xlsx"
      hoja: "Formulario"
      celda_inicial: "B53"
      celda_final: "I18"
    register: datos
```
## Nota

- Este módulo utiliza la librería `openpyxl` para leer archivos Excel.
- Se debe de definir `celda_final` o `delimitador` para la finalización de la lectura, ambos parametros no pueden ir juntos.

## Author

- **John Freidman** - [@Xploit9999](https://github.com/Xploit9999)
