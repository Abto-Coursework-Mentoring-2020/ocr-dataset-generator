from abc import ABC
from numpy import array
from tensorflow import Tensor


class BaseImageOperation(ABC):
    """
    Base class for all image operations. Provides an interface for successor classes. 
    """
    
    _op = None

    def process(self, X: array or Tensor) -> Tensor:
        if not self._op:
            raise NotImplemented
        
        return self._op(X)

    def __call__(self, X: array or Tensor, *args, **kwargs) -> Tensor:
        if not self._op:
            raise NotImplemented
        
        return self._op(X)
