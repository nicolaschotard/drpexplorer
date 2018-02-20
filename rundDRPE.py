#!/usr/bin/env python
import sys

import explorer

from django.core.management import call_command
from django.utils import termcolors
from django import setup
setup()


def test_packages():
    """ """
    for p in ('numpy', 'scipy', 'matplotlib'):
        try:
            exec('import ' + p)
        except ImportError:
            print('Python package %s not found!' % p)
            sys.exit()


def run(**kwargs):
    """

    :param **kwargs: port and reload

    """
    print(termcolors.colorize('Launching server...', fg='green'))
    call_command('runserver', str(kwargs.get('port', 4242)),
                 use_reloader=kwargs.get('reload', False))

if __name__ == '__main__':

    from optparse import OptionParser, OptionGroup
    usage = '%prog [options]'
    parser = OptionParser(usage=usage)
    r = OptionGroup(parser, 'Run options')
    r.add_option('-p', '--port', type='int', default=1986,
                 help='Start server under localhost:port [%default]')
    parser.add_option_group(r)

    opts, args = parser.parse_args()

    # check python dependencies
    test_packages()
    run(port=opts.port)