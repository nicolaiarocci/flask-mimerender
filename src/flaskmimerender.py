"""
Python module for RESTful resource representation using MIME Media-Types
This is a Flask port from the excellent mimerender v0.2.3 by Martin Blech
(http://code.google.com/p/mimerender/)
"""

__version__ = '0.1.2'
__author__ = 'Nicola Iarocci <nicola@nicolaiarocci.com>'
__license__ = 'MIT'
__copyright__ = '2012 Nicola Iarocci'

from flask import request, make_response
from functools import wraps

XML = 'xml'
JSON = 'json'
YAML = 'yaml'
XHTML = 'xhtml'
HTML = 'html'
TXT = 'txt'
CSV = 'csv'
TSV = 'tsv'
RSS = 'rss'
RDF = 'rdf'
ATOM = 'atom'
M3U = 'm3u'
PLS = 'pls'
XSPF = 'xspf'
ICAL = 'ical'
KML = 'kml'
KMZ = 'kmz'

_MIME_TYPES = {
    JSON:  ('application/json',),
    XML:   ('application/xml', 'text/xml', 'application/x-xml',),
    YAML:  ('application/x-yaml', 'text/yaml',),
    XHTML: ('application/xhtml+xml',),
    HTML:  ('text/html',),
    TXT:   ('text/plain',),
    CSV:   ('text/csv',),
    TSV:   ('text/tab-separated-values',),
    RSS:   ('application/rss+xml',),
    RDF:   ('application/rdf+xml',),
    ATOM:  ('application/atom+xml',),
    M3U:   ('audio/x-mpegurl', 'application/x-winamp-playlist',
            'audio/mpeg-url', 'audio/mpegurl',),
    PLS:   ('audio/x-scpls',),
    XSPF:  ('application/xspf+xml',),
    ICAL:  ('text/calendar',),
    KML:   ('application/vnd.google-earth.kml+xml',),
    KMZ:   ('application/vnd.google-earth.kmz',),
}


def register_mime(shortname, mime_types):
    """
    Register a new mime type.
    Usage example:
    After this you can do:
        mimerender.register_mime('svg', ('application/x-svg', 'application/svg+xml',))
        @mimerender.mimerender(svg=render_svg)
        def GET(...
            ...
    """
    if shortname in _MIME_TYPES:
        raise MimeRenderException('"%s" has already been registered' %
                                  shortname)
    _MIME_TYPES[shortname] = mime_types


class MimeRenderException(Exception):
    pass


def _get_mime_types(shortname):
    try:
        return _MIME_TYPES[shortname]
    except KeyError:
        raise MimeRenderException('No mime type for shortname "%s"' %
                                  shortname)


def _get_short_mime(mime):
    for shortmime, mimes in _MIME_TYPES.items():
        if mime in mimes:
            return shortmime
    raise MimeRenderException('No short mime for type "%s"' % mime)


def _best_mime(supported):
    return request.accept_mimetypes.best_match(supported)

global_default = None
global_override_arg_idx = None
global_override_input_key = None
global_charset = None


def mimerender(default=None, override_arg_idx=None, override_input_key=None,

               charset=None, **renderers):
    """
    Usage:
        @mimerender(default='xml', override_arg_idx=-1, override_input_key='format', , <renderers>)
        GET(self, ...) (or POST, etc.)

    The decorated function must return a dict with the objects necessary to
    render the final result to the user. The selected renderer will be called
    with the map contents as keyword arguments.
    If override_arg_idx isn't None, the wrapped function's positional argument
    at that index will be removed and used instead of the Accept header.
    override_input_key works the same way, but with web.input().

    Example:
    class greet:
        @mimerender.mimerender(
            default = 'xml',
            override_arg_idx = -1,
            override_input_key = 'format',
            html    = render_html,
            xml     = render_xml,
            json    = json_render,
            yaml    = json_render,
            txt     = json_render,
        )
        def GET(self, param):
            message = 'Hello, %s!'%param
            return {'message':message}
    """
    def get_renderer(mime):
        try:
            return renderer_dict[mime]
        except KeyError:
            raise MimeRenderException('No renderer for mime "%s"' % mime)

    if not default:
        default = global_default
    if not override_arg_idx:
        override_arg_idx = global_override_arg_idx
    if not override_input_key:
        override_input_key = global_override_input_key
    if not charset:
        charset = global_charset

    supported = list()
    renderer_dict = dict()
    for shortname, renderer in renderers.items():
        for mime in _get_mime_types(shortname):
            supported.append(mime)
            renderer_dict[mime] = renderer
    if default:
        default_mime = _get_mime_types(default)[0]
        default_renderer = get_renderer(default_mime)

    else:
        default_mime, default_renderer = renderer_dict.items()[0]

    def wrap(target):
        @wraps(target)
        def wrapper(*args, **kwargs):
            mime = None
            shortmime = None
            if override_arg_idx != None:
                shortmime = args[override_arg_idx]
            if not shortmime and override_input_key and \
                    override_input_key in request.args.keys():
                shortmime = request.args[override_input_key]
            if shortmime:
                mime = _get_mime_types(shortmime)[0]
            if not mime:
                mime = _best_mime(supported)
            if mime:
                renderer = get_renderer(mime)
            else:
                mime, renderer = default_mime, default_renderer
            if not shortmime:
                shortmime = _get_short_mime(mime)
            result, status = target(*args, **kwargs)
            resp = make_response(renderer(**result), status)
            resp.mimetype = mime
            resp.charset = charset
            return resp
        return wrapper

    return wrap

if __name__ == "__main__":
    import unittest

    class TestMimeRender(unittest.TestCase):
        pass

    unittest.main()
