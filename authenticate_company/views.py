from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from authenticate_company.serializers import AuthenticateCompanySerializer
from helpers.authenticate import authenticate_company, re_auth
from helpers.modify_auth_json import ModifyAuthJson


class Login(generics.CreateAPIView):
    serializer_class = AuthenticateCompanySerializer

    def post(self, request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_status, cookies, response_body = authenticate_company(
            base_url=serializer.validated_data['base_url'],
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        server_type = serializer.validated_data['type']
        if response_status == 200:
            auth_json = ModifyAuthJson()
            json_file_data = auth_json.get_auth_data()
            json_file_data[server_type] = {
                'base_url': serializer.validated_data['base_url'],
                'username': serializer.validated_data['username'],
                'password': serializer.validated_data['password'],
                'cookies': cookies.get_dict()
            }
            auth_json.set_auth_data(json_file_data)

            return Response({
                'success': True,
                'data': {
                    server_type + '-authenticated': True
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'data': {
                'response_status': response_status,
                'auth_response_body': response_body
            }
        }, status=status.HTTP_401_UNAUTHORIZED)


class GetServerInfo(generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR')
        auth_json = ModifyAuthJson()

        return Response({
            'success': True,
            'data': {
                'source': {
                    'server': auth_json.get_base_url('source'),
                    'user': auth_json.get_username('source')
                },
                'target': {
                    'server': auth_json.get_base_url('target'),
                    'user': auth_json.get_username('target')
                }
            }
        }, status=status.HTTP_200_OK)


class ReAuthServer(generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR')
        re_auth('source')
        re_auth('target')

        return Response({
            'success': True,
            'data': None
        }, status=status.HTTP_200_OK)
