#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Fields:
    """ This class verify if the fields used is blank or contain spaces.

        Args:
          field (str): The filed variable, like 'name', 'change' etc...
          textField (stg): The question for the field, like 'Whats de LPAR name'
                           'Whats the change number' etc .
    """

    def __init__(self, field, textfield, variable=''):
        """ Initial to get field and textField arguments. """

        self.field = field
        self.textField = textfield
        self.variable = variable

    def chkfieldstr(self):
        """ Check field strings doesn't has a blank or spaces. """

        while True:

            self.variable = raw_input('{0}'.format(self.textField))
            if (self.variable.isspace()) or (self.variable == '') or \
                    (' ' in self.variable):
                print ("{0} can not be blank or contain spaces".
                       format(self.field))
            else:
                break

    def strvarout(self):
        """ Returns the answer to question field. """

        return self.variable
