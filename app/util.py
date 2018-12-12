import csv
from deepmoji.global_variables import ROOT_PATH

"""Maps the ids given by the model to the unicode form of the Emojis"""
map_id_to_emoji = []
with open('{}/emoji_unicode.csv'.format(ROOT_PATH), 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        map_id_to_emoji.append(row[0])

def get_emoji(i):
    """Simply gets an emoji from the map"""
    if i < 0 or i >= len(map_id_to_emoji):
        raise KeyError('Invalid Emoji ID')
    return map_id_to_emoji[i]

def emojify(t_score):
    """Transforms a t_score into an Emoji.
    
    Right now, it simply chooses the best Emoji, but in the fututure it could return
    a random Emoji with the selection weighted by the Emoji confidences."""
    i = t_score['ids'][0]
    return get_emoji(i).decode('unicode-escape')
