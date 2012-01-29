# Copyright Michael Murphy, 2010
#
# TikzViz class
#
# This file is part of the tikzviz module for python
#
# tikzviz is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 2 of the License, or (at your
# option) any later version.
#
# tikzviz is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with tikzviz. If not, see <http://www.gnu.org/licenses/>.

import math, sys
from operator import attrgetter
from tikznode import TikzNode
from tikzconn import TikzConnector

class TikzViz:
    def __init__(self):
        """Create a new visualisation from nodes, connectors, labels,
        and axes"""
        self.nodes = []
        self.connectors = []
        self.fonts = {}
        self.defaultfont = ""
        self.background_color = ""

    def add_node(self, uid):
        """Add a node to the visualisation and returns a reference to
        it"""
        n = TikzNode(uid)
        if self.defaultfont:
            n.font = self.defaultfont
        self.nodes.append(n)
        return n

    def add_connector(self, a, b):
        """Add a node to the visualisation and returns a reference to
        it"""
        c = TikzConnector(a, b)
        self.connectors.append(c)
        return c

    def add_font(self, fontext):
        """Add a font for use in text"""
        fontint = fontext.lower().translate(None, " ")
        self.fonts[fontext] = fontint

    def set_default_font(self, fontext):
        """Sets the default font for newly created nodes"""
        if fontext in self.fonts:
            self.defaultfont = self.fonts[fontext]
        else:
            print "I don't know the font", fontext

    def preamble(self):
        """Preamble for the output tex file"""
        tex = "\usemodule[tikz]\n\n"
        #tex += "\input colorfix\n"
        for fontext, fontint in self.fonts.iteritems():
            tex += "\definefont[{0}][name:{1}]\n".format(fontint, fontext)
        tex += "\usetikzlibrary[backgrounds]"
        tex += "\input tikzcolors\n"
        tex += "\starttext\n\n"
        return tex

    def postamble(self):
        """Postamble for the output tex file"""
        tex = "\stoptext\n"
        return tex

    def prepicture(self):
        """Code before each picture for the output tex file"""
        tex = "\startTEXpage\n"
        tex += "\starttikzpicture\n"
        if self.background_color:
            tex += "[background rectangle/.style={fill="
            tex += self.background_color
            tex += "}, show background rectangle]\n\n"
        return tex

    def postpicture(self):
        """Code after each picture for the output tex file"""
        tex = "\stoptikzpicture\n"
        tex += "\stopTEXpage\n"
        return tex

    def arrange_in_circle(self, padding, sort=False, reverse=False):
        """Arranges the node in a circle, each taking up a proportional
        part of the circle"""
        # get the approximate total size of the circle
        total_c = sum([2*getattr(node, 'radius', 0) for node in self.nodes])
        # get the radius of a circle with a slightly larger circumference
        radius = ((1 + padding) * total_c) / (2 * math.pi)
        # possibly sort the nodes
        if sort:
            nodes = sorted(self.nodes, key=attrgetter('radius'), reverse=reverse)
        else:
            nodes = self.nodes
        # arrange the nodes around the circle
        angle = 0
        for node in nodes:
            angle += 2 * math.pi * node.radius / total_c
            node.xpos = radius * math.cos(angle)
            node.ypos = radius * math.sin(angle)
            node.angle_inout = -180 + math.trunc(angle * 180 / math.pi)
            angle += 2 * math.pi * node.radius / total_c

    def arrange_in_list(self, padding, sort=False, reverse=False):
        """Arranges the node in a list, each taking up a proportional
        part of the list"""
        if sort:
            nodes = sorted(self.nodes, key=attrgetter('radius'), reverse=reverse)
        else:
            nodes = self.nodes
        y = 0
        for node in nodes:
            y += node.radius
            node.xpos = 0
            node.ypos = y
            node.angle_inout = 0
            y += node.radius
            y += padding

    def writetikzpicture(self, filename):
        """Ouputs the entire tex file"""
        try:
            f = open(filename, "w")
        except:
            print "filename", filename, "not valid, or you do not have",
            "sufficient permissions to create the file"
            sys.exit()
        f.write(self.preamble())
        f.write(self.prepicture())
        for conn in self.connectors:
            f.write(conn.tikzcode())
        for node in self.nodes:
            f.write(node.tikzcode())
        f.write(self.postpicture())
        f.write(self.postamble())
