# Copyright Michael Murphy, 2010
#
# TikzNode class
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

import math, tikzutils

class TikzNode:
    """An element of a visualisation that represents a single set of
    data.
    """
    _mapping_defaults = {
        "xpos" : 0,
        "ypos" : 0,
        "radius" : 1,
        "width" : 1,
        "height" : 1,
        "opacity" : 1,
        "tint" : 0,
        "label" : ""}

    def __init__(self, uid):
        """Create a new node"""
        self.uid = uid
        self.base_color = 'black'
        self.tint_color = 'white'
        self.font = None
        self.shape_options = []
        self.node_options = []
        self.angle_inout = 0

    def map_data(self, data, properties):
        """Map an array of data to an array of internal node
        properties"""
        # if we are given radius, then we must have a circle
        if 'radius' in properties:
            self.shape = 'circle'
            self.radius = data[properties.index('radius')]
        # if we get a height or width, then we have a rectangle
        elif 'height' in properties or 'width' in properties:
            self.shape = 'rectangle'
            if 'width' not in properties:
                self.width = data[properties.index('height')]
                self.height = data[properties.index('height')]
            elif 'height' not in properties:
                self.width = data[properties.index('width')]
                self.height = data[properties.index('width')]
            else:
                self.width = data[properties.index('width')]
                self.height = data[properties.index('height')]
        # otherwise we have a coordinate
        else:
            self.shape = 'coordinate'
        # look for x and y pos
        if 'xpos' in properties and 'ypos' in properties:
            self.xpos = data[properties.index('xpos')]
            self.ypos = data[properties.index('ypos')]
        # look for rotation
        if 'rotation' in properties:
            self.rotation = data[properties.index('rotation')]
        # look for tint
        if 'tint' in properties:
            self.tint = data[properties.index('tint')]
            color = self.tint_color + "!" + str(self.tint) + "!" + self.base_color
        else:
            color = self.base_color
        self.shape_options.append('fill=' + color)
        # look for opacity
        if 'opacity' in properties:
            self.opacity = data[properties.index('opacity')]
            self.shape_options.append('opacity=' + str(self.opacity))
        # look for label
        if 'label' in properties:
            self.label = data[properties.index('label')]

    def tikzcode(self):
        """Returns the tikz code to draw the node"""
        # first, draw the shape (if there is one)
        tex = ""
        if hasattr(self, 'shape') and self.shape in ['circle', 'rectangle']:
            tex += r"\fill"
            if len(self.shape_options):
                options = ', '.join(self.shape_options)
                tex += "[{options}] ".format(options=options)
            tex += "({xpos:.4f},{ypos:.4f}) {shape!s} ".format(
                xpos = self.getdefattr('xpos'),
                ypos = self.getdefattr('ypos'),
                shape = self.shape)
            if self.shape is 'circle':
                tex += "({radius!s})".format(
                    radius = self.getdefattr('radius'))
            else:
                tex += "+({width!s}, {height!s})".format(
                    width = self.getdefattr('width'),
                    height = self.getdefattr('height'))
            tex += ";\n"
        tex += r"\node"
        # then draw the node
        node_options = []
        if self.font:
            node_options.append("font=\{font}".format(font=self.font))
        if len(node_options):
            options = ', '.join(node_options)
            tex += "[{options}] ".format(options=options)
        tex += "({self.uid}) at ({self.xpos:.4f},{self.ypos:.4f}) ".format(self=self)
        tex += "{" + self.getdefattr('label') + "} ;\n"
        # finally, draw a label text
        return tex

    def show(self):
        """Print out all information about the node"""
        print "## Node information"
        for p in ['uid', 'shape', 'xpos', 'ypos', 'radius',
                  'width', 'height', 'rotation']:
            print p, ':', getattr(self, p, 'not defined')
        print self.tikzcode()
        
    def getdefattr(self, attribute):
        """Returns the value of an attribute, or its default value if
        the attribute is not yet set"""
        return getattr(self, attribute, TikzNode._mapping_defaults[attribute])
