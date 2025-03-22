from datasets import load_dataset
from torchvision import transforms
from torchvision.transforms import functional as TF
from PIL import Image, ImageFilter
import os
import torch
import numpy as np
from scipy.ndimage import label
import torchvision.utils as vutils

save_dir = "image/preprocessed_samples"
os.makedirs(save_dir, exist_ok=True)

ds = load_dataset("ethz/food101", split="train[:50]")

# Resize, Grayscale, Denoise
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(),
    transforms.Lambda(lambda img: img.filter(ImageFilter.GaussianBlur(radius=0.5)))
])

# Normalized Tensor
to_tensor_norm = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Augmentation
def apply_augmentations(pil_img):
    return {
        "preprocessed": pil_img,
        "flip": TF.hflip(pil_img),
        "rotate": pil_img.rotate(90),
        "color": transforms.ColorJitter(
            brightness=0.5, contrast=0.5, saturation=1
        )(pil_img)
    }

# Brightness filtering
def is_bright_enough(tensor_img, threshold=0.4):
    unnorm = tensor_img * 0.5 + 0.5
    return unnorm.mean().item() >= threshold

# Object detection
def detect_largest_object(tensor_img, area_thresh=0.03):
    unnorm = tensor_img * 0.5 + 0.5
    np_img = unnorm.squeeze().numpy()  # [H, W]
    binary = (np_img > 0.3).astype(np.uint8)
    labeled, num = label(binary)

    if num == 0:
        return False, binary, 0.0

    max_area = max(np.sum(labeled == i) for i in range(1, num + 1))
    total = np_img.shape[0] * np_img.shape[1]
    ratio = max_area / total

    biggest_mask = (labeled == (np.argmax([np.sum(labeled == i) for i in range(1, num + 1)]) + 1))
    return ratio >= area_thresh, biggest_mask, ratio


for i, item in enumerate(ds):
    raw_img = item["image"]
    folder_name = f"{i:04}"
    folder_path = os.path.join(save_dir, folder_name)


    # Step 1: 전처리
    pre_img = preprocess(raw_img)

    # Step 2: 필터링 (전처리된 원본 이미지만 대상)
    tensor_img = to_tensor_norm(pre_img)
    if not is_bright_enough(tensor_img):
        continue

    valid, obj_mask, obj_ratio = detect_largest_object(tensor_img)
    mask_tensor = torch.tensor(obj_mask).unsqueeze(0).float()

    if not valid:
        continue
    
    # 필터링된 이미지 저장
    os.makedirs(folder_path, exist_ok=True)
    raw_img.save(os.path.join(folder_path, f"{folder_name}.png"))
    vutils.save_image(mask_tensor, os.path.join(folder_path, f"{folder_name}_preprocessed_mask.png"))

    # Step 3: 증강 (필터링 통과 후만 적용)

    augmented_imgs = apply_augmentations(pre_img)

    for key, pil_aug_img in augmented_imgs.items():
        aug_tensor = to_tensor_norm(pil_aug_img)
        pil_aug_img.save(os.path.join(folder_path, f"{folder_name}_{key}.png"))
