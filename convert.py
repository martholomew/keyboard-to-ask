#!/bin/python

import sys
from lxml import etree as et


android_ns = "{http://schemas.android.com/apk/res/android}"
ask_ns = "{http://schemas.android.com/apk/res-auto}"
ns_map = {
    "android": "http://schemas.android.com/apk/res/android",
    "ask": "http://schemas.android.com/apk/res-auto"
}


def xml_shiz(keyboard):
    rows = [key for key in keyboard if "s" not in key]
    xml_root = et.Element("Keyboard", nsmap=ns_map)
    width = str(100 / max([len(keyboard[row]) for row in rows]))[:4] + "%p"
    xml_root.attrib[android_ns + "keyWidth"] = width
    xml_root.attrib[android_ns + "keyHeight"] = "@integer/key_normal_height"
    xml_root.attrib[ask_ns + "autoCap"] = "false"
    for row in rows:
        left = False
        right = False
        xml_row = et.SubElement(xml_root, "Row")
        if row == rows[-1]:
            left = True
            right = True
            xml_key = et.SubElement(xml_row, "Key")
            xml_key.attrib[android_ns + "keyEdgeFlags"] = "left"
            xml_key.attrib[android_ns + "codes"] = "@integer/key_code_shift"
            xml_key.attrib[android_ns + "isModifier"] = "true"
            xml_key.attrib[android_ns + "isSticky"] = "true"
        for i in range(len(keyboard[row])):
            xml_key = et.SubElement(xml_row, "Key")
            if i == 0 and not left:
                xml_key.attrib[android_ns + "keyEdgeFlags"] = "left"
            elif i == len(keyboard[row]) - 1 and not right:
                xml_key.attrib[android_ns + "keyEdgeFlags"] = "right"
            shift_key = keyboard[row + "s"][i]
            key = keyboard[row][i].split(',')
            key = [k.lstrip().rstrip() for k in key]
            key = [k for k in key if k != shift_key or k == key[0]]
            print(key)
            if len(key[0]) == 1:
                xml_key.attrib[android_ns + "codes"] = key[0]
            else:
                xml_key.attrib[ask_ns + "keyOutputText"] = key[0]
                xml_key.attrib[ask_ns + "keyLabel"] = key[0]
            if len(key) > 1:
                xml_key.attrib[android_ns + "popupCharacters"] = ''.join(key[1:])
            if len(shift_key) == 1:
                xml_key.attrib[ask_ns + "shiftedCodes"] = shift_key
            else:
                xml_key.attrib[ask_ns + "shiftedKeyOutputText"] = shift_key
                xml_key.attrib[ask_ns + "shiftedKeyLabel"] = shift_key
        if row == rows[-1]:
            left = True
            right = True
            xml_key = et.SubElement(xml_row, "Key")
            xml_key.attrib[android_ns + "keyEdgeFlags"] = "right"
            xml_key.attrib[android_ns + "codes"] = "@integer/key_code_delete"
            xml_key.attrib[android_ns + "isRepeatable"] = "true"
    with open(str(sys.argv[1].split('.')[0]) + ".xml", "w") as f:
        f.write(et.tostring(xml_root, encoding='unicode', method='xml', pretty_print=True))




if __name__ == "__main__":
    file_name = sys.argv[1]
    with open(file_name, "r") as f:
        lines = f.readlines()
    headers = ["1", "1s", "2", "2s", "3", "3s", "4", "4s"]
    keyboard = {}
    for line in lines:
        line = line.rstrip()
        if line in headers:
            header = line
            keyboard[header] = []
        else:
            keyboard[header].append(line)
    if len(keyboard["1"]) != len(keyboard["1s"]):
        print("Issue on row 1.")
        exit()
    if len(keyboard["2"]) != len(keyboard["2s"]):
        print("Issue on row 2.")
        exit()
    if len(keyboard["3"]) != len(keyboard["3s"]):
        print("Issue on row 3.")
        exit()
    if len(keyboard["4"]) != len(keyboard["4s"]):
        print("Issue on row 4.")
        exit()
    xml_shiz(keyboard)
