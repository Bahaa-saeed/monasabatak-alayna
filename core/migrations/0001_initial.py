# Generated initial migration for the project models.
import uuid
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Venue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160, verbose_name="اسم المكان")),
                ("venue_type", models.CharField(choices=[("hall", "قاعة مناسبات"), ("restaurant", "مطعم"), ("cafe", "كافيه"), ("chalet", "شاليه"), ("training", "قاعة تدريب"), ("other", "مكان آخر")], default="hall", max_length=20, verbose_name="نوع المكان")),
                ("city", models.CharField(max_length=100, verbose_name="المدينة")),
                ("area", models.CharField(blank=True, max_length=120, verbose_name="المنطقة / الحي")),
                ("address", models.CharField(blank=True, max_length=250, verbose_name="العنوان")),
                ("capacity", models.PositiveIntegerField(default=20, verbose_name="السعة القصوى")),
                ("price_from", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="السعر يبدأ من (شيكل)")),
                ("description", models.TextField(blank=True, verbose_name="وصف المكان")),
                ("facilities", models.TextField(blank=True, help_text="افصل بين المرافق بفواصل.", verbose_name="المرافق والخدمات")),
                ("phone", models.CharField(blank=True, max_length=40, verbose_name="هاتف التواصل")),
                ("image", models.ImageField(blank=True, null=True, upload_to="venues/", verbose_name="صورة المكان")),
                ("is_active", models.BooleanField(default=True, verbose_name="ظاهر على الموقع")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")),
            ],
            options={"verbose_name": "مكان", "verbose_name_plural": "الأماكن", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Vendor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160, verbose_name="اسم المورد")),
                ("category", models.CharField(max_length=100, verbose_name="التخصص")),
                ("city", models.CharField(max_length=100, verbose_name="المدينة")),
                ("phone", models.CharField(blank=True, max_length=40, verbose_name="رقم الهاتف")),
                ("description", models.TextField(blank=True, verbose_name="ملاحظات")),
                ("is_active", models.BooleanField(default=True, verbose_name="نشط")),
            ],
            options={"verbose_name": "مورد", "verbose_name_plural": "الموردون"},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=140, verbose_name="اسم الخدمة")),
                ("description", models.TextField(blank=True, verbose_name="الوصف")),
                ("starting_price", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="السعر يبدأ من (شيكل)")),
                ("is_active", models.BooleanField(default=True, verbose_name="متاحة")),
                ("vendor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.vendor", verbose_name="المورد")),
            ],
            options={"verbose_name": "خدمة إضافية", "verbose_name_plural": "الخدمات الإضافية"},
        ),
        migrations.CreateModel(
            name="EventRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference", models.CharField(editable=False, max_length=14, unique=True, verbose_name="الرقم المرجعي")),
                ("customer_name", models.CharField(max_length=120, verbose_name="اسم العميل")),
                ("phone", models.CharField(max_length=40, verbose_name="رقم الهاتف")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="البريد الإلكتروني")),
                ("event_type", models.CharField(choices=[("birthday", "عيد ميلاد"), ("engagement", "خطوبة / زفاف"), ("graduation", "تخرج"), ("newborn", "استقبال مولود"), ("corporate", "فعالية شركة"), ("medical", "يوم طبي"), ("training", "دورة / ورشة تدريبية"), ("other", "مناسبة أخرى")], max_length=20, verbose_name="نوع المناسبة")),
                ("city", models.CharField(max_length=100, verbose_name="المدينة")),
                ("area", models.CharField(blank=True, max_length=120, verbose_name="المنطقة")),
                ("event_date", models.DateField(verbose_name="تاريخ المناسبة")),
                ("guest_count", models.PositiveIntegerField(verbose_name="عدد الأشخاص")),
                ("budget", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="الميزانية (شيكل)")),
                ("notes", models.TextField(blank=True, verbose_name="تفاصيل إضافية")),
                ("status", models.CharField(choices=[("new", "طلب جديد"), ("reviewing", "قيد المراجعة"), ("offers_sent", "تم إرسال العروض"), ("confirmed", "تم التأكيد"), ("in_progress", "جارٍ التنسيق"), ("completed", "مكتمل"), ("cancelled", "ملغي")], default="new", max_length=20, verbose_name="حالة الطلب")),
                ("internal_notes", models.TextField(blank=True, verbose_name="ملاحظات داخلية")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="تاريخ الطلب")),
                ("requested_services", models.ManyToManyField(blank=True, to="core.service", verbose_name="الخدمات المطلوبة")),
            ],
            options={"verbose_name": "طلب تنسيق", "verbose_name_plural": "طلبات التنسيق", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160, verbose_name="عنوان العرض")),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="السعر الإجمالي (شيكل)")),
                ("included_services", models.TextField(blank=True, verbose_name="الخدمات المشمولة")),
                ("excluded_services", models.TextField(blank=True, verbose_name="الخدمات غير المشمولة")),
                ("proposed_date", models.DateField(blank=True, null=True, verbose_name="التاريخ المقترح")),
                ("expires_at", models.DateField(blank=True, null=True, verbose_name="صالح حتى")),
                ("is_selected", models.BooleanField(default=False, verbose_name="اختاره العميل")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")),
                ("request", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="offers", to="core.eventrequest", verbose_name="طلب التنسيق")),
                ("venue", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.venue", verbose_name="المكان")),
            ],
            options={"verbose_name": "عرض سعر", "verbose_name_plural": "عروض الأسعار"},
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("pending", "بانتظار التأكيد"), ("confirmed", "مؤكد"), ("preparing", "قيد التجهيز"), ("ready", "جاهز"), ("completed", "مكتمل"), ("cancelled", "ملغي")], default="pending", max_length=20, verbose_name="حالة الحجز")),
                ("deposit_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="العربون (شيكل)")),
                ("paid_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="المبلغ المدفوع (شيكل)")),
                ("coordination_fee", models.DecimalField(decimal_places=2, default=200, max_digits=10, verbose_name="رسوم التنسيق (شيكل)")),
                ("commission_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="العمولة (شيكل)")),
                ("notes", models.TextField(blank=True, verbose_name="ملاحظات")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الحجز")),
                ("offer", models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name="booking", to="core.offer", verbose_name="العرض")),
            ],
            options={"verbose_name": "حجز", "verbose_name_plural": "الحجوزات"},
        ),
    ]
