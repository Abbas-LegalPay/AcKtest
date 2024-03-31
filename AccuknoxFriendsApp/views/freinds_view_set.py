from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from utility.results_pagination import StandardResultsSetPagination
from ..serializers import *
from ..models import *
from AccuknoxApp.models.accuknox_user_model import AccuKnoxUser


class FriendsRequestViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["received_requests__email", "received_requests__first_name", "received_requests__last_name"]
    pagination_class = StandardResultsSetPagination
    serializer_class = FriendReqSerializer

    def get_queryset(self):
        self.queryset = FriendRequest.objects.filter(from_user=self.request.user)
        return self.queryset

    @action(detail=False, methods=['get'], url_path="list", url_name="list")
    def friend_list(self, request):
        friend_list = FriendRequest.objects.filter(from_user_id=request.user.id, is_accepted=True)
        if friend_list.exists():
            serializer = FriendReqSerializer(friend_list, many=True)
            return Response(serializer.data)

        return Response({'message': 'No friends found'}, status=400)

    @action(detail=False, methods=['post'], url_path="send_req", url_name="send_req")
    def send_friend_request(self, request):
        to_user = request.data['to_user_email']
        try:
            req_user = AccuKnoxUser.objects.get(email=to_user)
        except AccuKnoxUser.DoesNotExist:
            return Response({'message': 'requested user not found'}, status=400)
        if request.user.id != to_user:
            if FriendRequest.objects.filter(from_user=request.user, to_user=req_user).exists():
                return Response({'message': 'you are already friends'}, status=400)
            friend_request = FriendRequest.objects.create(from_user=request.user, to_user=req_user)
            serializer = FriendReqSerializer(friend_request)
            return Response(serializer.data)
        return Response({'message': 'Cannot send friend request to yourself'}, status=400)

    @action(detail=False, methods=['get'], url_path="pending", url_name="pending")
    def pending_friend_request(self, request):
        pending_friend_request = FriendRequest.objects.filter(from_user_id=request.user.id, is_accepted=False)
        if pending_friend_request.exists():
            serializer = FriendReqSerializer(pending_friend_request, many=True)
            return Response(serializer.data)

        return Response({'message': 'No any pending friend request'}, status=400)

    def partial_update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
