import unittest
import upload

def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
    	self.assertTrue(simplistic_regex('.git', '.git'))
    	
    def test_simplistic_regex():
    	
    	self.assertTrue(simplistic_regex('.git', '.git'))

    	self.assertFalse(simplistic_regex('.git', 'turtle'))
    	#Directories should be filtred out on their, so this should not match
    	self.assertFalse(simplistic_regex('.git', '.git/something'))
    	self.assertTrue(simplistic_regex('*.py', 'something.com.py'))
    	self.assertFalse(simplistic_regex('*.py', 'something.com.py.something'))



def main():
    unittest.main()

if __name__ == '__main__':
    main()

# print should_prune('index.html'), ' Should be False'
