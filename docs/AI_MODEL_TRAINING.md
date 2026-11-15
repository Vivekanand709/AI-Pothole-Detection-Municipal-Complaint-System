# Training a genuine pothole detector

The repository intentionally does not ship fabricated weights. The included YOLO checkpoint (if downloaded by Ultralytics on first run) is only a generic initialization model; it is **not** a pothole detector until trained on pothole-labelled data.

## 1. Obtain a dataset
Use a pothole-specific object-detection dataset from a reputable source such as Roboflow Universe or a research dataset repository. Check the dataset's license, attribution requirements, permitted use, and whether redistribution is allowed before downloading or publishing it. Do not upload private or restricted datasets to this repository.

The dataset must be exported in **Ultralytics YOLO detection** format and include a `data.yaml`, images, and matching YOLO label text files. Each label row must use:
`class_id x_center y_center width height`
with normalized coordinates from 0 to 1. The class list must include the pothole class. Use a separate validation split. Do not use classification-only or segmentation-only exports for this detection script.

Typical structure:
```text
pothole-dataset/
  data.yaml
  train/images/
  train/labels/
  valid/images/
  valid/labels/
  test/images/       # optional
  test/labels/       # optional
```

## 2. Install training dependencies
From the repository root in PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install ultralytics pyyaml
```
For NVIDIA GPU training, install a PyTorch build compatible with the installed NVIDIA driver/CUDA version first, following the official PyTorch installation selector. CPU training is possible but may be slow.

## 3. Train
```powershell
python scripts/train_pothole_model.py --data "C:\path\to\pothole-dataset\data.yaml" --epochs 60 --imgsz 640 --batch 16
```
If GPU memory is limited, lower batch (for example `--batch 4`) or use `--device cpu`. Review training/validation metrics and inspect predictions on images that were not used for training. Do not claim accuracy without evaluating a held-out test set.

The script copies the best checkpoint to:
`backend/models/pothole_detector.pt`

## 4. Enable real inference
In `backend/.env`:
```env
DEMO_MODE=false
AI_MODEL_PATH=models/pothole_detector.pt
CONFIDENCE_THRESHOLD=0.5
```
Restart the backend. Check `GET /api/inspections/ai/status`; it should report `real_ai_ready: true` when the file exists and real mode is selected. This checks file readiness, not model quality; make a test inspection and review its detections before a presentation.

## Important
- Never rename a generic COCO model to `pothole_detector.pt` and call it trained for potholes.
- Demo Mode generates simulated detections for UI demonstrations only.
- Real mode without trained weights must fail clearly; it must not silently switch to simulated results.
- The pipeline's fallback GPS coordinates are not a live GPS trace. Supply a timestamped CSV/JSON GPS track for location-aware inspection results.
