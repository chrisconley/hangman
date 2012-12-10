
class DAWGNode:
    __slots__ = ["children", "final", "number"]

    def __init__(self, char):
        self.children = {}
        self.final  = False
        self.number = None

    def get_next(self, char):
        try:
            return self.children[char]
        except KeyError:
            return None

    def set_next(self, char, child):
        self.children[char] = child

    def has_transition(self, char):
        return char in self.children

    def __str__(self):
        return "<" + "".join(self.children.keys()) + ">"


def equivalence(p, q):
    "check if states p and q are equivalent"

    if p.final != q.final:
        return False

    if len(p.children) != len(q.children):
        return False

    s = set(p.children)
    if s != set(q.children):
        return False

    """
    # exact definition of equivalence
    for c in s:
        if not equivalence(p.children[c], q.children[c]):
                return False
    """
    # pratical implementation - constraints make
    # this much simpler and faster
    for c in s:
        if p.children[c] != q.children[c]:
            return False

    return True


class DAWG:
    def __init__(self):
        self._numbers_valid = False
        self.register = set()
        self.q0 = DAWGNode(None);
        self.wp = ''


    def add_word(self, word):
        assert word > self.wp
        return self.add_word_unchecked(word)


    def add_word_unchecked(self, word):
        # 1. skip existing
        i = 0;
        s = self.q0
        while i < len(word) and s.has_transition(word[i]):
            s = s.get_next(word[i])
            i = i + 1

        assert s != None

        # 2. minimize
        if i < len(self.wp):
            self._replace_or_register(s, self.wp[i:])


        # 3. add suffix
        while i < len(word):
            n = DAWGNode(word[i])
            s.set_next(word[i], n)
            assert n == s.get_next(word[i])
            s = n
            i = i + 1

        s.final = True
        self.wp = word
        self._numbers_valid = False


    def _replace_or_register(self, state, suffix):
        stack = []
        while suffix:
            letter = suffix[0]
            next   = state.get_next(letter)
            stack.append((state, letter, next))

            state = next
            suffix = suffix[1:]

        while stack:
            parent, letter, state = stack.pop()

            found = False
            for r in self.register:
                if equivalence(state, r):
                    assert(parent.children[letter] == state)
                    parent.children[letter] = r

                    found = True
                    break

            if not found:
                self.register.add(state)


    def freeze(self):
        self._replace_or_register(self.q0, self.wp)
        self._numbers_valid = False

    close = freeze


    def _num_nodes(self):
        def clear_aux(node):
            node.number = None
            for child in node.children.values():
                clear_aux(child)

        def num_aux(node):
            if node.number is None:
                n = int(node.final)
                for child in node.children.values():
                    n += num_aux(child)

                node.number = n

            return node.number

        if not self._numbers_valid:
            clear_aux(self.q0)
            num_aux(self.q0)
            self._numbers_valid = True


    def word2index(self, word):
        self._num_nodes()

        state = self.q0
        index = 0
        for c in word:
            try:
                next = state.children[c]
            except KeyError:
                return None

            for C in sorted(state.children):
                if C < c:
                    index += state.children[C].number
                else:
                    break

            state = next
            if state.final:
                index = index + 1
            print index
        #for

        return index

    def search(self, pattern, state=None, index=0, indices=[]):
        self._num_nodes()

        if not state:
            state = self.q0
        for c in pattern:
            if c == '-':
                for child in state.children.values():
                    self.search(pattern, child, (index+child.number), indices)
            else:
                try:
                    next = state.children[c]
                except KeyError:
                    return None

                for C in sorted(state.children):
                    if C < c:
                        index += state.children[C].number
                    else:
                        break

                state = next
                if state.final:
                    index = index + 1
                    print state
                    indices.append(index)


        return indices


    def index2word(self, index):
        self._num_nodes()

        state = self.q0
        count = index
        output_word = ""
        while True:
            for c in sorted(state.children):
                tmp = state.get_next(c)
                if tmp.number < count:
                    count -= tmp.number
                else:
                    output_word += c
                    state = tmp
                    if state.final:
                        count -= 1

                    break
            #for
            if count <= 0:
                break

        return output_word


    def as_dot(self, file):
        nodes = set()
        edges = []
        tmp   = set()

        def aux(node):
            nodes.add((id(node), node.final))
            tmp.add(node)

            for letter, child in node.children.items():
                aux(child)

        aux(self.q0)

        for node in tmp:
            for letter, child in node.children.items():
                edges.append((id(node), letter, id(child)))

        import dump2dot
        dump2dot.dumpdata2dot(nodes, edges, file)


    def words(self):
        L = []
        def aux(node, word):
            if node.final:
                L.append(word)

            for letter, child in node.children.items():
                aux(child, word + letter)

        aux(self.q0, '')
        return L


    def __iter__(self):
        return iter(self.words())


import os

def main():
    words = "aimaient aimais aimait aime aiment".split()
    words = "cat rat attribute tribute".split()

    def dump(name):
        with open(name, 'wt') as f:
            D.as_dot(f)


    D = DAWG()
    for word in sorted(words):
        print(word)
        D.add_word(word)

    D.freeze()

    # MPH test
    for word in words:
        print(word, "=>", D.word2index(word))

    for index in range(1, len(words) + 1):
        print(index, "=>", D.index2word(index))


    if 1:
        # show image of graph
        name = "dawg.dot"
        dump(name)
        os.system("dotty %s" % name)

    print(D.words(), set(D.words()) == set(words))


if __name__ == '__main__':
    main()
