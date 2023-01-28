from generate_zones import generate_zones

def generate_pipeline_file(rows, columns, srcfile, srcresolution):
    '''rows and columns refer to number of rows and columns of zones (integers)
    srcfile refers to the file path of mp4 file to be analysed (string)
    srcresolution refers to resolution of the mp4 file (array of 2 integers)'''

    zone_coords = generate_zones(rows, columns)

    with open("pipeline_config.yml", "w") as file:
        file.writelines(f'''nodes:
- input.visual:
    source: {srcfile}
- model.yolo:
    detect: ["person"]
- custom_nodes.dabble.bbox_to_mid_midpoint
- dabble.zone_count:
    resolution: {srcresolution}
    zones: {zone_coords}
- draw.bbox
- draw.btm_midpoint
- draw.zones
- draw.legend:
    show: ["zone_count"]
- output.screen
- output.media_writer:
    output_dir: output/''')

generate_pipeline_file(2, 1, 'raws/overhead_3.mp4', [848, 480])
