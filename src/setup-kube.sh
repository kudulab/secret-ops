#!/bin/bash
set -e

k8s_user="$1"
if [ -z "${k8s_user}" ]; then
  echo "Must specify k8s user name"
  exit 1
fi

mkdir -p ~/.kube

export VAULT_ADDR="${VAULT_ADDR:-https://vault.ai-traders.com:8200}"

vault kv get --field=key "secret/k8s/${k8s_user}" > ~/.kube/${k8s_user}.key
vault kv get --field=user_crt "secret/k8s/${k8s_user}" > ~/.kube/${k8s_user}.crt
vault kv get --field=ca "secret/k8s/${k8s_user}" > ~/.kube/ca.crt

chmod -c 0600 ~/.kube/${k8s_user}.key

cat << EOF > ~/.kube/config
apiVersion: v1
kind: Config
preferences: {}

clusters:
- name: default-cluster
  cluster:
    server: https://k8s2.ai-traders.com:6443
    certificate-authority: $HOME/.kube/ca.crt
users:
- name: ${k8s_user}
  user:
    client-certificate: $HOME/.kube/${k8s_user}.crt
    client-key: $HOME/.kube/${k8s_user}.key

contexts:
- name: default-context
  context:
    cluster: default-cluster
    user: ${k8s_user}

current-context: default-context
EOF
