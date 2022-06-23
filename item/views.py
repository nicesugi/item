from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from item.models import Item
# from item.serializers import CategorySerializer
from item.serializers import ItemSerializer
# from item.serializers import OrderSerializer

class ItemView(APIView):
    
    def get(self, request):
        print(request.data)
        posts = Item.objects.all()
        serialized_data = ItemSerializer(posts, many=True).data
        return Response(serialized_data) 


    
    def post(self, request):
        request.data['user'] = request.user.id
        item_serializer = ItemSerializer(data=request.data)
        # print(item_serializer)
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data)
        return Response(item_serializer.errors)

    
    
class OrderView(APIView):    
    def get(self, request):
        print(request.data)
        data = request.data
        
        return Response(ItemSerializer(data).data)
        return Response({})
    