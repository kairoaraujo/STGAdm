#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class Fields:
    """ This class verify if the fields used is blank or contain spaces.

        Args:
          field (str): The filed variable, like 'name', 'change' etc...
          textfield (stg): The question for the field, like 'Whats de LPAR name'
                           'Whats the change number' etc .
    """

    def __init__(self, field, textfield, variable=''):
        """ Initial to get field and textField arguments. """

        self.field = field
        self.textfield = textfield
        self.variable = variable

    def chkfieldstr(self):
        """ Check field strings doesn't has a blank or spaces. """

        while True:

            self.variable = raw_input('{0}'.format(self.textfield))
            if (self.variable.isspace()) or (self.variable == '') or \
                    (' ' in self.variable):
                print ("{0} can not be blank or contain spaces".
                       format(self.field))

            elif not re.match("^[A-Za-z0-9_-]*$", self.variable):
                print ("{0} can be only letters and numbers.".
                       format(self.field))

            else:
                break

    def strvarout(self):
        """ Returns the answer to question field. """

        return self.variable


class YesNo:
    """ A simple class to do questions and check the answer is y/n (yes or no).

        Args:
          question(str): The question do want to do like 'It is correct?'.
          answer(str): initial answer (default answer) y or n.

    """

    def __init__(self, question, answer):
        """ Get the args. """

        self.question = question
        self.answer = answer

    def check(self):
        """ Text menu to do question and check the answer. """

        check_ok = 0
        while check_ok == 0:
            self.answer = raw_input('{0}'.format(self.question))
            if (self.answer == 'y') or (self.answer == 'Y'):
                self.answer = 'y'
                check_ok = 1

            elif (self.answer == 'n') or (self.answer == 'N'):
                self.answer = 'n'
                check_ok = 1

            else:
                print ('Please use y or n!')
                check_ok = 0

        return self.answer
