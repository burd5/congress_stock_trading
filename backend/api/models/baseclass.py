class BaseClass():
    __table__ = None
    attributes = None

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.attributes:
                raise KeyError(f'{key} not in {self.attributes}')
            for k,v in kwargs.items():
                setattr(self, k, v)
    