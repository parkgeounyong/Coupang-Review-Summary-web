from flask import Flask, jsonify, request, render_template
import os
from main import *

#http://ip주소/html/chat.html로 접속
app = Flask(__name__, static_folder='./tampaltes', static_url_path='/')

@app.route('/process_url', methods=['POST'])
def process_url():
    data = request.json
    url = data['url']
    # 여기서 파이썬 코드로 URL 처리를 수행합니다.
    result = make_summary(url)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run()
