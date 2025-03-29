import cv2
import numpy as np
import os

def load_image(path):
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {path}")
    return image

def generate_depth_map(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    depth_map = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    return gray, depth_map

def generate_point_cloud(gray_img):
    h, w = gray_img.shape
    X, Y = np.meshgrid(np.arange(w), np.arange(h))
    Z = gray_img.astype(np.float32)
    points_3d = np.dstack((X, Y, Z))
    return points_3d

if __name__ == "__main__":
    image = load_image("/Users/sonjiyeon/Desktop/CV_project/2nd_task/sample.png") 
    gray, depth = generate_depth_map(image)

    cv2.imshow("Original", image)
    cv2.imshow("Depth Map", depth)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    points = generate_point_cloud(gray)
    os.makedirs("2nd_task/result", exist_ok=True)

    # 저장
    np.save("2nd_task/result/point_cloud.npy", points)
    cv2.imwrite("2nd_task/result/depth_map.jpg", depth)
