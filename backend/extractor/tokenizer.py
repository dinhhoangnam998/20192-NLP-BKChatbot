import string

data = []

def preprocess_msg(msg):
    ''' return a list of character of messenger without punctuation'''
    msg = msg.lower()
    # rm punctuation
    special_punc = string.punctuation
    for punc in "-+/:|":
        special_punc = special_punc.replace(punc, '')
    msg = ''.join(c for c in msg if c not in special_punc)
    return msg.split()


def tokenize(msg):
    ''' extract date in messenger by matching in synonyms.json '''

    words = preprocess_msg(msg)

    tokens = []
    n_grams = (8, 7, 6, 5, 4, 3, 2, 1)
    i = 0
    while i < len(words):
        has_gram = False
        token = None
        for n_gram in n_grams:
            token = ' '.join(words[i:i + n_gram])
            if token in data:
                w = words[i-1] if i > 0 else ''
                W = words[i+n_gram] if i < len(words) - n_gram else ''
                #i += n_gram
                has_gram = True
                break
        if has_gram is False:
            token = words[i]
            i += 1
        if token in data:
            if data[token] in ["daysago", "nextday", "lastweek", "nextweek", "lastmonth", "nextmonth", "lastyear", "nextyear"]:
                pass
            #     if w in number_str.keys():
            #         tokens.append({data[token]: number_str[w] + " " + token})
            #         words.remove(w)
            #         remove_token(words=words, token=token)
            #     elif w.isnumeric():
            #         tokens.append({data[token]: w + " " + token})
            #         words.remove(w)
            #         remove_token(words=words, token=token)
            #     else:
            #         tokens.append({data[token]: token})
            #         remove_token(words=words, token=token)
            #     continue
            # if data[token] in ["week", "year"]:
            #     if W in number_str.keys():
            #         tokens.append({data[token]: token + " " + number_str[W]})
            #         remove_token(words=words, token=token)
            #         words.remove(W)
            #     elif W.isnumeric():
            #         tokens.append({data[token]: token + " " + W})
            #         remove_token(words=words, token=token)
            #         words.remove(W)
            #     else:
            #         tokens.append({data[token]: token})
            #         remove_token(words=words, token=token)
            #     continue

            # tokens.append({data[token]: token})
            # remove_token(words=words, token=token)
    return tokens