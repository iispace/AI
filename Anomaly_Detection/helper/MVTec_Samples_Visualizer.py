# Random Samples 와 Coreset Subsamples의 시각적 비교를 위한 함수 정의

import torch 
import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE 

def DimensionReducer(data_np):
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data_np)
    reduced_data_ts = torch.from_numpy(reduced_data).float()
    return reduced_data_ts

def plot_memory_bank_vs_subsamples(mmb, random_subset, coreset, title="Random Sampling vs Coreset Sampling of Memory Bank", s=3, alpha=0.6):
    
    print(f"memory_bank: {mmb.shape}")
    print(f"random  samples: {random_subset.shape}")
    print(f"coreset samples: {coreset.shape}")
    
    memory_bank_2D = DimensionReducer(mmb.numpy())
    random_subset_2D = DimensionReducer(random_subset.numpy())
    coreset_2D = DimensionReducer(coreset.numpy())
    
    data   = [random_subset_2D, coreset_2D]
    titles = ['random samples(2D with PCA)', 'coreset samples(2D with PCA)']
    

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))

    for i, ax in enumerate(axs):
        ax.scatter(memory_bank_2D[:, 0], memory_bank_2D[:, 1],   label='memory_bank(2D with PCA)', alpha=alpha, s=s)
        ax.scatter(data[i][:, 0], data[i][:, 1], color="#ffa500", label="subsampled_memory_bank(2D with PCA)", alpha=alpha, s=s+1)
        ax.set_title(titles[i])

    # 제목
    fig.suptitle(title, fontsize=12)

    # 공통 범례 (제목 아래에 위치)
    handles, legend_labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, legend_labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 0.92))

    # layout 조정: rect 위쪽 여백을 줄여 제목과 범례가 가까워지도록
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.show()
 
