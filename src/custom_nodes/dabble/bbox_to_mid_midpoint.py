"""
This is a modified version of the bbox_to_btm_midpoint node
"""

from typing import Any, Dict

from peekingduck.pipeline.nodes.abstract_node import AbstractNode


class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.img_size = None

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Converts bounding boxes to a single point of reference for use in
        zone analytics.
        """
        # get xy midpoint of each bbox (x1, y1, x2, y2)
        # This is calculated as x is (x1-x2)/2 and y is y2
        bboxes = inputs["bboxes"]
        frame = inputs["img"]
        self.img_size = (frame.shape[1], frame.shape[0])  # type:ignore
        return {
            "btm_midpoint": [
                self._xy_on_img(((bbox[0] + bbox[2]) / 2), ((bbox[1] + bbox[3]) / 2)) for bbox in bboxes
            ]
        }

    def _xy_on_img(self, pt_x: float, pt_y: float):
        """Return a tuple of the int x y points of the midpoint on the original image"""
        assert self.img_size is not None
        return (int(pt_x * self.img_size[0]), int(pt_y * self.img_size[1]))