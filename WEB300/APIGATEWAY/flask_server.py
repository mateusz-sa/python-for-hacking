from flask import Flask, request, jsonify
from urllib.parse import unquote

app = Flask(__name__, static_url_path='/static')

@app.route('/callback', methods=['GET'])
def callback():
    data = request.query_string.decode('utf-8')
    decoded_data = unquote(data)
    print(f"Received data: {decoded_data}")
    return "Data received", 200

@app.route('/error', methods=['GET'])
def error():
    error = request.query_string.decode('utf-8')
    decoded_error = unquote(error)
    print(f"Received error: {decoded_error}")
    return "Error received", 200

@app.route('/logs', methods=['POST'])
def receive_logs():
    log_data = request.json
    print(f"Received log data: {log_data}")
    # Przetworzenie otrzymanych danych logów, np. zapis do bazy danych, dalsza analiza, itp.
    return jsonify({"status": "Log received"}), 200

@app.route('/<path:path>', methods=['GET'])
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
