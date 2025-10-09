from ninja import ModelSchema

from .models import Inquiry


class InquiryPostSchema(ModelSchema):
    class Meta:
        model = Inquiry
        fields = ( 'full_name', 'email', 'phone_number', 'message')
