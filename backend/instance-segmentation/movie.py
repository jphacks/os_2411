import cv2
import time
import torch
import numpy as np
from ultralytics import SAM

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model = SAM("sam2.1_s.pt").to(device)

def run_sam2(frame, bboxes):
    # Run inference with multiple bboxes prompt
    results = model(frame, bboxes=bboxes, show=False, stream=False)
    return results

def process_video(cap, bboxes):
    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Initialize variables for FPS calculation
    frame_count = 0
    start_time = time.time()

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break  # Exit the loop if no frame is captured
        
        # Run the model on the frame
        results = run_sam2(frame, bboxes)
        masks = results[0].masks  # Masksオブジェクトを取得

        # Apply each mask to cut out only the human portion in the frame
        if masks is not None and hasattr(masks, 'data'):
            for i in range(masks.data.shape[0]):
                mask = masks.data[i].cpu().numpy()  # マスクをNumPy配列に変換
                mask = (mask * 255).astype(np.uint8)  # スケール変換して白黒画像にする
                masked_frame = cv2.bitwise_and(frame, frame, mask=mask)  # マスクを適用して人物部分のみを抽出

                cv2.imshow(f"Masked Frame {i}", masked_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    video_path = "./image/01_dog.mp4"  # Specify your video path
    # Example bounding boxes: [x_min, y_min, x_max, y_max]
    bboxes = [[200, 100, 500, 700]]  # Multiple bounding boxes
    cap = cv2.VideoCapture(video_path)
    process_video(cap, bboxes)

if __name__ == "__main__":
    main()
