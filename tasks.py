#!/usr/bin/env python3

import logging
import sys
import click

import secret_ops

@click.group()
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warn', 'error']), default='info')
@click.pass_context
def cli(ctx, log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    root = logging.getLogger()
    root.setLevel(numeric_level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(numeric_level)
    formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

@cli.command()  # @cli, not @click!
@click.pass_context
def issue_vault_token(ctx):
    token = secret_ops.issue_vault_token(ttl='78h', policies=['gocd'])
    encrypted = secret_ops.gocd_encrypt(token['auth']['client_token'])
    secret_ops.replace_vault_token(encrypted)

if __name__ == "__main__":
    cli()