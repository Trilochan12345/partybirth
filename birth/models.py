from django.db import models


# -----------------------------
# Addon Model
# -----------------------------
class Addon(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='addons/', blank=True, null=True)

    def __str__(self):
        return self.name


# -----------------------------
# Time Slot Model
# -----------------------------
class TimeSlot(models.Model):
    start_time = models.TimeField(default="09:00")
    end_time = models.TimeField(default="10:00")

    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


# -----------------------------
# Event Booking Model
# -----------------------------
class EventBooking(models.Model):
    fname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    no_of_people = models.IntegerField()
    decoration = models.CharField(max_length=100, blank=True, null=True)
    timing = models.CharField(max_length=50)
    event_date = models.DateField()

    # ✅ ADD THIS
    base_price = models.IntegerField(default=0)

    payment_status = models.CharField(max_length=20, default="PENDING")
    payment_method = models.CharField(max_length=20, blank=True, null=True)

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fname
# -----------------------------
# Booking Addon Model
# -----------------------------
class BookingAddon(models.Model):
    booking = models.ForeignKey(
        EventBooking, on_delete=models.CASCADE, related_name='addons'
    )
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.addon.name} x {self.quantity}"
