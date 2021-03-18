import math, re
from sys import breakpointhook

def find_whole_words(target, options):
    """ Find a whole word in a set of options, and return the option that matches
        e.g. target = 'apple', options = {'apple sauce', 'brandy butter', 'applejack'}
        will return 'apple sauce' 

        If no match is found it will return None
    """
    target_match = None
    for option in options:
        careerfound = re.findall(r"\b" + target + r"\b", option)
        if target_match and careerfound:
            return target
        elif careerfound:
            target_match = option
    
    return target_match

def find_longest_prefix(target, options):
    """ From a set of options will return the one which has the longest prefix in common
        with target, e.g. target = 'cat', options = {'cat-burglar', 'house cat'} will
        return 'cat-burglar'

        If no match is found, or if multiple matches are found, will return None.
        So, target = 'cat', options = options = {'cat-burglar', 'catastrophe' will 
        return None.
    """
    longest_prefix = ''
    longest_match  = None
    ambiguous = False
    for option in options:
        import os
        longest_this_option = os.path.commonprefix([target,option])
        if len(longest_this_option)>len(longest_prefix):
            longest_prefix = longest_this_option
            longest_match  = option
            ambiguous = False
        elif longest_this_option==longest_prefix:
            ambiguous = True
    
    if ambiguous: return None
    else: return longest_match
    
# from https://stackoverflow.com/a/32558749/6386471
def levenshteinDistance(s1, s2):
    """Calculate Levenshtein Distance between two strings"""
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def find_best_match(target, options):
    """Use some simple heuristics to find the best match of a target string in a set 
    of options.

    The target must be at least three letters long for any heuristics to be applied.

    The order of heuristics is:
       1. If an exact match is found simply return it
       2. If a whole word matches in the options then return it, e.g. 'magus' for 'cult magus of tzeentch'
       3. Prefixes are matched, e.g. 'apo' for 'apothecary'
       4. Leventshtein distance to compensate for misspellings, e.g. 'oriest' for 'priest'
    """

    # Don't even try to match if we've been given fewer than three characters
    if len(target)<3:
        return target

    # Exact matches are easy!
    if target in options:
        return target

    # Check if words match
    word_match = find_whole_words(target, options)
    if word_match: return word_match

    # Check if it's a shortening
    # Ideally we should score the result so we can use this or the Leventshtein
    # distance as appropriate
    # At the moment 'vriest' says 'villager' instead of 'priest'
    prefix_match = find_longest_prefix(target,options)
    if prefix_match: 
        ## Score the prefix - every letter that doesn't match reduces the score
        for idx, char in enumerate(list(target)):
            if char!=prefix_match[idx]:
                breakpointhook
        score = idx - len(prefix_match)

        if score>0: return prefix_match

    # Leventshtein distance is good for misspellings but bad for abbreviations
    scores = {}
    for option in options:
        scores[option] = 1 - levenshteinDistance(target,option)

    import operator
    return max(scores.items(), key=operator.itemgetter(1))[0]

