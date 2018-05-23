# -*- coding: utf-8 -*-

__author__ = 'isturunt'


def is_family_union_closed(family):
    """
    Checks if the given family of sets is union-closed
    (for any subfamily of the `family` the union of its sets
    also belongs to the `family`).

    :param family: a family of sets
    :return: `True` if `family` if union-closed, `False` otherwise
    """
    p = len(family)
    family_list = list(family)
    for subfamily_index in range(2**p):
        mask = "{0:0{p}b}".format(subfamily_index, p=p)
        mask = [bool(int(b)) for b in mask]
        subfamily = set([family_list[i] for i in range(p) if mask[i]])
        if not subfamily <= family:
            return False
        return True


def is_family_well_graded(family):
    """
    Checks whether the given family is well-graded.

    A family of sets is **well-graded** if, for any two
    distinct sets of this family K, L, there exists
    a finite sequence of states K=K_0, K_1, ..., K_p = L,
    such that d(K_{i-1}, K_i) = 1 for all 1 ≤ i ≤ p
    and d(K,L) = p.
    [Learning Spaces: Interdisciplinary Applied Mathematics](https://books.google.ru/books?hl=ru&lr=&id=q4NWzFqSIvcC&oi=fnd&pg=PR5&dq=learning+spaces+interdisciplinary&ots=kyf_lmlzmJ&sig=8W4Z0V4nyiescx43qm4TwIb-t3A&redir_esc=y#v=onepage&q=learning%20spaces%20interdisciplinary&f=false)

    Equivalently, a family is well-graded if for any state K
    there exists q1 (a domain item) such that K\{q1} belongs to this family
    (or otherwise K is an empty set) and there also exists q2
    such that K + {q2} belongs to this family
    (or otherwise K = the domain)

    :param family: a family of sets
    :return: `True` if the given family is well-graded, `False` otherwise
    """
    Q = set().union(*family)
    for k_state in family:
        item_can_be_deleted = False
        item_can_be_added = False
        if k_state == set([]):
            item_can_be_deleted = True
        else:
            for item in k_state:
                if (k_state - {item}) in family:
                    item_can_be_deleted = True
                    break
        if k_state == Q:
            item_can_be_added = True
        else:
            for item in Q - k_state:
                if k_state | {item} in family:
                    item_can_be_added = True
                    break
        if not (item_can_be_added and item_can_be_deleted):
            return False
    return True


def is_family_antimatroid(family):
    """
    A family _K of subsets of some domain Q (and relatively a knowledge structure (Q, _K))
    is an antimatroid if it is closed under union and satisfies the axiom of
    antimatroid:

    [MA] For each nonempty K ∈ _K there exists q ∈ K, s.t. K\{q} ∈ _K

    :param family: a family of states
    :return: `True` is the given knowledge structure is an antimatroid,
    `False` otherwise
    """
    if not is_family_union_closed(family):
        return False
    for k_state in family - set([]):
        item_can_be_removed = False
        for item in k_state:
            if k_state - {item} in family:
                item_can_be_removed = True
                break
        if not item_can_be_removed:
            return False
    return True

