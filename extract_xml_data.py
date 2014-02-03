#!/usr/bin/python
#encoding: utf8

__author__ = 'Chancy'

import xml.etree.cElementTree as ET
import os
import re


class XMLParser(object):
    def __init__(self, xml_name):
        self.xml_name = xml_name

        self._do()

    def __str__(self):
        msg = ""
        msg += "%s\t" % os.path.basename(self.xml_name)
        msg += "%s\t" % self.get_title()
        msg += "%s\t" % self.get_author()
        msg += "%s\t" % self.get_date()
        msg += "%s" % self.get_epigraph()

        
        return msg

    def _parse(self, xml_name):
        try:
            xml_string  = file(xml_name, "rb").read()
        except IOError, e:
            raise Exception(e)

        
        xml_string = re.sub(' xmlns="[^"]+"', '', xml_string, count=1)
        return ET.fromstring(xml_string)

    def _do(self):
        self.xml = self._parse(self.xml_name)
        self.xml_root = self.xml

    def get_author(self):
        author = self.xml_root.find("teiHeader/fileDesc/titleStmt/author")
        if not ET.iselement(author):
            return ""

        author_str = ET.tostring(author, encoding="gbk", method="text").strip()
        return author_str

    def get_date(self):
        date = self.xml_root.find("teiHeader/fileDesc/publicationStmt/date")
        if not ET.iselement(date):
            return ""

        date_str = ET.tostring(date, encoding="gbk", method="text").strip()
        return date_str

    def get_title(self):
        title = self.xml_root.find("teiHeader/fileDesc/titleStmt/title")
        if not ET.iselement(title):
            return ""

        title_str = ET.tostring(title, encoding="gbk", method="text").strip()
        return title_str

    def get_epigraph(self):
        return ""


def get_curr_dir_xml_files(path="."):
    lst = os.listdir(path)
    new_lst = []
    for i in lst:
        if os.path.isfile(i) and i.endswith(".xml"):
            if i == "out.xml":
                continue
            new_lst.append(os.path.join(path, i))

    return new_lst


def main():
    #===========================================================================
    # import sys
    # if len(sys.argv) != 2:
    #     print "Usage: %s xml_name" % sys.argv[0]
    #     sys.exit(0)
    # xml_name = sys.argv[1]
    #===========================================================================

    xml_files = get_curr_dir_xml_files()

    import sys
    sys.stdout = file("out.xml", "w")
    #===========================================================================
    #building output xml tree
    #===========================================================================
    xml_data = ET.Element("root")

    for xml_name in xml_files:
        parser = XMLParser(xml_name)

        msg = str(parser)
        msg = msg.decode("gbk")

        filename, title, author, date, epigraph = msg.split("\t")

        channel = ET.Element("channel")

        tag_filename = ET.SubElement(channel, "filename")
        tag_filename.text = filename

        tag_title = ET.SubElement(channel, "title")
        tag_title.text = title

        tag_author = ET.SubElement(channel, "author")
        tag_author.text = author

        tag_date = ET.SubElement(channel, "date")
        tag_date.text = date

        tag_epigraph = ET.SubElement(channel, "epigraph")
        tag_epigraph.text = epigraph

        xml_data.append(channel)

    ET.dump(xml_data)


if __name__ == "__main__":
    main()




