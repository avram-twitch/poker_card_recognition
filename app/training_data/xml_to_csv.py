import xml.etree.ElementTree as ET
import pandas as pd
import csv
import os
import re


def read_xml(fp):
    """
    Really just getting the two xmin/ymin to xmax/ymax pairs
    for the two instances of the card label. The label will be
    in the filename
    """

    tree = ET.parse(fp)
    root = tree.getroot()
    width = root.find("size").find("width").text
    height = root.find("size").find("height").text

    out = []

    # Should have two...
    for member in root.findall('object'):
        bndbox = member.find("bndbox")
        box = {
            'xmin': bndbox.find("xmin").text,
            'ymin': bndbox.find("ymin").text,
            'xmax': bndbox.find("xmax").text,
            'ymax': bndbox.find("ymax").text,
            'height': height,
            'width': width
        }
        out.append(box)
    return out


def _get_filenames(in_directory):
    """
    Returns all filenames in in_directory
    """
    out = []
    for start, dirs, files in os.walk(in_directory):
        for name in files:
            # out.append(os.path.join(in_directory, name))
            out.append(name)
    
    return out


def _get_label_text(filename, text_to_label_mapping):
    """
    Extracts the Text label and integer label from the filename
    (Files are of the form 'cards-[{TEXT_LABEL}]-N.xml')
    """
    text = re.search(r'cards-\[([HDCSW].)\].*xml', filename).group(1)
    if "W" in text:
        return None, None
    label = text_to_label_mapping[text.lower()]
    return int(label), text


def _get_mapper(map_fp):
    """
    Return dictionary that maps text labels to int labels
    """
    out = {}
    with open(map_fp) as f:
        for line in f:
            label, text = line.split(": ")
            out[text.strip().lower()] = label
    return out


def create_csv(output_file, xml_directory, mapper_file):
    mapper = _get_mapper(mapper_file)
    column_name = [
        "filename",
        "width",
        "height",
        "label",
        "text",
        "xmin",
        "ymin",
        "xmax",
        "ymax"
    ]
    rows = []

    for filename in _get_filenames(xml_directory):
        fp = os.path.join(xml_directory, filename)
        label, text = _get_label_text(fp, mapper)
        if label is None:
            continue

        for box in read_xml(fp):
            row = [
                filename,
                box['width'],
                box['height'],
                label,
                text.lower(),
                box['xmin'],
                box['ymin'],
                box['xmax'],
                box['ymax']
            ]
            rows.append(row)

    df = pd.DataFrame(rows, columns=column_name)
    df.to_csv(output_file, index=None)


if __name__=='__main__':
    xml_directory = "./labeled_jpgs/"
    mapper_file = _get_mapper("./labels.txt")
    output_file = "./data.csv"
    create_csv(output_file, xml_directory, mapper_file)
