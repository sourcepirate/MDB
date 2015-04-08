__author__ = 'plasmashadow'


class UrlError(Exception):
    pass


class UrlBuilder(object):
    def __init__(self, scheme=None, username=None, password=None, host=None, port=None, path=None, database=None):
        self.scheme = scheme
        self.password = password
        self.username = username
        self.host = host
        self.path = path
        self.port = port
        self.database = database

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
        if u_part:
            return "@".join([u_part, h_part])
        else:
            return h_part

    def _build_url(self):
        if self.scheme:
            return "://".join([self.scheme, self._build_main_string()])
        raise UrlError("Scheme Not specified")

    def _build(self):
        if self.database:
            return "/".join([self._build_url(), self.database])

    def __str__(self):
        return "/".join([self._build(), ''])


class UrlBuilder2(object):
    """
    Implementation of UrlBuilder using descriptors
    """
    @property
    def scheme(self):
        return self.scheme

    @scheme.setter
    def scheme(self, value):
        if not value or not isinstance(value, str):
            raise UrlError("scheme value cannot be empty or invalid")
        self.scheme = value

    @property
    def host(self):
        return self.hostname, self.port

    @host.setter
    def host(self, value):
        if not value or not isinstance(value, tuple):
            raise UrlError("host value cannot be empty or invalid")
        self.hostname = value[0]
        self.port = value[1]

    @property
    def credentials(self):
        return self.username, self.password

    @credentials.setter
    def credentials(self, tup):
        if type(tup) is tuple and isinstance(tup[0],str) and isinstance(tup[1],str):
             raise UrlError("Invalid creditals refer type")
        self.username = tup[0]
        self.password = tup[1]

    def _build_user_pass_string(self):
        if self.username and self.password:
            return ":".join([self.username, self.password])
        if self.username:
            return self.username
        else:
            return ""

    def _build_domain_port_string(self):
        if self.hostname and self.port:
            return ":".join([self.hostname, str(self.port)])
        if self.hostname:
            return self.hostname
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





