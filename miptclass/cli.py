#   encoding: utf8
#   cli.py

import click
import logging

from miptclass import models
from miptclass.miner import mine_reference_groups


@click.group()
def main():
    logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            level=logging.INFO)

@main.command(help='Run webserver.')
def webserver():
    pass

@main.command(help='Mine user profiles and groups from VK.')
def mine():
    mine_reference_groups(models.db)
