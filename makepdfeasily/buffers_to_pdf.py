# makepdfeasily/buffers_to_pdf.py
# Function: convert a list of image buffers to a single PDF file
from typing import List, Union, Optional
from PIL import Image
import io
import os

ImageLike = Union[bytes, bytearray, io.BytesIO, Image.Image]

def buffers_to_pdf(
    images: List[ImageLike],
    output_dir: Optional[str] = None,
    output_name: str = "output.pdf",
) -> Union[str, bytes]:
    """
    Converts a list of image buffers into a single PDF file.

    Parameters:
    - images: list of items which can be:
        * bytes or bytearray (raw image bytes)
        * io.BytesIO (in-memory file)
        * PIL.Image.Image (Pillow image object)
      The order of images determines the pages order in the PDF.
    - output_dir: if provided, the PDF will be saved to this directory with the given output_name and the function returns the path (str).
                  If None, the PDF bytes are returned.
    - output_name: file name for saving when output_dir is provided (should include .pdf).

    Returns:
    - str: full path to saved PDF if output_dir is provided.
    - bytes: PDF content if output_dir is None.

    Raises:
    - ValueError: if images list is empty.
    - TypeError: if an unsupported item is in the list.
    - OSError: if opening or processing an image fails.
    """
    if not images:
        raise ValueError("قائمة الصور فارغة. الرجاء تمرير قائمة تحتوي على صورة واحدة على الأقل.")

    pil_images: List[Image.Image] = []

    for idx, item in enumerate(images):
        # Convert different input types to a BytesIO that PIL can open
        if isinstance(item, Image.Image):
            im = item
        else:
            if isinstance(item, (bytes, bytearray)):
                buf = io.BytesIO(item)
            elif isinstance(item, io.BytesIO):
                buf = item
                buf.seek(0)
            else:
                # Try to treat as file-like (object with read/seek)
                try:
                    buf = item  # type: ignore
                    buf.seek(0)
                except Exception:
                    raise TypeError(f"العنصر في الموضع {idx} ليس bytes/BytesIO/PIL.Image ولا يدعم seek/read.")

            try:
                im = Image.open(buf)
            except Exception as e:
                raise OSError(f"فشل فتح الصورة في الموضع {idx}: {e}")

        # Handle transparency and convert to RGB
        try:
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                bg = Image.new("RGB", im.size, (255, 255, 255))
                try:
                    alpha = im.split()[-1]
                    bg.paste(im.convert("RGBA"), mask=alpha)
                except Exception:
                    bg.paste(im.convert("RGB"))
                pil_images.append(bg)
            else:
                pil_images.append(im.convert("RGB"))
        except Exception as e:
            raise OSError(f"فشل معالجة الصورة في الموضع {idx}: {e}")

    first, rest = pil_images[0], pil_images[1:]

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        out_full = os.path.join(output_dir, output_name)
        first.save(out_full, "PDF", resolution=100.0, save_all=True, append_images=rest)
        return out_full
    else:
        out_io = io.BytesIO()
        first.save(out_io, "PDF", resolution=100.0, save_all=True, append_images=rest)
        out_io.seek(0)
        return out_io.getvalue()
