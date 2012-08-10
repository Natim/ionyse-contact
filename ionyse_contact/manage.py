#!/usr/bin/env python
try:
    import floppyforms
except ImportError:
    import sys
    print("\n    \033[1;31mN'oubliez pas d'activer votre virtualenv\n\n"
          "          $ source apps/bin/activate \033[0m\n")
    sys.exit(1)

from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    execute_manager(settings)
