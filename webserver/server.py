from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def serve_html():
    return send_file('sreality.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)