# 사전학습 모델과 동일한 조건으로 transform을 생성하기 위한 class 구현
import numpy as np 
import torch 
from torchvision.transforms import InterpolationMode, transforms 

class RN50Transform:
    def __init__(self, input_size=(224,224), resize_size=256, mean_=[0.485, 0.456, 0.406], std_=[0.229, 0.224, 0.225]):
        self.input_size = input_size
        self.resize_size = resize_size
        self.mean = mean_
        self.std = std_
        self.name = "ResNet50.IMAGENET1K_V1.transform"
        
        self.transform = transforms.Compose([
            transforms.Resize(resize_size, interpolation=InterpolationMode.BILINEAR),
            transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean_, std=std_)
        ])
        
    def __call__(self, img):
        return self.transform(img)
    
    def reverse_transform(self, img):
        out_img = img.clone().cpu() 
        for img_, m, s in zip(out_img, self.mean, self.std):
            # 역정규화: x = x * std + mean
            img_.mul_(s).add(m)  
        out_img = np.transpose(out_img, (1,2,0)) # C, H, W => H, W, C
        out_img = np.clip(out_img, 0, 1)
        return out_img 
            
        

# 비교를 위한 SimpleTransform class 정의
class SimpleTransform:
    def __init__(self, input_size=(224,224)):
        self.input_size = input_size 
        self.name = "SimpleTransform"
        
        self.transform = transforms.Compose([
            transforms.Resize(input_size),
            transforms.ToTensor()
        ])
        
    def __call__(self, img):
        return self.transform(img)
    
    def reverse_transform(self, img):
        out_img = img.clone().cpu()
        out_img = np.transpose(out_img, (1,2,0))  # C, H, W => H, W, C 
        out_img = np.clip(out_img, 0, 1)
        return out_img 
