import os
import sys

# django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'drpexplorer.settings'

# extract django when runing the first time
django_version = 'Django-2.0.2'
ppath = os.path.join(os.path.dirname(__file__), 'static/python/')
if not os.path.exists(ppath+django_version):
    import tarfile
    t = tarfile.open(ppath + django_version+'.tgz')
    t.extractall(path=ppath)
    t.close()

# add django and other library to the python path
sys.path.insert(0, ppath+django_version)
sys.path.insert(0, ppath)

# extract js9 the first time we run
js9_version = 'js9-2.0.2'
spath = os.path.join(os.path.dirname(__file__), 'static/')
if not os.path.exists(spath + js9_version):
    # extract js9
    import tarfile
    t = tarfile.open(spath + js9_version+'.tar.gz')
    t.extractall(path=spath)
    t.close()
    # create a sym link to this version of js9
    if os.path.islink(spath + 'js9'):
        os.remove(spath + 'js9')
    os.symlink(spath + js9_version, spath + 'js9')

# Create a links directory the first time we run
links_path = os.path.join(os.path.dirname(__file__), 'links')
if not os.path.isdir(links_path):
    os.mkdir(links_path)

__all__ = ['explorer', 'butler', 'db']
