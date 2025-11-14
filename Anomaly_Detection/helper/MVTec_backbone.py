# 특징 추출기(Pretrained encoder) class 구현
# Base code ref.: https://www.kaggle.com/code/akshaysom/anomaly-detection-using-patchcore-from-scratch

# 반복 처리
from tqdm.auto import tqdm  # 진행율 표시

# 이미지 기반 인공신경망 사용을 위한 라이브러리
import numpy as np 
from PIL import Image
import torch 
import torch.optim as optim 
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets import ImageFolder

# 이미지 변환기 생성, pretrained model 인스턴스 생성을 위한 라이브러리
import torchvision 
from torchvision.transforms import transforms 
from torchvision.models import resnet50, ResNet50_Weights

class patchcore_feature_extractor(nn.Module):
    def __init__(self, patch_size=3, stride=1, device='cpu', verbose=False):
        super(patchcore_feature_extractor, self).__init__()  # 부모 클래스인 nn.Module을 상속 받기 위한 초기화 
        
        self.patch_size = patch_size 
        self.stride = stride 
        self.device = device
        self.verbose = verbose 
        self.features = None
        
        self.model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        self.model.eval()
        # 모델이 학습하지 않도록 동결(freeze)
        for param in self.model.parameters():
            param.requires_grad =  False
        
        def hook(module, input, feature_map):
            self.features.append(feature_map)
            if (self.verbose):
                print(f"=> feature_map.shape: {feature_map.shape}")
                #print(f"module: {module.__class__.__name__}")      # Bottleneck
        
        # resnet50 모델의 "layer2" group과 "layer3" group의 마지막 layer에 대한 forward 계산이 끝났을 때 위에서 정의해 둔 "hook" 함수가 호출되도록 설정
        self.model.layer2[-1].register_forward_hook(hook)
        self.model.layer3[-1].register_forward_hook(hook)
        
    def forward(self, x, verbose=False):
        self.verbose = verbose
        self.features = []
        x = x.to(self.device)
        with torch.no_grad():
            # feature extraction
            _ = self.model(x)  # forward 계산 시, register_forward_hood()에 의해서 self.features에 자동으로 저장되는 feature_map만 사용하면 되므로, 모델 전체의 출력값을 반환 받을 필요가 없음.
            
        # locally aware patch feature 생성을 위한 객체 생성
        self.avgpool = torch.nn.AvgPool2d(kernel_size=self.patch_size, stride=self.stride)
        fmap_size = self.features[0].shape[-2]  # (28, 28)
        # 최종 출력되는 feature map의 크기가 fmap_size=(28,28)이 되도록 하는 adaptive pooler 생성
        self.adaptive_avg_pool = torch.nn.AdaptiveAvgPool2d(fmap_size) 
        
        ### shape 변화 추적용 출력
        if verbose:
            for i, ft_map in enumerate(self.features):
                avg_pooled_ft_map = self.avgpool(ft_map)
                adaptive_avg_pooled_ft_map = self.adaptive_avg_pool(avg_pooled_ft_map)
                print(f"\n[{i}] ft_map.shape                    : {ft_map.shape}")
                print(f"[{i}] avg_pooled_ft_map.shape         : {avg_pooled_ft_map.shape}")
                print(f"[{i}] adaptive_avg_pooled_ft_map.shape: {adaptive_avg_pooled_ft_map.shape}")
                print("-"*80)
            print("="*100)
        ###
        
        # locally aware patch feature 생성
        # feature map을 average pooling하고 크기 조정 => resized_maps: [1,512,28,28], [1,1024,28,28]
        resized_maps = [self.adaptive_avg_pool(self.avgpool(fmap)) for fmap in self.features]
        
        patchcore_features = torch.cat(resized_maps, dim=1)  # # feature map들을 C차원에서 합치기 => [1, 512, 28, 28]+[1, 1024, 28, 28]=[1, 1536, 28, 28]
        patchcore_features = patchcore_features.reshape(patchcore_features.shape[1], -1).T # [1536, 28, 28] => [1536, 28x28] => [28*28, 1536]  = [784, 1536]
        
        return patchcore_features
        
            
