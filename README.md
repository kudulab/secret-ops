# secret-ops

## Usage

```
if [[ ! -f ./secret-ops ]]; then
  wget --quiet http://os2.ai-traders.com:6780/swift/v1/secret-ops/0.1.0/secret-ops || { echo "cannot download secret-ops"; }
fi
source ./secret-ops
```

### generate_certs_token

```
generate_certs_token
```

*No arguments*

Generates token for gocd to use for generating certificates.

### insert_vault_token_gocd_yaml

```
insert_vault_token_gocd_yaml
```

*No arguments*

Puts previously generated and secuted vault token into gocd.yaml files.

**Remarks:** It is meant to be used right after `generate_certs_token`:
```
generate_certs_token
insert_vault_token_gocd_yaml
```

And your pipeline should have secure_variables at some point:
```yaml
secure_variables:
  VAULT_TOKEN: "will-be-replaced"
```
