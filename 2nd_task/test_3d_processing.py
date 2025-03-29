import numpy as np
import pytest
from depth_processing import (
    load_image, generate_depth_map, generate_point_cloud
)

def test_generate_depth_map():
    dummy_img = np.ones((100, 100, 3), dtype=np.uint8) * 128
    gray, depth_map = generate_depth_map(dummy_img)
    assert gray.shape == (100, 100)
    assert depth_map.shape == (100, 100, 3)
    assert np.allclose(gray, 128)

def test_generate_point_cloud():
    gray = np.ones((50, 60), dtype=np.uint8) * 100
    points = generate_point_cloud(gray)
    assert points.shape == (50, 60, 3)

    assert np.all(points[..., 2] == 100)
    assert np.all(points[0, :, 0] == np.arange(60)) 
    assert np.all(points[:, 0, 1] == np.arange(50))  

def test_load_image_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_image("this_file_does_not_exist.png")

# pytest 실행
if __name__ == "__main__":
    pytest.main()