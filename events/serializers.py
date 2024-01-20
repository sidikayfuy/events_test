from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser, Organization, Event


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class OrganizationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationUserSerializer(OrganizationAdminSerializer):
    class Meta(OrganizationAdminSerializer.Meta):
        read_only_fields = ('creator',)

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class OrganizationDetailMembersSerializer(OrganizationUserSerializer):
    members = CustomUserSerializer(many=True)
    address_postcode = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        exclude = ('address', 'postcode')
        read_only_fields = ('creator',)

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def get_address_postcode(self, obj):
        return f"{obj.address} {obj.postcode}"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventWithMembersSerializer(EventSerializer):
    members_by_organization = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_members_by_organization(self, obj):
        members = OrganizationDetailMembersSerializer(obj.organizers.all(), many=True).data
        return members

