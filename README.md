# FBC-APL: A Camera Fingerprint based Morphing Detection and Fingerprinting Model
This is the official repository of the paper: Fusion-based Few-Shot Morphing Attack Detection and Fingerprinting, including codes, data and pre-trained model.

Stay tuned for the updating!!!

![arch](fig/pipeline.png)

### link:

[[PDF]](https://arxiv.org/pdf/2210.15510.pdf)
[[Arxiv]](https://arxiv.org/abs/2210.15510)

# Introduction
This is an implementation of few-shot learning based morphing attacks detection model, and is extended from binary detection to multiclass fingerprinting. The model aims at learning discriminative features which can be generalized to unseen morphing attack types from predefined presentation attacks. A large-scale face morphing database is collected, which contains 5 face subdatasets and 8 different morphing algorithms, to benchmark the proposed method.

1. Face morphing attack detection (MAD): 
![arch](fig/MAD_few_shot.png)

2. Face morphing attack fingerprinting (MAF):
![arch](fig/fingerprint.png)


# Mudules
# 1. features extraction
![arch](fig/avg_feature.png)
left: bona fide; right: morphed faces.

* PRNU: handcrafted sensor pattern noise extractor
* Noiseprint: a CNN-based camera model fingerprint

[[PRNU]](https://dde.binghamton.edu/download/camera_fingerprint/)
[[Noiseprint]](https://github.com/grip-unina/noiseprint)

# 2. feature fusion
We use FBC (paper 'Revisiting Bilinear Pooling: A Coding Perspective').
![arch](fig/fbc.png)

[[paper]](https://ojs.aaai.org/index.php/AAAI/article/view/5811)

# 3. few-shot learning
Our model is based on a few-shot learning model : APL ('Adaptive Posterior Learning: few-shot learning with a surprise-based memory module').
![arch](fig/MAD_APL.png)

[[model]](https://github.com/cogentlabs/apl)



# Others:
# * Preprocessing: 
 [[face detection and cropping]](https://github.com/Practical-CV/Facial-Landmarks-Detection-with-DLIB) 
  
 







