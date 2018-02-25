"""
WSGI config for domectrl project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('d:/PROJECTS/_python/domectrl')
sys.path.append('d:/PROJECTS/_python/domectrl/domectrl')

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "domectrl.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "domectrl.settings"

# os.environ["wsgi.multiprocess"] = 'true'
# os.environ["wsgi.multithread"] = 'true'


application = get_wsgi_application()


# import pprint
# pprint.pprint(dict(os.environ.items()))

