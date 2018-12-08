# secret-ops

## Usage

```
if [[ ! -f ./secret-ops ]]; then
  wget --quiet http://os2.ai-traders.com:6780/swift/v1/secret-ops/0.4.0/secret-ops || { echo "cannot download secret-ops"; }
fi
if [[ ! -f ./secret_ops.py ]]; then
  wget --quiet http://os2.ai-traders.com:6780/swift/v1/secret-ops/0.4.0/secret_ops.py || { echo "cannot download secret_ops.py"; }
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

# Python

Python is in preview to see if it works better for scripting than bash.
To provide compatibility with bash and existing tasks, there is a CLI mode which allows to use `secret_ops.py`
also from command line. To see usage just run
```bash
python3 secret_ops.py
```

Python script may only depend on packages specified by http://gogs.ai-traders.com/platform/python-ops

By default logging is redirected to `secret_ops.log` so that output of commands can be captured with bash.
You can change log level in any command with `--log-level`, e.g.
```bash
python3 secret_ops.py --log-level debug encrypt-gocd --secret a --gocd-server go1
```

Example of mixed usage:
```bash
vault_token=$(vault token create -renewable=true -period=78h -policy=gocd -field token)
secured_token_gocd=$(python3 secret_ops.py encrypt-gocd --secret "${vault_token}" --gocd-server go1)
```

For full python usage I recommend following construct in `tasks`:
```bash
  *)
      python3 tasks.py "$@"
      exit $?
      ;;
```
And use `tasks.py` to implement remaining tasks in python (this repository is an example of such setup)
```python
#!/usr/bin/env python3

import logging
import sys
import click

import secret_ops

# Tasks using Click ...
```
