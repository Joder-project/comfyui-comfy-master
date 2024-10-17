from server import PromptServer
import folder_paths
from PIL import Image
import base64
from io import BytesIO
import torch
import numpy as np
from .encoding import encode_string, encode_image, encode_audio
import os
import torchaudio

var_prefix_name = "ComfyMasterVar_"

class InputImageNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "InputImage"}),
                "image": ("STRING", {"multiline": False}),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    CATEGORY = "comfyui-master"
    FUNCTION = "input_image"

    def input_image(self, var_name, image, export, description):
        imgdata = base64.b64decode(image)
        img = Image.open(BytesIO(imgdata))

        if "A" in img.getbands():
            mask = np.array(img.getchannel("A")).astype(np.float32) / 255.0
            mask = 1.0 - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

        img = img.convert("RGB")
        img = np.array(img).astype(np.float32) / 255.0
        img = torch.from_numpy(img)[None,]

        return (img, mask)
    

class InputStringNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "InputString"}),
                "text": ("STRING", {"multiline": True, "default": ""}),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("text", "export")
    CATEGORY = "comfyui-master"
    FUNCTION = "input_string"

    def input_string(self, var_name, text, export, description):
        return (text, export)

class InputEnumStringNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "InputEnum"}),
                "text": ("STRING", {"multiline": False, "default": ""}),
                "enums": ("STRING", {"multiline": True, "default": ""}),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "BOOLEAN")
    RETURN_NAMES = ("text", "enums", "export")
    CATEGORY = "comfyui-master"
    FUNCTION = "input_enum_string"

    def input_enum_string(self, var_name, text, enums, export, description):
        # Split enums by comma or newline, and strip whitespace
        enums = [enum.strip() for enum in enums.replace('\n', ',').split(',') if enum.strip()]
        if text not in enums:
            enums.append(text)
        return (text, enums, export)
    

class InputBooleanNode:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "InputBoolean"}),
                "value": ("BOOLEAN", {"default": False}),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "BOOLEAN")
    RETURN_NAMES = ("value", "export")
    CATEGORY = "comfyui-master"
    FUNCTION = "input_boolean"

    def input_boolean(self, var_name, value, export, description):
        return (value, export)
    

class InputIntNode:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "InputInt"}),
                "number": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("INT", "BOOLEAN")
    RETURN_NAMES = ("number", "export")
    CATEGORY = "comfyui-master"
    FUNCTION = "input_int"

    def input_int(self, var_name, number, export, description):
        return (number, export)
    

class InputRangeIntNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "InputRangeInt"}),
                "number": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                "min": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                "max": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "BOOLEAN")
    RETURN_NAMES = ("number", "min", "max", "export")
    CATEGORY = "comfyui-master"
    FUNCTION = "input_range_int"

    def input_range_int(self, var_name, number, min, max, export, description):
        if min > max:
            min, max = max, min
        if number < min:
            number = min
        if number > max:
            number = max
        return (number, min, max, export)
    

class InputFloatNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "InputFloat"}),
                "number": ("FLOAT", {"default": 0, "min": 0, "max": 0xffffffffffff, "step": 0.01}),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("FLOAT", "BOOLEAN")
    RETURN_NAMES = ("number", "export")
    CATEGORY = "comfyui-master"
    FUNCTION = "input_float"

    def input_float(self, var_name, number,export, description):
        return (number, export)
    

class InputRangeFloatNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "InputRangeFloat"}),
                "number": ("FLOAT", {"default": 0, "min": 0, "max": 0xffffffffffff, "step": 0.01}),
                "min": ("FLOAT", {"default": 0, "min": 0, "max": 0xffffffffffff, "step": 0.01}),
                "max": ("FLOAT", {"default": 0, "min": 0, "max": 0xffffffffffff, "step": 0.01}),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT", "BOOLEAN")
    RETURN_NAMES = ("number", "min", "max", "export")
    CATEGORY = "comfyui-master"
    FUNCTION = "input_range_float"

    def input_range_float(self, var_name, number, min, max, export, description):
        if min > max:
            min, max = max, min
        if number < min:
            number = min
        if number > max:
            number = max
        return (number, min, max, export)
    

class OutputStringNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "OutputString"}),
                "text": ("STRING", {"multiline": True, "forceInput": True}),
                "export": ("BOOLEAN", {"default": True, }),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ()
    CATEGORY = "comfyui-master"
    OUTPUT_NODE = True
    FUNCTION = "output_string"

    def output_string(self, var_name, text, export, description):
        server = PromptServer.instance
        server.send_sync(100001, encode_string(var_prefix_name + var_name, text), server.client_id)

        return { "ui": { "text": [{"var_name": var_prefix_name + var_name, "text": text}] } }



class OutputImageNode:

    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.filename_prefix = "ComfyMasterOutput_"
        self.type = "temp"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "OutputImage"}),
                "images": ("IMAGE", {"forceInput": True}),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "send_images"
    OUTPUT_NODE = True
    CATEGORY = "comfyui-master"

    def send_images(self, var_name, images, export, description):
        var_name = var_prefix_name + var_name
        filename_prefix = self.filename_prefix + var_name
        results = []
        
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        for i, tensor in enumerate(images):
            array = 255.0 * tensor.cpu().numpy()
            image = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))

            server = PromptServer.instance
            server.send_sync(100002, encode_image(var_prefix_name + var_name, image), server.client_id)
            filename_with_batch_num = filename.replace("%batch_num%", str(i))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            image.save(os.path.join(full_output_folder, file), pnginfo=None, compress_level=1)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })

        return {"ui": {"images": results}}
    

class OutputAudioNode:

    def __init__(self):
        self.output_dir = folder_paths.get_temp_directory()
        self.filename_prefix = "ComfyMasterOutput_"
        self.type = "temp"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"multiline": False, "default": "OutputAudio"}),
                "audio": ("AUDIO",),
                "export": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "send_audio"
    OUTPUT_NODE = True
    CATEGORY = "comfyui-master"

    def send_audio(self, var_name, audio, export, description):
        var_name = var_prefix_name + var_name
        filename_prefix = self.filename_prefix + var_name
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(os.path.join("audio", filename_prefix), self.output_dir)
        results = list()
        

        for (batch_number, waveform) in enumerate(audio["waveform"].cpu()):
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.wav"

            buff = BytesIO()
            torchaudio.save(buff, waveform, audio["sample_rate"], format="WAV")
            server = PromptServer.instance
            server.send_sync(100003, encode_audio(var_prefix_name + var_name, waveform, audio["sample_rate"]), server.client_id)
        
            with open(os.path.join(full_output_folder, file), 'wb') as f:
                f.write(buff.getbuffer())

            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return { "ui": { "audio": results } }