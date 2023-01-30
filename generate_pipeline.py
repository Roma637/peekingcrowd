from generate_zones import generate_zones
# from cv2 import VideoCapture as vidcap
# from cv2 import CAP_PROP_FRAME_HEIGHT as vidheight
# from cv2 import CAP_PROP_FRAME_WIDTH as vidwidth
import cv2

def generate_pipeline_file(rows, columns, srcfile):
    '''rows and columns refer to number of rows and columns of zones (integers)
    srcfile refers to the file path of mp4 file to be analysed (string)
    srcresolution refers to resolution of the mp4 file (array of 2 integers)'''

    zone_coords = generate_zones(rows, columns)

    vid = cv2.VideoCapture(srcfile)
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))

    placeholder = '''- output.media_writer:
    output_dir: output/'''

    with open("pipeline_config.yml", "w") as file:
        file.writelines(f'''nodes:
- input.visual:
    source: {srcfile}
- model.yolo:
    detect: ["person"]
- custom_nodes.dabble.bbox_to_mid_midpoint
- dabble.zone_count:
    resolution: [{width}, {height}]
    zones: {zone_coords}
- custom_nodes.draw.img_tint_test:
    rows: {rows}
    columns: {columns}
- draw.bbox
- draw.btm_midpoint
- draw.zones
- draw.legend:
    show : ["zone_count"]
- output.screen
- output.media_writer:
    output_dir : output/
''')

generate_pipeline_file(2,2, 'raws/overhead_3.mp4')
