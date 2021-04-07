from django.urls import path

from .views import profile, my_profile, profile_delete, profile_confirm_delete, profile_update, FeedbackListView, \
    FeedbackCreateView, DeleteFeedbackView, UpdateFeedbackView, inbox

urlpatterns = [
    path('myProfile', my_profile, name='profile'),
    path('inbox', inbox, name='inbox'),
    path('<int:pk>/', profile, name='profile-detail'),
    path('confirm_delete', profile_confirm_delete, name='profile-confirm-delete'),
    path('delete', profile_delete, name='profile-delete'),
    path('update', profile_update, name='profile-update'),
    path('<int:pk>/feedback/', FeedbackListView.as_view(), name='feedback'),
    path('<int:pk>/feedback/create_feedback/', FeedbackCreateView.as_view(), name='create-feedback'),
    path('feedback/delete_feedback/<int:pk>/', DeleteFeedbackView.as_view(), name='delete-feedback'),
    path('feedback/edit/<int:pk>/', UpdateFeedbackView.as_view(), name='update-feedback'),
]
