from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Conversation,
    Message,
    Diagnosis,
    Media,
    Booking,
)

from .services.chatbot import generate_basic_response
from .services.diagnosis import diagnose
from .serializers import BookingSerializer


# =========================================================
# CHAT API
# POST /api/chat/
# =========================================================

@api_view(["POST"])
def chat(request):

    message = request.data.get("message")

    # -----------------------------------------------------
    # Validate message
    # -----------------------------------------------------

    if not message:
        return Response(
            {"error": "Message is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    message = message.strip()

    if not message:
        return Response(
            {"error": "Message cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # Get existing conversation or create a new one
    # -----------------------------------------------------

    conversation_id = request.data.get("conversation_id")

    if conversation_id:

        try:
            conversation = Conversation.objects.get(
                id=conversation_id
            )

        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    else:
        conversation = Conversation.objects.create()

    # -----------------------------------------------------
    # Save the current user message
    # -----------------------------------------------------

    user_message = Message.objects.create(
        conversation=conversation,
        sender="user",
        message=message,
    )

    # -----------------------------------------------------
    # Get previous user messages
    # -----------------------------------------------------

    conversation_history = list(
        conversation.messages
        .exclude(id=user_message.id)
        .values("sender", "message")
    )

    # -----------------------------------------------------
    # Generate chatbot response
    # -----------------------------------------------------

    result = generate_basic_response(
        message,
        conversation_history=conversation_history,
    )

    bot_response = result["response"]

    # -----------------------------------------------------
    # Add follow-up question if required
    # -----------------------------------------------------

    if result.get("needs_follow_up"):

        bot_response += (
            "\n\n"
            + result["follow_up_question"]
        )

    # -----------------------------------------------------
    # Save bot message
    # -----------------------------------------------------

    Message.objects.create(
        conversation=conversation,
        sender="bot",
        message=bot_response,
    )

    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return Response(
        {
            "conversation_id": conversation.id,
            "user_message": message,
            "response": bot_response,
            "is_car_related": result.get(
                "is_car_related",
                False,
            ),
            "needs_follow_up": result.get(
                "needs_follow_up",
                False,
            ),
        },
        status=status.HTTP_200_OK,
    )


# =========================================================
# DIAGNOSIS API
# POST /api/diagnosis/
# =========================================================

@api_view(["POST"])
def diagnosis(request):

    conversation_id = request.data.get(
        "conversation_id"
    )

    # -----------------------------------------------------
    # Validate conversation ID
    # -----------------------------------------------------

    if not conversation_id:
        return Response(
            {
                "error": "conversation_id is required."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # Get conversation
    # -----------------------------------------------------

    try:
        conversation = Conversation.objects.get(
            id=conversation_id
        )

    except Conversation.DoesNotExist:
        return Response(
            {
                "error": "Conversation not found."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -----------------------------------------------------
    # Get user messages
    # -----------------------------------------------------

    user_messages = list(
        conversation.messages
        .filter(sender="user")
        .values_list("message", flat=True)
    )

    if not user_messages:
        return Response(
            {
                "error": "No user messages found."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # Run diagnostic engine
    # -----------------------------------------------------

    result = diagnose(user_messages)

    # -----------------------------------------------------
    # Not enough information
    # -----------------------------------------------------

    if not result:
        return Response(
            {
                "diagnosis_available": False,
                "message": (
                    "There is not enough information to "
                    "provide a reliable diagnosis yet. "
                    "Please provide more details about "
                    "the symptoms."
                ),
            },
            status=status.HTTP_200_OK,
        )

    # -----------------------------------------------------
    # Create or update diagnosis
    # -----------------------------------------------------

    diagnosis_obj, created = (
        Diagnosis.objects.update_or_create(
            conversation=conversation,
            defaults={
                "problem": result["problem"],
                "explanation": result["explanation"],
                "severity": result["severity"],
                "recommendation": result["recommendation"],
            },
        )
    )

    # -----------------------------------------------------
    # Return diagnosis
    # -----------------------------------------------------

    return Response(
        {
            "diagnosis_available": True,
            "diagnosis_id": diagnosis_obj.id,
            "conversation_id": conversation.id,
            "problem": diagnosis_obj.problem,
            "explanation": diagnosis_obj.explanation,
            "severity": diagnosis_obj.severity,
            "recommendation": diagnosis_obj.recommendation,
        },
        status=status.HTTP_200_OK,
    )


# =========================================================
# MEDIA UPLOAD API
# POST /api/upload/
# =========================================================

@api_view(["POST"])
def upload_media(request):

    conversation_id = request.data.get(
        "conversation_id"
    )

    uploaded_file = request.FILES.get("file")

    media_type = request.data.get(
        "media_type"
    )

    # -----------------------------------------------------
    # Validate conversation ID
    # -----------------------------------------------------

    if not conversation_id:
        return Response(
            {
                "error": "conversation_id is required."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # Get conversation
    # -----------------------------------------------------

    try:
        conversation = Conversation.objects.get(
            id=conversation_id
        )

    except Conversation.DoesNotExist:
        return Response(
            {
                "error": "Conversation not found."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -----------------------------------------------------
    # Validate file
    # -----------------------------------------------------

    if not uploaded_file:
        return Response(
            {
                "error": "File is required."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # Validate media type
    # -----------------------------------------------------

    allowed_types = [
        "image",
        "audio",
        "video",
    ]

    if media_type not in allowed_types:
        return Response(
            {
                "error": (
                    "Invalid media_type. "
                    "Use image, audio or video."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # Save media
    # -----------------------------------------------------

    media = Media.objects.create(
        conversation=conversation,
        file=uploaded_file,
        media_type=media_type,
    )

    # -----------------------------------------------------
    # Return upload information
    # -----------------------------------------------------

    return Response(
        {
            "message": "Media uploaded successfully.",
            "media_id": media.id,
            "conversation_id": conversation.id,
            "media_type": media.media_type,
            "file_url": media.file.url,
        },
        status=status.HTTP_201_CREATED,
    )


# =========================================================
# CREATE BOOKING API
# POST /api/booking/
# =========================================================

@api_view(["POST"])
def create_booking(request):

    serializer = BookingSerializer(
        data=request.data
    )

    # -----------------------------------------------------
    # Validate booking data
    # -----------------------------------------------------

    if serializer.is_valid():

        booking = serializer.save()

        return Response(
            {
                "message": (
                    "Mechanic booking created "
                    "successfully."
                ),
                "booking_id": booking.id,
                "status": booking.status,
                "booking": BookingSerializer(
                    booking
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )

    # -----------------------------------------------------
    # Invalid booking
    # -----------------------------------------------------

    return Response(
        {
            "error": "Invalid booking data.",
            "details": serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


# =========================================================
# GET BOOKING API
# GET /api/booking/{id}/
# =========================================================

@api_view(["GET"])
def get_booking(request, booking_id):

    try:
        booking = Booking.objects.get(
            id=booking_id
        )

    except Booking.DoesNotExist:
        return Response(
            {
                "error": "Booking not found."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        {
            "booking": BookingSerializer(
                booking
            ).data,
        },
        status=status.HTTP_200_OK,
    )