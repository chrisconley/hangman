import unittest

import lookahead.play
class EntropyTests(unittest.TestCase):
    def test_square_entropy(self):
        self.assertAlmostEqual(lookahead.play.square_entropy(1.0), 0, places=4)
        self.assertAlmostEqual(lookahead.play.square_entropy(0.0), 0, places=4)
        self.assertAlmostEqual(lookahead.play.square_entropy(0.5), 0.25, places=4)

        self.assertAlmostEqual(lookahead.play.square_entropy(0.01), 0.0099, places=4)
        self.assertAlmostEqual(lookahead.play.square_entropy(0.02), 0.0196, places=4)

        self.assertAlmostEqual(lookahead.play.square_entropy(0.98), 0.0196, places=4)
        self.assertAlmostEqual(lookahead.play.square_entropy(0.99), 0.0099, places=4)

    def test_log_entropy(self):
        self.assertAlmostEqual(lookahead.play.log_entropy(1.0), 0, places=4)
        self.assertAlmostEqual(lookahead.play.log_entropy(0.0), 0, places=4)
        self.assertAlmostEqual(lookahead.play.log_entropy(0.5), 0.5000, places=4)

        self.assertAlmostEqual(lookahead.play.log_entropy(0.01), 0.0664, places=4)
        self.assertAlmostEqual(lookahead.play.log_entropy(0.02), 0.1129, places=4)

        self.assertAlmostEqual(lookahead.play.log_entropy(0.98), 0.0286, places=4)
        self.assertAlmostEqual(lookahead.play.log_entropy(0.99), 0.0144, places=4)

    def test_reverse_log_entropy(self):
        self.assertAlmostEqual(lookahead.play.reverse_log_entropy(1.0), 0, places=4)
        self.assertAlmostEqual(lookahead.play.reverse_log_entropy(0.0), 0, places=4)
        self.assertAlmostEqual(lookahead.play.reverse_log_entropy(0.5), 0.5000, places=4)

        self.assertAlmostEqual(lookahead.play.reverse_log_entropy(0.01), 0.0144, places=4)
        self.assertAlmostEqual(lookahead.play.reverse_log_entropy(0.02), 0.0286, places=4)

        self.assertAlmostEqual(lookahead.play.reverse_log_entropy(0.98), 0.1129, places=4)
        self.assertAlmostEqual(lookahead.play.reverse_log_entropy(0.99), 0.0664, places=4)

    def test_most_entropy_duplicates(self):
        counters = {'e': {'ee': 18, 'eee': 2, '*': 107, 'e': 87}, 'x': {'x': 1, '*': 1}, '*': 185}
        g = lookahead.play.most_entropy(counters)
        self.assertEqual(g.next(), ('e', 1.4348619619430347))
        self.assertEqual(g.next(), ('x', 0.04848740692447222))

    def test_most_entropy_positional(self):
        #counters = {'e': {'e-e': 6, '-ee': 11, 'ee-': 1, 'eee': 2, '*': 107, 'e': 87}, 'x': {'x': 1, '*': 1}, '*': 185}
        #g = lookahead.play.most_entropy(counters)
        #self.assertEqual(g.next(), ('e', 1.551051838789653))
        #self.assertEqual(g.next(), ('x', 0.04848740692447222))
        counters = {u'e': {u'ee': 18, u'eee': 2, u'*': 107, u'e': 87}, u's': {u'ss': 16, u's': 69, u'*': 86, u'sss': 1}, u'l': {u'll': 7, u'*': 61, u'l': 52, u'lll': 2}, u'a': {u'aa': 11, u'a': 74, u'*': 85}, u'r': {u'r': 56, u'*': 67, u'rr': 11}, u'i': {u'i': 59, u'ii': 7, u'*': 66}, u't': {u'tt': 8, u'*': 61, u't': 53}, u'd': {u'dd': 6, u'*': 53, u'd': 47}, u'o': {u'oo': 11, u'*': 50, u'o': 39}, u'n': {u'*': 50, u'nn': 2, u'n': 48}, u'u': {u'uu': 3, u'*': 39, u'u': 36}, u'c': {u'cc': 2, u'c': 33, u'*': 35}, u'm': {u'mm': 2, u'*': 32, u'm': 30}, u'g': {u'gg': 5, u'*': 28, u'g': 23}, u'b': {u'*': 23, u'b': 21, u'bb': 2}, u'p': {u'p': 18, u'pp': 3, u'*': 21}, u'f': {u'*': 17, u'ff': 3, u'f': 14}, u'k': {u'kk': 1, u'k': 12, u'*': 13}, u'v': {u'*': 12, u'vv': 1, u'v': 11}, u'h': {u'h': 27, u'*': 27}, u'y': {u'y': 26, u'*': 26}, u'w': {u'*': 10, u'w': 10}, u'q': {u'q': 5, u'*': 5}, u'j': {u'*': 4, u'j': 4}, u'z': {u'*': 2, u'z': 2}, u'x': {u'x': 1, u'*': 1}, u'*': 185}
        g = lookahead.play.most_entropy(counters)
        #for (letter, entropy) in g:
            #print letter, entropy
        
        #print '------------------'

        counters = {u'e': {u'--e---': 10, u'----e-': 47, u'---e--': 7, u'-e--ee': 1, u'-e--e-': 9, u'-e----': 10, u'*': 107, u'-----e': 10, u'-e-ee-': 1, u'-e-e--': 4, u'e---e-': 1, u'----ee': 3, u'---ee-': 1, u'e-----': 3}, u's': {u'-s---s': 1, u'-----s': 35, u'----s-': 5, u'---s-s': 4, u'*': 86, u'--s--s': 4, u'---s--': 2, u'-s----': 2, u's---s-': 1, u'--s---': 10, u's---ss': 1, u'--ss--': 1, u's----s': 5, u's-----': 15}, u'r': {u'-r---r': 2, u'----r-': 2, u'r----r': 1, u'--rr--': 1, u'-----r': 13, u'--r---': 19, u'*': 67, u'---r--': 5, u'---r-r': 1, u'r---r-': 2, u'-rr---': 1, u'--r--r': 3, u'r-----': 6, u'-r----': 11}, u'o': {u'--oo--': 2, u'-o--o-': 2, u'---o--': 5, u'--o-o-': 1, u'*': 50, u'---oo-': 1, u'----o-': 4, u'--o---': 8, u'oo----': 1, u'o-----': 3, u'-oo---': 3, u'o--o--': 1, u'-----o': 2, u'-o----': 17}, u'a': {u'-a-a--': 2, u'aa----': 1, u'a-----': 9, u'---a-a': 1, u'----a-': 12, u'*': 85, u'a---a-': 3, u'-a--a-': 2, u'-a----': 32, u'-----a': 4, u'--a-a-': 2, u'---a--': 6, u'--a---': 11}, u't': {u'-----t': 9, u'*': 61, u'--t-t-': 1, u'--t--t': 3, u'-t----': 6, u'--tt--': 1, u't-----': 14, u'-t-t--': 1, u'---t--': 14, u'--t---': 3, u't---t-': 1, u'----t-': 7, u't--t--': 1}, u'l': {u'--ll--': 3, u'*': 61, u'l---l-': 1, u'-l----': 7, u'l-----': 5, u'---l--': 15, u'---ll-': 1, u'l-ll--': 1, u'-----l': 6, u'----l-': 14, u'--l-l-': 2, u'-ll-l-': 1, u'--l---': 5}, u'i': {u'-i-i--': 1, u'--i--i': 1, u'-i----': 14, u'-i--i-': 3, u'---i--': 18, u'*': 66, u'i-----': 3, u'i-i---': 1, u'----i-': 7, u'---i-i': 1, u'--i---': 16, u'-----i': 1}, u'd': {u'-d----': 3, u'd-----': 13, u'---d--': 9, u'd----d': 3, u'*': 53, u'---d-d': 1, u'--d--d': 2, u'-----d': 21, u'----d-': 1}, u'n': {u'-n--n-': 1, u'*': 50, u'--n---': 13, u'-n----': 4, u'n-----': 4, u'n----n': 1, u'---n--': 6, u'-----n': 10, u'----n-': 11}, u'm': {u'---m--': 4, u'*': 32, u'-m----': 2, u'--m---': 10, u'--mm--': 1, u'----m-': 3, u'-m---m': 1, u'm-----': 8, u'-----m': 3}, u'p': {u'--pp--': 1, u'--p---': 2, u'p-p---': 1, u'-----p': 2, u'p-----': 6, u'---p--': 5, u'---pp-': 1, u'*': 21, u'----p-': 3}, u'u': {u'-u----': 18, u'u-----': 2, u'-u-u--': 2, u'--u---': 5, u'*': 39, u'----u-': 7, u'-u--u-': 1, u'---u--': 4}, u'c': {u'--c---': 8, u'*': 35, u'c--c--': 1, u'---c--': 7, u'c---c-': 1, u'c-----': 10, u'----c-': 3, u'-c----': 5}, u'g': {u'g-----': 6, u'*': 28, u'---g--': 7, u'--gg--': 4, u'-----g': 5, u'g--g--': 1, u'--g---': 2, u'----g-': 3}, u'h': {u'--h---': 2, u'*': 27, u'---h--': 6, u'-h----': 7, u'----h-': 3, u'-----h': 5, u'h-----': 4}, u'f': {u'f-----': 10, u'-ff---': 1, u'*': 17, u'--f---': 2, u'----ff': 1, u'--ff--': 1, u'----f-': 2}, u'k': {u'-k----': 1, u'*': 13, u'----k-': 5, u'--k---': 2, u'k--k--': 1, u'---k--': 3, u'-----k': 1}, u'y': {u'--y---': 3, u'---y--': 2, u'*': 26, u'-----y': 16, u'-y----': 2, u'y-----': 3}, u'b': {u'--bb--': 2, u'b-----': 13, u'*': 23, u'-----b': 1, u'--b---': 3, u'---b--': 4}, u'v': {u'---v--': 3, u'*': 12, u'--v---': 2, u'v--v--': 1, u'v-----': 6}, u'w': {u'-w----': 1, u'*': 10, u'---w--': 2, u'--w---': 2, u'w-----': 5}, u'q': {u'q-----': 2, u'*': 5, u'-q----': 1, u'--q---': 1, u'---q--': 1}, u'j': {u'j-----': 3, u'*': 4, u'---j--': 1}, u'z': {u'--z---': 1, u'*': 2, u'---z--': 1}, u'x': {u'---x--': 1, u'*': 1}, u'*': 185}
        g1 = lookahead.play.most_entropy(counters)
        for r in g:
            print r, g1.next()

