from django.urls import path
from . import views
from .views import moodboard_list, create_moodboard, update_moodboard, delete_moodboard, creators_list, categories_list,about, register_user, login_user, logout_user, dashboard, creator_dashboard, buyer_dashboard,CustomPasswordResetView, profile, hire_designer, buy_moodboard, moodboard_details, creator_profile, contact, download_moodboard, respond_to_hire_request

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('moodboards/<int:category_id>/',moodboard_list,name="moodboard_list"),
    path('moodboards/create/',create_moodboard,name="create_moodboard"),
    path('moodboards/update/<int:id>/',update_moodboard,name='update_moodboard'),
    path('moodboards/delete/<int:id>/',delete_moodboard,name='delete_moodboard'),
    path('moodboards/creators/',creators_list,name='creators'),
    path('moodboards/categories/',categories_list,name='categories'),
    path('moodboards/about/',about,name='about'),
    path('moodboards/contact/',contact,name='contact'),
    path('moodboards/register/', register_user, name="register"),
    path('moodboards/login/', login_user, name="login"),
    path('moodboards/logout/', logout_user, name="logout"),
    path('moodboards/dashboard/', dashboard, name="dashboard"),
    path('moodboards/dashboard/creator/', creator_dashboard, name="creator_dashboard"),
    path('moodboards/dashboard/buyer/', buyer_dashboard, name="buyer_dashboard"),
	path('password-reset/', CustomPasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
	path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name="password_reset_done"),
	path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),name="password_reset_confirm"),
	path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name="password_reset_complete"),
    path('profile/', profile, name='profile'),
    path('hire/<int:designer_id>/', hire_designer, name='hire_designer'),

    path('buy/<int:moodboard_id>/', buy_moodboard, name='buy_moodboard'),
    path('details/<int:category_id>/<int:moodboard_id>/', moodboard_details, name='moodboard_details'),
    path('moodboards/<int:moodboard_id>/review/', views.submit_review, name='submit_review'),
    path('moodboards/creator/<int:creator_id>/', creator_profile, name='creator_profile'),
    path('moodboards/download/<int:moodboard_id>/', download_moodboard, name='download_moodboard'),
    path('hire-request/<int:request_id>/<str:action>/', respond_to_hire_request, name='respond_to_hire_request'),


]


