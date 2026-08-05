import http.server, socketserver, os, socket, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        rng = self.headers.get("Range")
        if rng: return self.serve_range(rng)
        return super().do_GET()
    def serve_range(self, rng):
        path = self.translate_path(self.path)
        if not os.path.isfile(path): self.send_error(404); return
        size = os.path.getsize(path)
        m = re.match(r"bytes=(\d*)-(\d*)", rng)
        start = int(m.group(1)) if m and m.group(1) else 0
        end = int(m.group(2)) if m and m.group(2) else size-1
        end = min(end, size-1); length = end-start+1
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(length)); self.end_headers()
        with open(path,"rb") as f:
            f.seek(start); rem=length
            while rem>0:
                c=f.read(min(65536,rem))
                if not c: break
                try: self.wfile.write(c)
                except (BrokenPipeError,ConnectionResetError): break
                rem-=len(c)
    def end_headers(self):
        self.send_header("Accept-Ranges","bytes"); super().end_headers()
    def log_message(self,*a): pass
class S(socketserver.ThreadingTCPServer):
    address_family=socket.AF_INET6; allow_reuse_address=True; daemon_threads=True
print("serving ~/spatial-web-demo on http://127.0.0.1:8778")
S(("::",8778),H).serve_forever()
