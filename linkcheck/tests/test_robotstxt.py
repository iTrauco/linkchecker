# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Test robots.txt parsing.
"""

import unittest
import linkcheck.robotparser2


class TestRobotsTxt (unittest.TestCase):
    """
    Test string formatting routines.
    """

    def setUp (self):
        """
        Initialize self.rp as a robots.txt parser.
        """
        self.rp = linkcheck.robotparser2.RobotFileParser()

    def test_robotstxt (self):
        lines = [
            "User-agent: *",
        ]
        self.rp.parse(lines)
        self.assert_(self.rp.mtime() > 0)
        self.assertEquals(str(self.rp), "\n".join(lines))

    def test_robotstxt2 (self):
        lines = [
            "User-agent: *",
            "Disallow: /search",
        ]
        self.rp.parse(lines)
        self.assertEquals(str(self.rp), "\n".join(lines))

    def test_robotstxt3 (self):
        lines = [
            "Disallow: /search",
            "",
            "Allow: /search",
            "",
            "Crawl-Delay: 5",
            "",
            "Blabla",
            "",
            "Bla: bla",
        ]
        self.rp.parse(lines)
        self.assertEquals(str(self.rp), "")

    def test_robotstxt4 (self):
        lines = [
            "User-agent: Bla",
            "Disallow: /cgi-bin",
            "User-agent: *",
            "Disallow: /search",
        ]
        self.rp.parse(lines)
        lines.insert(2, "")
        self.assertEquals(str(self.rp), "\n".join(lines))

    def test_robotstxt5 (self):
        lines = [
            "#one line comment",
            "User-agent: Bla",
            "Disallow: /cgi-bin # comment",
            "Allow: /search",
        ]
        lines2 = [
            "User-agent: Bla",
            "Disallow: /cgi-bin",
            "Allow: /search",
        ]
        self.rp.parse(lines)
        self.assertEquals(str(self.rp), "\n".join(lines2))

    def test_robotstxt6 (self):
        lines = [
            "User-agent: Bla",
            "",
        ]
        self.rp.parse(lines)
        self.assertEquals(str(self.rp), "")

    def test_crawldelay (self):
        lines = [
            "User-agent: Blubb",
            "Crawl-delay: 10",
            "",
            "User-agent: Hulla",
            "Crawl-delay: 5",
            "",
            "User-agent: *",
            "Crawl-delay: 1",
        ]
        self.rp.parse(lines)
        self.assertEquals(str(self.rp), "\n".join(lines))
        self.assertEquals(self.rp.get_crawldelay("Blubb"), 10)
        self.assertEquals(self.rp.get_crawldelay("Hulla"), 5)
        self.assertEquals(self.rp.get_crawldelay("Bulla"), 1)

    def test_crawldelay2 (self):
        lines = [
            "User-agent: Blubb",
            "Crawl-delay: X",
        ]
        self.rp.parse(lines)
        del lines[1]
        self.assertEquals(str(self.rp), "\n".join(lines))


def test_suite ():
    """
    Build and return a TestSuite.
    """
    return unittest.makeSuite(TestRobotsTxt)


if __name__ == '__main__':
    unittest.main()
