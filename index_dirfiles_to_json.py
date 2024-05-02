import os
import json

def run():
    basic_filters = ['.']
    jsons = {}
    with open('json_index.json', 'w') as json_index:
        for root, dirs, files in os.walk('.'):
            for dir in dirs.copy():
                for s in basic_filters:
                    if dir.startswith(s):
                        dirs.remove(dir)
            paths = [dirs, files]
            with open(os.path.join(root, "index.json"),'w') as f:
                json.dump(paths, f)
            jsons[root] = paths

        json.dump(jsons, json_index)

if __name__ == "__main__":
    run()