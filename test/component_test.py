import unittest
from apphost.default_components import Bootstrap, JQuery, MobileApp, Tether, UTF8Charset, BootstrapCDN, JQueryCDN, TetherCDN, ApplicationCSS, ApplicationJS


class ComponentTest(unittest.TestCase):
    def testBootstrap4(self):
        content = Bootstrap().render()
        self.assertTrue("bootstrap4.min.css" in content)
        self.assertTrue("bootstrap4.min.js" in content)

    def testJquery311(self):
        content = JQuery().render()
        self.assertTrue("jquery3.1.1.min.js" in content)

    def testTether140(self):
        content = Tether().render()
        self.assertTrue("tether1.4.0.min.js" in content)

    def testStylesheet(self):
        content = ApplicationCSS().render()
        self.assertTrue("application.css" in content)

    def testJavascript(self):
        content = ApplicationJS().render()
        self.assertTrue("application.js" in content)

    def testBootstrap4CDN(self):
        content = BootstrapCDN().render()
        self.assertTrue("bootstrap.min.css" in content)
        self.assertTrue("bootstrap.min.js" in content)

    def testJquery311CDN(self):
        content = JQueryCDN().render()
        self.assertTrue("jquery-3.1.1.slim.min.js" in content)

    def testTether140CDN(self):
        content = TetherCDN().render()
        self.assertTrue("tether.min.js" in content)