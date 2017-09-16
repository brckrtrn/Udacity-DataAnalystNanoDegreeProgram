# -*- coding: utf-8 -*-
"""
Rules:
* We process only top level tags: **"node"**, **"way"**
* We create two csv files of "node". One with empty child node called **nodes.csv** and other with "tag" child node called **nodes_tags.csv**
* We create three csv files of "way". One with empty child node called **ways.csv**, other with "nd" child node called **ways_nodes.csv** and one with "tag" child node called **ways_tags.csv**
* If the tag "k" value contains problematic characters, the tag should be ignored
* If the tag "k" value contains a ":" the characters before the ":" should be set as the tag type
  and characters after the ":" should be set as the tag key"""

import csv
import codecs
import re
import xml.etree.cElementTree as ET
import schema
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

OSM_PATH = "istanbul_turkey.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

mapping = {"istanbul" : "Istanbul",
           "İst" : "Istanbul",
           "Ist" : "Istanbul",
           "ist" : "Istanbul",
           "sk." : "Street",
           "Sk." : "Street",
           "Sk" : "Street",
           "sk" : "Street",
           "Sokak" : "Street",
           "Sok." : "Street",
           "sokak" : "Street",
           "Sokağı" : "Street",
           "Sokak," : "Street",
           "Cd" : "Avenue",
           "Cd,": "Avenue",
           "cd" : "Avenue",
           "Cd." : "Avenue",
           "cd." : "Avenue",
           "Cad." : "Avenue",
           "Cad" : "Avenue",
           "Caddesi" : "Avenue",
           "caddesi" : "Avenue",
           "İ" : "I",
           "ı" : "i",
           "Ş" : "S",
           "ş" : "s",
           "ğ" : "g",
           "Havalimanı" : "Airport",
           "Havalımanı" : "Airport",
           "havalimanı" : "Airport",
           "Liman" : "Port",
           "liman": "Port",
           "Şirinyer" : "Sirinyer",
           "Bulvar" : "Boulevard",
           "Blv." : "Boulevard",
           "Bulv.": "Boulevard",
           "Bulvari" : "Boulevard",
           "bulvarı": "Boulevard",
           "Bulvarı": "Boulevard",
           "Mh" : "Neighborhood",
           "mh": "Neighborhood",
           "mahallesi": "Neighborhood",
           "Mahallesi": "Neighborhood",
           "Mah," : "Neighborhood",
           "Mah.": "Neighborhood",
           "Mh.," : "Neighborhood",
           "Yerleşkesi" : "Campus",
           "Meydanı" : "Square",
           "Meydan" : "Square",
           "Şirinkapı" : "Sirinkapi",
           "İstikbal" : "Istikbal",
           "Gaziosmanpaşa" : "Gaziosmanpasa",
           "İstiklal" : "Istiklal",
           "sahil" : "Coast",
           "sahili" : "Coast",
           "İskele" : "Port",
           "İskelesi" : "Port",
           "Alışveriş Merkezi": "Shopping Center",
           "Paşa" : "Pasa" ,
           "Şehitleri" : "Sehitleri",
           "Çevre Yolu" : "Highway",
           "Üniversite" : "University"
           }

def string_case(s):  # change string into titleCase except for UpperCase
    if s.isupper():
        return s
    else:
        return s.title()

# return the updated names
def update_name(name, mapping):
    name = name.split(' ')
    for i in range(len(name)):
        if name[i] in mapping:
            name[i] = mapping[name[i]]
            name[i] = string_case(name[i])
        else:
            name[i] = string_case(name[i])

    name = ' '.join(name)

    return name

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []

    if element.tag == 'node':
        for attrib in element.attrib:
            if attrib in NODE_FIELDS:
                node_attribs[attrib] = element.attrib[attrib]

        for child in element:
            node_tag = {}
            if LOWER_COLON.match(child.attrib['k']):
                node_tag['type'] = child.attrib['k'].split(':', 1)[0]
                node_tag['key'] = child.attrib['k'].split(':', 1)[1]
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = update_name(child.attrib['v'],mapping)
                tags.append(node_tag)
            elif PROBLEMCHARS.match(child.attrib['k']):
                continue
            else:
                node_tag['type'] = 'regular'
                node_tag['key'] = child.attrib['k']
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = update_name(child.attrib['v'],mapping)
                tags.append(node_tag)

        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':
        for attrib in element.attrib:
            if attrib in WAY_FIELDS:
                way_attribs[attrib] = element.attrib[attrib]

        position = 0
        for child in element:
            way_tag = {}
            way_node = {}

            if child.tag == 'tag':
                if LOWER_COLON.match(child.attrib['k']):
                    way_tag['type'] = child.attrib['k'].split(':', 1)[0]
                    way_tag['key'] = child.attrib['k'].split(':', 1)[1]
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = update_name(child.attrib['v'],mapping)
                    tags.append(way_tag)
                elif PROBLEMCHARS.match(child.attrib['k']):
                    continue
                else:
                    way_tag['type'] = 'regular'
                    way_tag['key'] = child.attrib['k']
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = update_name(child.attrib['v'],mapping)
                    tags.append(way_tag)

            elif child.tag == 'nd':
                way_node['id'] = element.attrib['id']
                way_node['node_id'] = child.attrib['ref']
                way_node['position'] = position
                position += 1
                way_nodes.append(way_node)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Function                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'w') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = csv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = csv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    process_map(OSM_PATH, validate=True)

