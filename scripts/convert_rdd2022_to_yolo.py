"""Convert annotated RDD2022 Pascal-VOC XML data into a one-class YOLO pothole dataset.

RDD2022 uses D40 for potholes. This converter keeps D40 objects only and
creates deterministic train/valid/test splits from the annotated images.

Example:
  python scripts/convert_rdd2022_to_yolo.py --source "D:/RDD2022_India" --output "D:/pothole_yolo"
"""
import argparse
import random
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
POTHOLE_NAMES = {"d40", "pothole", "potholes"}


def find_image(xml_path: Path, source: Path):
    filename = (xml_path.parent / (xml_path.stem)).name
    for ext in IMAGE_EXTENSIONS:
        candidate = xml_path.with_suffix(ext)
        if candidate.is_file():
            return candidate
    for candidate in source.rglob(xml_path.stem + ".*"):
        if candidate.suffix.lower() in IMAGE_EXTENSIONS:
            return candidate
    return None


def parse_annotation(xml_path: Path, image_path: Path):
    root = ET.parse(xml_path).getroot()
    size = root.find("size")
    if size is None:
        raise ValueError(f"Missing image size in {xml_path}")
    width = float(size.findtext("width", "0"))
    height = float(size.findtext("height", "0"))
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid image dimensions in {xml_path}")

    labels = []
    for obj in root.findall("object"):
        name = (obj.findtext("name") or "").strip().lower()
        if name not in POTHOLE_NAMES:
            continue
        box = obj.find("bndbox")
        if box is None:
            continue
        xmin = max(0.0, min(width, float(box.findtext("xmin", "0")) - 1))
        ymin = max(0.0, min(height, float(box.findtext("ymin", "0")) - 1))
        xmax = max(0.0, min(width, float(box.findtext("xmax", "0"))))
        ymax = max(0.0, min(height, float(box.findtext("ymax", "0"))))
        if xmax <= xmin or ymax <= ymin:
            continue
        x_center = ((xmin + xmax) / 2) / width
        y_center = ((ymin + ymax) / 2) / height
        box_width = (xmax - xmin) / width
        box_height = (ymax - ymin) / height
        labels.append(f"0 {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}")
    return labels


def main():
    parser = argparse.ArgumentParser(description="Convert RDD2022 VOC annotations to YOLO pothole format")
    parser.add_argument("--source", required=True, help="Extracted RDD2022 India folder")
    parser.add_argument("--output", required=True, help="Output YOLO dataset folder")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train-ratio", type=float, default=0.8)
    parser.add_argument("--valid-ratio", type=float, default=0.1)
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not source.is_dir():
        raise SystemExit(f"Source folder not found: {source}")
    if args.train_ratio <= 0 or args.valid_ratio <= 0 or args.train_ratio + args.valid_ratio >= 1:
        raise SystemExit("Train and valid ratios must be positive and sum to less than 1.")

    records = []
    xml_files = sorted(source.rglob("*.xml"))
    for xml_path in xml_files:
        image_path = find_image(xml_path, source)
        if image_path is None:
            continue
        try:
            labels = parse_annotation(xml_path, image_path)
        except (ET.ParseError, ValueError) as exc:
            print(f"Skipping {xml_path}: {exc}")
            continue
        records.append((image_path, labels))

    if not records:
        raise SystemExit("No matching XML/image pairs found. Check the extracted RDD2022 India folder.")

    random.Random(args.seed).shuffle(records)
    train_end = int(len(records) * args.train_ratio)
    valid_end = train_end + int(len(records) * args.valid_ratio)
    splits = {
        "train": records[:train_end],
        "valid": records[train_end:valid_end],
        "test": records[valid_end:],
    }

    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"Output folder is not empty: {output}. Choose a new folder or clear it first.")

    total_boxes = 0
    for split, items in splits.items():
        image_dir = output / split / "images"
        label_dir = output / split / "labels"
        image_dir.mkdir(parents=True, exist_ok=True)
        label_dir.mkdir(parents=True, exist_ok=True)
        for index, (image_path, labels) in enumerate(items):
            target_name = f"{index:06d}{image_path.suffix.lower()}"
            shutil.copy2(image_path, image_dir / target_name)
            (label_dir / f"{Path(target_name).stem}.txt").write_text(
                "\n".join(labels), encoding="utf-8"
            )
            total_boxes += len(labels)

    (output / "data.yaml").write_text(
        "path: .\ntrain: train/images\nval: valid/images\ntest: test/images\nnames:\n  0: pothole\n",
        encoding="utf-8",
    )
    print(f"Converted {len(records)} annotated images and {total_boxes} pothole boxes.")
    for split, items in splits.items():
        print(f"{split}: {len(items)} images")
    print(f"YOLO dataset config: {output / 'data.yaml'}")


if __name__ == "__main__":
    main()
