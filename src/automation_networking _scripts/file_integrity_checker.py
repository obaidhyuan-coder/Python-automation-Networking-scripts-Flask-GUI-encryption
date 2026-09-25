import os
import hashlib
import json



def scan_path(folder = r"C:\Users\obaid\aes-project"):
  

        files = []
          
        for item in os.listdir(folder):
               full_path = os.path.join(folder, item)
       
               if os.path.isfile(full_path) and os.path.basename(full_path) != "baseline.json":
                   files.append(full_path)
       
        return files




def file_hash(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)

    return h.hexdigest()


def save_hash(folder, hash_store="baseline.json"):
    data = {}

    for file_path in scan_path(folder):
        data[file_path] = file_hash(file_path)

    with open(hash_store, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def file_compare(folder, baseline_file):
    current = {}
    for file_path in scan_path(folder):
        current[file_path] = file_hash(file_path)

    with open(baseline_file, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    for path, hash_value in current.items():
        if path not in baseline:
            print("added:", path)
        elif baseline[path] != hash_value:
            print("modified:", path)

    for path in baseline:
        if path not in current:
            print("deleted:", path)

def main():
    folder = r"C:\Users\obaid\aes-project"
    baseline = r"C:\Users\obaid\aes-project\baseline.json"

    if not os.path.exists(baseline):
        save_hash(folder, baseline)
       
    else:
        file_compare(folder, baseline)

if __name__== "__main__" :
    main()










