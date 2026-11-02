from django.contrib import admin
from .models import DiagnosisResult


@admin.register(DiagnosisResult)
class DiagnosisResultAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'risk_score',
        'risk_level',
        'scanned_at',
    )

    list_filter = ('risk_level',)

    search_fields = (
        'user__username',
        'summary',
    )