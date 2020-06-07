import re
from .levenshtein import get_similarity


def get_list_subject(text, subjects):
    list_subject = set()
    # part 1: check subject_name in message
    for subject in schedule["subject_schedule"].keys():
        if subject in text:
            list_subject.add(subject)

    # part 2: check regex subject is similarity with subject_name
    list_regex = re.findall(r'\"(.*?)\"', text)
    best_similarity = 0.5
    for regex in list_regex:
        best = None
        for subject in schedule["subject_schedule"].keys():
            similar = get_similarity(regex, subject)
            if similar > best_similarity:
                best_similarity = similar
                best = subject
        if best:
            list_subject.add(best)

    return list(list_subject)