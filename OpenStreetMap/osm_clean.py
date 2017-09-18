import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE_sample = "istanbul_turkey.osm"
regex_street = re.compile(r'\b\S+\.?', re.IGNORECASE)
regex_postalcode = re.compile(r'^\d{5}$')

expected = [ "Izmir" , "Izkent" , "Sirinkapi", "Istikbal" , "Gaziosmanpasa", "University" ,"Coast" ,"Road", "Avenue","Airport","Street","Port","Boulevard", "Neighborhood" ,"Campus", "Square", "Shopping Center" ,"Highway"]  # expected names in the dataset

mapping = {"istanbul" : "Istanbul",
           "�st" : "Istanbul",
           "Ist" : "Istanbul",
           "ist" : "Istanbul",
           "sk." : "Street",
           "Sk." : "Street",
           "Sk" : "Street",
           "sk" : "Street",
           "Sokak" : "Street",
           "Sok." : "Street",
           "sokak" : "Street",
           "Soka��" : "Street",
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
           "�" : "I",
           "�" : "i",
           "�" : "S",
           "�" : "s",
           "�" : "g",
           "Havaliman�" : "Airport",
           "Haval�man�" : "Airport",
           "havaliman�" : "Airport",
           "Liman" : "Port",
           "liman": "Port",
           "�irinyer" : "Sirinyer",
           "Bulvar" : "Boulevard",
           "Blv." : "Boulevard",
           "Bulv.": "Boulevard",
           "Bulvari" : "Boulevard",
           "bulvar�": "Boulevard",
           "Bulvar�": "Boulevard",
           "Mh" : "Neighborhood",
           "mh": "Neighborhood",
           "mahallesi": "Neighborhood",
           "Mahallesi": "Neighborhood",
           "Mah," : "Neighborhood",
           "Mah.": "Neighborhood",
           "Mh.," : "Neighborhood",
           "Yerle�kesi" : "Campus",
           "Meydan�" : "Square",
           "Meydan" : "Square",
           "�irinkap�" : "Sirinkapi",
           "�stikbal" : "Istikbal",
           "Gaziosmanpa�a" : "Gaziosmanpasa",
           "�stiklal" : "Istiklal",
           "sahil" : "Coast",
           "sahili" : "Coast",
           "�skele" : "Port",
           "�skelesi" : "Port",
           "Al��veri� Merkezi": "Shopping Center",
           "Pa�a" : "Pasa" ,
           "�ehitleri" : "Sehitleri",
           "�evre Yolu" : "Highway",
           "�niversite" : "University"
           }

# Search string for the regex. If it is matched and not in the expected list then add this as a key to the set.
def audit_key(default_dicts, attribute, key):
    if(key == "street"):
        m = regex_street.search(attribute)
    elif (key == "postcode"):
        m = regex_postalcode.search(attribute)
    if m:
        default_dict = m.group()
        if(key == "street"):
            if default_dict not in expected:
                default_dicts[default_dict].add(attribute)
        

def is_expected_key(elem, key):  # Check if it is a street name
    expected_key = "addr:"+key
    return (elem.attrib['k'] == expected_key)

def audit(osmfile, key):  # return the list that satify the above two functions
    osm_file = open(osmfile, "r")
    default_dict = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_expected_key(tag, key):
                    audit_key(default_dict, tag.attrib['v'], key)

    return default_dict


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


update_street = audit(OSMFILE_sample,"street")

# print the updated names
for street_type, ways in update_street.items():
    for name in ways:
        better_name = update_name(name, mapping)

update_postcode = audit(OSMFILE_sample,"postcode")

# print the updated names
for postcode_type, ways in update_postcode.items():
    for name in ways:
        better_name = update_name(name, mapping)

