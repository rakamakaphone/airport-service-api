from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from airport_service.models import (
    Airport,
    Crew,
    Route,
    AirplaneType,
    Airplane,
    Flight, Order, Ticket,
)
from airport_service.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport_service.serializers import (
    AirportSerializer,
    CrewSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    FlightSerializer, RouteListSerializer, AirplaneListSerializer, FlightListSerializer, OrderSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminUser,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminUser,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return AirplaneSerializer

    def get_queryset(self):
        return self.queryset.select_related("type")


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminUser,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related("source", "destination")
        return queryset


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        return FlightSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related("airplane", "route__source", "route__destination")
        if self.action == "retrieve":
            queryset = self.queryset.prefetch_related("crew")

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        queryset = queryset.prefetch_related("tickets__flight")

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
