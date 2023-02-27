from rest_framework.serializers import ModelSerializer

from groups.models import Branch


class BranchModelSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class BranchListModelSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name')
