# YOLO model weights

Place your trained Ultralytics YOLO pothole-detection weights in this folder as
`pothole_detector.pt`, or set `AI_MODEL_PATH` in `backend/.env` to the
correct relative or absolute path.

The project does not include trained model weights. Do not rename a generic
COCO model to pothole_detector.pt and assume it detects potholes: the weights
must be trained/fine-tuned for pothole classes. Until suitable weights are
available, keep `DEMO_MODE=true`.
