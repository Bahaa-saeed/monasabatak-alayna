import uuid
from django.db import models
from django.utils import timezone

class Venue(models.Model):
    TYPES = [
        ("hall", "قاعة مناسبات"),
        ("restaurant", "مطعم"),
        ("cafe", "كافيه"),
        ("chalet", "شاليه"),
        ("training", "قاعة تدريب"),
        ("other", "مكان آخر"),
    ]
    name = models.CharField("اسم المكان", max_length=160)
    venue_type = models.CharField("نوع المكان", max_length=20, choices=TYPES, default="hall")
    city = models.CharField("المدينة", max_length=100)
    area = models.CharField("المنطقة / الحي", max_length=120, blank=True)
    address = models.CharField("العنوان", max_length=250, blank=True)
    capacity = models.PositiveIntegerField("السعة القصوى", default=20)
    price_from = models.DecimalField("السعر يبدأ من (شيكل)", max_digits=10, decimal_places=2, default=0)
    description = models.TextField("وصف المكان", blank=True)
    facilities = models.TextField("المرافق والخدمات", blank=True, help_text="افصل بين المرافق بفواصل.")
    phone = models.CharField("هاتف التواصل", max_length=40, blank=True)
    image = models.ImageField("صورة المكان", upload_to="venues/", blank=True, null=True)
    is_active = models.BooleanField("ظاهر على الموقع", default=True)
    created_at = models.DateTimeField("تاريخ الإضافة", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "مكان"
        verbose_name_plural = "الأماكن"

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField("اسم المورد", max_length=160)
    category = models.CharField("التخصص", max_length=100)
    city = models.CharField("المدينة", max_length=100)
    phone = models.CharField("رقم الهاتف", max_length=40, blank=True)
    description = models.TextField("ملاحظات", blank=True)
    is_active = models.BooleanField("نشط", default=True)

    class Meta:
        verbose_name = "مورد"
        verbose_name_plural = "الموردون"

    def __str__(self):
        return f"{self.name} — {self.category}"

class Service(models.Model):
    name = models.CharField("اسم الخدمة", max_length=140)
    description = models.TextField("الوصف", blank=True)
    starting_price = models.DecimalField("السعر يبدأ من (شيكل)", max_digits=10, decimal_places=2, default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المورد")
    is_active = models.BooleanField("متاحة", default=True)

    class Meta:
        verbose_name = "خدمة إضافية"
        verbose_name_plural = "الخدمات الإضافية"

    def __str__(self):
        return self.name

class EventRequest(models.Model):
    EVENT_TYPES = [
        ("birthday", "عيد ميلاد"),
        ("engagement", "خطوبة / زفاف"),
        ("graduation", "تخرج"),
        ("newborn", "استقبال مولود"),
        ("corporate", "فعالية شركة"),
        ("medical", "يوم طبي"),
        ("training", "دورة / ورشة تدريبية"),
        ("other", "مناسبة أخرى"),
    ]
    STATUSES = [
        ("new", "طلب جديد"),
        ("reviewing", "قيد المراجعة"),
        ("offers_sent", "تم إرسال العروض"),
        ("confirmed", "تم التأكيد"),
        ("in_progress", "جارٍ التنسيق"),
        ("completed", "مكتمل"),
        ("cancelled", "ملغي"),
    ]
    reference = models.CharField("الرقم المرجعي", max_length=14, unique=True, editable=False)
    customer_name = models.CharField("اسم العميل", max_length=120)
    phone = models.CharField("رقم الهاتف", max_length=40)
    email = models.EmailField("البريد الإلكتروني", blank=True)
    event_type = models.CharField("نوع المناسبة", max_length=20, choices=EVENT_TYPES)
    city = models.CharField("المدينة", max_length=100)
    area = models.CharField("المنطقة", max_length=120, blank=True)
    event_date = models.DateField("تاريخ المناسبة")
    guest_count = models.PositiveIntegerField("عدد الأشخاص")
    budget = models.DecimalField("الميزانية (شيكل)", max_digits=10, decimal_places=2)
    notes = models.TextField("تفاصيل إضافية", blank=True)
    requested_services = models.ManyToManyField(Service, blank=True, verbose_name="الخدمات المطلوبة")
    status = models.CharField("حالة الطلب", max_length=20, choices=STATUSES, default="new")
    internal_notes = models.TextField("ملاحظات داخلية", blank=True)
    created_at = models.DateTimeField("تاريخ الطلب", default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "طلب تنسيق"
        verbose_name_plural = "طلبات التنسيق"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = "MA-" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} — {self.customer_name}"

class Offer(models.Model):
    request = models.ForeignKey(EventRequest, on_delete=models.CASCADE, related_name="offers", verbose_name="طلب التنسيق")
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المكان")
    title = models.CharField("عنوان العرض", max_length=160)
    total_price = models.DecimalField("السعر الإجمالي (شيكل)", max_digits=10, decimal_places=2)
    included_services = models.TextField("الخدمات المشمولة", blank=True)
    excluded_services = models.TextField("الخدمات غير المشمولة", blank=True)
    proposed_date = models.DateField("التاريخ المقترح", null=True, blank=True)
    expires_at = models.DateField("صالح حتى", null=True, blank=True)
    is_selected = models.BooleanField("اختاره العميل", default=False)
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)

    class Meta:
        verbose_name = "عرض سعر"
        verbose_name_plural = "عروض الأسعار"

    def __str__(self):
        return f"{self.title} ({self.request.reference})"

class Booking(models.Model):
    STATUSES = [
        ("pending", "بانتظار التأكيد"),
        ("confirmed", "مؤكد"),
        ("preparing", "قيد التجهيز"),
        ("ready", "جاهز"),
        ("completed", "مكتمل"),
        ("cancelled", "ملغي"),
    ]
    offer = models.OneToOneField(Offer, on_delete=models.PROTECT, related_name="booking", verbose_name="العرض")
    status = models.CharField("حالة الحجز", max_length=20, choices=STATUSES, default="pending")
    deposit_amount = models.DecimalField("العربون (شيكل)", max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField("المبلغ المدفوع (شيكل)", max_digits=10, decimal_places=2, default=0)
    coordination_fee = models.DecimalField("رسوم التنسيق (شيكل)", max_digits=10, decimal_places=2, default=200)
    commission_amount = models.DecimalField("العمولة (شيكل)", max_digits=10, decimal_places=2, default=0)
    notes = models.TextField("ملاحظات", blank=True)
    created_at = models.DateTimeField("تاريخ الحجز", auto_now_add=True)

    class Meta:
        verbose_name = "حجز"
        verbose_name_plural = "الحجوزات"

    def __str__(self):
        return f"حجز {self.offer.request.reference}"

    @property
    def remaining_amount(self):
        return max(self.offer.total_price + self.coordination_fee - self.paid_amount, 0)
