from django.urls import path

from .views import profile, my_profile, profile_delete, profile_confirm_delete, profile_update, FeedbackListView
#add_feedback

urlpatterns = [
    path('myProfile', my_profile, name='profile'),
    path('<int:pk>/', profile, name='profile-detail'),
    path('confirm_delete', profile_confirm_delete, name='profile-confirm-delete'),
    path('delete', profile_delete, name='profile-delete'),
    path('update', profile_update, name='profile-update'),
    #path('<int:pk>/feedback/', add_feedback, name='feedback')
    path('<int:pk>/feedback/', FeedbackListView.as_view(), name='feedback')
]
