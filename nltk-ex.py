import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.sem import relextract
import re
import pprint


def main() :
    pattern = 'NP: {<DT>?<JJ>*<NN>}'
    #IN = re.compile(r'.*\bin\b(?!\b.+ing)')

    with open("wiki-abstracts-only.txt", "r") as fin:
        for line in fin:
            sent = nltk.word_tokenize(line)
            #augment with POS tags
            sent = nltk.pos_tag(sent)
            cp = nltk.RegexpParser(pattern)
            cs = cp.parse(sent)
            #print(cs)
            ne_tree = nltk.ne_chunk(pos_tag(word_tokenize(line)))
            #print(ne_tree)
            #for rel in nltk.sem.extract_rels('ORG', 'LOC', line, corpus='ieer', pattern = IN):
            #    print(nltk.sem.rtuple(rel))
            pairs = relextract.tree2semi_rel(ne_tree)
            reldicts = relextract.semi_rel2reldict(pairs)
            #print(len(reldicts))
            for r in reldicts:
                #print('[' + r['subjtext'] + '] : [' + r['filler'] + '] : [' + r['objtext'] + ']')
                # remove POS tags
                sub = r['subjtext'].replace('/NNPS','').replace('/NNP','').replace('/JJ','');
                obj = r['objtext'].replace('/NNPS','').replace('/NNP','');
                vb = r['filler'].replace('/NNS','').replace('/NNP','').replace('/NN','').replace('/CC','').\
                replace('/PRP$','').replace('/DT','').replace('/CD','').replace('/JJ','').replace('/PRP','').\
                replace('/WP','').replace('/IN',"").replace('/VBD','').replace('/VBN','');
                print('[' + sub + '] : [' + vb + '] : [' + obj + ']')

main()
