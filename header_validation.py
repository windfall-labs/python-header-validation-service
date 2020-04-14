import dkim
import array
from cgi import FieldStorage

def app(environ, start_response):
    try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
      request_body_size = 0

    form = FieldStorage(fp=environ['wsgi.input'], environ=environ)

    eml = form["eml"].value.encode('utf8')

    cv, results, comment = dkim.arc_verify(eml)

    arc = "arc verification: cv=%s %s" % (cv, comment)
    dkimz = ""
    res = dkim.verify(eml)
    if not res:
      dkimz = "signature verification failed"
    else:
      dkimz = "signature ok"
    
    message = arc + "\n" + dkimz
    b = message.encode('ascii')

    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(message)))
    ]
    
    start_response(status, response_headers)
    return iter([b])