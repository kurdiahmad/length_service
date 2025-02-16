from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/length', methods=['POST'])
def string_length():
    input_data = request.get_data(as_text=True).strip()
    if not input_data:
        return "No input provided", 400
    
    return str(len(input_data))

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
