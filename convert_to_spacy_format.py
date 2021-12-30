"""
This script will convert vlsp 2018 to spacy data format
"""
import os
import glob
import random
import re
import json
from extract_ners import case1, case2

s = set()
def create_files_list(path):

    dirs = [dir for dir in os.listdir(path)]
    try:
        dirs.remove(".DS_Store")
    except ValueError:
        pass
    files = []
    for field in dirs:

        dir_path = os.path.join(os.getcwd(), path, field)
        files += glob.glob(os.path.join(dir_path, "*.muc"))
        files += glob.glob(os.path.join(dir_path, "*.txt"))


    random.Random(4).shuffle(files)
    # print(len(files))
    return files


def convert_to_json(files):
    json_list = []
    count_misc = 0

    for file in files:
        with open(file, 'r') as rf:
            lines = [line for line in rf.read().split('\n')]

        for line in lines:
            if not line:
                continue

            ners = re.findall(re.compile("<ENAMEX.+?>.+?<\.?/ENAMEX.?>"), line)
            if len(ners) == 0:  # line without entities
                continue

            l = line
            text_insides = []
            ent = []

            for ner in ners:
                if len(re.findall("ENAMEX", ner)) == 2:
                    text_inside = case1(ner)
                    text_insides += text_inside
                    # print(text_inside[0][0])
                    # print(l)
                    # print(ner)
                    l = l.replace(ner, text_inside[0][0], 1)
                else:
                    text_inside = case2(ner)
                    text_insides += text_inside
                    # print(file)
                    # print(text_inside)
                    # print('-'*50)
                    # print(ners)
                    # print(ner)

                    l = l.replace(ner, text_inside[0][0] + " " + text_inside[1][0], 1)

                    l = l.replace("</ENAMEX>", "", 1)

            if l.find("ENAMEX") != -1:
                continue

            for text, type in text_insides:
                result = [(_.start(), _.end()) for _ in re.finditer(text, l)]
                for start, end in result:
                    ent.append((start, end, type))
                    if type == "MISCELLANEOUS":
                        count_misc += 1


            ents = {"entities": ent}
            json_list.append([l, ents])
    print(count_misc)
    print(a)
    return json_list

# train_files = create_files_list('data/dev')
# train_json = convert_to_json(train_files)
# # total: 6666 sentences with entities
# # after ignoring corner cases: 6498 sentences

# val_files = create_files_list('data/dev')
# val_json = convert_to_json(val_files)
# # total: 2225 sentences with entities,
# # after ignoring corner cases: 2209 sentences

# with open('data/train_data.json', 'w', encoding="utf-8") as outfile:
#     json.dump(train_json, outfile, ensure_ascii=False)

# with open('data/valid_data.json', 'w', encoding="utf-8") as outfile:
#     json.dump(val_json, outfile, ensure_ascii=False)

test_files = create_files_list('data/test')
test_json = convert_to_json(test_files)

# with open('data/test_data.json', 'w', encoding="utf-8") as outfile:
#     json.dump(test_json, outfile, ensure_ascii=False)

# 2629

# misc: train: 934, dev: 193, test: 338













