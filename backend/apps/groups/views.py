from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Group, GroupMember
from .serializers import GroupSerializer, AddMemberSerializer
# Create your views here.


User = get_user_model()

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def groups_view(request):

    if request.method == "POST":

        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():

            group = serializer.save(
                created_by=request.user
            )

            GroupMember.objects.create(
                user=request.user,
                group=group,
                role="admin"
            )

            return Response(
                GroupSerializer(group).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    groups = Group.objects.filter(
        members__user=request.user
    )

    serializer = GroupSerializer(
        groups,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_member(request, group_id):

    group = get_object_or_404(
        Group,
        id=group_id
    )

    is_admin = GroupMember.objects.filter(
        group=group,
        user=request.user,
        role="admin"
    ).exists()

    if not is_admin:

        return Response(
            {"error": "Only admins can add members"},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = AddMemberSerializer(data=request.data)

    if serializer.is_valid():

        email = serializer.validated_data["email"]

        user = get_object_or_404(
            User,
            email=email
        )

        already_member = GroupMember.objects.filter(
            group=group,
            user=user
        ).exists()

        if already_member:

            return Response(
                {"error": "User already in group"},
                status=status.HTTP_400_BAD_REQUEST
            )

        GroupMember.objects.create(
            group=group,
            user=user
        )

        return Response(
            {"message": "Member added successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
