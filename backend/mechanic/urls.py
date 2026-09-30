from django.urls import path

from .views import (
    chat,
    diagnosis,
    upload_media,
    create_booking,
    get_booking,
)


urlpatterns = [
    path("chat/", chat, name="chat"),
    path("diagnosis/", diagnosis, name="diagnosis"),
    path("upload/", upload_media, name="upload-media"),
    path("booking/", create_booking, name="create-booking"),
    path("booking/<int:booking_id>/", get_booking, name="get-booking"),
]