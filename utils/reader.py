import itertools
import codecs

class IterableCorpus(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with codecs.open(self.filename, 'r', 'utf-8') as fn:
            for key, group in itertools.groupby(fn, lambda line: line.startswith('>>> DOCUMENT <<<')):
                if not key:
                    yield '\n'.join(list(group))

