# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
#
# from users.models import User
#
#
# @registry.register_document
# class UserDocument(Document):
#     class Index:
#         name = 'users'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#         }
#
#     class Django:
#         model = User
#         fields = 'first_name', 'last_name', 'phone'
