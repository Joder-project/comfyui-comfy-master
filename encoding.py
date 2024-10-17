from io import BytesIO
import struct
import torchaudio

def encode_string(name: str, string: str) -> bytes:
    bytesIO = BytesIO()
    ns = name.encode("utf-8")
    bytesIO.write(struct.pack(">I", len(ns)))
    bytesIO.write(ns)
    val = string.encode("utf-8")
    bytesIO.write(struct.pack(">I", len(val)))
    bytesIO.write(val)
    return bytesIO.getvalue()



def encode_image(name: str, image) -> bytes:
    bytesIO = BytesIO()
    ns = name.encode("utf-8")
    bytesIO.write(struct.pack(">I", len(ns)))
    bytesIO.write(ns)
    image.save(bytesIO, format="PNG", quality=100, compress_level=1)
    preview_bytes = bytesIO.getvalue()
    return preview_bytes


def encode_audio(name: str, audio, sample_rate) -> bytes:
    bytesIO = BytesIO()
    ns = name.encode("utf-8")
    bytesIO.write(struct.pack(">I", len(ns)))
    bytesIO.write(ns)

    buff = BytesIO()
    torchaudio.save(buff, audio, sample_rate, format="WAV")
    bytesIO.write(buff.getvalue())
    preview_bytes = bytesIO.getvalue()
    print("len: ", len(preview_bytes))
    return preview_bytes


# def encode_video(name: str, video) -> bytes:
#     bytesIO = BytesIO()
#     ns = name.encode("utf-8")
#     bytesIO.write(struct.pack(">I", len(ns)))
#     bytesIO.write(ns)
#     video.save(bytesIO, format="MP4", quality=100, compress_level=1)
#     preview_bytes = bytesIO.getvalue()
#     return preview_bytes
