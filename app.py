from flask import Flask, render_template, request, jsonify
from organizer import FileOrganizer
import threading
import os

app = Flask(__name__)

# Global organizer instance
organizer_instance = None


@app.route("/", methods=["GET", "POST"])
def home():
    global organizer_instance
    message = ""

    if request.method == "POST":
        path = request.form.get("path")
        dry_run = request.form.get("dry_run") == "on"

        # Handle invalid path
        if not os.path.exists(path):
            message = "❌ Invalid Path!"
            return render_template("index.html", message=message)

        try:
            # Create organizer instance
            organizer_instance = FileOrganizer(path, dry_run=dry_run)

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
    