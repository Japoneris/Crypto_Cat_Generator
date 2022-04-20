"""
Try to get faster by modifying the url directly of stuff searched
"""


from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.models import Slider, CustomJS
from bokeh.palettes import Plasma256, inferno


from bokeh.models import Slider, RadioGroup
from bokeh.layouts import column, row

import os


PATH = "./templates/"

# Mouth

PATH_MOUTH = PATH + "mouth/"
files_mouth = sorted(os.listdir(PATH_MOUTH))
set_mouth = sorted(set(map(lambda x: x[:-4], files_mouth)))
dico = {"url": [PATH_MOUTH + files_mouth[0]],
        "x": [0], "y": [0], "w": [1], "h": [1]}
source_mouth = ColumnDataSource(dico)

# Eyes
PATH_EYE = PATH + "eye_png/"
files_eyes = sorted(os.listdir(PATH_EYE))
set_eye_shapes = sorted(set(map(lambda x: x.split("_",1)[0], files_eyes)))
set_eye_colors = sorted(set(map(lambda x: x.split("_",1)[1].split(".")[0], files_eyes)))
dico = {"url": [PATH_EYE + files_eyes[0]],
        "x": [0], "y": [0], "w": [1], "h": [1]}
source_eye = ColumnDataSource(dico)


# Body shape
PATH_BODY = PATH + "body_png/"
files_body = sorted(os.listdir(PATH_BODY))
set_body_shape   = sorted(set(map(lambda x: x.split("-",1)[0], files_body)))
set_body_pattern = sorted(set(map(lambda x: x.split("-",2)[1], files_body)))
set_body_col_P1   = list(filter(lambda x: "-P_" in x, files_body))
set_body_col_P    = sorted(set(map(lambda x: x.split("-P_")[1][:-4], set_body_col_P1)))
set_body_col_S1   = list(filter(lambda x: "-S_" in x, files_body))
set_body_col_S    = sorted(set(map(lambda x: x.split("-S_")[1][:-4], set_body_col_S1)))
set_body_col_T1   = list(filter(lambda x: "-T_" in x, files_body))
set_body_col_T    = sorted(set(map(lambda x: x.split("-T_")[1][:-4], set_body_col_T1)))

source_P = ColumnDataSource({"url": [PATH_BODY + set_body_col_P1[0]],
        "x": [0], "y": [0], "w": [1], "h": [1]})
source_S = ColumnDataSource({"url": [PATH_BODY + set_body_col_S1[0]],
        "x": [0], "y": [0], "w": [1], "h": [1]})
source_T = ColumnDataSource({"url": [PATH_BODY + set_body_col_T1[0]],
        "x": [0], "y": [0], "w": [1], "h": [1]})


###########
# Buttons #
###########
W = 100
button_mouth     = RadioGroup(labels=set_mouth, active=0, width=W)
button_eye_shape = RadioGroup(labels=set_eye_colors, active=0, width=W)
button_eye_color = RadioGroup(labels=set_eye_shapes, active=0, width=W)
button_body_shape   = RadioGroup(labels=set_body_shape, active=0, width=W)
button_body_pattern = RadioGroup(labels=set_body_pattern, active=0, width=W)
button_body_col_P   = RadioGroup(labels=set_body_col_P, active=0, width=W)
button_body_col_S   = RadioGroup(labels=set_body_col_S, active=0, width=W)
button_body_col_T   = RadioGroup(labels=set_body_col_T, active=0, width=W)

##########
# Figure #
##########

p = figure()
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None


# Remove the grid
p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels


# Display each shapes in the correct order

p.image_url(url="url", x="x", y="y", w="w", h="h", source=source_P,
            anchor="bottom_left")
p.image_url(url="url", x="x", y="y", w="w", h="h", source=source_S,
            anchor="bottom_left")
p.image_url(url="url", x="x", y="y", w="w", h="h", source=source_T,
            anchor="bottom_left")
p.image_url(url="url", x="x", y="y", w="w", h="h", source=source_mouth,
            anchor="bottom_left")
p.image_url(url="url", x="x", y="y", w="w", h="h", source=source_eye,
            anchor="bottom_left")


callback_mouth = CustomJS(args=dict(source=source_mouth,
    b_mouth=button_mouth),
    code="""
    var b = b_mouth.active

    console.log(b)
    console.log(source.data.url)
    source.data.url[0] = "./templates/mouth/" + b_mouth.labels[b] + ".png"

    source.change.emit()
    """)

button_mouth.js_on_click(callback_mouth)


callback_eye = CustomJS(args=dict(source=source_eye,
    b_shape=button_eye_shape,
    b_color=button_eye_color),
    code="""
    var shape = b_shape.active
    var color = b_color.active

    source.data.url[0] = "./templates/eye_png/" + b_color.labels[color] + "_" +  b_shape.labels[shape] + ".png"

    source.change.emit()
    """)
button_eye_shape.js_on_click(callback_eye)
button_eye_color.js_on_click(callback_eye)

callback_body = CustomJS(args=dict(source_P=source_P,
    source_S=source_S,
    source_T=source_T,
    b_shape=button_body_shape,
    b_pattern=button_body_pattern,
    b_cP=button_body_col_P,
    b_cS=button_body_col_S,
    b_cT=button_body_col_T),
    code="""
    
    var shape   = b_shape.labels[b_shape.active]
    var pattern = b_pattern.labels[b_pattern.active]
    var col_P   = b_cP.labels[b_cP.active]
    var col_S   = b_cS.labels[b_cS.active]
    var col_T   = b_cT.labels[b_cT.active]


    source_P.data.url[0] = "./templates/body_png/" + shape + "-" + pattern + "-P_" + col_P + ".png"
    source_S.data.url[0] = "./templates/body_png/" + shape + "-" + pattern + "-S_" + col_S + ".png"
    source_T.data.url[0] = "./templates/body_png/" + shape + "-" + pattern + "-T_" + col_T + ".png"
    
    source_P.change.emit()
    source_S.change.emit()
    source_T.change.emit()
    """)


button_body_col_P.js_on_click(callback_body)
button_body_col_S.js_on_click(callback_body)
button_body_col_T.js_on_click(callback_body)
button_body_pattern.js_on_click(callback_body)
button_body_shape.js_on_click(callback_body)



output_file("free_cryptocat.html", title="Make your free cryptocat !")
show(column(row(button_mouth, button_eye_shape, button_eye_color,
    button_body_shape, button_body_pattern,
    button_body_col_P, button_body_col_S, button_body_col_T), p))

