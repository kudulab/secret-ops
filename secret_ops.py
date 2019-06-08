import os
import hvac
import getpass
import logging
import click
import requests
import re
import fileinput
import glob

logger = logging.getLogger(__name__)

def get_vault_token():
    vault_token = os.environ.get('VAULT_TOKEN', None)
    if vault_token is not None:
        return vault_token
    else:
        logger.info('VAULT_TOKEN not set, trying load from file')
        with open(os.path.join(os.environ['HOME'], '.vault-token'), 'r') as myfile:
            return myfile.read()

def _create_vault_client():
    return hvac.Client(url='https://vault.kudulab.io:8200', verify='/usr/local/share/ca-certificates/ait.crt',
                token=get_vault_token())

def read_vault_kv(path):
    client = _create_vault_client()
    secret_response = client.read(path)
    if secret_response is None:
        raise ValueError('Failed to read secret at %s' % path)
    else:
        return secret_response['data']

def my_vault_username():
    user = getpass.getuser()
    if user == 'go':
        return 'gocd'
    return user

def read_my_gocd_password():
    user = my_vault_username()
    data = read_vault_kv('secret/%s/gocd_password' % user)
    return data['value']

def issue_vault_token(*args, **kwargs):
    client = _create_vault_client()
    return client.create_token(*args, **kwargs)


def gocd_encrypt(secret,server='go1'):
    """
    Encrypts secret with gocd server
    :param secret: secret to encrypt
    :param server: identifier of the GoCD server, either go1 or go2
    :return:
    """
    with requests.Session() as s:
        if server == 'go1' or server == 'kudu':
            url = 'https://go2-production.kudulab.io:8154'
            s.auth = (getpass.getuser(), read_my_gocd_password())
        else:
            raise ValueError('Invalid gocd server identifier, use go1')
        url = url + '/go/api/admin/encrypt'
        response = s.post(url, verify=False, headers={'Accept': 'application/vnd.go.cd.v1+json'}, json={ 'value': secret })
        if response.status_code != 200:
            raise ValueError("Failed to encrypt with GoCD, status code: %s, message %s" % (response.status_code, response.json()))
        return response.json()['encrypted_value']

def _replace_vault_token_line(line, token):
    return re.sub(r"(\s*VAULT_TOKEN:) .*", r'\1 "' + token + "\"", line)

def replace_vault_token(token, pattern='**/*.gocd.yaml'):
    for filepath in glob.glob(pattern):
        with fileinput.FileInput(filepath, inplace=True, backup='.bak') as file:
            for line in file:
                print(_replace_vault_token_line(line, token), end='')

# CLI for bash and existing tasks integration

@click.group()
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warn', 'error']), default='info')
@click.pass_context
def cli(ctx, log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logging.basicConfig(filename='secret_ops.log',
                        filemode='w',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=numeric_level)

@cli.command()  # @cli, not @click!
@click.pass_context
def vault_token(ctx):
    click.echo(get_vault_token())

@cli.command()  # @cli, not @click!
@click.pass_context
def my_gocd_password(ctx):
    click.echo(read_my_gocd_password())

@cli.command()  # @cli, not @click!
@click.option('--secret')
@click.option('--gocd-server', type=click.Choice(['go1', 'go2']), default='go1')
@click.pass_context
def encrypt_gocd(ctx, secret, gocd_server):
    click.echo(gocd_encrypt(secret, gocd_server))

if __name__ == "__main__":
    cli()
