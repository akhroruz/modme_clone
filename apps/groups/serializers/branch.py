from rest_framework.serializers import ModelSerializer

from groups.models import Branch


class BranchModelSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('name', 'address', 'company', 'about', 'phone', 'image')


class BranchListModelSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name')
