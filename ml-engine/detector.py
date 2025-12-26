import os
import sys
import json
from ultralytics import YOLO

class AegisVision:
    def __init__(self, model_path='yolov8n.pt'):
        print(f"[-] [AEGIS_INIT] Loading Neural Network: {model_path}...")
        try:
            self.model = YOLO(model_path) 
            print("[+] [AEGIS_READY] Vision Core Online.")
        except Exception as e:
            print(f"[!] [CRITICAL_ERROR] Model Failed to Load: {e}")
            sys.exit(1)

    def scan_threat(self, image_path):
        if not os.path.exists(image_path):
            return {"error": f"Image file not found: {image_path}"}

        print(f"[*] [SCANNING] Processing: {image_path}")
        # Run AI (Low confidence threshold so it sees EVERYTHING)
        results = self.model(image_path, conf=0.1, verbose=False) 
        
        detections = []
        
        for result in results:
            for box in result.boxes:
                label = self.model.names[int(box.cls[0])]
                confidence = float(box.conf[0])
                
                # Add everything to the list, no matter what it is
                detections.append({
                    "detected_object": label,
                    "confidence": f"{round(confidence * 100, 1)}%",
                    "action_protocol": "LOGGING_ONLY",
                    "severity": "INFO"
                })

        return {
            "system": "A.E.G.I.S. Vision V1",
            "status": "OBJECTS_DETECTED" if detections else "NO_VISUALS",
            "total_objects": len(detections),
            "data": detections
        }

if __name__ == "__main__":
    bot = AegisVision()
    # RUN THE SCAN
    report = bot.scan_threat("test.jpg")
    print(json.dumps(report, indent=4))