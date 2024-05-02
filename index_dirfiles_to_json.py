import os
import json

def run():
    basic_filters = ['.']
    jsons = {}
    for root, dirs, files in os.walk('.'):
        for dir in dirs.copy():
            for s in basic_filters:
                if dir.startswith(s):
                    dirs.remove(dir)
        with open(os.path.join(root, "index.json"),'w') as f:
            json.dump([dirs, files], f)
        jsons[root] = files
    with open('json_index.json', 'w') as f:
        json.dump(jsons, f)

if __name__ == "__main__":
    run()