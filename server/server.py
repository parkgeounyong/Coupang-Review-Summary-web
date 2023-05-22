from flask import Flask, jsonify, request, render_template
from main import *

app = Flask(__name__, static_folder='../web', static_url_path='/')

@app.route('/process_url', methods=['POST'])
def process_url():
    data = request.json
    url = data['url']
    # 여기서 파이썬 코드로 URL 처리를 수행합니다.
    result = make_summary(url)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run()
