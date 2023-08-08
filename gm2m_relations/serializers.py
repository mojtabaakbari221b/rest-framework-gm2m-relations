from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from generic_relations.relations import GenericRelatedField


MANY_RELATION_KWARGS = (
    'read_only', 'write_only', 'required', 'default', 'initial', 'source',
    'label', 'help_text', 'style', 'error_messages', 'allow_empty',
    'html_cutoff', 'html_cutoff_text',
)


class GM2MSerializer(GenericRelatedField):
    def __new__(cls, *args, **kwargs):
        # We override this method in order to automagically create
        # `ManyRelatedField` classes instead when `many=True` is set.
        if kwargs.pop('many', False):
            return cls.many_init(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)
    
    @classmethod
    def many_init(cls, *args, **kwargs):
        list_kwargs = {
            'child_relation': cls(*args, **kwargs),
        }

        for key in kwargs:
            if key in MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]

        return serializers.ManyRelatedField(**list_kwargs)
    
    def to_internal_value(self, data):
        try:
            serializer = self.get_deserializer_for_data(data)
        except ImproperlyConfigured as e:
            raise serializers.ValidationError(e)
        
        return serializer.to_internal_value(data)

    def to_representation(self, instance):
        serializer = self.get_serializer_for_instance(instance=instance)
        return serializer.to_representation(instance)

    def get_serializer_for_instance(self, instance):
        try :
            return self.serializers[instance.__class__]
        except KeyError :
            raise serializers.ValidationError(self.error_messages['no_model_match'])
    
    def get_choices(self, cutoff=None):
        return {}