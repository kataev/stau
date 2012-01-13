import base64
import numpy as np
from django.db import models


class Base64Field(models.TextField):
    def __init__(self, *args, **kwargs):
        self.dtype = 'int64'
        super(Base64Field, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        if self.db_column is None:
            self.db_column = name
        self.field_name = name + '_base64'
        super(Base64Field, self).contribute_to_class(cls, self.field_name)
        setattr(cls, name, property(self.get_data, self.set_data))

    def get_data(self, obj):
        buffer = base64.decodestring(getattr(obj, self.field_name))
        return np.frombuffer(buffer,self.dtype).tolist()

    def set_data(self, obj, data):
        data = np.array(data)
        self.dtype = str(getattr(obj,self.db_column+'_dtype','int64'))
        setattr(obj, self.field_name, base64.encodestring(data))