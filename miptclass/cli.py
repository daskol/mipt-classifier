#   encoding: utf8
#   cli.py

import click
import logging

from miptclass import models
from miptclass.miner import mine_reference_groups


def init_app(app):
    cmds = app.cli.command()
    for cmd in (syncdb, mine):
        cmds(cmd)

def syncdb():
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    engine = models.db.get_bind()
    models.Base.metadata.create_all(engine)

def mine():
    logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            level=logging.INFO)

    mine_reference_groups(models.db)
