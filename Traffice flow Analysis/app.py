import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from sort import Sort  # Simple Online and Realtime Tracking
import time

# ====== Load YOLOv8 Model ======
model = YOLO('yolov8n.pt')  # small & fast model

# ====== Initialize Tracker ======
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

# ====== Lane Definitions (Adjust for your video) ======
# Format: (top_left), (bottom_right)
lanes = {
    1: ((50, 300), (200, 720)),
    2: ((220, 300), (400, 720)),
    3: ((420, 300), (600, 720))
}

# ====== Counters ======
counts = {1: 0, 2: 0, 3: 0}
vehicle_log = []

# ====== Open Video ======
cap = cv2.VideoCapture(r"C:\Users\Shree\vs_code\OpenCV\Traffice flow Analysis\4K Road traffic video for object detection and tracking - free download now!.mp4")
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    timestamp = time.strftime("%H:%M:%S", time.gmtime(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))

    # ====== Vehicle Detection ======
    results = model(frame, stream=True)
    detections = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            if model.names[cls_id] in ["car", "truck", "bus", "motorbike"]:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                detections.append([x1, y1, x2, y2, float(box.conf[0])])

    if len(detections) > 0:
        detections = np.array(detections)
    else:
        detections = np.empty((0, 5))

    # ====== Tracking ======
    tracked_objects = tracker.update(detections)

    for obj in tracked_objects:
        x1, y1, x2, y2, obj_id = map(int, obj)
        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

        # ====== Check Lane ======
        for lane_num, ((lx1, ly1), (lx2, ly2)) in lanes.items():
            if lx1 < cx < lx2 and ly1 < cy < ly2:
                if obj_id not in [v[0] for v in vehicle_log]:
                    counts[lane_num] += 1
                    vehicle_log.append((obj_id, lane_num, frame_count, timestamp))

        # Draw Tracking Box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{obj_id}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # ====== Draw Lanes & Counts ======
    for lane_num, ((lx1, ly1), (lx2, ly2)) in lanes.items():
        cv2.rectangle(frame, (lx1, ly1), (lx2, ly2), (255, 0, 0), 2)
        cv2.putText(frame, f"Lane {lane_num}: {counts[lane_num]}",
                    (lx1, ly1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255, 255, 255), 2)

    cv2.imshow("Traffic Flow Analysis", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# ====== Save to CSV ======
df = pd.DataFrame(vehicle_log, columns=["Vehicle_ID", "Lane", "Frame", "Timestamp"])
df.to_csv("traffic_counts.csv", index=False)

print("Total Counts per Lane:", counts)
