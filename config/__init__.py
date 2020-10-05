import os

from config.base import *  # noqa

for name in list(locals()):
    if name in os.environ:
        locals().update({name: os.environ.get(name)})


def update_config_from_args(args):
    pass
