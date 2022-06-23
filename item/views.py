from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from item.models import Item
from item.models import Category
from item.models import ItemOrder

from item.serializers import ItemSerializer
from item.serializers import ItemOrderSerializer

from datetime import timedelta

class ItemView(APIView):
    # 카테고리에 따른 Response data 반환(아이템name,카테고리name,이미지url,카테고리id)
    def get(self, request):
        # 방법1
        category = request.data['category']
        items = Item.objects.filter(category__name=category)
        serializered_data = ItemSerializer(items, many=True)
        print(serializered_data)
        return Response(serializered_data.data, status=status.HTTP_200_OK)

        # 방법2
        # category = request.POST.get('category', None)
        # items = Category.objects.prefetch_related('item_set').get(name=category).item_set.all()
        # if items.exists():
        #     serializers = ItemSerializer(items, many=True)
        #     print(serializers)
        #     return Response(serializers.data, status=status.HTTP_200_OK)
        # return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)



    # item serializer를 이용하여 item을 등록
    def post(self, request):
        # 방법1
        item_serializer = ItemSerializer(data=request.data)
        category = Category.objects.get(id=request.data['category'])
        
        if item_serializer.is_valid():
            item_serializer.save(category=category)
            return Response(item_serializer.data, status=status.HTTP_200_OK)
        return Response(item_serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
        # 방법2:인스턴스 생성
        # item_serializer = ItemSerializer(data=request.data)
        # if item_serializer.is_valid():
        #     category_instance = get_object_or_404(Category, id=request.data['category'])
            
        #     item_serializer.save(category=category_instance)
        #     return Response(item_serializer.data, status=status.HTTP_200_OK)
        # return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class ItemOrderView(APIView):    
    def get(self, request):
        order_id = self.request.query_params.get('order_id')

        data = ItemOrder.objects.filter(
            Q(order__order_date__range=[timezone.now() - timedelta(days=7), timezone.now()]) &
            Q(order_id=order_id)
        )

        if data.exists():
            serializer = ItemOrderSerializer(data, many=True)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


    