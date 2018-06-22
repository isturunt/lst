# -*- coding: utf-8 -*-
from unittest import TestCase

from lst.exceptions import ProbabilisticKnowledgeStructureInitError
from lst.objects import ProbabilisticKnowledgeStructure, KnowledgeStructure

__author__ = 'isturunt'


class TestProbabilisticKnowledgeStructure(TestCase):

    def setUp(self):
        domain = list('abcdef')
        states = {
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
        probs = {
            frozenset([]): 0,
            frozenset(list('d')): 0,
            frozenset(list('ac')): 0,
            frozenset(list('ef')): 0,
            frozenset(list('abc')): 0,
            frozenset(list('acd')): 0,
            frozenset(list('def')): 0,
            frozenset(list('abcd')): 0,
            frozenset(list('acef')): 0,
            frozenset(list('acdef')): 0,
            frozenset(list('abcdef')): 1
        }

        self.pks = ProbabilisticKnowledgeStructure(
            domain=domain,
            states=states,
            probabilities=probs
        )

    def test_if_knowledge_structure_created(self):
        self.assertIsInstance(self.pks.ks, KnowledgeStructure)

    def test_probabilities(self):
        self.assertEqual(sum(self.pks.distribution.values()), 1, msg="Probabilities must sum to 1")
        for k_state in self.pks.distribution:
            prob = self.pks.distribution[k_state]
            self.assertGreaterEqual(prob, 0, "Probability cannot be negative: p({0}) = {1}".format(
                k_state,
                prob
            ))

    def test_should_raise_exception_on_incorrect_probabilities_init(self):
        self.assertRaises(
            ProbabilisticKnowledgeStructureInitError,
            ProbabilisticKnowledgeStructure,
            domain={'a', 'b', 'c'},
            states=[{}, {'a'}, {'b'}, {'a', 'b', 'c'}],
            probabilities={
                frozenset({'a'}): -1
            }
        )
        self.assertRaises(
            ProbabilisticKnowledgeStructureInitError,
            ProbabilisticKnowledgeStructure,
            domain={'a', 'b', 'c'},
            states=[{}, {'a'}, {'b'}, {'a', 'b', 'c'}],
            probabilities={
                frozenset({'a'}): 1,
                frozenset({'b'}): 0.5,
            }
        )

    def test_should_provide_all_ks_attributes_directly(self):
        for key in self.pks.ks.__class__.__dict__.keys():
            if not key.startswith('__'):
                attr_value_1 = getattr(self.pks, key)
                attr_value_2 = getattr(self.pks.ks, key)
                self.assertEqual(attr_value_1, attr_value_2)
