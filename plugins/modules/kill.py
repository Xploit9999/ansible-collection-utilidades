#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: kill
short_description: Kill a process by PID or name using a specified signal
description:
  - This module allows you to kill a process by either its PID or its name using a specified signal.
options:
  process:
    description:
      - The PID or name of the process to kill.
    required: true
    type: str
  signal:
    description:
      - The signal to send to the process.
    required: true
    type: str
author:
  - John Freidman (@Xploit9999)
'''

EXAMPLES = r'''
- name: Kill a process by name
  xploit9999.utilidades.kill:
    process: apache2
    signal: 9
'''

RETURN = r'''
msg:
  description: Message indicating success or failure
  type: str
  returned: always
changed:
  description: Whether the kill action was performed
  type: bool
  returned: always
failed:
  description: Whether the action failed
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
        process=dict(type='str', required=True),
        signal=dict(type='str', required=True),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    process = module.params['process']
    signal = module.params['signal']

    script_dir = os.path.join(os.path.dirname(__file__), 'bash_scripts')
    script_path = os.path.join(script_dir, 'kill.bash')

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as var_file:
        var_file.write(f"process='{process}'\nsignal='{signal}'\n")
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
        module.fail_json(msg="Error ejecutando kill.bash", stdout=e.stdout, stderr=e.stderr, rc=e.returncode)

def main():
    run_module()

if __name__ == '__main__':
    main()

