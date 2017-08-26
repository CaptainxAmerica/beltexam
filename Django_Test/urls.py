from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('apps.logreg.urls'))
    url(r'^', include('apps.review.urls'))
]
