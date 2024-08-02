import os
import json
import random
import shutil

def load_transforms(file_path):
    with open(file_path, 'r') as f:
        transforms = json.load(f)
    return transforms

def save_transforms(transforms, file_path):
    with open(file_path, 'w') as f:
        json.dump(transforms, f, indent=4)

def split_data(images, transforms, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1"
    
    total_images = len(images)
    random.shuffle(images)
    
    train_end = int(total_images * train_ratio)
    val_end = train_end + int(total_images * val_ratio)
    
    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]
    
    def filter_transforms(images):
        image_set = set(images)
        return {
            'camera_angle_x': transforms['camera_angle_x'],
            'frames': [frame for frame in transforms['frames'] if os.path.basename(frame['file_path']) in image_set]
        }
    
    train_transforms = filter_transforms(train_images)
    val_transforms = filter_transforms(val_images)
    test_transforms = filter_transforms(test_images)
    
    return train_images, val_images, test_images, train_transforms, val_transforms, test_transforms

def copy_files(images, src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for image in images:
        shutil.copy(os.path.join(src_dir, image), os.path.join(dst_dir, image))

def main(images_dir, transforms_path, output_dir):
    images = [img for img in os.listdir(images_dir) if img.endswith(('png', 'jpg', 'jpeg'))]
    transforms = load_transforms(transforms_path)
    
    train_images, val_images, test_images, train_transforms, val_transforms, test_transforms = split_data(images, transforms)
    
    copy_files(train_images, images_dir, os.path.join(output_dir, 'train'))
    copy_files(val_images, images_dir, os.path.join(output_dir, 'val'))
    copy_files(test_images, images_dir, os.path.join(output_dir, 'test'))
    
    save_transforms(train_transforms, os.path.join(output_dir, 'train', 'transforms_train.json'))
    save_transforms(val_transforms, os.path.join(output_dir, 'val', 'transforms_val.json'))
    save_transforms(test_transforms, os.path.join(output_dir, 'test', 'transforms_test.json'))

if __name__ == "__main__":
    images_dir = 'C:/Users/conni//Desktop/nestea_dataset/images'
    transforms_path = 'C:/Users/conni/Desktop/nestea_dataset/transforms.json'
    output_dir = 'C:/Users/conni/Desktop/nestea_dataset'
    
    main(images_dir, transforms_path, output_dir)
