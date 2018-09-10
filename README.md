# secret-ops

## Usage

```
if [[ ! -f ./secret-ops ]]; then
  wget --quiet http://os2.ai-traders.com:6780/swift/v1/secret-ops/0.3.1/secret-ops || { echo "cannot download secret-ops"; }
fi
source ./secret-ops
```

### encrypt_with_gocd

```
$ encrypt_with_gocd "my-secret-password"
$ echo ${secured_value}
"+D6rVPSCLOroDzMVXgumeOoOO3dphWdK"
```

Asks GoCD server to encrypt a string.

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

# setup-kube

`setup-kube` is a script that will configure current host to have access to k8s.
Usage:
```
./setup-kube k8s-user-name
```
You need:
 - vault binary
 - sufficient permissions to vault and ~/.vault-token
 - trust ait CA

The script provisions:
 - `~/.kube/${k8s_user}`
 - `~/.kube/${k8s_user}.crt`
 - `~/.kube/ca.crt`
 - `~/.kube/config`
