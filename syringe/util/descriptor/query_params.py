class QueryParams:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if "_query_cache" not in obj.__dict__:

            qs = obj._raw_path.partition("?")[2]
            obj.__dict__["_query_cache"] = (
                dict(pair.split("=", 1) for pair in qs.split("&") if "=" in pair)
                if qs
                else {}
            )
        return obj.__dict__["_query_cache"]
