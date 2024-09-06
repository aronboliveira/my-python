import json
import os
def main():
    json_file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    print(json.dumps(data))
if __name__ == "__main__":
    main()