from typing import Any, Dict

from peekingduck.pipeline.nodes.abstract_node import AbstractNode

class Node(AbstractNode):
    """This node is a modified version of the bbox_to_btm_midpoint node. 
    This node is necessary because for our specific purpose, the tracking needs to be done using the middle midpoint.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.img_size = None

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """

        Args:
            inputs (dict): Dictionary with keys "img", "bboxes".

        Returns:
            outputs (dict): Dictionary with keys "btm_midpoint".
        """

        bboxes = inputs["bboxes"]
        frame = inputs["img"]

        self.img_size = (frame.shape[1], frame.shape[0])  # type:ignore

        return {
            #this key is still kept btm_midpoint instead of mid_midpoint because other nodes further down will take in btm_midpoint as an input
            "btm_midpoint": [
                # get xy midpoint of each bbox (x1, y1, x2, y2)
                # This is calculated as x is (x1+x2)/2 and y is (y1+y2)/2
                self._xy_on_img(((bbox[0] + bbox[2]) / 2), ((bbox[1] + bbox[3]) / 2)) for bbox in bboxes
            ]
        }

    def _xy_on_img(self, pt_x: float, pt_y: float):
        """Return a tuple of the int x y points of the midpoint on the original image"""
        assert self.img_size is not None
        return (int(pt_x * self.img_size[0]), int(pt_y * self.img_size[1]))