import tempfile
import unittest
from pathlib import Path

from app.ai.gps_processor import GPSProcessor
from app.ai.pothole_detector import PotholeDetector


class GPSProcessorTests(unittest.TestCase):
    def test_interpolates_between_points(self):
        gps = GPSProcessor(default_lat=0.0, default_lon=0.0)
        gps.add_gps_point(0, 10.0, 20.0)
        gps.add_gps_point(10, 20.0, 40.0)
        self.assertEqual(gps.get_coordinates_at_timestamp(5), (15.0, 30.0))

    def test_clamps_outside_recorded_time_range(self):
        gps = GPSProcessor()
        gps.add_gps_point(5, 31.0, 75.0)
        gps.add_gps_point(10, 32.0, 76.0)
        self.assertEqual(gps.get_coordinates_at_timestamp(0), (31.0, 75.0))
        self.assertEqual(gps.get_coordinates_at_timestamp(20), (32.0, 76.0))


class PotholeDetectorTests(unittest.TestCase):
    def test_real_mode_fails_clearly_when_weights_are_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            missing_weights = Path(directory) / "missing_pothole_model.pt"
            with self.assertRaisesRegex(RuntimeError, "model weights"):
                PotholeDetector(model_path=str(missing_weights), demo_mode=False)


if __name__ == "__main__":
    unittest.main()
