import numpy as np
import string


def clean_string(text):
    stopwords = ['với', 'được', 'nữa', 'nhỉ', 'nha', 'nhá', 'luôn']
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text


def levenshtein_distance(first, second):
    first = clean_string(first)
    second = clean_string(second)

    first_len = len(first)
    second_len = len(second)

    if first_len == 0 or second_len == 0:
        raise ValueError("Inputs must not have length 0")

    matrix = np.zeros((first_len+1, second_len+1), dtype=np.int)
    matrix[:,0] = range(first_len+1)
    matrix[0,:] = range(second_len+1)

    for i, first_char in enumerate(first, start=1):
        for j, second_char in enumerate(second, start=1):
            if first_char == second_char:
                cost = 0
            else:
                cost = 1
            min_cost = min(
                matrix[i-1, j] + 1,
                matrix[i, j-1] + 1,
                matrix[i-1, j-1] + cost
            )
            matrix[i, j] = min_cost

    return matrix[first_len, second_len]


def get_similarity(first, second):
    changes = levenshtein_distance(first, second)
    min_total_chars = min(len(first), len(second))
    return (min_total_chars - changes)/min_total_chars