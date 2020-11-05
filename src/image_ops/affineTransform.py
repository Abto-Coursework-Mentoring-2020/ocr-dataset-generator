from image_ops.base import BaseImageOperation
from transformations import affineTransform


class AffineTransformOperation(BaseImageOperation):
    """
    Class that implements affine transformation operation of an image
    """
    def __init__(self, pts1, pts2):
        self._op = lambda X: affineTransform(X, pts1, pts2)
