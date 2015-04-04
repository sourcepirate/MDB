__author__ = 'plasmashadow'


class UrlError(Exception):
    pass


class UrlBuilder(object):
    def __init__(self, scheme=None, username=None, password=None, host=None, port=None, path=None):
        self.scheme = scheme
        self.password = password
        self.username = username
        self.host = host
        self.path = path
        self.port = port

    def _build_user_pass_string(self):
        if self.username and self.password:
            return ":".join([self.username, self.password])
        if self.username:
            return self.username
        else:
            return ""

    def _build_domain_port_string(self):
        if self.host and self.port:
            return ":".join([self.host, str(self.port)])
        if self.host:
            return self.host
        else:
            raise UrlError("Host parameter not specified")

    def _build_main_string(self):
        u_part = self._build_user_pass_string()
        h_part = self._build_domain_port_string()
        if u_part.count(":") and h_part.count(":"):
            return "@".join([u_part, h_part])
        if u_part.count(":"):
            return "@".join([u_part, h_part])

    def _build_url(self):
        if self.scheme:
            return "://".join([self.scheme, self._build_main_string()])
        raise UrlError("Scheme Not specified")

    def __str__(self):
        return "/".join([self._build_url(), ''])

