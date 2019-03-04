# -*- coding: utf-8 -*-

"""Console script for microrun."""
import asyncio
import logging
import os
import sys
from functools import update_wrapper

import click
import yaml

from microrun.main import MicroRun
from .servicerunner import MultiServiceManager

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.StreamHandler()
logging.basicConfig(level=LOGLEVEL, format=FORMAT)

pass_sm = click.make_pass_decorator(MicroRun)


@click.group()
@click.option('--config',
              default='microrun.yaml',
              type=click.Path(),
              help='microrun.yaml config file.')
@click.pass_context
def main(ctx, config):
    """Console script for microrun."""
    ctx.obj = MicroRun()
    with open(config, 'r') as stream:
        try:
            ctx.obj.config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


@main.command()
@pass_sm
def serve(sm):
    """Starts the microrun"""
    sm.setup()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(sm.run())
    loop.run_forever()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
