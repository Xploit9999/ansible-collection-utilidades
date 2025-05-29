#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: openssl_sign
short_description: Firma contenido o archivos usando OpenSSL a través de un script bash.
description:
  - Este módulo permite firmar un texto o archivo usando el comando OpenSSL.
  - Soporta métodos de firma con "dgst" o "pkeyutl" y varios algoritmos hash.
options:
  content:
    description:
      - Texto a firmar directamente.
      - No debe ser una ruta de archivo.
    required: false
    type: str
  path:
    description:
      - Ruta a archivo cuyo contenido será firmado.
      - No puede usarse junto con content.
    required: false
    type: str
  algorithm:
    description:
      - Algoritmo hash usado para la firma (ej: sha256, md5).
    required: true
    type: str
    choices: ['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'md5']
  privatekey:
    description:
      - Ruta al archivo con la clave privada para firmar.
    required: true
    type: str
  signed_with:
    description:
      - Comando OpenSSL para firmar, puede ser "dgst" o "pkeyutl".
    required: false
    type: str
    choices: ['dgst', 'pkeyutl']
    default: 'dgst'
author:
  - John Freidman (@xploit9999)
'''

EXAMPLES = r'''
- name: Firmar un texto con sha256 usando dgst
  xploit9999.utilidades.openssl_sign:
    content: "Este es mi texto a firmar"
    algorithm: "sha256"
    privatekey: "/ruta/a/mi_key.pem"

- name: Firmar un archivo con sha512 usando pkeyutl
  xploit9999.utilidades.openssl_sign:
    path: "/ruta/a/archivo.txt"
    algorithm: "sha512"
    privatekey: "/ruta/a/mi_key.pem"
    signed_with: "pkeyutl"
'''

RETURN = r'''
signature:
  description: Firma generada en base64 URL-safe (sin signos +/=).
  type: str
  returned: success
changed:
  description: Si la operación realizó una firma
  type: bool
  returned: always
failed:
  description: Si el módulo falló
  type: bool
  returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess
import tempfile
import os
import json

def run_module():
    module_args = dict(
        content=dict(type='str', required=False, default=None),
        path=dict(type='str', required=False, default=None),
        algorithm=dict(type='str', required=True,
                       choices=['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'md5']),
        privatekey=dict(type='str', required=True),
        signed_with=dict(type='str', required=False, choices=['dgst', 'pkeyutl'], default='dgst'),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    content = module.params['content']
    path = module.params['path']
    algorithm = module.params['algorithm']
    privatekey = module.params['privatekey']
    signed_with = module.params['signed_with']

    if not content and not path:
        module.fail_json(msg="Debes proporcionar 'content' o 'path'.")
    if content and path:
        module.fail_json(msg="No puedes usar ambos: 'content' y 'path'.")

    script_dir = os.path.join(os.path.dirname(__file__), '../../bash_scripts')
    script_path = os.path.join(script_dir, 'openssl_sign.bash')

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as var_file:
        if content:
            var_file.write(f"content='{content}'\n")
        if path:
            var_file.write(f"path='{path}'\n")
        var_file.write(f"algorithm='{algorithm}'\n")
        var_file.write(f"privatekey='{privatekey}'\n")
        var_file.write(f"signed_with='{signed_with}'\n")
        var_file_path = var_file.name

    try:
        result = subprocess.run([script_path, var_file_path], capture_output=True, text=True, check=True)
        output_json = json.loads(result.stdout)
        os.unlink(var_file_path)

        if output_json.get("failed", False):
            module.fail_json(msg=output_json.get("msg", "Error desconocido"), **output_json)
        else:
            module.exit_json(**output_json)

    except subprocess.CalledProcessError as e:
        if os.path.exists(var_file_path):
            os.unlink(var_file_path)
        module.fail_json(msg="Error ejecutando openssl_sign.bash", stdout=e.stdout, stderr=e.stderr, rc=e.returncode)

def main():
    run_module()

if __name__ == '__main__':
    main()
