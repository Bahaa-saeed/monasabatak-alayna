from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Venue, Service, EventRequest
from .forms import EventRequestForm

def home(request):
    venues = Venue.objects.filter(is_active=True)[:6]
    services = Service.objects.filter(is_active=True)[:6]
    return render(request, "core/home.html", {"venues": venues, "services": services})

def venue_list(request):
    venues = Venue.objects.filter(is_active=True)
    q = request.GET.get("q", "").strip()
    city = request.GET.get("city", "").strip()
    venue_type = request.GET.get("type", "").strip()
    guests = request.GET.get("guests", "").strip()
    if q:
        venues = venues.filter(Q(name__icontains=q) | Q(area__icontains=q) | Q(city__icontains=q))
    if city:
        venues = venues.filter(city__icontains=city)
    if venue_type:
        venues = venues.filter(venue_type=venue_type)
    if guests.isdigit():
        venues = venues.filter(capacity__gte=int(guests))
    return render(request, "core/venue_list.html", {
        "venues": venues, "q": q, "city": city, "selected_type": venue_type,
        "guests": guests, "venue_types": Venue.TYPES
    })

def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk, is_active=True)
    return render(request, "core/venue_detail.html", {"venue": venue})

def request_create(request):
    if request.method == "POST":
        form = EventRequestForm(request.POST)
        if form.is_valid():
            event_request = form.save()
            messages.success(request, "تم استلام طلبك بنجاح. سنراجع التفاصيل ونتواصل معك.")
            return redirect("request_success", reference=event_request.reference)
    else:
        form = EventRequestForm()
    return render(request, "core/request_form.html", {"form": form})

def request_success(request, reference):
    event_request = get_object_or_404(EventRequest, reference=reference)
    return render(request, "core/request_success.html", {"event_request": event_request})
