# -*- coding: utf-8 -*-
import os

from lst import objects
from utility import is_family_union_closed, is_family_well_graded

__author__ = 'isturunt'


def create(domain, states):
    """
    Creates an appropriate type of a knowledge structure
    for the domain and the family of its subsets (`states`) given.
    `states` MUST include an empty set AND the whole domain (`domain`)
    at least.
    Otherwise an exception is raised (since this is the minimal
    requirement for knowledge structures).

    * If the `states` family is both union-closed and well-graded
    the function returns a `objects.LearningSpace` instance.
    * If the `states` family is union-closed but NOT well-graded
    the function returns a `objects.KnowledgeSpace` instance.
    * If the `states` family is not union-closed
    the function returns a `objects.KnowledgeStructure` instance.


    :param domain: a set of items
    :param states: a family of subsets of the `domain`; it is required
    to include at least an empty set and the whole domain
    :return: `objects.KnowledgeStructure` (`objects.KnowledgeSpace` or
    `objects.LearningSpace` if possible)
    """
    if is_family_union_closed(states):
        if is_family_well_graded(states):
            return objects.LearningSpace(domain=domain, states=states)
        else:
            return objects.KnowledgeSpace(domain=domain, states=states)
    else:
        return objects.KnowledgeStructure(domain=domain, states=states)


def create_knowledge_structure(domain, states):
    """
    Creates and returns a knowledge structure
    (an instance of `objects.KnowledgeStructure`).

    :param domain: a set of items
    :param states: a family of subsets of the `domain`; it is required
    to include at least an empty set and the whole domain
    :return: `objects.KnowledgeStructure`
    """
    return objects.KnowledgeStructure(domain, states)


def create_knowledge_space(domain, states):
    """
    Creates and returns a knowledge space
    (an instance of `objects.KnowledgeSpace`).

    The `states` has to be a union-closed family.
    Otherwise an exception is raised.

    :param domain: a set of items
    :param states: a union-closed family of subsets of the `domain`; it is required
    to include at least an empty set and the whole domain
    :return: `objects.KnowledgeSpace`
    """
    if not is_family_union_closed(states):
        raise ValueError("Cannot create a knowledge space: the family of states is not union-closed")
    return objects.KnowledgeSpace(domain, states)


def create_learning_space(domain, states):
    """
    Creates and returns a learning space
    (an instance of `objects.LearningSpace`).

    The `states` family has to be be union-closed AND well-graded.
    Otherwise an exception is raised.

    :param domain: a set of items
    :param states: a union-closed well-graded family of subsets of the `domain`;
    it is required to include at least an empty set and the whole domain
    :return: `objects.LearningSpace`
    """
    if not is_family_union_closed(states):
        raise ValueError("Cannot create a learning space: the family of states is not union-closed")
    if not is_family_well_graded(states):
        raise ValueError("Cannot create a learning space: the family of states is not well-graded")
    return objects.LearningSpace(domain, states)


def from_list(states_list):
    """
    Creates a knowledge structure from a list of states :param states_list:.

    :param states_list: is not required to include an empty set.
    However, it is required to include the whole domain.
    The domain is considered to be the union of all of the states
    in :param states_list:.

    >>> states_list = [['A'], ['B'], ['A', 'B'], ['A', 'C'], ['B', 'C'], ['A', 'B', 'C']]
    >>> ls = from_list(states_list)
    >>> ls.domain
    frozenset(['A', 'C', 'B'])
    >>> ls.states
    frozenset([frozenset(['A', 'C', 'B']), frozenset(['C', 'B']), frozenset(['A', 'C']), frozenset(['B']), frozenset(['A']), frozenset([]), frozenset(['A', 'B'])])


    :param states_list: a list of states
    :return: `objects.KnowledgeStructure`
    """
    domain = set().union(*states_list)
    states = set()
    for k_state in states_list:
        states.add(frozenset(k_state))
    states.add(frozenset([]))
    return create(domain=domain, states=states)


def from_string(text, states_sep=os.linesep, items_sep=','):
    """
        Creates a knowledge structure based on a data in :param text:.

        A text should define the states of a knowledge structure
        (including the whole domain).
        An empty set is not required inside the :param text:.
        The states are separated with :param states_sep: (defaults to `os.linesep`),
        the items in a state are separated with :param items_sep: (defaults to ',').
        Spaces are ignored.

        >>> ls = from_string('A\\nB\\nA,B\\nA,C\\nB,C\\nA,B,C')
        >>> is_family_well_graded(ls.states)
        True
        >>> ls.domain
        frozenset(['A', 'C', 'B'])
        >>> ls.states
        frozenset([frozenset(['A', 'C', 'B']), frozenset(['C', 'B']), frozenset(['A', 'C']), frozenset(['B']), frozenset(['A']), frozenset([]), frozenset(['A', 'B'])])
        >>> ls.__class__.__name__
        'LearningSpace'


        :param text: a text specifying states
        :param states_sep: states separator (default: `os.linesep`)
        :param items_sep: items separator (default: `','`)
        :return: `objects.KnowledgeStructure`
        """
    states = set()
    text = text.replace(' ', '')
    for k_state in text.split(states_sep):
        states.add(frozenset(k_state.split(items_sep)))
    domain = set().union(*states)
    states.add(frozenset([]))
    return create(domain=domain, states=states)


def from_file(file_path, states_sep=os.linesep, items_sep=','):
    """
    Creates a knowledge structure based on a data found in
    the text file specified by :param file_path:.

    A text file should define the states of a knowledge structure
    (including the whole domain).
    An empty set is not required to be included in the file.
    The states are separated with :param states_sep: (defaults to `os.linesep`),
    the items in a state are separated with :param items_sep: (defaults to ',').
    Spaces are ignored.

    Example:

        A
        B
        A,C
        B,C
        A,B,C

    The example above evaluates into a knowledge structure with the domain
    `{'A','B','C'}` and the following states:

        {{}, {'A'}, {'B'}, {'A','C'}, {'B','C'}, {'A','B','C'}}

    :param file_path: file path
    :param states_sep: states separator (default: `os.linesep`)
    :param items_sep: items separator (default: `','`)
    :return: `objects.KnowledgeStructure`
    """
    with open(file_path) as in_file:
        text = in_file.read()
    return from_string(text, states_sep=states_sep, items_sep=items_sep)
