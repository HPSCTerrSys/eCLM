import setuptools
import site, sys

exec(open('clm5nl/_version.py').read())
if "--user" in sys.argv[1:]:
    # Enables --editable install with --user
    # https://github.com/pypa/pip/issues/7953#issuecomment-645133255
    site.ENABLE_USER_SITE = True
    __version__ += ".dev"

setuptools.setup(version = __version__)