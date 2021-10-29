"""
This script will convert vlsp 2018 to spacy data format
"""
import os
import glob
import random
import re
import json

def create_files_list(path):
    files = []
    for i in range(len(path)):
        dirs = [dir for dir in os.listdir(path[i])]
        try:
            dirs.remove(".DS_Store")
        except ValueError:
            pass

        for field in dirs:
            dir_path = os.path.join(os.getcwd(), path[i], field)
            files += glob.glob(os.path.join(dir_path, "*.muc"))
            files += glob.glob(os.path.join(dir_path, "*.txt"))



    random.Random(4).shuffle(files)
    return files


def convert_to_json(files):
    json_list = []
    for file in files:
        with open(file, 'r') as rf:

            lines = [line for line in rf.read().split('\n')]
        for line in lines:
            if not line:
                continue
            ners = re.findall(re.compile("<ENAMEX.+?>.+?<\/ENAMEX>"), line)
            if len(ners) == 0:
                continue

            l = line
            text_insides = []
            ent = []
            for ner in ners:
                text_inside = re.findall("<ENAMEX.+?>(.+?)<\/ENAMEX>",
                            ner)[0]
                type = re.findall('<ENAMEX TYPE="(.+)">', ner)[0]

                l = re.sub(re.escape(ner), text_inside, l)

                text_insides.append((text_inside, type))
                # print(text_inside,)
                # print(l)

            if l.find("ENAMEX") != -1:  # For simplicity, ignore corner cases left
                continue

            for text, type in text_insides:
                result = [_.start() for _ in re.finditer(text, l)]
                for start in result:
                    end = start + len(text)
                    ent.append((start, end, type))

            ents = {"entities": ent}
            # print(l)
            json_list.append([l, ents])
            # print()
            # print(json_list)

    return json_list

files = create_files_list(['data/train', 'data/dev'])
data_json = convert_to_json(files)
n = len(data_json)
print(n)

train_size = 0.8
train_json = data_json[0:int(n * train_size)]
valid_json = data_json[int(n * train_size):]

with open('data/train_data.json', 'w') as outfile:
    json.dump(train_json, outfile, ensure_ascii=False)

with open('data/valid_data.json', 'w') as outfile:
    json.dump(valid_json, outfile, ensure_ascii=False)

print(1)














