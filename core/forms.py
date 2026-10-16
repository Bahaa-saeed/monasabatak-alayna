from django import forms
from django.utils import timezone
from .models import EventRequest, Service

class EventRequestForm(forms.ModelForm):
    requested_services = forms.ModelMultipleChoiceField(
        label="الخدمات الإضافية المطلوبة",
        queryset=Service.objects.filter(is_active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = EventRequest
        fields = [
            "customer_name", "phone", "email", "event_type", "city", "area",
            "event_date", "guest_count", "budget", "requested_services", "notes"
        ]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date", "min": timezone.localdate().isoformat()}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "احكِ لنا عن الثيم أو احتياجاتك الخاصة..."}),
            "budget": forms.NumberInput(attrs={"min": "0", "step": "1"}),
            "guest_count": forms.NumberInput(attrs={"min": "1"}),
        }

    def clean_event_date(self):
        date = self.cleaned_data["event_date"]
        if date < timezone.localdate():
            raise forms.ValidationError("يرجى اختيار تاريخ اليوم أو تاريخ لاحق.")
        return date

    def clean_guest_count(self):
        count = self.cleaned_data["guest_count"]
        if count < 1:
            raise forms.ValidationError("عدد الأشخاص يجب أن يكون شخصًا واحدًا على الأقل.")
        return count
