# -*- coding: utf-8 -*-

"""Console script for servicerunner."""
import asyncio
from functools import update_wrapper
import sys
import click
import logging
import yaml
import os
from .servicerunner import ServiceManager

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.StreamHandler()
logging.basicConfig(level=LOGLEVEL, format=FORMAT)

pass_sm = click.make_pass_decorator(ServiceManager)


def coro(f):
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        except KeyboardInterrupt:
            raise
    return update_wrapper(wrapper, f)


@click.group()
@click.option('--config', default='servicerunner.yaml', type=click.Path(), help='servicerunner.yaml config file.')
@click.pass_context
def main(ctx, config):
    """Console script for servicerunner."""
    ctx.obj = ServiceManager()
    with open(config, 'r') as stream:
        try:
            ctx.obj.config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


@main.command()
@pass_sm
@coro
def serve(sm):
    """Starts the servicerunner"""
    try:
        yield from sm.serve()
    except KeyboardInterrupt:
        yield from sm.killall()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
