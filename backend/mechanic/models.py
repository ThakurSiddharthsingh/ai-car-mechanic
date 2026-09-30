from django.db import models


class Conversation(models.Model):
    """
    Represents one complete conversation between
    a customer and the AI mechanic.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Stores individual messages exchanged
    between the customer and the mechanic bot.
    """

    SENDER_CHOICES = [
        ("user", "User"),
        ("bot", "Bot"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.CharField(
        max_length=10,
        choices=SENDER_CHOICES,
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}"


class Media(models.Model):
    """
    Stores images, audio and video uploaded
    by the customer during a conversation.
    """

    MEDIA_TYPES = [
        ("image", "Image"),
        ("audio", "Audio"),
        ("video", "Video"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="media",
    )

    file = models.FileField(
        upload_to="uploads/",
    )

    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} - {self.id}"


class Diagnosis(models.Model):
    """
    Stores the final diagnosis generated
    for a conversation.
    """

    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        related_name="diagnosis",
    )

    problem = models.CharField(
        max_length=255,
    )

    explanation = models.TextField()

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
    )

    recommendation = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.problem


class Booking(models.Model):
    """
    Stores mechanic booking requests
    created after a diagnosis.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer_name = models.CharField(
        max_length=150,
    )

    phone = models.CharField(
        max_length=20,
    )

    vehicle = models.CharField(
        max_length=150,
    )

    service = models.CharField(
        max_length=255,
    )

    preferred_date = models.DateField()

    preferred_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.customer_name} - "
            f"{self.vehicle} - "
            f"{self.service}"
        )