from django.urls import path, include
from rest_framework import routers

from base.views import DocumentViewSet, AddCollaboratorAPIView

router = routers.DefaultRouter()

router.register(r'documents', DocumentViewSet, basename="documents")

urlpatterns = [
    path('', include(router.urls)),
    path('documents/sharing', AddCollaboratorAPIView.as_view(), name="add_collaborator"),
]
