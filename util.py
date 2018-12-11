import csv
from deepmoji.global_variables import ROOT_PATH

map_id_to_emoji = []
with open('{}/emoji_unicode.csv'.format(ROOT_PATH), 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        map_id_to_emoji.append(row[0])

def get_emoji(i):
    if i < 0 or i >= len(map_id_to_emoji):
        raise KeyError('Invalid Emoji ID')
    return map_id_to_emoji[i]

def emojify(t_score):
    i = t_score['ids'][0]
    return get_emoji(i).decode('unicode-escape')
