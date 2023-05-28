import socket
import os

def create_http_response(content):
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n".encode(
        'utf-8')
    response += content
    return response

def handle_http_request(request):
    method, path, _ = request.split('\n')[0].split()
    path = path[1:]
    if path == "":
        path = "index.html"
    if method == "GET":
        if os.path.exists(path):
            with open(path, 'rb') as file:
                file_content = file.read()
            server_respone = "HTTP/1.1 200 OK\r\n"
            response = create_http_response(file_content)
        else:
            server_respone = "HTTP/1.1 404 Not Found"
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found".encode('utf-8')
        return server_respone, response
    else:
        # Metode HTTP yang tidak didukung
        server_respone = "HTTP/1.1 405 Method Not Allowed"
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod not allowed".encode('utf-8')
        return server_respone, response

def start_web_server():
    # Buat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket ke alamat dan port tertentu
    server_address = ('', 8080)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print('Web server telah dimulai di {}:{}'.format(server_address[0], server_address[1]))

    while True:
        # Terima koneksi dari client
        client_socket, client_address = server_socket.accept()
        print('Menerima koneksi dari: {}'.format(client_address))

        # Terima HTTP request dari client
        request = client_socket.recv(1024).decode('utf-8')

        # Tangani HTTP request dan buat HTTP response
        server_respone, response = handle_http_request(request)

        # Menampilkan detail Request, Path, dan Response dari Server
        method, req, protocol = request.split('\n')[0].split()
        filepath = os.path.join(os.getcwd(), request.split()[1][1:])
        print('Method   : {}'.format(method))
        print('Request  : {}'.format(req))
        print('Path     : {}'.format(filepath))
        print('Protocol : {}'.format(protocol))
        print('Respone  : {}\n'.format(server_respone))
        # Kirimkan HTTP response ke client
        client_socket.sendall(response)

        # Tutup koneksi dengan client
        client_socket.close()

if __name__ == '__main__':
    start_web_server()
