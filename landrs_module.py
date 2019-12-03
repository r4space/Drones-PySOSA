# -*- coding: utf-8 -*-
"""Python module for instantiating and serializing W3C/OGC SSN-EXT Observation Collection.

This module provides utility class objects for maintaining a Observation Collection and the ability to serialize the collections as JSON-LD.

Todo:
    * Add configuration for sensors.
    * Additional Organizational Information

"""

from rdflib import Graph, URIRef, BNode, Literal, Namespace, RDF, RDFS

from pyld import jsonld
from datetime import datetime
from pytz import timezone

import json
import uuid

# Contexts for SOSA, SSN-EXT, SOSA
#  SOSA https://github.com/opengeospatial/ELFIE/blob/master/docs/json-ld/sosa.jsonld
#  Timeseries ML  https://github.com/opengeospatial/ELFIE/blob/master/docs/json-ld/tsml.jsonld
#  SSN-EXT https://github.com/opengeospatial/SELFIE/blob/master/docs/contexts/ssn-ext.jsonld
#  QUDT https://github.com/opengeospatial/SELFIE/blob/master/docs/contexts/qudt.jsonld
# datetime.datetime.now(pytz.timezone('Europe/Paris')).isoformat()
# UUID str(uuid.uuid4())
# https://github.com/w3c/sdw/blob/gh-pages/proposals/ssn-extensions/rdf/ssn-ext.jsonld 

# For images that are observations IIF 
# https://github.com/zimeon/iiif-ld-demo
from pyobs_pyobs import obsgraph, sosa, Sensor, ssnext


class Platform(object):
    """
    Creates a Platform object that represents a SOSA Platform
    SOSA Platform is an entity that hosts other entities,particularly Sensors, Actuators, Samplers and other Platform 
"""
    # Maybe remove list if makes object too big/not needed, or might want a func that returns this list
    # Attributes of the platform class

    sensors = []
    actuators = []
    samplers = []

    def __init__(self, comment, label):
        self.platform_id = BNode()
        self.label = Literal(label)
        self.comment = Literal(comment)
        obsgraph.add((self.platform_id, RDF.type, sosa.Platform))
        obsgraph.add((self.platform_id, RDFS.comment, self.comment))
        obsgraph.add((self.platform_id, RDFS.label, self.label))

    def add_sensor(self, Sensor):
        if isinstance(self, Sensor):
            sensor_uri = Sensor.get_uri()
            self.sensors.append(sensor_uri)
            obsgraph.add((self.platform_id, sosa.hosts, sensor_uri))
            Sensor.add_platform_id(self.platform_id)
        else:
            raise Exception('Object is not of type Sensor')

    def remove_sensor(self, sensor):
        a_uri = Sensor.get_uri()
        self.sensors.remove(a_uri)
        obsgraph.remove(self.platform_id, sosa.hosts, a_uri)
        Sensor.add_platform_id(self.platform_id)

    """
    Actuator is a device used by, or implements,an (Actuation)or Procedure that changes the state of the world
    """

    def add_actuator(self, Actuator):
        if isinstance(self, Actuator):
            a_uri = Actuator.get_uri()
            self.actuators.append(a_uri)
            obsgraph.add((self.platform_id, sosa.hosts, a_uri))
            Actuator.add_platform_id(self.platform_id)
        else:
            raise Exception('Object is not of type Actuator')

    def remove_actuator(self, sensorURI, sensor):
        a_uri = Sensor.get_uri()
        self.actuators.remove(a_uri)
        obsgraph.add((self.platform_id, sosa.hosts, a_uri))
        Sensor.add_platform_id(self.platform_id)

    # Sampler : A device that is used by,or implements, a (Sampling) Procedure to create or transform one or more samples

    def add_sampler(self, Sampler):
        if isinstance(self, Sampler):
            sampler_uri = Sampler.get_uri()
            self.samplers.append(sampler_uri)
            obsgraph.add((self.platform_id, sosa.hosts, sampler_uri))
            Sampler.add_platform_id(self.platform_id)
        else:
            raise Exception('Object is not of type Sampler')

    def remove_sampler(self, sensorURI, FeatureURI, result):
        a_uri = Sensor.get_uri()
        self.actuators.remove(a_uri)
        obsgraph.add((self.platform_id, sosa.hosts, a_uri))
        Sensor.add_platform_id(self.platform_id)


class Sensor(object):
    observations = []

    def __init__(self, sensor_description, observable_property, observable_property_uri, detects):
        x = Literal
        y = Literal
        z = Literal
        self.sensor_id = BNode()
        self.platform_id = BNode()
        self.observable_property = x
        self.detects = y
        self.implements_procedure = z
        # self.observable_property = Literal(x)
        self.sensor_description = Literal(sensor_description)
        obsgraph.add((self.sensorid, RDF.type, sosa.Sensor))
        obsgraph.add((self.sensorid, sosa.Observes, observable_property_uri))
        obsgraph.add((self.sensorid, RDFS.comment, self.sensor_description))

    def addObservation(self, sensorURI, FeatureURI, result):
        obsid = BNode()
        resultTime = datetime.now(tz=None)
        resultTimeLiteral = Literal(resultTime)
        resultLiteral = Literal(result)
        obsgraph.add((obsid, RDF.type, sosa.Observation))
        obsgraph.add((obsid, sosa.madeBySensor, sensorURI))
        obsgraph.add((self.obscollid, ssnext.hasMember, obsid))
        obsgraph.add((obsid, sosa.resultTime, resultTimeLiteral))
        obsgraph.add((obsid, sosa.hasSimpleResult, resultLiteral))
