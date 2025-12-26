from django.urls import path
from . import views

urlpatterns = [
    path("booknow/", views.booknow, name="booknow"),
    path("booking_create/", views.booking_create, name="booking_create"),
    # path("booking/success/", views.booking_success, name="booking_success"),
    path('booking-details/', views.booking_details, name='booking_details'),
    path('booking/', views.booking, name='booking'),
    path("booking/payment/<int:booking_id>/", views.booking_payment, name="booking_payment"),
    path("payment/success/", views.payment_success),
    path("payment/cod/<int:booking_id>/", views.cod_payment, name="cod_payment"),
  # ← Add this
]
