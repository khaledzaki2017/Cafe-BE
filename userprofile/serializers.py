from rest_framework import serializers


class CategoryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import CategoryMaster

        model = CategoryMaster
        fields = ('id', 'name', 'point', 'is_percentage')
        read_only_fields = fields


class UserProfileSerializer(serializers.ModelSerializer):
    category = CategoryMasterSerializer(many=False, read_only=True)

    class Meta:
        from .models import UserProfile

        model = UserProfile
        fields = ('id', 'category', 'company', 'designation')
        read_only_fields = ('id', 'category', )
