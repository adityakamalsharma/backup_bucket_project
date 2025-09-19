import os
import time
from flask import Flask, send_from_directory, abort

app = Flask(__name__)

# Directory where backups are stored
BACKUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backups'))

@app.route('/')
def index():
    return "<h1>Backup Server</h1><p>Try to find the secrets backup at /backups/&lt;id&gt;</p>", 200

@app.route('/backups/<int:backup_id>')
def get_backup(backup_id):
    """
    Serves a backup file based on its ID.
    This is the vulnerable endpoint.
    """
    # Optional delay to slow down brute-forcing
    time.sleep(0.2)
    
    try:
        filename = f"backup{backup_id}.tar.gz"
        
        # Security check: Ensure filename is safe (though int conversion helps)
        if not filename.startswith('backup') or '..' in filename:
            abort(400, "Invalid filename.")
        
        # Check if file exists before attempting to send
        if not os.path.exists(os.path.join(BACKUP_DIR, filename)):
            abort(404, "Backup ID not found.")

        return send_from_directory(
            directory=BACKUP_DIR,
            path=filename,
            as_attachment=True
        )

    except (ValueError, FileNotFoundError):
        abort(404, "Backup ID not found.")

if __name__ == '__main__':
    # Note: For production, use a proper WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=False)