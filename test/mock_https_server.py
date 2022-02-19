#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import ssl
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from typing import Union, Optional

__all__ = ["always_respond_with", "with_https_server"]


def always_respond_with(response_body: Union[str, bytes], encoding: str = "utf8", content_type: str = "text/html"):
    if isinstance(response_body, str):
        response_body = response_body.encode(encoding)

    class HTTPResponseRepeater(BaseHTTPRequestHandler):
        def _send_headers(self):
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()

        def do_GET(self):
            self._send_headers()
            self.wfile.write(response_body)

        def do_POST(self):
            self._send_headers()
            self.wfile.write(response_body)

        def do_HEAD(self):
            self._send_headers()

    return HTTPResponseRepeater


def with_https_server(http_request_handler_class, cert_filename: str, key_filename: str, host: str = "localhost",
                      port: int = 8207):
    def decorator(func):
        def wrapper(*args, **kwargs):
            server_address = (host, port)
            httpd = ThreadingHTTPServer(server_address, http_request_handler_class)
            httpd.socket = ssl.wrap_socket(httpd.socket,
                                           server_side=True,
                                           certfile=cert_filename,
                                           keyfile=key_filename,
                                           ssl_version=ssl.PROTOCOL_TLS)
            serving_thread = threading.Thread(target=httpd.serve_forever, args=(0.1,))
            serving_thread.start()
            try:
                func(*args, **kwargs)
            except Exception as e:
                httpd.shutdown()
                serving_thread.join()
                raise e
            else:
                httpd.shutdown()
                serving_thread.join()

        return wrapper

    return decorator
