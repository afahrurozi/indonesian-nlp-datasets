#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import MySQLdb as mdb
import settings as s
from utils import FetchAllAssoc

mapping = {
    'adj'   : 'ADJ',
    'adv'   : 'ADV',
    'i'     : 'PRT',
    'k'     : 'CONJ',
    'l'     : 'PRT',
    'n'     : 'NOUN',
    'num'   : 'NUM',
    'pre'   : 'ADP',
    'pron'  : 'PRON',
    'v'     : 'VERB'
}

# open file
file    = 'lexicon-id-kateglo.json';
fp      = open(file, 'w');

# get lemma
db      = mdb.connect(s.host, s.user, s.password, s.dbname)
qb      = db.cursor()
sql     = "SELECT phrase, lex_class FROM phrase WHERE actual_phrase IS NULL \
           AND lex_class != 'bt' group by phrase order by phrase"

# this is a stupid trick on how to write a json file, but who cares, it works
# i keep this original trick just so you know that the history has been done
# from now on, everytime you see a hashtag followed by code, that's mean
# the original trick used by our php superhero. kudos for them.

#fp.write("{\n")
#started = False

lexicon = {}

# Fetch all data and return it as list of dicts
fetch   = FetchAllAssoc(qb,sql)
for row in fetch:
    phrase  = row['phrase']
    lexicon[phrase] = []
    #print phrase + '\n' #just to indicate progress. well... em.. nevermind
    if mapping[row['lex_class']]:
        lexicon[phrase].append(mapping[row['lex_class']])

    # get class from definition
    sql2    = "SELECT lex_class FROM definition \
               WHERE phrase = '%s' AND lex_class IS NOT NULL" % row['phrase'];
    class2  = FetchAllAssoc(qb,sql2)
    if len(class2) > 0:
        for c in class2:
            if mapping[c['lex_class']] not in lexicon[phrase]:
                lexicon[phrase].append(mapping[c['lex_class']])
    #if not started:
    #    started = True
    #else:
    #    fp.write(',\n')

    #fp.write('\t"' + phrase + '":["' + '","'.join(lexicon[phrase]) + '"]')

#finalize
#fp.write('\n}')
fp.write(json.dumps(lexicon))
fp.close()
