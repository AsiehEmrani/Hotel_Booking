from rest_framework.views import APIView
from .models import Room, Hotel
from .serializers import RoomSerializers, HotelSerializers
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from utils.commen import IdSerializer
from rest_framework.permissions import IsAdminUser


class RoomView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Show Rooms",
        responses={201: RoomSerializers},
    )
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializers(rooms, many=True)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Add Room",
        request=RoomSerializers,
    )
    def post(self, request):
        serializer = RoomSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="The new room was created successfully")

    @extend_schema(
        summary="Update Room",
        parameters=[IdSerializer],
        request=RoomSerializers
    )
    def update(self, request):
        room = Room.objects.get(id=request.GET.get('id'))
        serializers = RoomSerializers(room, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(data=RoomSerializers(serializers))

    @extend_schema(
        summary="Delete Room",
        parameters=[IdSerializer]
    )
    def delete(self, request):
        room = Room.objects.get(id=request.GET.get('id'))
        if room:
            room.delete()
            return Response(data="", status=204)
        else:
            return Response(data="This room dose not exist")


class HotelView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Show Hotels",
        responses={201: HotelSerializers},
    )
    def get(self, request):
        hotels = Hotel.objects.all()
        serializers = HotelSerializers(hotels, many=True)
        return Response(data=serializers.data)

    @extend_schema(
        summary="Delete Hotel",
        parameters=[IdSerializer]
    )
    def delete(self, request):
        hotel = Hotel.objects.get(id=request.GET.get('id'))
        if hotel:
            hotel.delete()
            return Response(data="", status=204)
        else:
            return Response(data="This hotel dose not exist")