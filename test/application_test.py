import unittest
from apphost.application import Application
from application.unittest import Unittest


class ApplicationTest(unittest.TestCase):

    def setUp(self):
        self.app = Application()

    def testRenderHTML(self):
        content = self.app.html()
        self.assertTrue('''<!DOCTYPE html>''' in content)
        self.assertTrue('''<html lang="en">''' in content)
        self.assertTrue('''bootstrap4.min.js''' in content)
        self.assertTrue('''My Application''' in content)

    def testRenderKwargs(self):
        content = self.app.html(title="unique_string") # send title from html() all the way to
        self.assertTrue('''unique_string''' in content)

    def testCustomApp(self):
        self.app = Unittest()
        content = self.app.html()
        self.assertTrue('''<!DOCTYPE html>''' in content)
        self.assertTrue('''<html lang="en">''' in content)
        self.assertTrue('''bootstrap.min.js''' in content)
        self.assertTrue('''4.0.0-alpha.6''' in content)
        self.assertTrue('''ajax''' in content)
        self.assertTrue('''tether.min.js''' in content)
        self.assertTrue('''code.jquery''' in content)
        self.assertTrue('''My Application''' in content)


