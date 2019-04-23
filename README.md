# secret-ops

These are common functions to handle secrets using vault and GoCD.
This is published only as a reference, it will have little usability in other infrastructure.

## Usage

```bash
SECRET_OPS_VERSION="0.6.3"
SECRET_OPS_FILE="ops/secret-ops"
SECRET_OPS_TAR_FILE="ops/secret-ops-${SECRET_OPS_VERSION}.tar.gz"

mkdir -p ops
if [[ ! -f $SECRET_OPS_TAR_FILE ]];then
  wget --quiet -O $SECRET_OPS_TAR_FILE https://github.com/kudulab/secret-ops/releases/download/${SECRET_OPS_VERSION}/secret-ops.tar.gz
  tar -xf $SECRET_OPS_TAR_FILE -C ops
fi
source $SECRET_OPS_FILE
```

### encrypt_with_gocd_top

```
$ secured_token_gocd=$(secret_ops::encrypt_with_gocd_top "${secret_value}")
$ echo ${secured_token_gocd}
"+D6rVPSCLOroDzMVXgumeOoOO3dphWdK"
```

Asks GoCD server to encrypt a string.

### generate_certs_token

```
secret_ops::generate_certs_token_gocd_top
```

*No arguments*

Generates token for gocd to use for generating certificates.

### insert_vault_token_gocd_yaml

```
secret_ops::insert_vault_token_gocd_yaml "${secured_token_gocd}"
```

Puts previously generated and secured vault token "${secured_token_gocd}" into gocd.yaml files.

It expects that our pipeline should have secure_variables with `VAULT_TOKEN`:
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

Python script may only depend on packages specified by [ops-base](https://github.com/kudulab/ops-base).

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
      ;;
```
And use `tasks.py` to implement remaining tasks in python (this repository is an example of such setup)
```python
#!/usr/bin/env python3

import logging
import sys
import click

from ops.secret_ops import *

# Tasks using Click ...
```

## License

Copyright 2019 Ewa Czechowska, Tomasz Sętkowski

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
