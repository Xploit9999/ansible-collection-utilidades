# `kill` Ansible Module

## Description

The `kill` module allows you to terminate a process by either its PID or its name using a specified signal. It ensures that the user has the necessary privileges to execute the command and provides feedback on the operation's success or failure.

## Options

| Parameter | Description                                                | Required | Type | Default |
|-----------|-----------------------------------------------------------|----------|------|---------|
| `process` | The PID or name of the process to kill.                   | Yes      | str  | None    |
| `signal`  | The signal to send to the process (e.g., SIGTERM, SIGKILL). | Yes      | str  | None    |

### Notes
- The module requires root privileges to terminate processes. The user must execute the playbook with appropriate permissions.
- Valid signals are typically represented as integers (e.g., 15 for SIGTERM, 9 for SIGKILL).
- The process can be specified either by its PID (numeric) or by its name (string).

## Usage Examples

### 1. Kill a process by PID
```yaml
- name: Kill a process by PID
  kill:
    process: "1234"
    signal: "9"
```
## Author

- **John Freidman** - [@Xploit9999](https://github.com/Xploit9999)
