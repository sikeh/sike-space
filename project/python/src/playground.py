values = range(1, 11) + 'Jack Queen King'.split()
suits = 'diamonds clubs hears spades'.split()

deck = ['%s of %s' % (v, s) for v in values for s in suits]

from random import shuffle
shuffle(deck)

from pprint import pprint
pprint(deck)