from flask import Flask, render_template, request, jsonify
from organizer import FileOrganizer
import threading
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload folder setup
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Global organizer instance
organizer_instance = None


@app.route("/", methods=["GET", "POST"])
def home():
    global organizer_instance
    message = ""

    if request.method == "POST":
        files = request.files.getlist("files")
        dry_run = request.form.get("dry_run") == "on"

        # Check if files selected
        if not files or files[0].filename == "":
            message = "❌ No files selected!"
            return render_template("index.html", message=message)

        try:
            # Clear old files (optional but recommended)
            for f in os.listdir(UPLOAD_FOLDER):
                os.remove(os.path.join(UPLOAD_FOLDER, f))

            # Save uploaded files
            for file in files:
                if file:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            # Create organizer instance using upload folder
            organizer_instance = FileOrganizer(UPLOAD_FOLDER, dry_run=dry_run)

            # Run in background thread
            thread = threading.Thread(target=organizer_instance.organize)
            thread.start()

            message = "🚀 Organization Started..."

        except Exception as e:
            message = f"❌ Error: {str(e)}"

    return render_template("index.html", message=message)


# API for real-time status
@app.route("/status")
def status():
    global organizer_instance

    if organizer_instance:
        return jsonify({
            "progress": organizer_instance.progress,
            "logs": organizer_instance.logs[-10:],  # last 10 logs
            "error": organizer_instance.error
        })

    return jsonify({
        "progress": 0,
        "logs": [],
        "error": None
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)