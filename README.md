# gm2m_relations

This library implements [Django REST Framework](http://www.django-rest-framework.org/) serializers to handle generic many to many relations.

# Requirements

Any currently-supported combination of [rest-framework-generic-relations](https://github.com/LilyFoote/rest-framework-generic-relations), Django REST Framework, Python, and Django.

# Installation

Install using `pip` :
```sh
pip install gm2m_relations
```

# API Reference

## GM2MSerializer

serializes django generic many-to-many field. For a primer on generic many-to-many field, first see: https://github.com/tkhyn/django-gm2m


Let's assume a `Post` model which has a generic m2m relationship with other arbitrary models:

```python
from gm2m import GM2MField


class Post(models.Model):
    text = models.SlugField()

    author = GM2MField()
```

And the following two models, which may have associated authors:

```python
class User(models.Model):
    name = models.CharField()

class Organ(models.Model):
    name = models.CharField()
```

Now we define serializers for each model that may get associated with posts.

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name',)

class OragnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organ
        fields = ('name',)
```

The model serializer for the `Post` model could look like this:

```python
from gm2m_relations.serializers import GM2MSerializer

class PostSerializer(serializers.ModelSerializer):
    """
    A `Post` serializer with a `GM2MField` mapping all possible
    models to their respective serializers.
    """
    author = GM2MSerializer(
        {
            User: UserSerializer(),
            Organ: OragnSerializer(),
        },
        many=True,
    )

    class Meta:
        model = Post
        fields = ('text', 'author')
```

The JSON representation of a `Post` object with `text='django'` and its generic m2m field pointing to `User` object with `name='Ali'` would look like this:

```json
{
    "author": [
        {
            "name" : "Ali",
        }
    ],
    "text": "django"
}
```

## Writing to generic many to many field

The above `PostSerializer` is also writable. By default, a `GenericRelatedField` iterates over its nested serializers and returns the value of the first serializer that is actually able to perform `to_internal_value()` without any errors.

```python
post_serializer = PostSerializer(
    data={
        'text': 'python',
        'author': [
            {
                "name" : "Ali",
            },
        ],
    },
)

post_serializer.is_valid()
post_serializer.save()
```

If you feel that this default behavior doesn't suit your needs, implement your own way of decision-making.
