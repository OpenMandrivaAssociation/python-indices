"""Sequence index and item ranges.

   The indices, irange, xindices, and xirange functions (based on PEP
   212) provide simple solutions for the common idiom of iterating
   over indices of a sequence, or over both indices and items.

   PEP 212 provided a naive definition for eagerly-evaluated
   single-argument functions indices and irange, but suggested that
   they could be implemented lazily, and should be easy to extend to
   accept more than one sequence argument.

   This module extends indices and irange to multiple sequences. On
   analogy with zip (see BDFL's decisions on PEP 201), with multiple
   sequences, the functions range over only those indices that all
   sequences have in common (rather than padding). That is, the
   resulting sequence is as long as the shortest input sequence.

   The lazy evaluation versions are prefixed with an x, on analogy
   with xrange, etc.

   The enumerate function from PEP 279 is a lazy version of the
   original irange (restricted to a single sequence). Since enumerate
   will be a built-in function, it has been included exactly as
   defined. When the multi-argument functionality is unnecessary,
   enumerate should be used (to make it easier to switch to the
   built-in function in the future).

"""

# indices.py version 0.1
# Written 23 June 2003 by andi payn <payn@myrealbox.com>
# This work is released under the LGPL, version 2.1 or later

from __future__ import generators

def indices(*sequences):
    """indices([seq1 [, seq2 [...]]]) -> [0, 1, ...]

       Returns a list of all indices in a sequence--or, for multiple
       sequences, of all indices common to all sequences (that is,
       from 0 to the minimum length). If no sequences are passed, the
       list is empty. This is an eager-evaluation equivalent of
       xindices.

       So indices([1,2,3], "ab") == [0, 1].

       The goal is to simplify the following idiom:

         for i in range(len(sequence)):
           dostuffwith(i, sequence[i])

         for i in range(min(len(seq1), len(seq2))):
           dostuffwith(i, seq1[i], seq2[i])

       The latter can be written as follows:
         for i in indices(seq1, seq2):
           dostuffwith(i, seq1[i], seq2[i])
    """
    if len(sequences) == 0: return range(0)
    return range(min([len(sequence) for sequence in sequences]))

def xindices(*sequences):
    """xindices([seq1 [, seq2 [...]]]) -> generator for 0, 1, ...

       Returns a generator for all indices in a sequence--or, for
       multiple sequences, for all indices common to all sequences
       (that is, from 0 to the minimum length). If no sequences are
       passed, the generator is empty. This is a lazy-evaluation
       equivalent of indices.

       So xindices([1,2,3], "ab") generates 0, then 1.
       
       The goal is to simplify the following idiom:

         for i in xrange(len(sequence)):
           dostuffwith(i, sequence[i])

         for i in xrange(min(len(seq1), len(seq2))):
           dostuffwith(i, seq1[i], seq2[i])

       The latter can be written as follows:
         for i in indices(seq1, seq2):
           dostuffwith(i, seq1[i], seq2[i])
    """
    if len(sequences) == 0: return xrange(0)
    return xrange(min([len(sequence) for sequence in sequences]))

def irange(*sequences):
    """irange(seq1 [, seq2 [...]]) ->
            [[0, seq1[0], seq2[0], ...], [1, seq1[0], seq2[0], ...], ...]

       Returns a list of lists, one for each element in the sequence
       (or, for multiple sequences, for each index that all sequences
       share), each consisting of the index and the appropriate
       element from each sequence. This is an eager-evaluation
       equivalent of xirange.

       So irange([1,2,3], "ab") == [[0, 1, "a"], [1, 2, "b"]].

       The goal is to simplify the following idiom:

         for i, e in zip(range(len(sequence)), sequence):
           dostuffwith(i, e)

         l=min(len(seq1), len(seq2))
         for i, e1, e2 in zip(range(l), seq1, seq2):
           dostuffwith(i, e1, e2)

       The latter can be written:
         for i, e1, e2 in irange(seq1, seq2)

       Note that irange returns a list of lists, rather than of tuples
       (because there is no tuple comprehension constructor).
    """
    if len(sequences) > 0:
        l=min([len(sequence) for sequence in sequences])
        return [tuple([i] + [sequence[i] for sequence in sequences]) for i in range(l)]

def xirange(*sequences):
    """xirange(seq1 [, seq2 [...]]) -> generator for
            [0, seq1[0], seq2[0], ...], [1, seq1[0], seq2[0], ...], ...

       Generates a sequence of lists, one for each element in the
       sequence (or, for multiple sequences, for each index that all
       sequences share), each consisting of the index and the
       appropriate element from each sequence. This is a lazy-
       evaluation equivalent of irange.

       So xirange([1,2,3], "ab") generates [0, 1, "a"], then [1, 2, "b"].

       The goal is to simplify the following idiom:

         for i, e in zip(range(len(sequence)), sequence):
           dostuffwith(i, e)

         l=min(len(seq1), len(seq2))
         for i, e1, e2 in zip(range(l), seq1, seq2):
           dostuffwith(i, e1, e2)

       The latter can be written:
         for i, e1, e2 in xirange(seq1, seq2)

       (Except that the xirange version is valuated lazily, which is
       non-trivial to accomplish in a for statement otherwise.)

       Note that xirange returns a range of lists, rather than of
       tuples (because there is no tuple comprehension constructor),
       and it requires both list comprehensions and generators (so it
       will only work with Python 2.2 or later).
    """
    if len(sequences) > 0:
        l=min([len(sequence) for sequence in sequences])
        for i in xrange(l):
            yield tuple([i] + [sequence[i] for sequence in sequences])

def enumerate(sequence):
    """enumerate(seq) -> generator for (0, seq[0]), (1, seq[1]), ...

       Generates a sequence of tuples, one for each element in the
       sequence, each consisting of the index and the appropriate
       element from the sequence. This is equivalent to xirange,
       except that it takes only a single sequence, and generates
       tuples rather than lists.
    """
    i = 0
    it = iter(sequence)
    while 1:
        yield(i, it.next())
        i += 1
