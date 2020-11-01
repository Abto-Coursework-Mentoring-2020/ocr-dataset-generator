from numpy.core.fromnumeric import mean
import tensorflow as tf
import numpy as np
from numpy.random import randint
from enum import Enum


class NoiseTypes(Enum):
    """
    Enumeration type for different types of noises.
    
    SALT_AND_PEPPER: replaces random pixels with 0 or 1.
    GAUSSIAN: gaussian-distributed additive noise.
    POISSON: poisson-distributed noise generated from the data.
    SPECKLE: multiplicative noise using out = image + n * image, where n is uniform noise 
        with specified mean & variance.
    """
    SALT_AND_PEPPER = 1
    GAUSSIAN = 2
    POISSON = 3
    SPECKLE = 4

def noisify(image: tf.Tensor, noise_type: NoiseTypes, **kwargs) -> tf.Tensor:
    """
    Function adds selected randomly sampled noise to an image.

    Args:
        image (tf.Tensor): tensor representing an image
        noise_type (NoiseTypes): type of noise to use (e.g Gaussian, S&P, etc)
        amount (float): value within [0;1] range specifying ratio of all pixels in an image
            that will be distorted (only for Salt and Pepper noise).
        salt_vs_pepper (float): value within [0;1] that meet the equation 
            N_salt = salt_vs_pepper * N_distorted and
            N_pepper = (1 - salt_vs_pepper) * N_distorted. (only for Salt and Pepper noise).

    Returns:
        tf.Tensor: tensor representing the noised image
    """

    image = tf.cast(image, 'float32')
    noised = image.numpy()
    
    if noise_type == NoiseTypes.SALT_AND_PEPPER:
        salt_vs_pepper = float(kwargs.get('salt_vs_pepper', 0.5))
        amount = float(kwargs.get('amount', 0.01))

        if not (0.0 <= salt_vs_pepper <= 1.0 and 0.0 <= amount <= 1.0):
            raise ValueError('salt_vs_pepper and amount ratios must be within [0;1] range')
        
        H, W = image.shape[:2]
        num_distorted_pixels = H * W * amount

        num_salt_pixels = int(num_distorted_pixels * salt_vs_pepper)
        # salt i, j indices in an image
        noised[randint(0, H - 1, num_salt_pixels), randint(0, W - 1, num_salt_pixels)] = 255.0

        num_pepper_pixels = int(num_distorted_pixels * (1 - salt_vs_pepper)) 
        # pepper i, j indices in an image
        noised[randint(0, H - 1, num_pepper_pixels), randint(0, W - 1, num_pepper_pixels)] = 0.0
    elif noise_type == NoiseTypes.GAUSSIAN:
        noised = image + tf.random.normal(image.shape, mean=kwargs.get('mean', 0), stddev=kwargs.get('stddev', 1))
    elif noise_type == NoiseTypes.SPECKLE:
        noised = image + image * tf.random.normal(image.shape, mean=kwargs.get('mean', 0), stddev=kwargs.get('stddev', 1))
    elif noise_type == NoiseTypes.POISSON: 
        noised = np.random.poisson(lam=image, size=None)
    else:
        raise ValueError('Ivalid noise type given. Must be one of NoiseTypes')
    
    return tf.cast(noised, 'uint8')
