import os
import sys
from . import custom_nodes

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dependencies"))


NODE_CLASS_MAPPINGS = {
    "CM_InputImage": custom_nodes.InputImageNode,
    "CM_InputString": custom_nodes.InputStringNode,
    "CM_InputEnumString": custom_nodes.InputEnumStringNode,
    "CM_InputInt": custom_nodes.InputIntNode,
    "CM_InputRangeInt": custom_nodes.InputRangeIntNode,
    "CM_InputBoolean": custom_nodes.InputBooleanNode,
    "CM_InputFloat": custom_nodes.InputFloatNode,
    "CM_InputRangeFloat": custom_nodes.InputRangeFloatNode,
    "CM_OutputImage": custom_nodes.OutputImageNode,
    "CM_OutputString": custom_nodes.OutputStringNode,
    "CM_OutputAudio": custom_nodes.OutputAudioNode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "CM_InputImage": "Input Image",
    "CM_InputString": "Input String",
    "CM_InputEnumString": "Input Enum String",
    "CM_InputInt": "Input Int",
    "CM_InputRangeInt": "Input Range Int",
    "CM_InputBoolean": "Input Boolean",
    "CM_InputFloat": "Input Float",
    "CM_InputRangeFloat": "Input Range Float",
    "CM_OutputImage": "Output Image",
    "CM_OutputString": "Output String",
    "CM_OutputAudio": "Output Audio",
}

all = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']