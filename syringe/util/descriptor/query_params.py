class QueryParams:
    def __get__(self, obj, objType=None):
        if obj is None:
            return self
        if "_query_params_cache" not in obj.__dict__:
            obj.__dict__["_query_params_cache"] = self._parse(obj.path)
        return obj.__dict__["_query_params_cache"]

    def _parse(self, raw_path: str):
        raw_params = raw_path.split("?")[1]
        dct = {}
        for raw_p in raw_params.split("&"):
            p_name, p_val = raw_p.split("=", 1)
            dct[p_name] = p_val
        return dct
