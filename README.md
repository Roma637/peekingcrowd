This program takes in a video, counts the number of people per zone and highlights each zone depending on how crowded they are relative to each other. Zones are drawn in a grid system.
The generate_pipeline.py file defines a function generate_pipeline_file() that takes in 3 parameters: the number of rows and columns of the grid respectively, followed by the filepath of the video file intended to be analysed.
This function then writes a pipeline_config.yml file according to the parameters.
For example, the call generate_pipeline_file(1, 2, 'raw_footage/example.mp4') will write a pipeline_config.yml file with 2 zones, each zone taking the right and left halves of the screen, and the input file being the example.mp4 file in the raws/ folder.
You can also pass a string of the number that corresponds to the webcam port to have the webcam as the input.
After writing to the pipeline_config.yml file, the peekingduck run command can be given to process the video, and the output video will be saved under the outputs/ folder.
Zones that are too crowded are coloured red, those that are too empty are coloured blue, zones that have the optimal number of people (ie closest to the average number of people per zone) are coloured green. 
There are two custom nodes. 
The first is a dabble node, a variation of the bbox_to_btm_midpoint.
The second is a draw node, which is what shades the zones based on the number of people detected in each zone.
