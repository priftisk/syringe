def make_response(body, status=200, content_type="text/html"):
    """Build a raw HTTP/1.1 response string."""
    status_text = {200: "OK", 404: "Not Found", 500: "Internal Server Error"}
    return (
        f"HTTP/1.1 {status} {status_text[status]}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        "\r\n" + body
    )


class Response:
    def __bytes__(self):
        pass
