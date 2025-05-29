# `get_pids` Ansible Module

## Description

The `get_pids` module allows you to retrieve process IDs (PIDs) based on the user who owns the process or by the process name. It supports case-insensitive searches and outputs the PIDs in JSON format.

### Features
- Retrieve PIDs by process name or by username.
- Supports case-insensitive searches.
- Outputs PIDs in JSON format.

## Options

| Parameter    | Description                                                                 | Required | Type  | Default |
|--------------|-----------------------------------------------------------------------------|----------|-------|---------|
| `by_user`    | The username for which you want to retrieve the processes.                  | No       | str   | None    |
| `by_name`    | The name of the process to search for.                                      | No       | str   | None    |
| `ignore_case`| Set this to `true` to perform a case-insensitive search.                    | No       | bool  | `false` |

### Notes
- Either `by_user` or `by_name` must be provided. If neither is provided, the module will fail.
- The `ignore_case` option defaults to `false`, meaning the search is case-sensitive unless specified otherwise.
- This module does not change the state of the system but retrieves process information.

## Usage Examples

### 1. Retrieve PIDs by username
```yaml
- name: Retrieve PIDs by username
  get_pids:
    by_user: "john"
```

### 2. Retrieve PIDs by process name
```yaml
- name: Retrieve PIDs by process name
  get_pids:
    by_name: "bash"
```

### 3. Case-insensitive search by process name
```yaml
- name: Case-insensitive search by process name
  get_pids:
    by_name: "BASH"
    ignore_case: true
```

### 4. Case-insensitive search by username
```yaml
- name: Retrieve PIDs by username, case-insensitive
  get_pids:
    by_user: "JOHN"
    ignore_case: true
```

## Author

- **John Freidman** - [@Xploit9999](https://github.com/Xploit9999)

