# /usr/bin/env python3
"""
Generate your cat using a CLI
"""

import argparse
import json
import os

BASE = "cattributes/"

if __name__ == "__main__":
    

    with open("cattributes/colors.json", "r") as fp:
        colors = json.load(fp)

    eye_shapes = sorted(map(lambda x: x[:-4], os.listdir("cattributes/eye/")))    
    mouth_shapes = sorted(map(lambda x: x[:-4], os.listdir("cattributes/mouth/")))    
    bodies = sorted(map(lambda x: x[:-4], os.listdir("cattributes/body/")))
    shapes = sorted(set(map(lambda x: x.split("-")[0], bodies)))
    patterns = sorted(set(map(lambda x: x.split("-")[1], bodies)))

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('mouth_shape', 
            choices=mouth_shapes, type=str,
                    help='Mouth shape')
    
    parser.add_argument('eye_shape', 
            choices=eye_shapes, type=str,
                    help='Eye shape')
    parser.add_argument('eye_color', 
            choices=sorted(colors["EyeColor"].keys()), type=str,
                    help='Eye color')

    parser.add_argument('shape', choices=shapes, type=str,
                    help='Cat shape')
    parser.add_argument('pattern', choices=patterns, type=str,
                    help='Cat color pattern')
    
    parser.add_argument('prim_color', 
            choices=sorted(colors["Primary"].keys()), type=str,
                    help='Primary color')
    parser.add_argument('sec_color', 
            choices=sorted(colors["Secondary"].keys()), type=str,
                    help='Secondary color')
    parser.add_argument('ter_color', 
            choices=sorted(colors["Tertiary"].keys()), type=str,
                    help='Tertiary color')

    parser.add_argument('--path', default="mycat.svg", type=str,
                    help='Save pathr')
    args = parser.parse_args()
    
    
    # Mouth part
    mshape = args.mouth_shape
    data_mouth = None
    with open("{}mouth/{}.svg".format(BASE, mshape), "r") as fp:
        data_mouth = fp.read()

    # Eye part
    eshape = args.eye_shape
    data_eye = None
    with open("{}eye/{}.svg".format(BASE, eshape), "r") as fp:
        data_eye = fp.read()
    
    c_eye = colors["EyeColor"][args.eye_color]
    for c in colors["EyeColor"].values():
        data_eye = data_eye.replace(c, c_eye)
    
    # Body part
    bshape = args.shape
    bpattern = args.pattern
    data_body = None
    with open("{}body/{}-{}.svg".format(BASE, bshape, bpattern), "r") as fp:
        data_body = fp.read()
    
    c_prim = colors["Primary"][args.prim_color]
    c_sec  = colors["Secondary"][args.sec_color]
    c_ter  = colors["Tertiary"][args.ter_color]

    for c in colors["Primary"].values():
        data_body = data_body.replace(c, c_prim)

    for c in colors["Secondary"].values():
        data_body = data_body.replace(c, c_sec)
    
    for c in colors["Tertiary"].values():
        data_body = data_body.replace(c, c_ter)

    
    P1 = data_body.split("\n")
    P2 = data_eye.split("\n")
    P3 = data_mouth.split("\n")

    # Join
    PP = P1[:-1] + P2[2:-1] + P3[2:]
    #PP = P1[:-1] + P2[2:] 

    with open(args.path, "w") as fp:
        fp.write("\n".join(PP))

