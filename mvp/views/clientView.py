from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mvp.models import Client
from mvp.permissions import OwnerPermission
from mvp.serializers import ClientSerializer


class ListCreateClientView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        clientserializer = ClientSerializer(data=request.data)
        clientserializer.is_valid(raise_exception=True)
        clientserializer.save()
        return Response(status=status.HTTP_201_CREATED, data=clientserializer.data)


class GetUpdateDeleteClientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated & OwnerPermission]
