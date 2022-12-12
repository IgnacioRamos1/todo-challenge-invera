from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken
    )
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer

import logging

logger = logging.getLogger('main')


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            logger.info(f'User {user.username} created successfully.')

            return Response({
                "user": RegistrationSerializer(
                    user,
                    context=self.get_serializer_context()
                    ).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            }, status=201)

        logger.error(f'User could not be created. {serializer.errors}')
        return Response(
            {'message': 'Something went wrong', 'errors': serializer.errors},
            status=400
            )


user_registration = RegistrationAPIView.as_view()


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(
                {"status": "OK, goodbye, all refresh tokens blacklisted"},
                status=200
                )

        refresh_token = self.request.data.get('refresh_token')
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is required'},
                status=400
                )

        token = RefreshToken(token=refresh_token)
        token.blacklist()

        logger.info(f'User {request.user.username} logged out successfully.')

        return Response({"status": "OK, goodbye"}, status=200)


user_logout = LogoutView.as_view()
