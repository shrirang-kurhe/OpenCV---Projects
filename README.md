🚦 **Traffic Flow Analysis**
📌 Overview
This project analyzes traffic flow from a video feed by:

Detecting vehicles in three distinct lanes.

Tracking each vehicle across frames.

Counting vehicles per lane in real-time.

Exporting results to a CSV file with details like Vehicle ID, Lane Number, Frame Count, and Timestamp.

The system uses YOLOv8 for object detection and SORT (Simple Online and Realtime Tracking) for tracking vehicles to avoid duplicate counts.

📂 Features
Vehicle Detection: Detects cars, trucks, buses, and motorbikes using YOLOv8 (COCO dataset).

Lane Definition: Manually defined lane boundaries to count vehicles separately per lane.

Vehicle Tracking: Uses SORT to maintain unique IDs for vehicles across frames.

Real-time Counting: Displays lane-wise counts directly on the video.

CSV Export: Logs every detected vehicle’s ID, lane number, frame count, and timestamp.

Summary Output: Displays total count per lane after processing.

📹 Example Output
Visual Output: Shows live detection boxes, tracking IDs, lane boundaries, and live counts.

CSV File:

python-repl
Copy
Edit
Vehicle_ID, Lane, Frame, Timestamp
3, 1, 12, 00:00:01
4, 2, 15, 00:00:01
5, 3, 18, 00:00:02
...
⚙️ Installation
1️⃣ Clone Repository
bash
Copy
Edit
git clone https://github.com/yourusername/traffic-flow-analysis.git
cd traffic-flow-analysis
2️⃣ Install Requirements
bash
Copy
Edit
pip install ultralytics opencv-python pandas numpy filterpy lap scikit-image
3️⃣ Download sort.py
Download sort.py from the SORT repository:
📂 https://raw.githubusercontent.com/abewley/sort/master/sort.py
Place it in the same folder as your Python script.

▶️ How to Run
Download a traffic video (e.g., Traffic Sample Video) and save it as traffic.mp4 in the project folder.

Run:

bash
Copy
Edit
python traffic_flow_analysis.py
Press q to quit video processing.

Output:

Live Video Window → Shows lanes & real-time counts.

CSV File → traffic_counts.csv with (Vehicle_ID, Lane, Frame, Timestamp).

Terminal → Shows total vehicle count per lane.

🛠 Technical Approach
Detection:

YOLOv8 (pre-trained on COCO) detects vehicles.

Classes used: car, truck, bus, motorbike.

Tracking:

SORT assigns a unique ID to each detected vehicle.

Prevents multiple counts when the same vehicle appears across frames.

Lane Definition:

Lanes are rectangular regions defined by (x1, y1) and (x2, y2).

Vehicle center coordinates (cx, cy) determine lane assignment.

Counting:

If a tracked vehicle enters a lane rectangle and hasn’t been counted before, increment count.

Output:

Overlay lane boundaries & counts on the video.

Save all detection logs to CSV.

📊 Challenges & Solutions

1. Duplicate Counting
   Challenge: Same vehicle detected multiple times in consecutive frames.
   Solution: Used SORT tracker to maintain a unique obj_id for each vehicle across frames.
2. Lane Misclassification
   Challenge: Vehicles close to lane boundaries sometimes counted in the wrong lane.
   Solution: Adjusted lane coordinates manually after test runs for accuracy.
3. Small/Fast Vehicles Missing
   Challenge: Motorbikes moving quickly or far away were missed.
   Solution: Used YOLOv8’s confidence threshold tuning (conf > 0.25) to balance precision and recall.
4. Real-time Performance
   Challenge: High-resolution videos slowed processing.
   Solution: Used YOLOv8n (nano model) instead of larger models for near real-time performance.

📅 Timeline
Day 1-2: Set up YOLO detection & SORT tracking.

Day 3: Defined lanes & implemented counting logic.

Day 4: CSV export & overlay visuals.

Day 5: Optimized performance.

Day 6: Testing & bug fixes.

Day 7: Documentation & video demo.

📦 Deliverables
✅ traffic_flow_analysis.py → Main Python script.

✅ traffic_counts.csv → Output file with detection logs.

✅ README.md → This documentation.

✅ Demo video showcasing real-time counting.

📌 Future Improvements
Automatic lane detection from road markings.

Support for multiple camera angles.

Integration with live CCTV feeds.

Use of ByteTrack for more robust tracking instead of SORT.
