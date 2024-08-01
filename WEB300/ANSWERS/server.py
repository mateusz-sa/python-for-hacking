from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/get-data', methods=['GET'])
def get_data():
    # Pobierz dane z zapytania GET
    data = request.args
    return jsonify(data)

@app.route('/post-data', methods=['POST'])
def post_data():
    # Pobierz dane z zapytania POST
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)