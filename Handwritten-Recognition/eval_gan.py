from keras.models import load_model
from numpy.random import randn
from matplotlib import pyplot
import numpy as np
import uuid
import cv2
import os



TRAINED_MODEL_PATH="./models/wgan/wgan_model_v4_digit_7_33600_.h5"
IMAGE_SAVE_PATH="/home/naresh/Tarento/Handwritten-Digit-Recognition/generated_images/wgan/wgan_model_v4_digit_7_33600/"


###### load trained generator model
model = load_model(TRAINED_MODEL_PATH)

##### fixed vector length for generator input. It should be same as used in model training
latent_dim = 50

##### no of samples to generate
n_samples=5500

def generate_latent_points(latent_dim, n_samples):
    # generate points in the latent space
    x_input = np.random.randn(latent_dim * n_samples)
    # reshape into a batch of inputs for the network
    x_input = x_input.reshape(n_samples, latent_dim)
    return x_input

# create and save a plot of generated images (reversed grayscale)
def save_image(examples, n_samples):
    for i in range(n_samples):
        img = cv2.convertScaleAbs(examples[i], alpha=(255.0))
        cv2.imwrite(os.path.join(IMAGE_SAVE_PATH,str(uuid.uuid4())+".jpg"),img)

def save_image_wgan(examples, n_samples):
    for i in range(n_samples):
        img = cv2.convertScaleAbs(examples[i], alpha=(255))
        cv2.imwrite(os.path.join(IMAGE_SAVE_PATH,str(uuid.uuid4())+".jpg"),img)



latent_points = generate_latent_points(latent_dim, n_samples)

#generate images
X = model.predict(latent_points)
save_image_wgan(X, n_samples)