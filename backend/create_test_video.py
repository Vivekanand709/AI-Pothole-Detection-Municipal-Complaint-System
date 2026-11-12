"""
Create a small test video for demonstration purposes.
This creates a simple video with changing colors to simulate road inspection footage.
"""
import cv2
import numpy as np
import os

def create_test_video(output_path, duration=5, fps=30, width=640, height=480):
    """Create a test video with changing colors."""
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_frames = duration * fps

    for frame_num in range(total_frames):
        # Create a frame with changing colors
        # Simulate road surface with gray and some variation
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Base road color (gray)
        base_color = int(100 + 50 * np.sin(frame_num / 10))
        frame[:, :] = [base_color, base_color, base_color]

        # Add some texture/noise
        noise = np.random.randint(0, 30, (height, width, 3), dtype=np.uint8)
        frame = cv2.add(frame, noise)

        # Add some "road markings" (lines)
        if frame_num % 60 < 30:  # Every second
            cv2.line(frame, (width // 2, 0), (width // 2, height), (255, 255, 255), 3)

        # Add frame number text
        cv2.putText(frame, f'Frame: {frame_num}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Write frame
        out.write(frame)

    out.release()
    print(f"Test video created: {output_path}")
    print(f"Duration: {duration}s, FPS: {fps}, Frames: {total_frames}")

if __name__ == "__main__":
    # Create demo directory if it doesn't exist
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    demo_dir = os.path.join(backend_dir, '..', 'data', 'demo')
    os.makedirs(demo_dir, exist_ok=True)

    # Create test video
    video_path = os.path.join(demo_dir, 'test_inspection.mp4')
    create_test_video(video_path, duration=5, fps=30)
