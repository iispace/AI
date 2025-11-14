# 파일 처리
import os, shutil 
from pathlib import Path

# 시각화 
import matplotlib.pyplot as plt 
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 깨짐 방지 설정
plt.rcParams['axes.unicode_minus'] = False     # 마이너스 기호 깨짐 방지 설정

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


# 장치 설정
# GPU 사용 가능하면 cuda, 아니면 CPU로 선택됨

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"device: {device}")


##############################################################################
# 사용할 사전학습 모델이 학습시 사용한 transform의 조건 확인
mean_imgnet = ResNet50_Weights.IMAGENET1K_V1.transforms().mean
std_imgnet  = ResNet50_Weights.IMAGENET1K_V1.transforms().std
input_size = ResNet50_Weights.IMAGENET1K_V1.transforms().crop_size
resize_size = ResNet50_Weights.IMAGENET1K_V1.transforms().resize_size
interpolation = ResNet50_Weights.IMAGENET1K_V1.transforms().interpolation
antialias = ResNet50_Weights.IMAGENET1K_V1.transforms().antialias  # 이미지를 resize할 때 생기는 계단 현상을 줄여주는 역할. 경계를 부드럽게 하면서 이미지를 축소하기 위함

print(f"mean_imgnet: {mean_imgnet}")
print(f"std_imgnet : {std_imgnet}")
print(f"resize_size : {resize_size}")
print(f"input_size : {input_size}")
print(f"interpolation: {interpolation}")
print(f"antialias: {antialias}")  

##############################################################################
from helper.MVTec_transforms import RN50Transform, SimpleTransform 

# 이미지 크기만 조정하고 다른 전처리는 하지 않는 기본 transform
#transform = SimpleTransform((224, 224))

# ImageNet 사전학습과 동일한 transform  
transform = RN50Transform(input_size=input_size, resize_size=resize_size, mean_=mean_imgnet, std_=std_imgnet)


##############################################################################
## 데이터(test 이미지 & Fault class name) 확인

# 이상 탐지 품목 선택
object_name = "pill"

# test 폴더에 포함된 상태 종류 가져와서 출력하기
data_group = "test"
sample_folder_path = Path(rf"..\Dataset\MVTec\{object_name}\{data_group}")
classes = [f.name for f in sample_folder_path.iterdir() if f.is_dir()]
print(f"classes in sample path: {classes}\n")

# test 이미지 중에서 샘플 이미지 한 장 시각화해 보기
sample_img_path = sample_folder_path / classes[0] / "000.png"
print(f"Sample image path: {sample_img_path}")

# 샘플 이미지 로드
sample_img = Image.open(sample_img_path)
print(f"sample img: {sample_img.size}\t {type(sample_img)}")

# 이미지 변환
sample_img_transformed = torch.clamp(transform(sample_img), 0.0, 1.0).unsqueeze(0)
print(f"\nsample img({transform.__class__.__name__}): {sample_img_transformed.shape}\t {type(sample_img_transformed)}")

# 시각화
fig, axs = plt.subplots(1,2, figsize=(6,3))
tensorized_sample_img = transforms.ToTensor()(sample_img)  
#tensorized_sample_img = transforms.ToTensor()(np.clip(np.array(sample_img), 0.0, 1.0))  
imgs = [tensorized_sample_img.permute(1,2,0), sample_img_transformed[0].permute(1,2,0)]
titles = ["original image", "transformed image" ]
for i, ax in enumerate(axs):
    ax.imshow(imgs[i])
    #ax.axis('off')
fig.suptitle(f"{data_group}\{classes[0]}")
plt.show();


##############################################################################
# 특징 추출기 (feature_extracotr) 인스턴스 생성
from helper.MVTec_backbone import patchcore_feature_extractor

patch_size = 3 
stride = 1

feature_extractor = patchcore_feature_extractor(patch_size=patch_size, stride=stride, device=device, verbose=True).to(device)

# 샘플 이미지 한 장을 특징 추출기에 입력으로 주고 특징 추출해 보기
features = feature_extractor(sample_img_transformed, verbose=True)


##############################################################################
## 정상 이미지 특징 분포 생성 (memory bank from Good images)
memory_bank = [] 

train_folder_path = Path(rf"..\Dataset\MVTec\{object_name}\train")

for pth in tqdm(train_folder_path.iterdir(), desc="memory_bank 생성 ", leave=False):
    for fn in tqdm(pth.iterdir()):
        with torch.no_grad():
            data = transform(Image.open(fn)).unsqueeze(0)
            features = feature_extractor(data, verbose=False)
            memory_bank.append(features.cpu().detach())

print(f"len(memory_bank): {len(memory_bank)}")   
print(f"memory_bank[0].shape: {memory_bank[0].shape}")  # memory bank의 첫 번째 feature map의 크기 출력  => 첫 번째 정상 이미지의 특성 분포 크기: torch.Size([784, 1536]) => (28x28, 512+1024)
memory_bank = torch.cat(memory_bank, dim=0)             # (len(memory_bank), num_features) 형태로 변환
print(f"memory_bank.shape   : {memory_bank.shape}")     # memory bank의 전체 크기 => 학습한 모든 정상 이미지의 특성 분포를 합친 것:  torch.Size([num_imgsx28x28, 1536]) 


##############################################################################
# 1. Random Sampling
sample_size = len(memory_bank)//10
print(f"sample_size: {sample_size}")

selected_indicies =  np.random.choice(len(memory_bank), size=sample_size, replace=False)
sub_random_memory_bank =  memory_bank[selected_indicies]

print(f"sub_random_memory_bank.sape: {sub_random_memory_bank.shape}")


##############################################################################
# 2. Coreset Sampling
# Coreset Sampler Code Source: https://github.com/amazon-science/patchcore-inspection/blob/main/src/patchcore/sampler.py
from helper.MVTec_PatchCore_Subsampler import ApproximateGreedyCoresetSampler, GreedyCoresetSampler

percent = 0.1

# coreset_sampler = GreedyCoresetSampler(percent, device)  # CUDA out of memory

coreset_sampler = ApproximateGreedyCoresetSampler(0.1, device, number_of_starting_points=10, dimension_to_project_features_to=512)
subsampled_coreset_memory_bank = coreset_sampler.run(memory_bank)
print(f"subsampled_coreset_memory_bank.shape: {subsampled_coreset_memory_bank.shape}")

check_point_file_name = rf"..\Dataset\MVTec\{object_name}\PatchSize_{patch_size}_subsampled_coreset_memory_bank_{int(percent*100)}p.pt"

torch.save(subsampled_coreset_memory_bank, check_point_file_name)
print(f"check_point saved to the file, {check_point_file_name}")

##############################################################################
# 저장해 둔 checkpoint 로드할 때
#subsampled_coreset_memory_bank = torch.load(check_point_file_name)
#print(f"subsampled_coreset_memory_bank.shape: {subsampled_coreset_memory_bank.shape}")  


##############################################################################
# Random Samples 와 Coreset Subsamples 비교를 위한 시각화
from helper.MVTec_Samples_Visualizer import plot_memory_bank_vs_subsamples

print(f"patch_size: {patch_size}\tstride: {stride}\n")
plot_memory_bank_vs_subsamples(mmb=memory_bank, random_subset=sub_random_memory_bank, coreset=subsampled_coreset_memory_bank, s=2)


##############################################################################
# Sampling 방식 선택
 
#subsampled_memory_bank = sub_random_memory_bank
subsampled_memory_bank = subsampled_coreset_memory_bank
print(f"subsampled_memory_bank.shape: {subsampled_memory_bank.shape}")  


##############################################################################
from helper.MVTec_Utils import anomaly_score_estimation

# k: 이상 점수(거리 계산)에 사용할 neighbour 수
k = 3

# 학습 이미지(정상 이미지)에 대한 이상 점수
train_folder_path = Path(rf"..\Dataset\MVTec\{object_name}\train")
train_classes = [f.name for f in train_folder_path.iterdir() if f.is_dir()]

anomaly_estimation_train = anomaly_score_estimation(feature_extractor, transform, subsampled_memory_bank, train_folder_path, train_classes, device, k=k, verbose=False)


# 테스트 이미지(정상 & 비정상 이미지)에 대한 이상 점수
test_folder_path = Path(rf"..\Dataset\MVTec\{object_name}\test")
test_classes = [f.name for f in test_folder_path.iterdir() if f.is_dir()]

anomaly_estimation_test  = anomaly_score_estimation(feature_extractor, transform, subsampled_memory_bank, test_folder_path,  test_classes,  device, k=k, verbose=False)



##############################################################################
for i, (k, v) in enumerate(anomaly_estimation_train.items()):
    print(f"{k:15}", len(v))

print()
print("anomaly scores of train (good) images: ")
for score in anomaly_estimation_train['anomaly_scores'][:5]:
    print(f"score: {score}")

for i, (k, v) in enumerate(anomaly_estimation_test.items()):
    print(f"{k:15}", len(v))

print()
print("anomaly scores of test (good or bad) images: ")
for score in anomaly_estimation_test['anomaly_scores'][:5]:
    print(f"score: {score}")


##############################################################################

from helper.MVTec_Utils import visualize_anomaly_scores 

# 훈련(정상) 이미지 영역별 이상 점수 시각화를 위한 shape 확인
print(f"segm_maps[0].shape: {anomaly_estimation_train['segm_maps'][0].shape}")
segm_map_img_good = anomaly_estimation_train['segm_maps'][0].squeeze().cpu()   # torch.Size([28, 28]) <= Batch와 Channel 차원 제거

# 시각화
visualize_anomaly_scores(anomaly_estimation_train, 5)
visualize_anomaly_scores(anomaly_estimation_test, 5)


##############################################################################
# 정상(train) 이미지와 test 이미지의 이상 점수 분포 비교 확인
from helper.MVTec_Utils import performance_metrics, plot_anomaly_score_distibution
# 사람이 몇 가지 임계값을 가정하여 직접 설정하는 경우

anomaly_score_mean_train = np.mean(anomaly_estimation_train['anomaly_scores'])
anomaly_score_std_train  = np.std(anomaly_estimation_train['anomaly_scores'])
print(f"anomaly_scores_train 평균   : {anomaly_score_mean_train:.5f}")
print(f"anomaly_scores_train 표준편차: {anomaly_score_std_train:.5f}\n")

# 정상과 이상을 구별하는 임계값을 평균 + 3*표준편차로 설정
threshold_1 = anomaly_score_mean_train + 4 * anomaly_score_std_train
threshold_2 = anomaly_score_mean_train + 3 * anomaly_score_std_train
threshold_3 = anomaly_score_mean_train + 2 * anomaly_score_std_train
threshold_4 = anomaly_score_mean_train + 1 * anomaly_score_std_train

for i, th in enumerate([threshold_1, threshold_2, threshold_3, threshold_4]):
    print(f"threshold_{i+1} = {th:.5f}")

manual_threshold = threshold_1
plot_anomaly_score_distibution(anomaly_estimation_train, manual_threshold)

plot_anomaly_score_distibution(anomaly_estimation_test, manual_threshold)


##############################################################################
# 사람이 몇 가지 임계값을 가정하여 직접 설정한 후, 그 중 한 가지 임계값으로 평가한 결과
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

y_trues_test = [float(x) for x in anomaly_estimation_test['y_trues']]
y_preds_test = [1 if float(item) >= manual_threshold else 0 for item in anomaly_estimation_test['anomaly_scores']]

# Confusion Matrix 생성 및 시각화
print("=== 사람이 몇 가지 임계값을 가정하여 직접 설정한 후, 그 중 한 가지 임계값으로 평가한 결과 ===")
print(f"Applied threshold: {manual_threshold:.5f}")
cm = confusion_matrix(y_trues_test, y_preds_test)  # numpy array (2 x 2)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Normal (0)", "Anomaly (1)"])
fig, ax = plt.subplots()
disp.plot(ax=ax)

ax.text(0.17, 1.8, f"(manual_threshold: {manual_threshold:.5f})", fontsize=10, color='blue')
plt.show();

pm_manual_test = performance_metrics(y_trues_test, y_preds_test)
print(f"manual_threshold: {manual_threshold:.5f}")
print("\nPerformance Metrics based on manual_threshold:")
for key, value in pm_manual_test.items():
    print(f"{key:>13}: {value:.4f}")  # 각 성능 지표 출력


##############################################################################
from helper.MVTec_Utils import get_best_threshold_and_visualize_roc

f1_based_best_threshold_dict, roc_curve_results_dict = get_best_threshold_and_visualize_roc(y_trues_test, anomaly_estimation_test, "F1")
mcc_based_best_threshold_dict, roc_curve_results_dict = get_best_threshold_and_visualize_roc(y_trues_test, anomaly_estimation_test, "MCC")

##############################################################################
youden_J_based_best_threshold_dict, roc_curve_results_dict = get_best_threshold_and_visualize_roc(y_trues_test, anomaly_estimation_test, "Youden's J")

youden_J_threshold = youden_J_based_best_threshold_dict['best_threshold']
youden_J_y_preds_test = [1 if float(item) >= youden_J_threshold else 0 for item in anomaly_estimation_test['anomaly_scores']] # threshold보다 크거나 같으면 비정상, 작으면 정상

pm = performance_metrics(y_trues_test, youden_J_y_preds_test)
print(f"youden_J_threshold: {youden_J_threshold:.5f}")
print("\nPerformance Metrics based on optimal_threshold:")
for key, value in pm.items():
    print(f"{key:>13}: {value:.4f}")  # 각 성능 지표 출력


##############################################################################


# 시각적으로 threshold 비교하기
"""
곡선이 수평에 가깝게 유지되는 구간 → 성능이 안정적
즉, threshold 값을 약간 바꿔도 TPR/FPR이 크게 흔들리지 않음

반대로 곡선이 기울기 급변하는 구간 → 민감한 구간
threshold를 조금만 바꿔도 성능이 확 바뀌는 위험한 영역
"""
thresholds = roc_curve_results_dict["thresholds"]
tpr = roc_curve_results_dict["tpr"]
fpr = roc_curve_results_dict["fpr"]

f1_based_best_threshold = f1_based_best_threshold_dict['best_threshold']
youden_J_best_threshold = youden_J_based_best_threshold_dict['best_threshold']

plt.figure()
plt.plot(thresholds, tpr, label="TPR (Recall)", color="green")
plt.plot(thresholds, fpr, label="FPR", color="red")
plt.axvline(x=manual_threshold,  color='#996633', linestyle='--', label=f'manual_threshold: {manual_threshold:.4f}')  # 50% 기준선
plt.axvline(x=f1_based_best_threshold, color='#131339', linestyle='--', label=f'f1_based_best_threshold: {f1_based_best_threshold:.4f}')  # 50% 기준선
plt.axvline(x=youden_J_best_threshold, color='#0000ff', linestyle='--', label=f'youden_J_best_threshold: {youden_J_best_threshold:.4f}')  # 50% 기준선
plt.xlabel("Threshold")
plt.ylabel("Rate")
plt.title("TPR & FPR by Threshold")
plt.legend()
plt.grid(True)
plt.show()


##############################################################################

print(f"object: {object_name}")
print(f"Applired transform: {transform.__class__.__name__}")

from helper.MVTec_Utils import final_visualization

final_visualization(anomaly_estimation_test, f1_based_best_threshold, classes[0], transform,  time_interval=1)

##############################################################################



