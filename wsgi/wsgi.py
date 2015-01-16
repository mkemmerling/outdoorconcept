#!/usr/bin/env python
import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()

def application(environ, start_response):

    ctype = 'text/plain'
    response_body = ['%s: %s' % (key, value)
                for key, value in sorted(environ.items())]
    response_body = '\n'.join(response_body)
    status = '200 OK'
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    #
    start_response(status, response_headers)
    return [response_body]
