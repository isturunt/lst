# -*- coding: utf-8 -*-

"""
This module includes definitions for the main
objects of the package.
Note that you should never use these classes
directly.
"""
import os

from exceptions import *

__author__ = 'isturunt'


class KnowledgeStructure(object):
    """
    A class for knowledge structures
    """

    def __init__(self, domain, states):
        """
        :param domain: a non-empty set (or any iterable) of items. Items can be of any type
        but are required to be hashable.
        :param states: a set of knowledge states (i.e. a family of subsets of the domain).
        A set of states is required to include at least an empty set and the whole domain.
        """
        if len(domain) == 0:
            raise KnowledgeStructureInitError("Domain cannot be empty")
        for state in states:
            if not state <= domain:
                raise KnowledgeStructureInitError("The set of states can contain only the domain's subsets")
        if frozenset(domain) not in states or frozenset([]) not in states:
            raise KnowledgeStructureInitError("The family of states should contain at least ø and the whole domain")

        self._domain = frozenset(domain)
        self._states = frozenset(states)

    @classmethod
    def trivial(cls, domain):
        """
        Given a domain Q returns a trivial knowledge structure {Q, {ø, Q}}

        :param domain: an iterable of items
        :return: `KnowledgeStructure` object
        """
        return cls(domain=domain, states=[[], domain])

    @property
    def Q(self):
        """
        Alias for `domain`
        """
        return self._domain

    @property
    def domain(self):
        """
        Domain
        """
        return self._domain

    @property
    def K(self):
        """
        Alias for `states`
        """
        return self._states

    @property
    def states(self):
        """
        Set of states over the `domain`
        """
        return self._states

    def states_with_item(self, item):
        """
        Returns a frozenset of states containing `item`
        """
        return frozenset([state for state in self.states if item in state])

    def states_without_item(self, item):
        """
        Returns a frozenset of states that do NOT contain `item`
        """
        return frozenset([state for state in self.states if item not in state])

    def notion(self, item):
        """
        Return the notion of the knowledge structure for the given item `item`
        (i.e. the set of all items contained in the same states as `item`)
        """
        item_states = self.states_with_item(item)
        return frozenset([other for other in self.domain if self.states_with_item(other) == item_states])

    def get_domain_partition(self):
        """
        Returns a partition of the domain, i.e.
        the collection of all notions
        :return:
        """
        return frozenset(
            [self.notion(item) for item in self.domain]
        )

    def is_discriminative(self):
        """
        Checks whether the knowledge structure is discriminative
        (each notion contains a single item)
        or not
        """
        for item in self.domain:
            if len(self.notion(item)) > 1:
                return False
        return True

    def get_discriminative_reduction(self, join_func=str.__add__):
        """
        Returns a discriminative reduction of the knowledge structure.

        :param join_func: (default: `str.__add__`) A function to form new (reduced)
        items based on the original domain items. A join function should accept 2
        arguments (item_1 and item_2) and return a new item of hashable type
        such that other items can also be joined using this function.
        The `reduce` function is used to obtain the new item based on a set
        of original items (in fact, a notion):

        >>> notion = {'a', 'b', 'c'}
        >>> join_func = str.__add__
        >>> reduce(join_func, notion)
        'acb'

        By default, `str.__add__` function is used (assuming that the original
        items are strings). In this case, if item {'a', 'b', 'c'} form a notion
        of a knowledge structure they will be reduced to a new item 'abc'
        (which is the result of `reduce(str.__add__, {'a', 'b', 'c'})`).

        If the items of your domain are not strings then you definitely
        should pass your own `join_func`. While it can do whatever is
        appropriate to your items' data type, it needs to be reducible.

        >>> notion = {1,2,3}
        >>> join_func = lambda x, y: 100 * (x + y)
        >>> reduce(join_func, notion)
        30300

        -------

        Example:

        >>> Q = list('abcdef')
        >>> K = map(lambda x: frozenset(list(x)), ['', 'd', 'ac', 'ef', 'abc', 'acd', 'def', 'abcd', 'acef', 'acdef', 'abcdef'])
        >>> ks = KnowledgeStructure(domain=Q, states=K)
        >>> ks.is_discriminative()
        False
        >>> ksd = ks.get_discriminative_reduction()
        >>> ",".join(ksd.domain)
        'ac,b,ef,d'
        >>> ";".join(['{' + ",".join(state) + '}' for state in ksd.states])
        '{d};{ac,b,d};{ac,ef};{};{ef};{ac,ef,d};{ac,b};{ef,d};{ac,d};{ac,b,ef,d};{ac}'
        >>> ksd.is_discriminative()
        True

        :return: KnowledgeStructure
        """
        reduced_states = set()
        partition = list(self.get_domain_partition())
        items_newitems = dict()
        reduced_items = list()
        for part in partition:
            new_item = reduce(join_func, part)
            reduced_items.append(new_item)
            for item in part:
                items_newitems[item] = new_item
        for state in self.states:
            new_state = set()
            for item in state:
                new_state.add(items_newitems[item])
            reduced_states.add(frozenset(new_state))
        return type(self)(domain=reduced_items, states=reduced_states)

    def __str__(self):
        res = self.__class__.__name__ + os.linesep * 2
        res += "Domain: " + ', '.join(map(str, self.domain)) + os.linesep * 2
        res += "States:" + os.linesep
        for state in self.states:
            res += "    {" + ','.join(map(str, state)) + "}" + os.linesep
        return res

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        res = self.__class__.__name__ + os.linesep * 2
        res += "Domain: " + ', '.join(map(unicode, self.domain)) + os.linesep * 2
        res += "States:" + os.linesep
        for state in self.states:
            res += "    {" + ','.join(map(unicode, state)) + "}" + os.linesep
        return res


class KnowledgeSpace(KnowledgeStructure):
    pass


class LearningSpace(KnowledgeSpace):
    pass


if __name__ == '__main__':
    Q = list('abcdef')
    K = {
        frozenset([]),
        frozenset(list('d')),
        frozenset(list('ac')),
        frozenset(list('ef')),
        frozenset(list('abc')),
        frozenset(list('acd')),
        frozenset(list('def')),
        frozenset(list('abcd')),
        frozenset(list('acef')),
        frozenset(list('acdef')),
        frozenset(list('abcdef'))
    }

    map(lambda x: frozenset(list(x)), ['', 'd', 'ac', 'ef', 'abc', 'acd', 'def', 'abcd', 'acef', 'acdef', 'abcdef'])

    ks = KnowledgeStructure(domain=Q, states=K)
    print ks

    print "-" * 100
    ksd = ks.get_discriminative_reduction()
    print "Domain:", ",".join(ksd.domain)
    print "States:", ";".join(['{' + ",".join(state) + '}' for state in ksd.states])