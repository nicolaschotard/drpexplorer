#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
import subprocess

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
                 use_reloader=kwargs.get('reload', True))

if __name__ == '__main__':

    description = """Run the DRP explorer localy or from a distant host."""
    prog = "runDRPE.py"
    usage = """%s [options]""" % prog
    
    parser = ArgumentParser(prog=prog, usage=usage, description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    r = parser.add_argument_group('General', 'Run options')
    r.add_argument('-p', '--port', default=1986,
                   help='Start server under localhost:port')

    h = parser.add_argument_group('Host', 'Distant host options')
    h.add_argument('-H', "--host", default=None,
                   help="Name of the target host.")
    h.add_argument('-u', '--username',
                   help="Your user name on the host. If not given, ssh will try to "
                   "figure it out from you ~/.ssh/config or will use your local user name.")
    h.add_argument('-r', "--repo", default=None,
                   help="Path to your 'drpexplorer' repository.")
    h.add_argument('-C', '--compression', action='store_true', default=False,
                   help='Activate ssh compression option (-C).')
    args = parser.parse_args()

    # Run from a distant host
    if args.host is not None:
        args.username = "" if args.username is None else args.username + "@"

        # Start building the command line that will be launched on the host
        # Open the ssh tunnel to the host
        cmd = "ssh -X -Y %s -tt -L 20001:localhost:%i %s%s << EOF\n" % \
              ("-C" if args.compression else "", args.port, args.username, args.host)

        # Move to the working directory
        if args.repo is None:
            raise IOError("You must give the path to your install of 'drpexplorer'")
        cmd += "if [[ ! -d %s ]]; then echo 'Error: directory %s does not exist'; exit 1; fi\n" % \
               (args.repo, args.repo)
        cmd += "cd %s\n" % args.repo
            
        # Launch the explorer
        cmd += './runDRPE.py &\n'
        cmd += "printf '\\n    Copy/paste this URL into your browser to run the drp explorer" + \
               " localy \n\\x1B[01;92m       'http://localhost:20002/' \\x1B[0m\\n\\n'\n"

        # Go back to the server
        cmd += 'fg\n'

        # And make sure we can kill it properly
        cmd += "kill -9 `ps | grep jupyter | awk '{print $1}'`\n"

        # Close
        cmd += "EOF"

        # Run jupyter
        subprocess.call(cmd, stderr=subprocess.STDOUT, shell=True)
        
        
    # Run locally
    else:
        # check python dependencies
        test_packages()
        run(port=args.port)