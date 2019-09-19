'''
(C) Chintan Maniyar
File created 20:47,
May 28, 2019
'''

import json

import inflect
import nltk


def mapNounFrequency(sentenceList):
    '''
    This function tags entities for a given list of sentences and returns a
    frequency map preserving the likeliness of singular and plural occurences
    '''
    fMap = {}

    if sentenceList == []:
        return fMap
    
    p = inflect.engine()

    for sentence in sentenceList:
        is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = nltk.word_tokenize(sentence)
        entities = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
        for entity in entities.copy():
            entities.remove(entity)
            if not p.singular_noun(entity):
                entities.append(p.plural(entity).lower())
            else:
                entities.append(entity.lower())
        entities = set(entities)
        for entity in entities:
            if entity in fMap:
                fMap[entity] += 1
            else:
                fMap[entity] = 1

    if len(entities)==0:
        return fMap
    frequency = list(fMap.values())
    normalizer = max(frequency)
    for entity, raw in zip(fMap, frequency):
        fMap[entity] = int((raw/normalizer)*100)
    return fMap


def generate_wordcloud(input_wordcloud):
    '''   
    main/ driver function
    '''
    # if __name__ == "__main__":
    data = {}
    words = {}

    data = input_wordcloud

    for domains in data:
        words[domains] = []
        for cats in data[domains]:
            temp = {}
            temp[cats] = {}
            words[domains].append(temp)
            tempargs = []
            for scoredresponse in data[domains][cats]:
                tempargs.append(scoredresponse['response'].split('-')[-1].strip())
            temp[cats] = mapNounFrequency(tempargs)
    return words
