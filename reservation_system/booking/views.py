import datetime
from rest_framework.views import APIView
from .serializers import BookingSerializers, ShowGuestBookingSerializers, ShowBookingSerializers, ShowBillSerlializers,\
    SearchSerializers, RequestBookingSerializers
from rest_framework.response import Response
from .models import Booking, Bill
from room.models import Room, Hotel
from room.serializers import RoomSerializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from dateutil.parser import parse
from django.contrib.auth.models import AnonymousUser
from  rest_framework.permissions import AllowAny, IsAuthenticated


class BookingView(APIView):
    authentication_classes = []
    permission_classes = []

    def create_obj_bill(self, obj_booking, request, validated_data):
        obj_room = Room.objects.get(id=validated_data['room'].id)
        obj_room.occupancy = True
        obj_room.save()

        stay_days = parse(request.data['checkout_date']) - parse(request.data['checkin_date'])
        total_price = obj_room.price * (stay_days.days + 1)
        obj_bill = Bill.objects.create(email=validated_data['email'],
                                       booking=obj_booking,
                                       price=total_price)
        return obj_bill

    @extend_schema(
        summary='create Booking',
        request=RequestBookingSerializers,
    )
    def post(self, request):
        if request.user == AnonymousUser():
            user = AnonymousUser()
        else:
            user = request.user.id
        serializer = BookingSerializers(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        reservations = Booking.objects.filter(room_id=request.data['room']).order_by('checkin_date')

        if not reservations:

            obj_booking = serializer.create(serializer.validated_data)
            obj_bill = self.create_obj_bill(obj_booking=obj_booking, request=request,
                                            validated_data=serializer.validated_data)
            return Response(data=ShowBillSerlializers(obj_bill).data)
        else:
            # (B0 < E1) && (B1 < E0)
            available = []

            for reservation in reservations:
                request_checkin_date = datetime.datetime.strptime(request.data['checkin_date'], '%Y-%m-%d').date()
                request_checkout_date = datetime.datetime.strptime(request.data['checkout_date'], '%Y-%m-%d').date()
                if request_checkin_date < reservation.checkin_date and \
                        request_checkout_date < reservation.checkout_date:
                    available.append(True)

                elif reservation.checkin_date < request_checkout_date and\
                        request_checkin_date > reservation.checkout_date:
                    available.append(True)
                    # break
                else:
                    available.append(False)
                    continue

            if False in set(available):
                return Response(data="The room is not accessible")
            else:
                obj_booking = serializer.create(serializer.validated_data)
                obj_bill = self.create_obj_bill(obj_booking=obj_booking, request=request, validated_data=serializer.validated_data)
                return Response(data=ShowBillSerlializers(obj_bill).data)

    @extend_schema(
        summary='list Booking',
        parameters=[ShowGuestBookingSerializers],
        responses={201: BookingSerializers},
    )
    def get(self, request):
        try:
            data = Bill.objects.filter(email=request.GET.get('email'))
            if data:
                # context = {
                #     'booking': data}
                # return render(request=request, template_name='booking/show_booking.html', context=context)
                serializers_data = ShowBillSerlializers(data, many=True)
                return Response(data=serializers_data.data)
            else:
                return Response(data='there is not any bookings')
        except Booking.DoesNotExist:
            return Response(data="Error")


class SearchView(APIView):
    permission_classes = []
    authentication_classes = []
    class STATUS:
        ALL = 'all',

    @extend_schema(
        summary='search available rooms',
        parameters=[SearchSerializers]
    )
    def get(self, request):
        request_checkin_date = datetime.datetime.strptime(request.GET.get('checkin_date'), '%Y-%m-%d').date()
        request_checkout_date = datetime.datetime.strptime(request.GET.get('checkout_date'), '%Y-%m-%d').date()
        if request_checkin_date and request_checkout_date:
            pass
        else:
            raise Response(data="please enter your date")

        rooms_id = Booking.objects.filter(checkin_date__lte=request_checkout_date,
                                          checkout_date__gte=request_checkout_date).values('room_id')

        if request.GET.get('status') == self.STATUS.ALL[0]:
            if rooms_id:
                available_rooms = Room.objects.exclude(id__in=[room['room_id'] for room in rooms_id])
            else:
                available_rooms = Room.objects.all()
            return Response(data=RoomSerializers(available_rooms, many=True).data)

        elif request.GET.get('city'):
            exist_hotel = False
            if rooms_id:
                rooms = Room.objects.exclude(id__in=[room['room_id'] for room in rooms_id])
                available_room = []

                for room in rooms:
                    obj_hotel = Hotel.objects.get(id=room.hotel_code.id)
                    if obj_hotel:
                        if obj_hotel.city == request.GET.get('city'):
                            available_room.append(room)
                            exist_hotel = True
                    else:
                       pass
            else:
                available_room = Room.objects.filter(hotel_code__in=[hotel.id for hotel in Hotel.objects.filter(city=request.GET.get('city'))])
                if available_room:
                    exist_hotel = True
            if exist_hotel:
                return Response(data=RoomSerializers(available_room, many=True).data)
            else:
                return Response(data=f"There is not any rooms in {request.GET.get('city')}")

        elif request.GET.get('hotel_id'):
            pass
        else:
            raise Response(data="Please select a suitable status")

    # def get(self, request, *args, **kwargs):
    #     return super(SearchView, self).get(request, *args, **kwargs)