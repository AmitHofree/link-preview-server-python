import json

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from link_preview import WebScraper

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/preview', methods=['GET'])
@cross_origin()
def get_preview():
    url = request.args.get('url', None)
    if url:
        w = WebScraper(url)
        preview_obj = w.getPreview()
        print("Done")
        return jsonify(preview_obj)
    else:
        return "Missing 'url' parameter", 400

if __name__ == "__main__":
    app.run('0.0.0.0', 8000)
