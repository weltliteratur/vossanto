#!/usr/bin/python2
# -*- coding: utf-8 -*-

#
# Testing vossanto.py
#
# Usage:
#
# Author: rja
#
# Changes:
# 2016-06-12 (rja)
# - initial version

from __future__ import print_function
import re
import unittest
import vossanto

class TestVossanto(unittest.TestCase):

    def test_many(self):
        self.tv("Everybody knows that Helmut Kohl is the Shakespeare of politics.", "Helmut Kohl", "Shakespeare", "politics")
        self.tv("Yesterday, Helmut Kohl - the Shakespeare of politics - talked about cars.", "Helmut Kohl", "Shakespeare", "politics")
        self.tv("Yesterday, Helmut Kohl, the Shakespeare of politics, talked about trees.", "Helmut Kohl", "Shakespeare", "politics")
        self.tv("Angela Merkel is the Woody Allen of Baroque.", "Angela Merkel", "Woody Allen", "Baroque")
        self.tv("Angela Merkel is the Heino of German Literature.", "Angela Merkel", "Heino", "German Literature")
        self.tv("Angela Merkel is the Brad Pitt of Germany.", "Angela Merkel", "Brad Pitt", "Germany")
        self.tv("Angela Merkel is the Mozart of chess.", "Angela Merkel", "Mozart", "chess")
        self.tv("Angela Merkel is the Mozart of mass protest.", "Angela Merkel", "Mozart", "mass protest")
        self.tv("Angela Merkel is the Mozart of 100 meter sprint.", "Angela Merkel", "Mozart", "100 meter sprint")
        self.tv("Angela Merkel is the Mozart of Theology.", "Angela Merkel", "Mozart", "Theology")
        self.tv("Angela Merkel is the Boris Entrup of cow care.", "Angela Merkel", "Boris Entrup", "cow care")
        self.tv("Angela Merkel is the Newton of a blade of grass.", "Angela Merkel", "Newton", "a blade of grass")
        self.tv("Angela Merkel is the Lionel Messi of grill models.", "Angela Merkel", "Lionel Messi", "grill models")
        self.tv("Angela Merkel is the Günter Grass of barbers.", "Angela Merkel", "Günter Grass", "barbers")
        self.tv("Angela Merkel is the Leni Riefenstahl of public opinion polls.", "Angela Merkel", "Leni Riefenstahl", "public opinion polls")
        # does not work: "Homer" is detected as NNP not PERSON
        #self.tv("Angela Merkel is the Homer of insects.", "Angela Merkel", "Homer", "insects")
        # does not work, since "Justin Bieber" is detected as (ORGANIZATION Justin) Bieber/NNP
        #self.tv("Angela Merkel is the Justin Bieber of Cretaceous.", "Angela Merkel", "Justin Bieber", "Cretaceous")
        self.tv("Angela Merkel is the Elvis of Cretaceous.", "Angela Merkel", "Elvis", "Cretaceous")
        self.tv("Angela Merkel is the Elvis of the Cretaceous period.", "Angela Merkel", "Elvis", "the Cretaceous period")
        self.tv("Angela Merkel is the Helmut Kohl among spreads.", "Angela Merkel", "Helmut Kohl", "spreads")
        self.tv("Angela Merkel is the Breton cow of literature.", "Angela Merkel", "Breton cow", "literature")
        self.tv("Angela Merkel is the Jon Bon Jovi of mediators.", "Angela Merkel", "Jon Bon Jovi", "mediators")
        self.tv("Angela Merkel is the Nana Mouskouri of internal security.", "Angela Merkel", "Nana Mouskouri", "internal security")
        self.tv("Angela Merkel is the Mount Everest of masturbation.", "Angela Merkel", "Mount Everest", "masturbation")
        # not yet possible: 
        self.tv("Angela Merkel is the Tuberkulose of the digital age.", "Angela Merkel", "Tuberkulose", "the digital age")
        self.tv("Angela Merkel is the Porsche Cayenne among shoes.", "Angela Merkel", "Porsche Cayenne", "shoes")
        self.tv("Harris has been called the Queen of Country Music.", "Harris", "Queen", "Country Music")
        self.tv("Harris is called the Queen of Country Music.", "Harris", "Queen", "Country Music")
        self.tv("Harris is often called the Queen of Country Music.", "Harris", "Queen", "Country Music")
        self.tv("Harris is sometimes called the Queen of Country Music.", "Harris", "Queen", "Country Music")
        self.tv("Berlin is the New York of Germany.", "Berlin", "New York", "Germany")

    def test_non_vossanto(self):
        self.tnv("This is a simple example of a road.")
        self.tnv("This is a simple example of a fast road.")
        self.tnv("This is a simple example of cancer.")
        self.tnv("Angela Merkel is chancelor of the Federal Republic of Germany.")
        self.tnv("Helmut Kohl is a boring speaker.")

    def tv(self, s, x, y, z):
        self.assertEqual(vossanto.vossanto(s, True), (x, y, z))

    def tnv(self, s):
        self.assertEqual(vossanto.vossanto(s, True), None)
        
if __name__ == '__main__':
    unittest.main()
