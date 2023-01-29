"""
Node template for creating custom nodes.
"""

from typing import Any, Dict

from peekingduck.pipeline.nodes.abstract_node import AbstractNode

import cv2

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

        print(inputs["zones"])
        print(inputs["zone_count"])

        result = cv2.cvtColor(inputs["img"], cv2.COLOR_BGR2GRAY)
        outputs = {"img": result}
        return outputs
