import json

class ToJSON:

    @staticmethod
    def save_json_output(data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\nData saved in: {filename}")