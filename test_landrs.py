#!/usr/bin/env python
import unittest

from . import pyobs_pyobs
import rdflib


def test_Observation():
    obs = pyobs_pyobs.ObservationCollection(comment="mycol")
    this_graph = pyobs_pyobs.get_graph()
    print(this_graph.serialize(format='turtle'))


def test_Platform():
    obs = pyobs_pyobs.ObservationCollection(comment='mycol2')
    this_graph = pyobs_pyobs.get_graph()
    print(this_graph.serialize(format='turtle'))


def test_Sensor():
    obs = pyobs_pyobs.ObservationCollection(comment='mycol3')
    this_graph = pyobs_pyobs.get_graph()
    print(this_graph.serialize(format='turtle'))


if __name__ == '__main__':
    test_Platform()

#if __name__ == '__main__':
#    unittest.main()
