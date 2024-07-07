from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('files/', include('sender_file.urls')),
]