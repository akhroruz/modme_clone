from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.groups.models import Group
from apps.groups.serializers import GroupModelSerializer


class GroupAPIVIew(GenericAPIView):
    queryset = Group.objects.order_by('-created_at')
    serializer_class = GroupModelSerializer
    permission_classes = (AllowAny,)
    lookup_url_kwarg = 'uuid'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': True,
                'status': 201,
                'data': serializer.data
            }
            return Response(data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        groups = Group.objects.all()
        serializer = self.serializer_class(groups, many=True)
        data = {
            'success': True,
            'status': 200,
            'data': serializer.data
        }
        return Response(data, status.HTTP_200_OK)


class GroupDetailAPIView(GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    lookup_url_kwarg = 'uuid'

    def get(self, request, uuid, *args, **kwargs):
        pass

    def put(self, request, uuid, *args, **kwargs):
        group = Group.objects.get(uuid=uuid)
        serializer = self.serializer_class(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': True,
                'status': 200,
                'data': serializer.data
            }
            return Response(data, status.HTTP_200_OK)

    def delete(self, request, uuid, *args, **kwargs):
        group = Group.objects.get(uuid=uuid)
        group.delete()
        data = {
            'success': True,
            'status': 204
        }
        return Response(data, status.HTTP_204_NO_CONTENT)
