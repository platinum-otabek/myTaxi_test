from rest_framework import generics, status
from rest_framework.response import Response

from mvp.models import Order, Client
from mvp.serializers import OrderSerializer


class ListCreateOrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UpdateOrderStatus(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        request_status = request.data['status']
        if order.status == 'created':
            if request_status == 'accepted' or request_status == 'cancelled':
                return self.partial_update(request, *args, **kwargs)
            elif request_status == 'finished':
                return Response(data={
                    'msg': 'You can not change status from create to finish. First you can accept or cancel this order'},
                    status=status.HTTP_409_CONFLICT)
            else:
                return Response(data={'msg': 'Not allowed status for order'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif order.status == 'accepted':
            if request_status == 'finished':
                return self.partial_update(request, *args, **kwargs)
            elif request_status == 'created' or request_status == 'cancelled':
                return Response(data={
                    'msg': 'You can not change status from accept to cancel or create.'},
                    status=status.HTTP_409_CONFLICT)
            else:
                return Response(data={'msg': 'Not allowed status for order'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif order.status == 'finished' or order.status == 'cancelled':
            return Response(data={'msg': 'You can not change finished or cancelled orders'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)


class OrderClientDetail(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        try:
            client = Client.objects.get(user_ptr_id=self.kwargs['pk'])
        except Client.DoesNotExist:
            return Response(data={'msg': 'Client not Found'}, status=status.HTTP_404_NOT_FOUND)
        all_orders = Order.objects.filter(client_id=client.user_ptr_id, date__range=[from_date, to_date])
        serializer_orders = OrderSerializer(all_orders, many=True)
        return Response(data=serializer_orders.data)
