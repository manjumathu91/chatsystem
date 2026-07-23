
from django.contrib import admin
from .models import StaffProfile, Ticket, Message


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "department",
        "created_at",
    )

    list_filter = (
        "department",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = (
        "user__username",
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "user",
        "priority",
        "status",
        "assigned_to",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "assigned_to",
        "created_at",
    )

    search_fields = (
        "subject",
        "description",
        "user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ticket",
        "user",
        "short_message",
        "created_at",
    )

    search_fields = (
        "ticket__subject",
        "user__username",
        "content",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "created_at",
    )

    list_per_page = 30

    def short_message(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + "..."
        return obj.content

    short_message.short_description = "Message"