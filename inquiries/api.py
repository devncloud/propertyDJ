from ninja import Router
from .models import Inquiry

from .schemas import InquiryPostSchema

router = Router(tags=["Inquiry"])



@router.post("/inquiry/submit/")
def submit_inquiry(request, payload: InquiryPostSchema):
    inquiry = Inquiry.objects.create(
        full_name = payload.full_name,
        email = payload.email,
        phone_number = payload.phone_number,
        subject = payload.subject,
        message = payload.message
    )
    return inquiry