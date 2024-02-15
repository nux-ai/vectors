from flask import Flask, request, jsonify
from host import Host

app = Flask(__name__)
host_instance = Host("models.json")  # Ensure this path is correct


@app.route('/get_embedding', methods=['POST'])
def embedding_endpoint():
    data = request.json
    text = data.get('text', '')
    if text:
        embedding = host_instance.get_embedding(text)
        return jsonify({"embedding": embedding.tolist()})
    else:
        return jsonify({"error": "Text is required."}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
