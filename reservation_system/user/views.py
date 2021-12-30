from rest_framework.views import APIView
from user.serializers import UserRegistrationSerializers, UserSerializers, StatusShowUserInfoSerializers
from rest_framework.response import Response
from drf_spectacular.views import extend_schema
from user.models.users import User
from rest_framework.permissions import IsAdminUser
from utils.commen import IdSerializer


class UserView(APIView):
    permission_classes = [IsAdminUser]

    class STATUS:
        ALL = 'all'

    @extend_schema(
        summary='Add staff by Admin User',
        request=UserSerializers
    )
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(data="The new staff was created successfully")

    @extend_schema(
        summary='Show User Info',
        parameters=[StatusShowUserInfoSerializers]
    )
    def get(self, request):
        if request.GET.get('status') == self.STATUS.ALL:
            objs = User.objects.all()
        else:
            objs = User.objects.filter(id=request.GET.get('id'))

        return Response(data=UserSerializers(objs, many=True).data)

    @extend_schema(
        summary='Delete User',
        parameters=[IdSerializer]
    )
    def delete(self, request):
        obj = User.objects.get(id=request.GET.get('id'))
        obj.delete()
        return Response(data="THe user was deleted successfully")


class UserRegistrationView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        summary='Register new user',
        request=UserRegistrationSerializers
    )
    def post(self, request):
        serializer = UserRegistrationSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="The new user was created successfully")


# class GuestView(APIView):
#     permission_classes = []
#     authentication_classes = []
#
#     @extend_schema(
#         summary="Create a New guest account",
#         request=GuestSerializers,
#     )
#     def post(self, request):
#         serializers = GuestSerializers(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         obj = serializers.save()
#
#         return Response(data=ShowGuestSerializers(obj).data)