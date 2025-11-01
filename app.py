from flask import Flask, request, jsonify, render_template
from qa_engine import answer_question
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('demo.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    q = request.json.get('question','')
    resp = answer_question(q)
    return jsonify(resp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
