# Ansible Module: openssl_sign

## Description
The `openssl_sign` module allows you to sign a text string or file using a specified hashing algorithm and private key with OpenSSL. It supports two signing methods: `dgst` and `pkeyutl`, and outputs the signature in base64 format.

## Options

### `content`
- **Description**: A string of text to sign.
  - Must be provided as plain text and not as a file path.
- **Required**: No
- **Type**: `str`

### `path`
- **Description**: The path to a file containing content to sign.
  - Cannot be used at the same time as `content`.
- **Required**: No
- **Type**: `str`

### `algorithm`
- **Description**: The hashing algorithm to use for signing.
  - Supported algorithms are `sha1`, `sha224`, `sha256`, `sha384`, `sha512`, and `md5`.
- **Required**: Yes
- **Type**: `str`

### `privatekey`
- **Description**: Path to the private key file used for signing.
- **Required**: Yes
- **Type**: `str`

### `signed_with`
- **Description**: The OpenSSL command to use for signing.
  - Accepts either `dgst` or `pkeyutl`. Defaults to `dgst`.
- **Required**: No
- **Type**: `str`
- **Choices**: [ `dgst`, `pkeyutl` ]
- **Default**: `dgst`

## Notes
- Either `content` or `path` must be provided for signing, but not both.
- The module requires OpenSSL to be installed on the target machine.
- This module only performs a signing operation and does not change the system state.

## Examples

### Sign a string with sha256 using dgst
```yaml
  - name: Sign a string with sha256 using dgst
    openssl_sign:
      content: "This is my content to sign"
      algorithm: "sha256"
      privatekey: "/path/to/private_key.pem"
```

## Author

- **John Freidman** - [@Xploit9999](https://github.com/Xploit9999)