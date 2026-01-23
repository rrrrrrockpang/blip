from http.server import BaseHTTPRequestHandler
import subprocess

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            result = subprocess.run(['python3', 'app/_0overall.py'], 
                                  capture_output=True, text=True, cwd='/var/task')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Success: {result.stdout}'.encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())