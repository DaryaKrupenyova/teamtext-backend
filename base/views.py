import logging.config

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny


logger = logging.getLogger(__name__)

