"""
SVG to PNG

For each cattributes, extract the unique features.
"""

import argparse
import json
import os

import xml.etree.ElementTree as ET


PATH_COLOR     = "cattributes/colors.json"
PATH_EYE_SHAPE = "cattributes/eye/"
PATH_BODY      = "cattributes/body/"
PATH_MOUTH     = "cattributes/mouth/"

PATH_SAVE_EYE = "templates/eye_svg/"
PATH_SAVE_EYE_PNG = "templates/eye_png/"
PATH_SAVE_MOUTH = "templates/mouth/"
PATH_SAVE_BODY = "templates/body_svg/"
PATH_SAVE_BODY_PNG = "templates/body_png/"


def keep_ary(tree, name="PRIMARY"):
    lst_rm = []

    for ch in tree.getchildren():
        if "fill" in ch.attrib:
            if ("ARY" in ch.attrib["fill"]) & (name not in ch.attrib["fill"]):
                lst_rm.append(ch)
                continue
        else:
            keep_ary(ch, name)

    for x in lst_rm:
        tree.remove(x)

    return tree

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('action', choices=["extract", "to_png"], type=str,
            help='First: extract. Second: to_png.')
    parser.add_argument('-W', type=int, default=1000,
                    help='Pixel width.')

    args = parser.parse_args()
    
    if args.action == "extract":
        with open(PATH_COLOR, "r") as fp:
            dic_colors = json.load(fp)

        dic_col_eye = dic_colors["EyeColor"]
        del(dic_colors["EyeColor"])

        # Process eyes
        files = os.listdir(PATH_EYE_SHAPE)
        os.makedirs(PATH_SAVE_EYE, exist_ok=True)
        for file in files:
            print("Eye file: {}".format(file))
            with open(PATH_EYE_SHAPE + file, "r") as fp:
                data = fp.read()
        
            # Replace color by a place-holder
            for c in dic_col_eye.values():
                data = data.replace(c, "[EYE_COLOR]")

            # Save the new svg
            for n, c in dic_col_eye.items():
                data_i = data.replace("[EYE_COLOR]", c)
                with open(PATH_SAVE_EYE + "{}_{}".format(n, file), "w") as fp:
                    fp.write(data_i)

        # Process body
        os.makedirs(PATH_SAVE_BODY, exist_ok=True)
        for file in os.listdir(PATH_BODY):
            data = None
            with open("{}{}".format(PATH_BODY, file), "r") as fp:
                data = fp.read()
    
            for name, palette in dic_colors.items():
                NAME = name.upper()
                for c in palette.values():
                    data = data.replace(c, "[{}]".format(NAME))
    
            # Primary block
            #print("Primary color")
            root = ET.fromstring(data)
            root = keep_ary(root, "PRIMARY")
            transformed = ET.tostring(root).decode()
            for n, c in dic_colors["Primary"].items(): # n: name of the color
                transformed_i = transformed.replace("[PRIMARY]", c)
                with open("{}{}-P_{}.svg".format(PATH_SAVE_BODY, file[:-4], n), "w") as fp:
                    fp.write(transformed_i)

            # Secondary block
            #print("Secondary color")
            root = ET.fromstring(data)
            root = keep_ary(root, "SECONDARY")
            transformed = ET.tostring(root).decode()
            for n, c in dic_colors["Secondary"].items(): # n: name of the color
                transformed_i = transformed.replace("[SECONDARY]", c)
                with open("{}{}-S_{}.svg".format(PATH_SAVE_BODY, file[:-4], n), "w") as fp:
                    fp.write(transformed_i)

    
            # Tertiary block
            #print("Tertiary color")
            root = ET.fromstring(data)
            root = keep_ary(root, "TERTIARY")
            transformed = ET.tostring(root).decode()
    
            for n, c in dic_colors["Tertiary"].items(): # n: name of the color
                transformed_i = transformed.replace("[TERTIARY]", c)
                with open("{}{}-T_{}.svg".format(PATH_SAVE_BODY, file[:-4], n), "w") as fp:
                    fp.write(transformed_i)

    else:
        W = args.W

        os.makedirs(PATH_SAVE_MOUTH, exist_ok=True)
        os.makedirs(PATH_SAVE_EYE_PNG, exist_ok=True)
        os.makedirs(PATH_SAVE_BODY_PNG, exist_ok=True)

        # Mouth
        svg_files = os.listdir(PATH_MOUTH)
        for file in svg_files:
            print(file)
            os.system('inkscape {}{} -e {}{}.png -w={}'.format(PATH_MOUTH, file, 
                PATH_SAVE_MOUTH, file[:-4], W))
        
        # Eyes
        svg_files = os.listdir(PATH_SAVE_EYE)
        for file in svg_files:
            print(file)
            os.system('inkscape {}{} -e {}{}.png -w={}'.format(PATH_SAVE_EYE, file, 
                PATH_SAVE_EYE_PNG, file[:-4], W))

        # Body
        svg_files = os.listdir(PATH_SAVE_BODY)
        for file in svg_files:
            print(file)
            os.system('inkscape {}{} -e {}{}.png -w={}'.format(PATH_SAVE_BODY, file, 
                PATH_SAVE_BODY_PNG, file[:-4], W))
    
