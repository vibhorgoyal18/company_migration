from rest_framework import serializers


class AuthenticateCompanySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    base_url = serializers.CharField(
        max_length=50,
        allow_blank=False,
        allow_null=False,
        required=True
    )
    username = serializers.CharField(
        max_length=50,
        allow_blank=False,
        allow_null=False,
        required=True)

    password = serializers.CharField(
        max_length=200,
        style={'input_type': 'password'},
        write_only=True,
        allow_blank=False,
        allow_null=False,
        required=True)

    type = serializers.ChoiceField(
        allow_null=False,
        allow_blank=False,
        required=True,
        choices=['source', 'target']
    )

    class Meta:
        fields = '__all__'
