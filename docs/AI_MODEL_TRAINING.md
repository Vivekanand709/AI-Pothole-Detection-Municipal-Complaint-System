# Train a genuine pothole detector

The repository does not contain fabricated model weights. The detector becomes a pothole detector only after training on pothole-labelled images and validating it on held-out data.

## Recommended starting dataset: RDD2022 India

Use the official Road Damage Detection 2022 (RDD2022) dataset. The India subset contains road images captured in India; potholes are labelled as class **D40**.

- [RDD2022 dataset information](https://crddc2022.sekilab.global/data/)
- [Official dataset repository and download links](https://github.com/sekilab/RoadDamageDetector)
- [RDD2022 Figshare record](https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547)

Download the India subset and extract it locally. The annotations are Pascal VOC XML, not YOLO text labels. This repository includes `scripts/convert_rdd2022_to_yolo.py`, which filters class D40 and creates reproducible 80/10/10 train/valid/test splits.

Run from the repository root in PowerShell:

```powershell
python scripts/convert_rdd2022_to_yolo.py --source "D:\\RDD2022_India" --output "D:\\pothole_yolo"
```

Use the actual extracted folder as `--source` if its name differs. Review the converter's image/box counts and inspect some converted labels before training. Check the dataset licence/terms before use or redistribution and cite RDD2022 in your report.

## Install training dependencies

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install ultralytics pyyaml
```

For NVIDIA GPU training, install a PyTorch build compatible with the installed driver/CUDA version using the official PyTorch selector. CPU training is possible but may be slow.

## Train

```powershell
python scripts/train_pothole_model.py --data "D:\\pothole_yolo\\data.yaml" --epochs 60 --imgsz 640 --batch 8
```

Reduce batch to 4 if GPU memory is limited, or add `--device cpu` for CPU training. Ultralytics starts from a generic pretrained checkpoint; the resulting checkpoint becomes a pothole detector only after this dataset-specific training. Review training curves, validation metrics, confusion matrix and predictions on held-out images. Do not claim an accuracy score without a held-out test evaluation.

The training script copies the best checkpoint to `backend/models/pothole_detector.pt`.

## Enable real inference

In `backend/.env`:

```env
DEMO_MODE=false
AI_MODEL_PATH=models/pothole_detector.pt
CONFIDENCE_THRESHOLD=0.5
```

Restart the backend and check `GET /api/inspections/ai/status`. A ready status confirms the weights file can be found; it does not prove model quality. Run sample videos and inspect detections before presenting.

## Important limitations

- Demo Mode generates simulated detections for UI demonstrations only.
- Real mode without trained weights must fail clearly; it must not silently switch to simulated results.
- The configured weights must be trained for pothole detection. Never rename a generic COCO checkpoint and claim it is a trained pothole model.
- GPS fallback coordinates are not a live GPS trace. Supply a timestamped CSV/JSON GPS track for location-aware inspection results.
