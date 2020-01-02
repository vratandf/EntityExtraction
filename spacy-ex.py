import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from textpipeliner import PipelineEngine, Context
from textpipeliner.pipes import *

#use nltk to split text into sentences
import nltk.data
from nltk.tokenize import sent_tokenize


nlp = spacy.load('en_core_web_sm')

def main() :
    with open("wiki-abstracts-only-small.txt", "r") as fin:
        for line in fin:
            # split into sentences
            lines = sent_tokenize(line)
            for sentence in lines:
                #print_for_debug(sentence)
                entity_pair = get_entities(sentence)
                reln = get_relation(sentence)
                if (entity_pair[0]) and (reln) and (entity_pair[1]):
                   print('[' + entity_pair[0] + '] : [' + reln + '] : [' + entity_pair[1] + ']')



def print_for_debug(sentence):
    doc = nlp(sentence)
    for tok in doc:
        print(tok.text, "...", tok.dep_)


# find the root verb, append any prepositions or agent words
def get_relation(sent):

  doc = nlp(sent)

  # Matcher class object
  matcher = Matcher(nlp.vocab)

  #define the pattern
  pattern = [{'DEP':'ROOT'},
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},
            {'POS':'ADJ','OP':"?"}]

  matcher.add("matching_1", None, pattern)

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]]

  return(span.text)



# get subject and object; add compound words and modifiers that preceed them
def get_entities(sent):
    subj = ""
    # dobj (direct obj) is preferred; if missing, using pobj (predicate obj)
    dobj = ""
    pobj = ""
    prefix = ""

    #print('Analyzing sentence: ' + sent)
    for tok in nlp(sent):
        #print('Analyzing: ' + tok.text + ', type: ' + tok.dep_)
        # if compound word or modifier, build the prefix
        if (tok.dep_ == "compound") or (tok.dep_.endswith("mod")):
            # build the prefix
            if (prefix == ""):
                prefix = tok.text
            else:
                prefix = prefix + " " + tok.text
            #print('Prefix: ' + prefix)

        # if subject, append any prefix to it
        elif (tok.dep_.find("subj") != -1):
            if (prefix == ""):
                subj = tok.text
            else:
                subj = prefix + " "+ tok.text
            prefix = ""
            #print('Subj: ' + subj)

        # if object, append any prefix to it
        elif (tok.dep_.find("dobj") != -1):
            if (prefix == ""):
                dobj = tok.text
            else:
                dobj = prefix + " "+ tok.text
            prefix = ""
            #print('dObj: ' + dobj)

        elif (tok.dep_.find("pobj") != -1):
            # there can be multiple
            if (prefix == ""):
                pobj = tok.text
            else:
                pobj = prefix + " "+ tok.text
            prefix = ""
            #print('pObj: ' + pobj)

    obj = dobj
    if (obj == ""):
        obj = pobj
    #print('subject = ' + subj.strip() + ', object = ' + obj.strip())
    return [subj.strip(), obj.strip()]


# This code works well with larger texts, such as an entire article. Not so well with abstract.
def main2() :
    with open("wiki-abstracts-only-small.txt", "r") as fin:
        for line in fin:
            doc = nlp(line)
            pipes_structure = [SequencePipe([FindTokensPipe("VERB/nsubj/*"),
                                             NamedEntityFilterPipe(),
                                             NamedEntityExtractorPipe()]),
                               FindTokensPipe("VERB"),
                               AnyPipe([SequencePipe([FindTokensPipe("VBD/dobj/NNP"),
                                                      AggregatePipe([NamedEntityFilterPipe("GPE"),
                                                                     NamedEntityFilterPipe("PERSON")]),
                                                      NamedEntityExtractorPipe()]),
                                        SequencePipe([FindTokensPipe("VBD/**/*/pobj/NNP"),
                                                      AggregatePipe([NamedEntityFilterPipe("LOC"),
                                                                     NamedEntityFilterPipe("PERSON")]),
                                                      NamedEntityExtractorPipe()])])]

            engine = PipelineEngine(pipes_structure, Context(doc), [0,1,2])
            processed = engine.process()
            print(processed)


main()
#main2()
