from .models import *
from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from django.contrib.auth.models import AbstractUser, User as UserAuth
from django.contrib.gis.measure import D
from django.db.models import Q


# UserAuth Serializers

class UserAuthSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserAuth
        fields = '__all__'


# User Serializers

class UserSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    # Method fields
    users_around = serializers.SerializerMethodField('get_users_around')

    class Meta:
        model = User
        fields = ['url', 'address', 'lat', 'lng', 'users_around']

    # Get list of users in 1km range around user address, without self user
    def get_users_around(self, user):
        if not user.location:
            return []

        # Filtering and serializing users
        users_query_set = User.objects.filter(location__distance_lte=(user.location, D(km=1))).filter(~Q(pk=user.pk))
        users = UserSerializer(instance=users_query_set, many=True, context=self.context, fields=['url']).data

        return users


# Category Serializers

class CategorySerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name', 'slug', 'id']


# Tag Serializers

class TagSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'name', 'slug', 'id']


# Blog Serializers

class BlogListSerializer(serializers.HyperlinkedModelSerializer):
    # Method fields
    category_username = serializers.SerializerMethodField('get_category_username')
    tags_names = serializers.SerializerMethodField('get_tags_name')
    author_name = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Blog
        fields = ['url', 'title', 'slug', 'category_username', 'tags_names', 'author_name']

    # Methods

    # Get name of blog category
    def get_category_name(self, blog):
        if blog.category is None:
            return None

        # Filtering and serializing category into category name
        category_query_set = Category.objects.filter(id=blog.category_id)
        category_data = CategorySerializer(instance=category_query_set, many=True, context=self.context,
                                           fields=['name']).data

        return category_data[0].get('name')

    # Get list of tag names
    def get_tags_name(self, blog):
        if not blog.tags:
            return []

        # Filtering and serializing tags
        blog_tags = blog.tags.all()[:1]
        tags_query_set = Tag.objects.filter(blog__tags__in=blog_tags)
        tag_field = TagSerializer(instance=tags_query_set, many=True, context=self.context, fields=['name']).data

        # Refactoring list of name dictionaries into list of names
        for i in range(len(tag_field)):
            tag_field[i] = tag_field[i].get('name')

        return tag_field

    # Get username of blog author
    def get_author_username(self, blog):

        # Filtering and serializing author
        author_query = UserAuth.objects.filter(pk=blog.author_id)
        author_field = UserAuthSerializer(instance=author_query, many=True, context=self.context,
                                          fields=['username']).data

        return author_field[0].get('username')


class BlogDetailSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    # Method fields
    comments_count = serializers.SerializerMethodField('get_comments_count')
    is_user_comment_inside = serializers.SerializerMethodField('get_is_user_comment_inside')
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = Blog
        fields = ['url', 'title', 'content', 'slug', 'creation_date', 'category', 'tags', 'author', 'comments_count',
                  'is_user_comment_inside', 'comments']

    # Methods

    # Get number of comments in blog
    def get_comments_count(self, blog):
        return Comment.objects.filter(blog=blog).count()

    # Get status if blog contains comment of logged user
    def get_is_user_comment_inside(self, blog):
        # Logged auth user
        logged_auth_user = self.context['request'].user.pk

        # Filtering and serializing comments
        comment_query_set = Comment.objects.filter(blog=blog, user=logged_auth_user)
        comments = CommentSerializer(instance=comment_query_set, many=True, context=self.context).data

        if not comments:
            return False

        return True

    # Get list of comments in blog
    def get_comments(self, blog):
        comment_query_set = Comment.objects.filter(blog=blog)
        return CommentSerializer(instance=comment_query_set, many=True, context=self.context).data


# Comment Serializers

class CommentSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['url', 'blog', 'comment', 'user']
