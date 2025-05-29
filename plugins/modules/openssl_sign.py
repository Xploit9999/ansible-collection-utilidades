#!/usr/bin/env python3
# -*- coding: utf-8 -*-
DOCUMENTATION = r'''
---
module: openssl_sign
short_description: Firma contenido o archivos usando OpenSSL a través de un script bash.
description:
  - Este módulo permite firmar un texto o archivo usando el comando OpenSSL.
  - Soporta métodos de firma con "dgst" o "pkeyutl" y varios algoritmos hash.
  - Es un wrapper que llama a un script bash externo (openssl_sign.bash) que hace la firma.
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
  openssl_sign:
    content: "Este es mi texto a firmar"
    algorithm: "sha256"
    privatekey: "/ruta/a/mi_key.pem"

- name: Firmar un archivo con sha512 usando pkeyutl
  openssl_sign:
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
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess
import json
import tempfile
import os

def main():
    module = AnsibleModule(
        argument_spec=dict(
            content=dict(type='str', required=False, default=None),
            path=dict(type='str', required=False, default=None),
            algorithm=dict(type='str', required=True,
                           choices=['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'md5']),
            privatekey=dict(type='str', required=True),
            signed_with=dict(type='str', required=False, choices=['dgst', 'pkeyutl'], default='dgst'),
        ),
        supports_check_mode=False
    )

    params = {
        'content': module.params['content'],
        'path': module.params['path'],
        'algorithm': module.params['algorithm'],
        'privatekey': module.params['privatekey'],
        'signed_with': module.params['signed_with'],
    }

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tempf:
        for k, v in params.items():
            if v is not None:
                safe_val = v.replace('"', '\\"') if isinstance(v, str) else str(v)
                tempf.write(f'{k}="{safe_val}"\n')
        temp_file = tempf.name

    script_path = '/ruta/a/openssl_sign.bash'  # Cambia a la ruta real de tu script

    try:
        completed = subprocess.run(
            ['bash', script_path, temp_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    finally:
        os.unlink(temp_file)

    if completed.returncode != 0:
        module.fail_json(msg=f"Error ejecutando openssl_sign.bash: {completed.stderr.strip()}")

    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        module.fail_json(msg="Salida JSON inválida del script bash", raw_output=completed.stdout)

    if result.get('failed'):
        module.fail_json(msg=result.get('msg', 'Error desconocido en openssl_sign'))

    module.exit_json(changed=result.get('changed', False), signature=result.get('sig'))

if __name__ == '__main__':
    main()

