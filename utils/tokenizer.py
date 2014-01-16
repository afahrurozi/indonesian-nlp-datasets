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

