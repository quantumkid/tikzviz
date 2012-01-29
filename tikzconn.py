# Copyright Michael Murphy, 2010
#
# TikzConnector class
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

class TikzConnector:
    """An element of a visualisation that joins two nodes together"""
    def __init__(self, node_a, node_b):
        """Create a new connector"""
        self.node_a = node_a
        self.node_b = node_b
        self.base_color = 'blue'
        self.tint_color = 'white'
        self.tint = 0
        self.options = []

    def map_data(self, data, properties):
        """Map an array of data to an array of internal connector
        properties"""
        # look for width
        if 'width' in properties:
            self.width = data[properties.index('width')]
            self.options.append('line width=' + str(self.width))
        # look for tint
        if 'tint' in properties:
            self.tint = data[properties.index('tint')]
            color = self.tint_color + "!" + str(self.tint) + "!" + self.base_color
        else:
            color = self.base_color
        self.options.append('draw=' + color)
        # look for opacity
        if 'opacity' in properties:
            self.opacity = data[properties.index('opacity')]
            self.options.append('opacity=' + str(self.opacity))

    def tikzcode(self):
        """Returns the tikz code to draw the connector"""
        tex = ""
        tex += r"\draw"
        if len(self.options):
            options = ', '.join(self.options)
            tex += "[{options}] ".format(options=options)
        tex += "({a.xpos:.4f},{a.ypos:.4f}) ".format(a=self.node_a)
        tex += "to"
        # if the nodes are arranged, then they have angle in/out
        inout = []
        inout.append('out={angle!s}'.format(angle=self.node_a.angle_inout))
        inout.append('in={angle!s}'.format(angle=self.node_b.angle_inout))
        if inout:
            tex += "[" + ", ".join(inout) + "] "
        tex += "({b.xpos:.4f},{b.ypos:.4f})".format(b=self.node_b)
        tex += ";\n"
        return tex
