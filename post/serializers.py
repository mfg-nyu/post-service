from post.models import Post, Comments

from rest_framework_mongoengine import serializers as mongoserializers


class AllowNestedWriteMixin:
    '''
    Allow embeded document written
    '''

    def create(self, validated_data):
        # raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model
        try:
            # recursively create EmbeddedDocuments from their validated data
            # before creating the document instance itself
            instance = self.recursive_save(validated_data)
        except TypeError as exc:
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception text was: %s.' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    type(self).__name__,
                    exc
                )
            )
            raise TypeError(msg)
        except ValidationError as exc:
            msg = (
                'Got a `ValidationError` when calling `%s.objects.create()`. '
                'This may be because request data satisfies serializer validations '
                'but not Mongoengine`s. You may need to check consistency between '
                '%s and %s.\nIf that is not the case, please open a ticket '
                'regarding this issue on https://github.com/umutbozkurt/django-rest-framework-mongoengine/issues'
                '\nOriginal exception was: %s' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    type(self).__name__,
                    exc
                )
            )
            raise ValidationError(msg)

        return instance


class CommentsSerializer(mongoserializers.EmbeddedDocumentSerializer):

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('created_at', 'id', 'user_id')


class PostSerializer(AllowNestedWriteMixin, mongoserializers.DocumentSerializer):
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        depth = 2
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'comments')


class ValidationError(Exception):
    pass
