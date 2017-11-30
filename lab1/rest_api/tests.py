from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import *
from .serializers import *

# Create your tests here.

class CreateUserTestCase(APITestCase):
    def setUp(self):
        self.data = {'username': 'bozo', 'password': 'bozo'}

    def test_create_user(self):
        response = self.client.post(reverse('user-list'), self.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class ReadUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')

    def test_read_user_list(self):
        response = self.client.get(reverse('user-list'), format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['username'], self.user.username)

    def tests_read_user_details(self):
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], self.user.username)
    
class UpdateUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', email='bozo@bozo.com', password='bozo')
        self.data = {'username': 'bozo', 'password': 'bozo', 'email': 'superbozo@bozo.com'}
        self.client.login(username=self.user.username, password='bozo')

    def test_update_user(self):
        response = self.client.put(reverse('user-detail', args=[self.user.id]), self.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['email'], self.data['email'])

class DeleteUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', email='bozo@bozo.com', password='bozo')
        self.client.login(username=self.user.username, password='bozo')

    def test_delete_user(self):
        response = self.client.delete(reverse('user-detail', args=[self.user.id]))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


# Test posts
class CreatePostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.data = {'title': 'Title', 'text': 'Text'}
        self.client.login(username='bozo', password='bozo')

    def test_create_post(self):
        response = self.client.post(reverse('post-list'), self.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class ReadPostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')

    def test_read_post_list(self):
        response = self.client.get(reverse('post-list'))

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_read_post_details(self):
        response = self.client.get(reverse('post-detail', args=[self.post.id]))

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], self.post.title)

class UpdatePostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')
        self.data = PostSerializer(self.post).data
        self.data.update(title='edited')
        self.client.login(username='bozo', password='bozo')

    def test_update_post(self):
        response = self.client.put(reverse('post-detail', args=[self.post.id]), self.data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], self.data['title'])

class DeletePostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')
        self.client.login(username='bozo', password='bozo')

    def test_delete_post(self):
        response = self.client.delete(reverse('post-detail', args=[self.post.id]))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
