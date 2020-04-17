import os

from config.base import *

for name in list(locals()):
    if name in os.environ:
        locals().update({name: os.environ.get(name)})


def update_config_from_args(args):
    global HOST, PORT, DEBUG
    HOST = args.host
    PORT = args.port
    DEBUG = args.debug

# docker run --rm --name my-wallet-container -p 8080:8080 -e 'DEBUG=1' my-wallet --host 0.0.0.0