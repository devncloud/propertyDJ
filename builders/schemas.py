from ninja import Schema, ModelSchema
from typing import List, Optional
from .models import Builder




class BuilderSchema(ModelSchema):
    class Meta:
        model = Builder
        fields = ['id', 'name', 'description', 'website', 'logo']