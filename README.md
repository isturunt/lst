# LST

A Python package for the Learning Spaces theory.


The Learning Spaces theory by J.-P. Doignon and J.-C. Falmagne
proposes a mathematical formalism for learning process.
Consider a field of knowledge.
A set of questions in this field, each having a correct response,
is called a 'domain'.
The theory operates mathematical structures over such domains.
A 'knowledge state' of a student is defined as a subset of
questions within the given domain that he masters.
In other words, we consider a student to be in a certain knowledge
state if he is capable of answering each item in this state correctly.
The concept of knowledge state is the key concept of the learning
spaces theory. It provides a formal representation for the
statuses of the learners in the suggested knowledge field.
A set of all possible knowledge states of some domain forms a
'knowledge structure' over this domain. Formally, a knowledge
structure is a pair $(Q,\mathcal{K})$
in which $Q$ is a domain and $\mathcal{K}$ is a
family of subsets of $Q$ (i.e., a set of knowledge states)
such that it contains at least $Q$ and ∅. A knowledge structure
that is closed under a union is called 'knowledge space'.
A well-graded knowledge space is called a 'learning space'.