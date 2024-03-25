from django.urls import path
from .views import customerDetail,makeReview,delete_booking,searchLawyer,update_mission,update_booking,lawyerData,lawyerDetail,insertLawyer,Reviews,insertCustomer,makeBooking,seeBooking,seeMissions

urlpatterns = [
    path('import-lawyers/',lawyerData),
    path('search-lawyers',searchLawyer),
    path('lawyer-detail/<int:id>/', lawyerDetail),
    path('customer-detail/<int:id>/', customerDetail),
    path('insert-lawyers/',insertLawyer),
    path('insert-customers/',insertCustomer),
    path('make-booking/',makeBooking),
    path('make-review/',makeReview),
    path('see-bookings/<int:id>/', seeBooking),
    path('see-missions/<int:id>/', seeMissions),
    path('reviews/<int:id>/',Reviews),
    path('update-booking/<int:booking_id>/', update_booking, name='update-booking'),
    path('update-mission/<int:mission_id>/', update_mission, name='update-booking'),
    path('delete-booking/<int:bookingId>/', delete_booking, name='delete-booking'),

]
