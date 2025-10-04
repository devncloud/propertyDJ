from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Builder
from .schemas import BuilderSchema
router = Router(tags=['Builders'])


@router.get('/builder/{slug}', response=BuilderSchema)
def builder_details(request, slug:str):
    builder = get_object_or_404(Builder, slug=slug)
    return builder
