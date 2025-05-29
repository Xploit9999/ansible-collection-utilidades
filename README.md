# Ansible Collection - mi_mundo.utilidades

Colección personal de módulos y roles que desarrollo sobre necesidades del día a día.

## 📦 Módulos disponibles

### 🔍 `get_pids`
Módulo para obtener los **PIDs (Process IDs)** de uno o varios procesos activos por su nombre.

- Útil para auditorías, chequeos de estado o validaciones previas a tareas de administración.
- Retorna una lista de PIDs que coinciden con el nombre del proceso especificado.

---

### 🛑 `kill`
Módulo para **finalizar procesos** por PID o por nombre.

- Permite detener procesos de forma selectiva.
- Compatible con señales de terminación personalizadas (ej. `SIGTERM`, `SIGKILL`).

---

### 📖 `leer_excel`
Módulo para la **lectura de archivos Excel** (`.xlsx`).

- Lee datos desde hojas y rangos definidos.
- Útil en flujos donde Ansible consume configuraciones o parámetros desde documentos externos.

---

### ✏️ `mod_excel`
Módulo para la **modificación de documentos Excel** (`.xlsx`).

- Permite la inserción de datos a un documento excel tomando de referencia un delimitador o un rango de celdas para su escritura.
- Ideal para generar reportes o registros automatizados en formato Excel.

---

### 🔐 `openssl_sig`
Módulo para **firmar contenido con OpenSSL**.

- Firma cadenas de texto o archivos usando claves privadas.
- Soporta los métodos `dgst` y `pkeyutl`.
- Retorna la firma en base64.
- Compatible con múltiples algoritmos de hashing (`sha256`, `sha512`, etc).

---

### ✏️ `graficos`
Módulo para la **generación de graficos (torta y barras)**.

- Genera graficos en torta y barra en formato png.
- Los graficos pueden ser insertados en tu codigo html en formato base64.
- Puedes insertar directamente las imagenes en tu PDF.

---

### ✏️ `html_pdf`
Módulo para **conversión de documentos html a pdf**.

- Convierte documentos html a PDF.
- Flexibilidad en la exportación para diferentes formatos de hoja u orientación.

---

## 🔧 Requisitos

- Python 3.x
- Ansible >=2.15.0
- Para los módulos relacionados con Excel:
  - `openpyxl` (instalable vía `pip install openpyxl`)
- Para `openssl_sig`:
  - OpenSSL disponible en el sistema (`openssl` CLI)
  - Claves privadas en formato PEM
- Para el modulo de graficos: `pip install <dependencias>`
  - dependencias Python:
    - Plotly
    - Kaleido
    - Numpy
    - Pandas
  - dependencias S.O:
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
- Para el modulo de conversión html a pdf: `pip install <dependencias>`
  - Python 3.7+
  - pyppeteer 

---

## 🧑‍💻 Autor

[Xploit9999](https://github.com/Xploit9999) 
