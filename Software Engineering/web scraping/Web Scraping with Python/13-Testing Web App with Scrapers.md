[TOC]

# Testing Web App with Scrapers

most of the time web app testing is testing on backend apis, frontend have less testing frameworks, scraping could be a good approach on testing frontend. instead of just checking manually on a checklist, we could from a series of unit tests and replace human for the testing.

## intro to testing

unit test or just simply 'test' generally has the characteristics below

- each test tests one aspect of the functionality of a component. often unit tests are grouped together in the same class based on the component they are testing. eg. testing on drawing -ve value from bank + drawing +ve value from bank
- each test can be run independently and any setup or teardown required for the test must be handled by the unit itself. independent in the sense unit test A outcome should not affect test B outcome nor the sequence of events matters
- each unit test contains at least one assertion, and occasionally contain only failure state
- unit tests are separated from the bulk of code, different directory different class. all necessary imports is done in the test script

there are other test that can be written - validation test, integration test but given the trend of TDD and the build in functionality of python unit test is the focus here.

example code

```python
import unittest

class TestAddition(unittest.TestCase):
    def setUp(self): # setup will be run before every test, if its not required we can use setUpClass instead
        print('setting up')
    def tearDown(self):
        print('teardown')
    def test_twoPlusTwo(self): # test_ is the convention for unittest to recognize the test
        total = 2 + 2
        self.assertEqual(4, total)
if __name__ == '__main__':
    unittest.main()
```

## note on testing with selenium

selenium test can be done more casually with, although there is no stopping of combining both unittest module and selenium package

```python
driver = webdriver.PhantomJS()
driver.get('link')
assert 'text' in driver.title
driver.close()
```

why selenium?

if we test with just requests, we could miss out actually interaction with the interface, selenium can help us by providing functions eg. click, click and hold, release, double click, send keys and etc. beside these common interaction, selenium can also accomplish drag-and-drop operation and taking screenshots