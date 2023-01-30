"""
Node template for creating custom nodes.
"""

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

        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node tints the image.

        Args:
            inputs (dict): Dictionary with keys "img", "zones", "zone_count".

        Returns:
            outputs (dict): Dictionary with keys "img".
        """

        # print(len(inputs["img"]))

        print(inputs["zones"])
        print(inputs["zone_count"])
        
        # print(self.config["rows"])
        # print(self.config["columns"])

        #this code depends on 
        # all the zones having the same width
        # the zone coordinates going topleft, topright, bottomright, bottomleft
        # there only being 1 row and x columns or x rows and 1 column
        

        # accumulator = []
        # for row in inputs["img"]:
        #     acc2 = []
        #     for pixel in range(zone_width):
        #         acc2.append(pixel)
        #     accumulator.append(acc2)
        # accumulator = np.array(accumulator)
        # print(accumulator.shape)
        # result = cv2.cvtColor(accumulator, cv2.COLOR_BGR2GRAY)

        # for r in range(self.config["rows"]):
        #     for c in range(self.config["columns"]):
        #         zone_name = f"row{r+1}col{c+1}"
        #         print(zone_name)

        #SPLIT THE IMAGE

        vsplit_arr = np.array([(i+1)* len(inputs["img"])//self.config["rows"] for i in range(self.config["rows"])])
        first_split = np.vsplit(inputs["img"], vsplit_arr)

        np_zones = {}

        for r in range(len(first_split)):
            #for every row
            hsplit_arr = np.array([(i+1)* len(first_split[r])//self.config["columns"] for i in range(self.config["columns"])])
            print(hsplit_arr)
            second_split = np.hsplit(first_split[r], hsplit_arr)
            for c in range(len(second_split)):
                print(second_split[c])
                print(type(second_split[c]))
                np_zones[f"row{r+1}col{c+1}"] = second_split[c]
                print(f"just saved row{r+1}col{c+1}")

        print(np_zones)

        #COLOUR THE ZONES

        plan = '''

        modified_a = cvt(a, gray)
        modified_b = cvt(b, pink)

        result = modified_a + modified_b'''

        # result = cv2.cvtColor(inputs["img"], cv2.COLOR_BGR2GRAY)

        #temporary
        np_zones["row1col1"] = cv2.cvtColor(np_zones["row1col1"], cv2.COLOR_BGR2GRAY)

        #PUT IMAGE BACK TOGETHER

        # result = hstack vstack

        #RETURN

        outputs = {"img": result}
        return outputs