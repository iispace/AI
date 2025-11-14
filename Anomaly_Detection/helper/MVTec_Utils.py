from pathlib import Path 
from tqdm.auto import tqdm 
from PIL import Image 
from typing import List
import matplotlib.pyplot as plt

import torch 

# 이상 점수 계산 함수 정의
def anomaly_score_estimation(backbone, transform, subsampled_mmb, data_path, classes:List[str], device:torch.device, k=1, verbose=False):
    """_summary_

    Args:
        backbone (module): feature_extractor module
        transform (_type_): tranform
        subsampled_mmb (torch.tensor): subsampled memory bank
        data_path (Path object): 
        device (torch.device): _description_
        k (int, optional): _description_. Defaults to 1.
        verbose (bool, optional): _description_. Defaults to False.
    Returns:
        anomaly_scores, segm_maps, y_trues, class_labels, files
    """
    anomaly_scores, segm_maps = [], []
    files, y_trues = [], []
    
    for class_name in classes:
        img_folder_path = Path(rf"{data_path}\{class_name}")
        for file in tqdm(img_folder_path.iterdir(), desc=f"{data_path}\{class_name} ",  leave=True):
            files.append(file)
            img = transform(Image.open(file)).unsqueeze(dim=0).to(device)
            
            # 이미지 특성 추출
            with torch.no_grad():
                features = backbone(img, verbose=False) # features.shape: torch.Size([784, 1536]) => 784 = 28x28, 1536=512+1024
                
            # 현재 이미지와 학습된 이미지 분포 간의 거리 계산
            distances = torch.cdist(features, subsampled_mmb.to(device), p=2)  # torch.Size([784, num_samples]), # p=2 means Euclidean distance, p=1 means Manhattan distance
            topk_distances, topk_distances_idxs = torch.topk(distances, k=k, dim=1, largest=False)  # topk_distances.shape: torch.Size([784, k]) 

            # 이미지 영역별 이상 점수
            distance_scores = torch.mean(topk_distances, dim=1) # dist_score.shape: torch.Size([784])

            # 해당 이미지에서 가장 이상해 보이는 영역의 점수
            max_anomaly_score = torch.max(distance_scores) 
            anomaly_scores.append(max_anomaly_score.cpu().numpy())
            
            y_trues.append(0 if class_name == "good" else 1)
            
            # 영역별 이상 점수를 시각화하기 위한 map 생성
            segm_map = distance_scores.view(1,1,28,28) 
            segm_maps.append(segm_map)
            
        if verbose:
            print(f"len(anomaly_scores)   : {len(anomaly_scores)}")
            print(f"\ndistances per image : {distances.shape}")
            print(f"distance_scores per image : {distance_scores.shape}")
            print(f"max_anomaly_score of the last image: {max_anomaly_score}")
            print("="*80)
    
    out = {'anomaly_scores': anomaly_scores, 'segm_maps': segm_maps, 'y_trues': y_trues, 'files': files}
    return out    


# 이상 점수 시각화 함수 정의
def visualize_anomaly_scores(anomaly_estimation_dict, num_img=5):
    fig, axs = plt.subplots(1,num_img, figsize=(12,3))
    for i, ax in enumerate(axs):
        #ax.axis("off")
        img = anomaly_estimation_dict['segm_maps'][i].squeeze().cpu()
        fn = "\\".join(anomaly_estimation_dict['files'][i].parts[-3:])
        ax.imshow(img, cmap='gray')
        ax.set_title(f"distance_scores of\n({fn})", fontsize=10)
    plt.show();
    



# 이진분류 문제의 성능 지표 산출 함수 정의
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef, roc_auc_score
def performance_metrics(y_trues_, y_preds_):
    accuracy = accuracy_score(y_trues_, y_preds_)
    precision = precision_score(y_trues_, y_preds_)
    recall = recall_score(y_trues_, y_preds_)
    f1 = f1_score(y_trues_, y_preds_)
    mcc = matthews_corrcoef(y_trues_, y_preds_)
    auc_roc = roc_auc_score(y_trues_, y_preds_)
    
    pm = {'Accuracy'   : accuracy,
         'Precision'   : precision,  
         'Recall'   : recall,
         'F1_score'   : f1,  
         'AUC_ROC(이산형)': auc_roc,
         'Matthews-Coef': mcc}
    
    return pm     

# 분포 히스토그램 그리기 함수 정의
def plot_anomaly_score_distibution(anomaly_estimation_dict, threshold_):
    data_group = anomaly_estimation_dict['files'][0].parts[3]
    plt.hist(anomaly_estimation_dict['anomaly_scores'], bins=50)
    plt.vlines(x=threshold_, ymin=0, ymax=30, color='r')
    plt.title(f"Anomaly score distribution for train dataset with threshold={threshold_:.5f}", fontsize=10)

    x_lim_width = plt.xlim()[1] - plt.xlim()[0]
    x_pos_auto = plt.xlim()[0] + x_lim_width / 4
    plt.text(x_pos_auto, 30, f"{data_group} 이미지들(정상)의 이상 점수 분포");
    
    
# F1 점수,MCC 또는 Youden's J statistic을 기준으로 최적의 임계값을 선택하는 함수 정의
from sklearn.metrics import roc_curve, confusion_matrix, ConfusionMatrixDisplay

def get_best_threshold_and_visualize_roc(y_trues_, anomaly_estimation_dict, base_name='F1', cm_text_position=(0.0, 1.8)):
    
    fpr, tpr, thresholds = roc_curve(y_trues_, anomaly_estimation_dict['anomaly_scores'])
    #print("fpr, tpr, thresholds: ", fpr, tpr, thresholds)
    roc_curve_results = {'fpr': fpr, 'tpr': tpr, 'thresholds': thresholds}

    if base_name == 'F1':
        values = [f1_score(y_trues_, anomaly_estimation_dict['anomaly_scores'] > threshold) for threshold in thresholds]
    elif base_name == 'MCC':
        values = [matthews_corrcoef(y_trues_, anomaly_estimation_dict['anomaly_scores'] > threshold) for threshold in thresholds]
    elif base_name == "Youden's J":
        values = tpr - fpr

    best_threshold = thresholds[np.argmax(values)]
    best_threshold_dict = {'name': base_name, 'score': max(values), 'best_threshold': best_threshold}
    print(best_threshold_dict)
    
    # roc 커브 시각화
    auc_roc = roc_auc_score(y_trues_, anomaly_estimation_dict['anomaly_scores'])
    
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.4f)' % auc_roc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random guess')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.text(0.5, 0.2, f'{base_name}_based_best_threshold = {best_threshold:.4f}', fontsize=10)
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

    # confusion matrix 생성 및 시각화
    print("="*75)
    print(f"가장 높은 {base_name} 점수를 만든 threshold={best_threshold:.4f} 조건에서의 혼돈행렬 생성")
    cm = confusion_matrix(y_trues_, (anomaly_estimation_dict['anomaly_scores'] >= best_threshold).astype(int))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['GOOD', 'BAD'])
    fig, ax = plt.subplots()
    disp.plot(ax=ax)

    ax.text(cm_text_position[0], cm_text_position[1], f"({base_name}_based_best_threshold: {best_threshold:.5f})", fontsize=10, color='blue')
    plt.show();

    return best_threshold_dict, roc_curve_results




import time
from IPython.display import clear_output 
from torchvision.transforms import transforms
import numpy as np

def final_visualization(anomaly_estimation_dict, threshold_, types_to_vis_, transform, time_interval=2):
    
    class_label = ["GOOD", "BAD"]
    
    gt_img_paths = [Path(str(path_).replace("test", "ground_truth").replace(".png", "_mask.png")) for path_ in anomaly_estimation_dict['files']]
    img_paths = anomaly_estimation_dict['files']
    segm_maps = anomaly_estimation_dict['segm_maps']
    anomaly_scores = anomaly_estimation_dict['anomaly_scores']
    y_preds_test_ = [1 if float(item) >= threshold_ else 0 for item in anomaly_estimation_dict['anomaly_scores']] # threshold보다 크거나 같으면 비정상, 작으면 정상
    
    for i, (img_file, segm_map, gt_img_file, img_anomaly_score) in enumerate(zip(img_paths, segm_maps, gt_img_paths, anomaly_scores)):
        fault_type = img_file.parts[-2]
        if fault_type in types_to_vis_:
            org_img =  transforms.Compose([
                        transforms.Resize(224), 
                        transforms.ToTensor(), 
                    ])(Image.open(img_file)).cpu().permute(1,2,0)
            #transformed_img = transform(Image.open(img_file)).unsqueeze(0).permute(0,2,3,1) 
            transformed_img = torch.clamp(transform(Image.open(img_file)), 0.0, 1.0).unsqueeze(0).permute(0,2,3,1) 
            heat_map = torch.nn.functional.interpolate(      # heat_map.shape: (224, 224)
                    segm_map,
                    size=(224,224),
                    mode='bilinear',
                ).cpu().squeeze().numpy()
            
            ground_truth = np.array(Image.open(gt_img_file))  # ground truth segmentation map     
            
            binary_threshold_map = heat_map > threshold_
            
            images = [org_img.squeeze(0).cpu(), transformed_img.squeeze(0).cpu(), heat_map, binary_threshold_map, ground_truth]
            titles = [f"Org Img({fault_type})", f"Transformed({fault_type})", f"Anomaly Score: {img_anomaly_score:.2f} | {class_label[y_preds_test_[i]]}", f"binary threshold map", "ground truth"]
            cmaps = [None, None, 'jet', 'gray', 'gray']
            
            fig, axs = plt.subplots(1, 5, figsize=(15, 3))

            for i, ax in enumerate(axs):
                if i == 2:
                    ax.imshow(images[i], cmap='jet', vmin=threshold_, vmax=threshold_*2)
                else:
                    ax.imshow(images[i], cmap=cmaps[i])

                ax.set_title(titles[i])            
            
            plt.show()
            
            time.sleep(time_interval)
            clear_output(wait=True)
        
