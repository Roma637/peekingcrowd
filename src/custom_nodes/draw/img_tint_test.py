from typing import Any, Dict

from peekingduck.pipeline.nodes.abstract_node import AbstractNode
import cv2
import numpy as np

class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node tints the image.

        Args:
            inputs (dict): Dictionary with keys "img", "zones", "zone_count".

        Returns:
            outputs (dict): Dictionary with keys "img".
        """

        #this code depends on 
        # all the zones having the same width
        # the zone coordinates going topleft, topright, bottomright, bottomleft

        #SPLIT THE IMAGE

        #cut image horizontally
        vsplit_arr = np.array([(i+1) * (len(inputs["img"])//self.config["rows"]) for i in range(self.config["rows"])])
        first_split = np.vsplit(inputs["img"], vsplit_arr)[:-1]

        np_zones = {}

        hsplit_arr = np.array([(i+1) * (first_split[0].shape[1]//self.config["columns"]) for i in range(self.config["columns"])])

        for r in range(self.config["rows"]):
            #cut each strip vertically
            second_split = np.hsplit(first_split[r], hsplit_arr)[:-1]
            for c in range(self.config["columns"]):
                np_zones[f"row{r+1}col{c+1}"] = second_split[c]

        print(np_zones.keys())

        #LOGIC FOR WHICH ZONES TO COLOUR

        #if difference between biggest and smallest zonecount is 1, colour everything green
        #else, calculate the average? everything above average is red everything below average is blue

        colour_flags = {}
        zone_names = list(np_zones.keys())

        if abs(max(inputs["zone_count"]) - min(inputs["zone_count"])) <= 1:
            colour_flags = {zn:'cv2.COLORMAP_DEEPGREEN' for zn in np_zones.keys()}
        else:
            average_count = round(sum(inputs["zone_count"]) / len(inputs["zone_count"]), 2)

            for index in range(len(inputs["zone_count"])):
                zone_name = zone_names[index]
                if 0<(inputs["zone_count"][index]-average_count)<1:
                    colour_flags[zone_name] = 'cv2.COLORMAP_HOT'
                elif inputs["zone_count"][index] > average_count:
                    colour_flags[zone_name] = 'cv2.COLORMAP_HOT'
                else:
                    colour_flags[zone_name] = 'cv2.COLORMAP_OCEAN'

        print(colour_flags)

        #COLOUR THE ZONES

        for zone in colour_flags:

            flag = colour_flags[zone]

            np_zones[zone] = cv2.cvtColor(np_zones[zone], cv2.COLOR_BGR2GRAY)
            np_zones[zone] = cv2.cvtColor(np_zones[zone], cv2.COLOR_GRAY2BGR)
            
            if flag=="cv2.COLORMAP_DEEPGREEN":
                np_zones[zone] = cv2.applyColorMap(np_zones[zone], cv2.COLORMAP_DEEPGREEN)
            elif flag=="cv2.COLORMAP_HOT":
                np_zones[zone] = cv2.applyColorMap(np_zones[zone], cv2.COLORMAP_HOT)
            elif flag=="cv2.COLORMAP_OCEAN":
                np_zones[zone] = cv2.applyColorMap(np_zones[zone], cv2.COLORMAP_OCEAN)

        #PUT IMAGE BACK TOGETHER

        temp_rows = {}

        for row in range(self.config["rows"]):
            temp_rows[f"row{row+1}"] = np.hstack(tuple([np_zones[f"row{row+1}col{col+1}"] for col in range(self.config["columns"])]))

        result = np.vstack(tuple(temp_rows.values()))

        #RETURN

        outputs = {"img": result}
        return outputs