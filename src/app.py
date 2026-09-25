from flask import Flask, jsonify, request
from pathlib import Path
from automation.backup import build_backup,rotate_backups


app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(
        message="AES Project Flask app is running",
        status="ready",
        routes=["/health", "/backup"],
    )

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/backup", methods=["POST"])
def backup():
    payload = request.get_json(silent=True) or {}
    source = payload.get("src")
    dest = payload.get("dest")
    keep = payload.get("keep", 7)

    if not source or not dest:
            return jsonify(error="Missing required fields: src and dest"), 400 

    src_path= Path(source)
    dest_path = Path(dest)

    try:
        build_backup(src_path,dest_path)
        rotate_backups(dest_path,keep)
    except Exception as e:
        return jsonify(error= "Missing src-path,dest_path"), 400
      
   
    return jsonify(
        message ="Backup complete",
        source = str(src_path),
        dest = str(dest_path),
        keep = keep,
        

    )
    

    
                    
                    
  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
