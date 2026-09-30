from rest_framework import serializers

from .models import (
    Conversation,
    Message,
    Media,
    Diagnosis,
    Booking,
)


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender",
            "message",
            "created_at",
        ]


class ConversationSerializer(serializers.ModelSerializer):

    messages = MessageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Conversation
        fields = [
            "id",
            "created_at",
            "updated_at",
            "messages",
        ]


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = [
            "id",
            "conversation",
            "file",
            "media_type",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class DiagnosisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diagnosis
        fields = [
            "id",
            "conversation",
            "problem",
            "explanation",
            "severity",
            "recommendation",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            "id",
            "customer_name",
            "phone",
            "vehicle",
            "service",
            "preferred_date",
            "preferred_time",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]