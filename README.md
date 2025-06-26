# ViMatch
This project is my graduation thesis developing an automatic Vietnamese text summarization system based on semantic space analysis. It is based on the paper *[Extractive Summarization as Text Matching](https://arxiv.org/abs/2004.08795)* and has purely academic value, with no commercial intent.

Here is the GitHub repository of the original author of MatchSum: [MatchSum](https://github.com/maszhongming/MatchSum)

## Installation

The following command installs all necessary packages:

```
pip install -r requirements.txt
```

## Dataset

The dataset used in this project can be downloaded from [this link](https://drive.google.com/file/d/1JbyfiWEUpKLfRNFbV_s_rpDVk5nrHcrt/view?usp=drive_link)

Note: This dataset is intended solely for my project. If you wish to use a different dataset, you can access `VNMD` to collect your own data. The provided code can be reused, but you may need to adapt it to suit other websites or data sources.

## Train

You can run the following command to train the model:

```
CUDA_VISIBLE_DEVICES=0,1 python train_matching.py --mode=train --encoder=phobert --save_path=./phobert --gpus=0,1
```


## Test

After completing the training process, several best checkpoints are stored in a folder named after the training start time. You can run the following command to get the results on test set (only one GPU is required for testing):

```
CUDA_VISIBLE_DEVICES=0 python train_matching.py --mode=test --encoder=phobert --save_path=./phobert/2025-06-20-06-47-43-595777/ --gpus=0
```
You must also install `pyrouge` in order to evaluate the model. You can follow the setup instructions provided [here](https://gist.github.com/donglixp/d7eea02d57ba2e099746f8463c2f6597)

## Results 
Test set (the average of three runs)

| Scenarios | R-1 | R-2 | R-L |
| :------ | :------: | :------: | :------: |
| ROUGE | 64.64 | 32.66 | 47.79 | 
| TF-IDF | 65.87 | 34 | 48.58 |

The results were obtained on a self-constructed dataset, which is not of the same quality as the original model's data. Hence, used for reference only and not for direct comparison with the original results.