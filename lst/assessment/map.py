# -*- coding: utf-8 -*-
"""
Markov Assessment Procedure.
"""
from inspect import getargspec

from lst.exceptions import MAPInitError

__author__ = 'isturunt'


class MAPMeta(type):

    Q_RULE_KEY = 'questioning_rule'
    U_RULE_KEY = 'updating_rule'
    Q_RULE_ARGS_DOC = [
        'a probabilistic knowledge structure, an instance of `lst.objects.ProbabilisticKnowledgeStructure`'
    ]
    U_RULE_ARGS_DOC = [
        'a probabilistic knowledge structure, an instance of `lst.objects.ProbabilisticKnowledgeStructure`',
        'current question, an item of the domain',
        'current response, `True` or `False`'
    ]
    Q_RULE_ARGS_COUNT = len(Q_RULE_ARGS_DOC)
    U_RULE_ARGS_COUNT = len(U_RULE_ARGS_DOC)
    Q_RULE_DOC = """
    A questioning rule is a function which implements some mechanism of question selection in
    a markov assessment procedure. When applied to a probability knowledge structure it
    should return the next question.
    
    Formally, a questioning rule is defined by a function Ѱ: (q, Ln) → Ѱ(q, Ln) which given
    a probability distribution Ln, for each item (question) q defines a probability of q to be selected.
    
    The function passed in '{key}' should return an item of the domain (the one to be asked next) 
    and accept {count} positional arguments:
    * {args} 
    """.format(
        key=Q_RULE_KEY,
        count=Q_RULE_ARGS_COUNT,
        args="\n\t* ".join(Q_RULE_ARGS_DOC)
    )
    U_RULE_DOC = """
    An updating rule specifies a way to update current probability distribution on the states of
    the probability knowledge structure when a response is obtained.
    
    The function passed in '{key}' should return a new distribution over the states 
    and accept {count} positional arguments:
    * {args}
    """.format(
        key=U_RULE_KEY,
        count=U_RULE_ARGS_COUNT,
        args="\n\t* ".join(U_RULE_ARGS_DOC)
    )

    def __new__(mcs, *args, **kwargs):
        obj = type.__new__(mcs, *args, **kwargs)
        obj.__doc__ += """
        {q_rule_doc}
        {u_rule_doc}
        """.format(
            q_rule_doc=mcs.Q_RULE_DOC,
            u_rule_doc=mcs.U_RULE_DOC
        )
        return obj

    def __call__(cls, *args, **kwargs):
        if cls.Q_RULE_KEY not in kwargs:
            raise MAPInitError("'questioning_rule' kwarg missing")
        if cls.U_RULE_KEY not in kwargs:
            raise MAPInitError("'updating_rule' kwarg missing")

        updating_rule = kwargs[cls.U_RULE_KEY]
        questioning_rule = kwargs[cls.Q_RULE_KEY]

        if not callable(updating_rule):
            raise MAPInitError("'%s' - callable expected" % cls.U_RULE_KEY)
        if not callable(questioning_rule):
            raise MAPInitError("'%s' - callable expected" % cls.Q_RULE_KEY)

        if len(getargspec(updating_rule).args) != 3:
            raise MAPInitError(
                "'{rule_name}' should accept {rule_args_count} positional argument{s}:\n"
                "{args_doc}".format(
                    rule_name=cls.U_RULE_KEY,
                    rule_args_count=cls.U_RULE_ARGS_COUNT,
                    s=('s' if cls.U_RULE_ARGS_COUNT > 1 else ''),
                    args_doc=";\n".join(cls.U_RULE_ARGS_DOC)
                )
            )
        if len(getargspec(questioning_rule).args) != 1:
            raise MAPInitError(
                "'{rule_name}' should accept {rule_args_count} positional argument{s}:\n"
                "{args_doc}".format(
                    rule_name=cls.Q_RULE_KEY,
                    rule_args_count=cls.Q_RULE_ARGS_COUNT,
                    s=('s' if cls.Q_RULE_ARGS_COUNT > 1 else ''),
                    args_doc=";\n".join(cls.Q_RULE_ARGS_DOC)
                )
            )

        def _updating_rule(self):
            return updating_rule(
                self._pks,
                self._current_question,
                self._current_response
            )

        def _questioning_rule(self):
            return questioning_rule(
                self._pks
            )

        obj = type.__call__(cls, *args, **kwargs)

        setattr(cls, '_updating_rule', _updating_rule)
        setattr(cls, '_questioning_rule', _questioning_rule)

        return obj


class MAP(object):
    """
    __Markov Assessment Procedure__ specifies a step-by-step
    algorithm for uncovering a latent state of a student.
    At each step a question is selected according to a
    particular _questioning rule_; after the question is asked
    and the subject's response is obtained the results are summarized
    in a _likelihood function_ which defines a likelihood of each state in
    the given knowledge structure. The likelihood function
    defines a probability distribution over a set of states of the
    knowledge structure. This function is used by the questioning
    rule to select the next question. The _updating rule_ specifies
    a way to update the probability distribution when the subject's
    response is received.

    The process begins with some initial likelihood which is used
    to select the first question.
    Under some particular assumptions the Markov Assessment Procedure
    is known to converge, meaning that the probability of the latent
    state converges to 1.

    `lst.assessment.map.MAP` should be instantiated with a
    probabilistic knowledge structure, a questioning rule,
    and an updating rule. The probability distribution
    of the given probabilistic knowledge structure is used
    as the initial likelihood function for the process.

    Note: You should consider using one of the predefined questioning
    rules and updating rules instead of specifying them yourself.
    If you really need to provide your own rules make sure they
    1. satisfy the theoretical necessary conditions,
    check [Learning Spaces: Interdisciplinary Applied Mathematics](https://www.springer.com/gp/book/9783642010385)
    2. satisfy all requirements below
    """

    __metaclass__ = MAPMeta

    def __init__(self, pks, **kwargs):
        """
        :param pks: an instance of `lst.objects.ProbabilisticKnowledgeStructure`
        :param questioning_rule:
        :param updating_rule:
        """
        self._pks = pks
        self._pks_orig = self._pks
        self._history = list()
        self._current_question = None
        self._current_distribution = self._pks.distribution
        self._current_response = None

    def _questioning_rule(self):
        raise NotImplemented()

    def _updating_rule(self):
        raise NotImplemented()

    def get_question(self):
        """
        Get next question.

        :return: A question (i.e., an item of the domain)
        """
        if self._current_question is None:
            self._current_question = self._questioning_rule()
        return self._current_question

    @property
    def current_question(self):
        return self.get_question()

    def submit_result(self, r):
        self._current_response = r
        l = self._updating_rule()
        self._history.append(
            (
                self._current_question,
                r,
                self._current_distribution
            )
        )
        self._current_question = None
        self._current_response = None
        self._current_distribution = l
