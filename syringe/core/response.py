from syringe.util.core import STATUS_TEXT


class Response:
    def __init__(self, body="", status=200, content_type="text/html; charset=utf-8"):
        self.body = body
        self.status = status
        self.content_type = content_type
        self.headers = {}

    def __bytes__(self) -> bytes:
        """Serialise to a complete HTTP/1.1 response."""
        body_bytes = self.body.encode("utf-8")
        status_line = (
            f"HTTP/1.1 {self.status} {STATUS_TEXT.get(self.status, 'Unknown')}"
        )
        base_headers = {
            "Content-Type": self.content_type,
            "Content-Length": str(len(body_bytes)),
        }
        all_headers = {**base_headers, **self.headers}
        header_block = "\r\n".join(f"{k}: {v}" for k, v in all_headers.items())
        preamble = f"{status_line}\r\n{header_block}\r\n\r\n".encode("utf-8")
        return preamble + body_bytes

    def __repr__(self):
        return f"<Response {self.status} {len(self.body)}b>"
