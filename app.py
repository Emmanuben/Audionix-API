import os
import tempfile
import shutil
from flask import Flask, request, send_file, jsonify
from spotdl import Spotdl
from spotdl.utils.config import DEFAULT_CONFIG
from datetime import datetime

app = Flask(__name__)
spotdl = Spotdl(DEFAULT_CONFIG)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Audionix API is running"}), 200

@app.route("/download", methods=["POST"])
def download_zip():
    data = request.get_json()
    playlist_url = data.get("url")

    if not playlist_url:
        return jsonify({"error": "Missing playlist URL"}), 400

    try:
        temp_dir = tempfile.mkdtemp()
        os.chdir(temp_dir)

        spotdl.download(playlist_url)

        zip_name = f"audionix_playlist_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
        zip_path = shutil.make_archive(zip_name.replace(".zip", ""), 'zip', temp_dir)

        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    app.run(debug=True)
