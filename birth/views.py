from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EventBooking, Addon, BookingAddon, TimeSlot
from django.shortcuts import render, get_object_or_404
from .models import EventBooking

import razorpay
from django.conf import settings


def booknow(request):
    package_id = request.GET.get("package")

    base_price = 0
    if package_id == "1":
        base_price = 899
    elif package_id == "2":
        base_price = 1499
    elif package_id == "3":
        base_price = 1699

    addons = Addon.objects.all()
    timeslots = TimeSlot.objects.all()

    return render(request, "booknow.html", {
        "addons": addons,
        "timeslots": timeslots,
        "base_price": base_price
    })
def booking_create(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        noofppl = request.POST.get("noofppl")
        decoration = request.POST.get("drequirement")
        timing = request.POST.get("timings")
        event_date = request.POST.get("event_date")
        base_price = int(request.POST.get("base_price", 0))  # ✅ IMPORTANT

        if not timing:
            messages.error(request, "Please select a timing.")
            return redirect("booknow")

        booking = EventBooking.objects.create(
            fname=fname,
            email=email,
            phone=phone,
            no_of_people=noofppl,
            decoration=decoration,
            timing=timing,
            event_date=event_date,
            base_price=base_price,   # ✅ SAVED
        )

        selected_addons = request.POST.getlist("addons")

        for addon_id in selected_addons:
            addon = Addon.objects.get(id=addon_id)
            BookingAddon.objects.create(
                booking=booking,
                addon=addon,
                quantity=1
            )

        return redirect("booking_payment", booking_id=booking.id)

    return redirect("booknow")


def booking_success(request):
    return render(request, "booking_success.html")


def booking_details(request):
    bookings = EventBooking.objects.prefetch_related("addons__addon").order_by("-created_at")
    return render(request, "bookdetails.html", {"bookings": bookings})


def booking(request):
    packages = [
        {
            "id": 1,
            "title": "Couple Show",
            "price": 899,
            "image": "media/images/celebration-2.jpg",
            "desc": "Celebrate birthdays with joy, love, gifts, and unforgettable memories!"
        },
        {
            "id": 2,
            "title": "Celebration Show",
            "price": 1499,
            "image": "media/images/couple-2.jpg",
            "desc": "Celebrate love, togetherness, and beautiful milestones of life."
        },
        {
            "id": 3,
            "title": "Family Show",
            "price": 1699,
            "image": "media/images/family-4.jpg",
            "desc": "Make your special day unforgettable with fun, friends, and celebration!"
        }
    ]

    return render(request, "booking.html", {"packages": packages})


def booking_payment(request, booking_id):
    booking = get_object_or_404(EventBooking, id=booking_id)
    addons = BookingAddon.objects.filter(booking=booking)

    addons_total = sum(a.addon.price for a in addons)
    total_amount = booking.base_price + addons_total

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": int(total_amount * 100),  # paise
        "currency": "INR",
        "payment_capture": 1
    })

    booking.razorpay_order_id = order["id"]
    booking.save()

    return render(request, "booking_payment.html", {
        "booking": booking,
        "addons": addons,
        "base_amount": booking.base_price,
        "addons_total": addons_total,
        "total_amount": total_amount,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": order["id"],
        "razorpay_amount": int(total_amount * 100)
    })


def payment_success(request):
    payment_id = request.GET.get("payment_id")
    order_id = request.GET.get("order_id")
    signature = request.GET.get("signature")

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    try:
        # Verify signature
        client.utility.verify_payment_signature({
            "razorpay_payment_id": payment_id,
            "razorpay_order_id": order_id,
            "razorpay_signature": signature
        })

        # ✅ FETCH BOOKING USING ORDER ID
        booking = EventBooking.objects.get(razorpay_order_id=order_id)

        # Update booking
        booking.payment_status = "PAID"
        booking.payment_method = "RAZORPAY"
        booking.razorpay_payment_id = payment_id
        booking.save()

        # ✅ PASS BOOKING TO TEMPLATE
        return render(request, "payment_success.html", {
            "booking": booking
        })

    except Exception as e:
        print("Payment verification failed:", e)
        return render(request, "payment_failed.html")

def payment_page(request, booking_id):
    booking = get_object_or_404(EventBooking, id=booking_id)
    addons = BookingAddon.objects.filter(booking=booking)

    total_amount = booking.base_price if hasattr(booking, "base_price") else 0
    for ad in addons:
        total_amount += ad.addon.price * ad.quantity

    return render(request, "payment_page.html", {
        "booking": booking,
        "addons": addons,
        "total_amount": total_amount,
    })



def payment_success(request):
    return render(request, "payment_success.html")

def payment_summary(request, booking_id):
    booking = get_object_or_404(EventBooking, id=booking_id)

    addons = BookingAddon.objects.filter(booking=booking)

    total = booking.base_price if hasattr(booking, "base_price") else 0
    for item in addons:
        total += item.addon.price

    return render(request, "payment_summary.html", {
        "booking": booking,
        "addons": addons,
        "total_amount": total,
    })

def cod_payment(request, booking_id):
    booking = get_object_or_404(EventBooking, id=booking_id)

    # update payment status
    booking.payment_status = "COD"
    booking.save()

    return render(request, "cod_success.html", {"booking": booking})