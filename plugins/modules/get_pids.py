#!/usr/bin/python
# -*- coding: utf-8 -*-
DOCUMENTATION = r'''
---
module: get_pids
short_description: Ejecuta get_pids.bash para obtener procesos
description:
  - Llama a un script bash para obtener IDs de procesos.
options:
  name:
    description: Nombre del proceso a buscar
    required: true
    type: str
author:
  - John (@Xploit9999)
'''

EXAMPLES = r'''
- name: Obtener pids de apache
  xploit9999.utilidades.get_pids:
    name: apache
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess
import os

def run_module():
    module_args = dict(
        name=dict(type='str', required=True)
    )

    module = AnsibleModule(argument_spec=module_args)

    script_dir = os.path.join(os.path.dirname(__file__), 'bash_scripts')
    script_path = os.path.join(script_dir, 'get_pids.bash')

    cmd = [script_path, module.params['name']]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        module.exit_json(changed=False, stdout=proc.stdout, stderr=proc.stderr)
    except subprocess.CalledProcessError as e:
        module.fail_json(msg='Error ejecutando get_pids.bash', stderr=e.stderr, stdout=e.stdout, rc=e.returncode)

def main():
    run_module()

if __name__ == '__main__':
    main()

