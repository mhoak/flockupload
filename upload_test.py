#!/usr/bin/env python
# pylint: disable=missing-docstring

import unittest
import upload as u

def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    	
    def test_simplistic_regex(self):
    	self.assertTrue(u.simple_regex_check(u.pre_compile_regex('.git'), '.git'))
    	self.assertFalse(u.simple_regex_check(u.pre_compile_regex('.git'), 'turtle'))
    	#Directories should be filtred out on their, so this should not match
    	self.assertFalse(u.simple_regex_check(u.pre_compile_regex('.git'), '.git/something'))
    	self.assertTrue(u.simple_regex_check(u.pre_compile_regex('*.py'), 'something.com.py'))
    	self.assertFalse(u.simple_regex_check(u.pre_compile_regex('*.py'), 'something.com.py.something'))



def testmain():
    unittest.main()

if __name__ == '__main__':
    testmain()

# print should_prune('index.html'), ' Should be False'
