from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mvp.models import Driver
from mvp.permissions import OwnerPermission
from mvp.serializers import DriverSerializer


class ListCreateDriverView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def post(self, request, *args, **kwargs):
        driverserializer = DriverSerializer(data=request.data)
        driverserializer.is_valid(raise_exception=True)
        driverserializer.save()
        return Response(status=status.HTTP_201_CREATED, data=driverserializer.data)


class GetUpdateDeletDriverView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & OwnerPermission]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
