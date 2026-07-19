from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from blog.views import EditProfileView, RegistrationView

urlpatterns = [
    path("pages/", include("pages.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "auth/registration/", RegistrationView.as_view(), name="registration"
    ),
    path("profile/edit/", EditProfileView.as_view(), name="edit_profile"),
    path("", include("blog.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.error500"
