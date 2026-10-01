from django.contrib import admin

from .models import (
    Conversation,
    Message,
    Media,
    Diagnosis,
    Booking,
)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "sender",
        "created_at",
    )

    list_filter = (
        "sender",
    )

    search_fields = (
        "message",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "media_type",
        "created_at",
    )

    list_filter = (
        "media_type",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "problem",
        "severity",
        "created_at",
    )

    list_filter = (
        "severity",
    )

    search_fields = (
        "problem",
        "explanation",
        "recommendation",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "phone",
        "vehicle",
        "service",
        "preferred_date",
        "preferred_time",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "preferred_date",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "phone",
        "vehicle",
        "service",
    )

    ordering = (
        "-created_at",
    )