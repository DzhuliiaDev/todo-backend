import json
import os
from typing import List
#from resources import Entry

class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    @classmethod
    def from_json(cls, value):
        new_entry = cls(value['title'])
        for sub_entry in value.get('entries', []):
            new_entry.add_entry(Entry.from_json(sub_entry))
        return new_entry

    def save(self, path):
        filepath = os.path.join(path, f"{self.title}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.json(), f, ensure_ascii=False, indent=4)
        print(f"Файл сохранён: {filepath}")

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
            return cls.from_json(content)

class EntryManager:
    def __init__(self, data_path: str):
        self.data_path: str = data_path
        self.entries: List[Entry] = []

    def save(self):
        for item in self.entries:
            item.save(self.data_path)

    def load(self):
        for fs in os.listdir(self.data_path):
            if fs.endswith('.json'):
                path = os.path.join(self.data_path, fs)
                entry = Entry.load(path)
                self.entries.append(entry)

    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)

def print_with_indent(value, indent=0):
    indentation = "\t" * indent
    print(indentation + str(value))