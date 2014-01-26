import re

def preprocess(text):
    unicode_replacements = {
        ur"[‘’‚‛`´ʹʻʼʾʿˋˊ˴]": "'",
        ur"[“”„‟ʺˮ˵˶˝]": "\"",
        u"…" : "...",
        u"«" : "<<",
        u"»" : ">>",
        u"–" : "--",
        u"—" : "--",
        u"×" : "x",
        ur"([?!\.])(\")" : r"\1 \2",
        ur"([?!\.])$" : r" \1",
    }
    for k, v in unicode_replacements.iteritems():
        text = re.sub(k, v, text)
    return text


abbreviations = set('''
    a.d a.h a.l a.m a.n a.n.b a.p a.s adm ak akt al ala anm ant ariz ark aug
    ay b.a b.b.a b.c b.ch.e b.d b.sc bancorp bc.a.k bc.ac.p bc.hk bc.i bc.kwn
    bc.t.t bhd bid brig bros c.c c.o c.q calif capt cf cie cit cmdr co col
    colo conn corp cos cpl d-mass d.a d.c d.l d.sc dec def del dept dkk dll dr
    dr. dr.litt dra drg drh drs dsb dst e.g ed eds eks etc ex exch ext feb fla
    fol fri ft fv ga gen gg gov h.c hj hlm i.c i.e ibid id ill inc ind ir it
    jan jansz jend jl jln jos jr k k.h k.l kab kan kapt kec kel kep ky l.a
    l.l la lamp litt loc lt ltd m.a m.ag m.b.a m.d m.hum m.kes m.kom m.m m.p
    m.p.a m.p.h m.pd m.ph m.sc m.si m.sn m.t maj mass md messrs mfg mgr mich
    minn miss mo mon mr mrs ms mt n.b n.c n.j n.n n.y neb nev nfatc nn no nos
    nov ny o.j oct okla ont op ore p.a p.c p.f p.f.v p.m p.p p.r p.t pa ph
    ph.d phil pjs plh pp prof prop psi psw pt pty q.e q.q q.v r.a r.ay r.i r.j
    r.m r.r red ref reg rep reps rev rhs rp rs s.ag s.c s.d s.e s.h s.hut s.ip
    s.ked s.kedg s.kedh s.kg s.kh s.km s.kom s.m s.p s.pd s.pi s.pol s.psi
    s.pt s.s s.si s.sn s.sos s.t s.tekp s.th s.tp sat saw sbb sbg sc sen sens
    sep sept seq sgt sol sp sp.m sr ssk st sun swt t.t tap tb tel tenn tex th
    thu tk tsb tst ttd ttg tue u.b u.k u.n u.p u.s v v.o.c v.v va vol vs vt
    w.j w.va wash wed wis wyo y.l ybs ytc yth yts'''.split())

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktWordTokenizer

punkt_param = PunktParameters()
punkt_param.abbrev_types = abbreviations
sent_tokenizer = PunktSentenceTokenizer(punkt_param)
word_tokenizer = PunktWordTokenizer()



corpus = codecs.open('1000news-tokenized.txt', 'r', 'utf-8').read().split()
corpus_tokens = []
boundaries = set()
offset = 0
for token in corpus:
    corpus_tokens.append(token)
    offset += len(token)
    boundaries.add(offset-1)


import regex

def wordshape(text):
    text = regex.sub('\p{N}', '0', text)
    text = regex.sub('\p{Ll}+', 'a', text)
    text = regex.sub('\p{Lt}+', 'A', text)
    return text

def punkt_features(tokens, i):
    return {
        'punct': tokens[i],
        #'pw': tokens[i-1].lower(),
        #'nw': tokens[i+1].lower(),
        'lpw': len(tokens[i-1]),
        'pwcap': tokens[i-1][0].isupper(),
        'pwdig': tokens[i-1][0].isdigit(),
        'nwcap': tokens[i+1][0].isupper(),
        'nwdig': tokens[i+1][0].isdigit(),
        'pw': tokens[i-1].lower(),
        #'pw-1': tokens[i-1][-1:].lower(),
        #'pw-2': tokens[i-1][-2:].lower(),
        #'pw-3': tokens[i-1][-3:].lower(),
        'nw': tokens[i+1].lower(),
        #'nw+1': tokens[i+1][:1].lower(),
        #'nw+2': tokens[i+1][:2].lower(),
        #'nw+3': tokens[i+1][:3].lower(),
        'pws': wordshape(tokens[i-1]),
        'nws': wordshape(tokens[i+1]),
    }

featuresets = [(punkt_features(corpus_tokens, i), (i in boundaries))
               for i in range(1, len(corpus_tokens)-1)
               if regex.match('\p{P}', corpus_tokens[i]) != None]

size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)


def segment_sentences(words):
    start = 0
    sents = []
    for i, word in enumerate(words):
        if word in '.?!' and classifier.classify(punkt_features(words, i)) == True:
            sents.append(words[start:i+1])
            start = i+1
    if start < len(words):
        sents.append(words[start:])
    return sents

def tokenize(text):
    result = ['']
    tokens = [token.strip() for token in regex.split('(\w+|\p{P})', text) if token.strip()] + ['JUNK']
    space_next = True
    for i, token in enumerate(tokens[:-1]):
        print i, token, classifier.classify(punkt_features(tokens, i))
        if regex.match('^\p{P}$', token) and tokens[i+1] == 'JUNK':
            result.append(token)
        elif regex.match('^\p{P}$', token) and classifier.classify(punkt_features(tokens, i)) == True:
            result[-1] += token
            space_next = False
        else:
            if space_next:
                result.append(token)
            else:
                result[-1] += token
                space_next = True
    return [token for token in result if token]
