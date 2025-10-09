from pyexpat import features

from ninja import Schema, FilterSchema, Field, ModelSchema
from typing import Optional, List

from .models import Property, City, FloorPlan, PropertyImage, Amenity, Feature
from builders.schemas import BuilderSchema


class FilteredSchema(FilterSchema):
    search: Optional[str] = Field(None, q='title__icontains')
    property_type: Optional[str] = Field(None, q='property_type__iexact')
    status: Optional[str] = Field(None, q='status__iexact')
    # city:Optional[str] = Field(None, q='city__iexact')

    class Config:
        from_attributes = True

class CitySchema(ModelSchema):
    class Meta:
        model = City
        fields = ['name']

class AmenitySchema(ModelSchema):
    class Meta:
        model = Amenity
        fields = ['id', 'name']


class FeatureSchema(ModelSchema):
    class Meta:
        model = Feature
        fields = ['id', 'name']


class FloorPlanSchema(ModelSchema):
    class Meta:
        model = FloorPlan
        fields = ['id', 'floor_plan_file', 'description']


class PropertyImageSchema(ModelSchema):
    class Meta:
        model = PropertyImage
        fields = [ 'id', 'image', 'is_primary']


class PropertyDetailedSchema(Schema):
    id: int
    title: str
    property_type: str
    # price: str
    location: Optional[str]
    address: str
    # city: CitySchema
    city: CitySchema
    features: List[FeatureSchema] = []
    amenities: List[AmenitySchema] = []
    floor_plans: List[FloorPlanSchema] = []
    property_images: List[PropertyImageSchema] = []
    builder: Optional[BuilderSchema] = None

    class Config:
        from_attributes = True


class GetAllSchema(Schema):
    property_type: str
    slug: str
    title: str
    description: str
    price: float
    address: str
    city_id: int
    status: str
    amenities: List[AmenitySchema] = []
    primary_image: List[PropertyImageSchema] = []

    class Config:
        from_attributes = True