from importlib import import_module
from logbook import StreamHandler
from decouple import config
import click
import sys

try:
    import hupper
    HAVE_RELOADER = True

except ImportError:
    HAVE_RELOADER = False


@click.command()
@click.argument('name')
def main(name):
    if HAVE_RELOADER:
        print('Live reload enabled')
        hupper.start_reloader('sud.cli.service.main')

    debug = config('DEBUG', default=False, cast=bool)
    loglevel = config('LOGLEVEL', default='DEBUG' if debug else 'INFO').upper()

    with StreamHandler(sys.stdout, level=loglevel).applicationbound():
        module_name = 'sud.services.{0}.server'.format(name.replace('-', '_'))
        module = import_module(module_name)
        module.main()
