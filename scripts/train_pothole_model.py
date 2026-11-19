"""Train a YOLO pothole detector from a correctly annotated YOLO-format dataset.

Example:
  python scripts/train_pothole_model.py --data path/to/data.yaml --epochs 60 --imgsz 640
The best checkpoint is copied to backend/models/pothole_detector.pt.
"""
import argparse
import shutil
from pathlib import Path

from ultralytics import YOLO


def main():
    parser = argparse.ArgumentParser(description="Train a YOLO pothole detector")
    parser.add_argument("--data", required=True, help="Path to dataset data.yaml")
    parser.add_argument("--model", default="yolov8n.pt", help="Starting pretrained YOLO checkpoint")
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default=None, help="For example 0 for CUDA GPU or cpu")
    args = parser.parse_args()

    data_file = Path(args.data).expanduser().resolve()
    if not data_file.is_file():
        raise SystemExit(f"Dataset YAML not found: {data_file}")
    if args.epochs < 1 or args.imgsz < 32 or args.batch < 1:
        raise SystemExit("epochs, imgsz and batch must be positive (imgsz >= 32)")

    model = YOLO(args.model)
    results = model.train(
        data=str(data_file),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project="runs/pothole",
        name="train",
        exist_ok=True,
    )
    best = Path(results.save_dir) / "weights" / "best.pt"
    if not best.is_file():
        raise SystemExit(f"Training finished but best checkpoint was not found: {best}")

    destination = Path(__file__).resolve().parents[1] / "backend" / "models" / "pothole_detector.pt"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(best, destination)
    print(f"Saved trained pothole model to: {destination}")
    print("Set DEMO_MODE=false in backend/.env and restart the backend to use real inference.")


if __name__ == "__main__":
    main()
