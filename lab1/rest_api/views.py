from rest_framework import generics
from rest_framework import viewsets, mixins
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import *
from django.shortcuts import get_object_or_404

# Create your views here.

class PostList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the posts.

    post:
    Create a new post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostByUserList(generics.ListAPIView):
    """
    Return a list of all posts of an user.
    """
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.filter(author=self.kwargs['author'])

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get: 
    Return a post with the id.

    put:
    Update a post with the id.

    delete:
    Delete a post with the id.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

class CommentList(generics.ListAPIView):
    """
    Return a list of all comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class CommentByPostList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the comments of a post.

    post:
    Create a new comment to a post.

    """
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post'])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post'])
        serializer.save(author=self.request.user, post=post)

class CommentByUserList(generics.ListAPIView):
    """
    Return a list of all comments of an user.
    """
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.filter(author=self.kwargs['author'])

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get: 
    Return a comment with the id.

    put:
    Update a comment with the id.

    delete:
    Delete a comment with the id.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class UserViewSet(viewsets.ModelViewSet):
    """
    list:
    Return a list of all users.

    retrieve:
    Return an user with the id.

    create:
    Create a new user.

    update:
    Updates an user.
    
    delete:
    Deletes an user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserIsOwnerOrReadAndCreateOnly,)

