class Headers:
    """Descriptor: parses headers only when first accessed."""

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if "_headers_cache" not in obj.__dict__:
            obj.__dict__["_headers_cache"] = self._parse(obj._raw)
        return obj.__dict__["_headers_cache"]

    def _parse(self, raw):
        lines = raw.split("\r\n")
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()
        return headers
