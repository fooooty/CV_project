import pandas as pd
import matplotlib.pyplot as plt

log_path = "/opt/homebrew/runs/detect/yolo_train/results.csv"
df = pd.read_csv(log_path)

# 정리: 컬럼명 앞뒤 공백 제거
df.columns = df.columns.str.strip()

plt.plot(df["metrics/precision(B)"], label="Precision")
plt.plot(df["metrics/recall(B)"], label="Recall")
plt.plot(df["metrics/mAP50(B)"], label="mAP@50")
plt.plot(df["metrics/mAP50-95(B)"], label="mAP@50-95")
plt.xlabel("Epochs")
plt.ylabel("Score")
plt.title("YOLOv8 Training Metrics")
plt.legend()
plt.grid(True)
plt.savefig("3rd_task/performance_from_results_csv.png")
plt.close()

print("[✓] 성능 그래프 저장 완료: performance_from_results_csv.png")
