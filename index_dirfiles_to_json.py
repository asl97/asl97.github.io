import os
import json

def run():
    jsons = {}
    for root, dirs, files in os.walk('.'):
        with open(os.path.join(root, "index.json"),'w') as f:
            json.dump(files, f)
        jsons[root] = files
    with open('json_index.json', 'w') as f:
        json.dump(jsons, f)

if __name__ == "__main__":
    run()