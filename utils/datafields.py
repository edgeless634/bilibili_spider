import os

import logging
import threading
base_path = os.path.dirname(os.path.dirname(__file__))
base_path = os.path.join(base_path, "datafield")


if not os.path.exists(base_path):
    os.mkdir(base_path)

def get_path(fieldname):
    return os.path.join(base_path, fieldname)

class DataField:
    def __init__(self):
        self.fields = set()
        self.field_cache = {}
        self.load_field()
        self.lock = threading.Lock()

    def load_field(self):
        for filename in os.listdir(base_path):
            if os.path.isfile(get_path(filename)):
                continue
            self.fields.add(filename)

    def new_field(self, fieldname):
        if fieldname in self.fields:
            return
        abs_path = get_path(fieldname)
        if not os.path.exists(abs_path):
            os.mkdir(abs_path)
        self.fields.add(fieldname)

    def load_field_data(self, fieldname):
        ret = []
        for root, _, files in os.walk(get_path(fieldname)):
            for file in files:
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    s = f.read()
                ret.append(s)
        return ret

    def get_field_data(self, fieldname):
        with self.lock:
            if fieldname not in self.field_cache or self.field_cache[fieldname] == []:
                self.field_cache[fieldname] = "\n".join(self.load_field_data(fieldname)).split("\n")
                self.field_cache[fieldname] = [i for i in self.field_cache[fieldname] if i != ""]

            if self.field_cache[fieldname] == []:
                return None
            
            ret = self.field_cache[fieldname].pop()
            return ret

    def save_to_field(self, fieldname, s, filename=None):
        if filename is None:
            for i in range(16, len(s)):
                filename = f"{s[:i].__hash__()}.txt"
                path = os.path.join(get_path(fieldname), filename)
                if not os.exist(path):
                    break
        else:
            path = os.path.join(get_path(fieldname), filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)


datafields = DataField()

if __name__ == '__main__':
    print(datafields.fields)
    print(datafields.get_field_data("up_mid"))
    print(datafields.get_field_data("up_mid"))
    print(datafields.get_field_data("up_mid"))