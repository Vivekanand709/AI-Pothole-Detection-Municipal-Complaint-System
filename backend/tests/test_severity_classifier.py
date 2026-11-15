import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.ai.severity_classifier import SeverityClassifier


class SeverityClassifierTests(unittest.TestCase):
    def setUp(self):
        self.classifier = SeverityClassifier()

    def test_small_area_is_low(self):
        severity, metadata = self.classifier.classify({
            "bbox": [0, 0, 20, 20],
            "confidence": 0.8,
        })
        self.assertEqual(severity, "Low")
        self.assertEqual(metadata["area"], 400)

    def test_large_area_is_high_or_critical(self):
        severity, _ = self.classifier.classify({
            "bbox": [0, 0, 120, 100],
            "confidence": 0.8,
        })
        self.assertIn(severity, {"High", "Critical"})

    def test_invalid_or_missing_bbox_defaults_safely(self):
        severity, metadata = self.classifier.classify({
            "bbox": [0, 0, 0, 0],
            "confidence": 0.5,
        })
        self.assertEqual(severity, "Low")
        self.assertEqual(metadata["area"], 0)


if __name__ == "__main__":
    unittest.main()
