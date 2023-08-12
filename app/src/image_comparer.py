from huggingface_hub import from_pretrained_keras
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import torch
import clip

class ImageComparer():
    def __init__(self) -> None:
        
        self._device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self._model_cifar = from_pretrained_keras("keras-io/cifar10_metric_learning")
        self._model, self._preprocess = clip.load("ViT-L/14", device=self._device)

    def compare(self, image1, image2):
        image1 = image1.resize((1024, 1024))
        image2 = image2.resize((1024, 1024))
        # Change images to rgb or bgr
        img1 = self._preprocess(image1).to(self._device)
        img2 = self._preprocess(image2).to(self._device)
        print(img1.shape, img2.shape)
        img = torch.stack([img1, img2])
        with torch.no_grad():
            image_features = self._model.encode_image(img)
        clip_score = image_features.corrcoef()[0, 1].item()

        img1 = np.array(image1.resize((32, 32)))[:,:,:3]
        img2 = np.array(image2.resize((32, 32)))[:,:,:3]
        img1 = np.expand_dims(img1 / 255, axis=0)
        img2 = np.expand_dims(img2 / 255, axis=0)
        print(img1.shape, img2.shape)
        img = np.append(img1, img2, axis=0)
        embeddings = self._model_cifar.predict(img)
        cifar_score = np.corrcoef(embeddings)[0, 1]

        ssim_score = ssim(np.array(image1), np.array(image2), channel_axis=2)

        mean_score = (clip_score + ssim_score + cifar_score) / 3
        ret = {"clip": clip_score, "ssim": ssim_score, "cifar": cifar_score, "mean": mean_score}
        return ret
