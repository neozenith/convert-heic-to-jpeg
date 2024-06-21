import os
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


def discover(start_dir: Path = Path("./data/")):
    """Recursively walk and discover a list of HEIC files to process."""
    return [
        start_dir / f
        for f in os.listdir(start_dir)
        if f.lower().endswith(".heic") or f.lower().endswith(".jpeg")
    ]


def process_image(img_path: Path, type: str = "JPEG"):
    """Given the path to a HEIC/JPEG, convert it to target type in target location."""
    image = Image.open(img_path)

    # try to get the original created date out of the EXIF data embedded in the image
    # do not trust the operating system metadata about dates.
    exif_data = image.getexif()

    if exif_data is not None:
        tag = 306  # DateTime
        exif_date = exif_data.get(tag)
        # Format of data is "YYYY:MM:DD HH:MM:SS"
        # So split on space and get the first part
        # replace : to make the string folder path friendly
        date_component = exif_date.split(" ")[0].replace(":", "-")
        target_path = (
            img_path.parent / "triaged" / date_component / img_path.name
        ).with_suffix(f".{type.lower()}")
    else:
        target_path = (img_path.parent / "triaged" / img_path.name).with_suffix(
            f".{type.lower()}"
        )

    if not target_path.exists():
        os.makedirs(target_path.parent, exist_ok=True)
        image.save(target_path, type)

    return target_path


def convert(start_dir: Path = Path("./data/")):
    """Process HEIC/JPEG images to JPEG."""
    return [process_image(f, "JPEG") for f in discover(start_dir)]
