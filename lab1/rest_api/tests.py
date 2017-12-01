from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import *
from .serializers import *

# Create your tests here.

# Test users
class CreateUserTestCase(APITestCase):
    def setUp(self):
        self.data = {'username': 'bozo', 'password': 'bozo'}

    def test_create_user(self):
        response = self.client.post(reverse('user-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_bad_request(self):
        response = self.client.post(reverse('user-list'), {'usernam':'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ReadUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')

    def test_read_user_list(self):
        response = self.client.get(reverse('user-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], self.user.username)

    def test_read_user_details(self):
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_read_nonexisting_user_details(self):
        response = self.client.get(reverse('user-detail', args=[219]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
class UpdateUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', email='bozo@bozo.com', password='bozo')
        self.data = {'username': 'bozo', 'password': 'bozo', 'email': 'superbozo@bozo.com'}

    def test_update_user(self):
        self.client.login(username=self.user.username, password='bozo')
        response = self.client.put(reverse('user-detail', args=[self.user.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.data['email'])

    def test_update_user_no_login(self):
        response = self.client.put(reverse('user-detail', args=[self.user.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_different_user(self):
        user = User.objects.create_user(username='novi', password='novi')
        self.client.login(username='novi', password='novi')
        response = self.client.put(reverse('user-detail', args=[self.user.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class DeleteUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', email='bozo@bozo.com', password='bozo')

    def test_delete_user(self):
        self.client.login(username=self.user.username, password='bozo')
        response = self.client.delete(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_no_login(self):
        response = self.client.delete(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_different_user(self):
        user = User.objects.create_user(username='novi', password='novi')
        self.client.login(username='novi', password='novi')
        response = self.client.delete(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Test posts
class CreatePostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.data = {'title': 'Title', 'text': 'Text'}

    def test_create_post(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.post(reverse('post-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_bad_request(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.post(reverse('post-list'), {'title':'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_no_login(self):
        response = self.client.post(reverse('post-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReadPostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')

    def test_read_post_list(self):
        response = self.client.get(reverse('post-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_read_post_details(self):
        response = self.client.get(reverse('post-detail', args=[self.post.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)
        
    def test_read_nonexisting_post_details(self):
        response = self.client.get(reverse('post-detail', args=[219]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdatePostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')
        self.data = PostSerializer(self.post).data
        self.data.update(title='edited')

    def test_update_post(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.put(reverse('post-detail', args=[self.post.id]), self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.data['title'])

    def test_update_nonexisting_post(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.put(reverse('post-detail', args=[219]), self.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_no_login(self):
        response = self.client.put(reverse('post-detail', args=[self.post.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_wrong_user(self):
        User.objects.create_user(username='ja', password='ja')
        self.client.login(username='ja', password='ja')
        response = self.client.put(reverse('post-detail', args=[self.post.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeletePostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')

    def test_delete_post(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.delete(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexisting_post(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.delete(reverse('post-detail', args=[219]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_no_login(self):
        response = self.client.delete(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_wrong_user(self):
        User.objects.create_user(username='ja', password='ja')
        self.client.login(username='ja', password='ja')
        response = self.client.delete(reverse('post-detail', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CreateCommentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')
        self.data = {'text':'text'}

    def test_create_comment(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.post(reverse('comment-by-post-list', args=[self.post.id]), self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_no_login(self):
        response = self.client.post(reverse('comment-by-post-list', args=[self.post.id]), self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ReadCommentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')
        self.comment = Comment.objects.create(author=self.user, post=self.post, text='text')


    def test_read_post_comment_list(self):
        response = self.client.get(reverse('comment-by-post-list', args=[self.post.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_read_comment_list(self):
        response = self.client.get(reverse('comment-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_read_user_comment_list(self):
        response = self.client.get(reverse('comment-by-user-list', args=[self.user.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_read_comment_details(self):
        response = self.client.get(reverse('comment-detail', args=[self.comment.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.comment.text)

    def test_read_nonexisting_comment_details(self):
        response = self.client.get(reverse('comment-detail', args=[219]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateCommentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')
        self.comment = Comment.objects.create(author=self.user, post=self.post, text='text')

        self.data = {'text': 'updated'}


    def test_update_comment(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.put(reverse('comment-detail', args=[self.comment.id]), self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.data['text'])

    def test_update_nonexisting_comment(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.put(reverse('comment-detail', args=[219]), self.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_comment_no_login(self):
        response = self.client.put(reverse('comment-detail', args=[self.comment.id]), self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_comment_wrong_user(self):
        User.objects.create_user(username='ja', password='ja')
        self.client.login(username='ja', password='ja')
        response = self.client.put(reverse('comment-detail', args=[self.comment.id]), self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteCommentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bozo', password='bozo')
        self.post = Post.objects.create(author=self.user, title='title', text='text')
        self.comment = Comment.objects.create(author=self.user, post=self.post, text='text')

    def test_delete_comment(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.delete(reverse('comment-detail', args=[self.comment.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexisting_comment(self):
        self.client.login(username='bozo', password='bozo')
        response = self.client.delete(reverse('comment-detail', args=[219]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_no_login(self):
        response = self.client.delete(reverse('comment-detail', args=[self.comment.id]))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_wrong_user(self):
        User.objects.create_user(username='ja', password='ja')
        self.client.login(username='ja', password='ja')
        response = self.client.delete(reverse('comment-detail', args=[self.comment.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
