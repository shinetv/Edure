from django.urls import path
from invoice import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.login),
    path('detail/',views.detail),
    path('details/',views.details),
    path('update/<int:id>/',views.update),
    path('DownloadCV/',views.DownloadCV),
    path('downloadCSV/',views.downloadCSV),
    path('logout/',views.logout),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
