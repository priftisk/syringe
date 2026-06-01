import socket, time

num_requests = 8000
host = "127.0.0.1"
port = 9999
start = time.time()
for i in range(num_requests):
    try:
        s = socket.socket()
        s.connect((host, port))

        request = (
            "GET /articles HTTP/1.1\r\n"
            "Host: 127.0.0.1\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        s.sendall(request.encode())

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

        # print(f"Request {i+1}: {len(response)} bytes")

    except Exception as e:
        print(e)

    finally:
        s.close()
print(f"{(num_requests / (time.time() - start)):.0f} reqs/sec")
