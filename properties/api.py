from ninja import Router
from django.db.models import Prefetch
from ninja.responses import JsonResponse
from typing import List
from django.shortcuts import get_object_or_404, get_list_or_404

from ninja.params.models import Query

from properties.models import Property, PropertyImage
from .schemas import GetAllSchema, FilteredSchema, PropertyDetailedSchema

router = Router(tags=["Property"])


@router.get("/properties/", response=List[GetAllSchema])
def get_all(request):
    properties = get_list_or_404(
        Property.objects.prefetch_related(
            Prefetch(
                "property_images",
                queryset=PropertyImage.objects.filter(is_primary=True),
                to_attr="primary_image"
            )
        ))
    return properties


@router.get('/properties/featured/', response=List[GetAllSchema])
def get_featured(request):
    properties = get_list_or_404(
        Property.objects.prefetch_related(
            Prefetch(
                "property_images",
                queryset=PropertyImage.objects.filter(is_primary=True),
                to_attr="primary_image"
            )
    ), is_featured=True)
    return properties


@router.get("/properties/results/", response=List[GetAllSchema])
def filtered_data(request, filters: FilteredSchema = Query(...), ):
    properties = Property.objects.all()
    properties = filters.filter(properties)
    return properties

@router.get('properties/{slug}/', response=PropertyDetailedSchema)
def property_detail(request, slug: str):
    property_instance = get_object_or_404(
        Property.objects.prefetch_related(
            'floor_plans',
            'property_images',
            'features',
            'amenities',
        ).select_related('builder', 'city'),
        slug=slug
    )
    return property_instance
