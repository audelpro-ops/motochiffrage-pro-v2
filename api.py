import sqlite3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class API(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect('moto.db')
        c = conn.cursor()

        if self.path == '/api/zones':
            c.execute("SELECT DISTINCT zone FROM zones WHERE modele='yamaha-r1'")
            zones = [row[0] for row in c.fetchall()]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(zones).encode())

        elif self.path.startswith('/api/pieces/'):
            zone = self.path.replace('/api/pieces/', '').replace('%20', ' ')
            c.execute("""SELECT p.ref, p.nom, p.prix
                        FROM pieces p
                        JOIN zones z ON p.zone_id = z.id
                        WHERE z.zone=? AND z.modele='yamaha-r1'""", (zone,))
            pieces = [{"ref": r[0], "nom": r[1], "prix": r[2]} for r in c.fetchall()]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(pieces).encode())

        elif self.path.startswith('/api/catalogue'):
            marque = self.path.split('marque=')[1] if 'marque=' in self.path else 'yamaha'
            c.execute("SELECT cylindree, annee, modele, url FROM catalogue WHERE marque=? ORDER BY cylindree+0, annee, modele", (marque,))
            modeles = [{"cylindree": r[0], "annee": r[1], "modele": r[2], "url": r[3]} for r in c.fetchall()]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(modeles).encode())

        conn.close()

    def log_message(self, format, *args):
        pass

print("API demarree sur port 8080")
HTTPServer(('localhost', 8080), API).serve_forever()
