import cv2
import torch
import numpy as np
from ultralytics import SAM

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model = SAM("./pt/sam2.1_t.pt").to(device)
frame_buffer = []
def run_sam2(frame, bboxes):
    # Run inference with the latest frame and multiple bboxes prompt
    results = model(frame, bboxes=bboxes, show=False, stream=False, device=device)
    return results

def preprocess_mask(mask):
    # Smooth the mask to reduce sharp edges
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    return mask

def process_frame(frame, bboxes):
    # Run the model on the given frame
    results = run_sam2(frame, bboxes)
    masks = results[0].masks

    # Apply each mask to cut out only the human portion in the frame
    if masks is not None and hasattr(masks, 'data'):
        for i in range(masks.data.shape[0]):
            mask = masks.data[i].cpu().numpy()
            mask = (mask * 255).astype(np.uint8)

            # Preprocess the mask to smooth edges
            mask = preprocess_mask(mask)

            # Inpainting: Remove the masked area from the original frame
            inpainted_frame = cv2.inpaint(frame, mask, inpaintRadius=10, flags=cv2.INPAINT_TELEA)

            # Display the inpainted frame
            cv2.imshow(f"Inpainted Frame {i}", inpainted_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

def buffer_frames(frame, bboxes, buffer_size=10):
    global frame_buffer

    frame_buffer.append(frame)

    # Check if the buffer is full
    if len(frame_buffer) >= buffer_size:
        # Only process the latest frame
        latest_frame = frame_buffer[-1]
        process_frame(latest_frame, bboxes)

        # Clear the buffer
        frame_buffer.clear()

def main():
    video_path = "./image/01_dog.mp4"
    bboxes = [[200, 100, 500, 700]]

    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        buffer_frames(frame, bboxes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
