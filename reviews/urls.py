from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls.static import static

# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

from . import views

urlpatterns = [
    path("", views.review),
    path("compare/", views.compare),
]
urlpatterns += staticfiles_urlpatterns()
# for conversion of normal func to class based view
# path("yhank-you", views.ThankYouView.as_view())