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

        #SPLIT THE IMAGE

        #cut image horizontally
        vsplit_arr = np.array([(i+1)* len(inputs["img"])//self.config["rows"] for i in range(self.config["rows"])])
        first_split = np.vsplit(inputs["img"], vsplit_arr)[:-1]

        print(f" LENGTH OF FIRST SPLIT IS {len(first_split)}")
        print([i.shape for i in first_split])

        np_zones = {}

        hsplit_arr = np.array([(i+1)* (first_split[0].shape[1])//self.config["columns"] for i in range(self.config["columns"])])
        print(hsplit_arr)

        for r in range(len(first_split)):
            #cut each strip vertically
            second_split = np.hsplit(first_split[r], hsplit_arr)[:-1]

            print(f" LENGTH OF SECOND SPLIT IS {len(second_split)}")
            print([i.shape for i in second_split])

            for c in range(len(second_split)):
                # print(second_split[c])
                # print(type(second_split[c]))
                np_zones[f"row{r+1}col{c+1}"] = second_split[c]
                # print(f"just saved row{r+1}col{c+1}")

        print("======= npzones is ========")
        print(np_zones)
        print("===========================")
        
        for zone in np_zones.values():
            print(zone.shape)

        #COLOUR THE ZONES

        # result = cv2.cvtColor(inputs["img"], cv2.COLOR_BGR2GRAY)

        #temporary
        np_zones["row1col1"] = cv2.cvtColor(np_zones["row1col1"], cv2.COLOR_BGR2GRAY)
        np_zones["row1col1"] = cv2.cvtColor(np_zones["row1col1"], cv2.COLOR_GRAY2BGR)

        #PUT IMAGE BACK TOGETHER

        temp_rows = {}

        for row in range(self.config["rows"]):
            print(np_zones[f"row{row+1}col1"])
            print(np_zones[f"row{row+1}col2"])
            temp_rows[f"row{row+1}"] = np.hstack(tuple([np_zones[f"row{row+1}col{col+1}"] for col in range(self.config["columns"])]))

        # print(temp_rows)

        result = np.vstack(tuple(temp_rows.values()))

        print(inputs["img"].shape)
        print(result.shape)

        #RETURN

        outputs = {"img": result}
        return outputs