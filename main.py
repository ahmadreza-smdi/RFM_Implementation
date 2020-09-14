# 1st step: importing data from xml file

import xml.etree.ElementTree as ET

tree = ET.parse('post.xml')
root = tree.getroot()

first_Creation_Date = root[0].attrib['CreationDate']
max_Creation_Date = first_Creation_Date
for i in range(len(root)):
    if max_Creation_Date < root[i].attrib['CreationDate']:
        max_Creation_Date = root[i].attrib['CreationDate']
    else:
        pass
print(max_Creation_Date)

# for i in range(len(root)):
#     print(root[i].attrib['CreationDate'])


# print(root[1].attrib)
