from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Activity
from datetime import datetime, timedelta

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_str_representation(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')


class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.activity_data = {
            'user': self.user,
            'activity_type': 'running',
            'duration': 30,
            'distance': 5.2,
            'calories_burned': 320,
            'date': datetime.now()
        }

    def test_create_activity(self):
        activity = Activity.objects.create(**self.activity_data)
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'running')
        self.assertEqual(activity.duration, 30)
        self.assertEqual(activity.distance, 5.2)
        self.assertEqual(activity.calories_burned, 320)

    def test_activity_str_representation(self):
        activity = Activity.objects.create(**self.activity_data)
        expected_str = f"{self.user.username} - running on {activity.date.strftime('%Y-%m-%d')}"
        self.assertEqual(str(activity), expected_str)


class AuthenticationAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')
        self.profile_url = reverse('user-profile')

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_user_login(self):
        # Create user first
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_profile_access(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class ActivityAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.activities_url = reverse('activity-list-create')
        self.activity_data = {
            'activity_type': 'running',
            'duration': 30,
            'distance': 5.2,
            'calories_burned': 320,
            'date': datetime.now().isoformat()
        }

    def test_create_activity(self):
        response = self.client.post(self.activities_url, self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        activity = Activity.objects.first()
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'running')

    def test_list_activities(self):
        # Create some activities
        Activity.objects.create(user=self.user, **self.activity_data)
        Activity.objects.create(
            user=self.user,
            activity_type='cycling',
            duration=45,
            distance=15.0,
            calories_burned=450,
            date=datetime.now()
        )
        
        response = self.client.get(self.activities_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_activity_detail(self):
        activity = Activity.objects.create(user=self.user, **self.activity_data)
        detail_url = reverse('activity-detail', kwargs={'pk': activity.pk})
        
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activity_type'], 'running')

    def test_update_activity(self):
        activity = Activity.objects.create(user=self.user, **self.activity_data)
        detail_url = reverse('activity-detail', kwargs={'pk': activity.pk})
        
        update_data = {
            'activity_type': 'cycling',
            'duration': 45,
            'distance': 15.0,
            'calories_burned': 450,
            'date': datetime.now().isoformat()
        }
        
        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        activity.refresh_from_db()
        self.assertEqual(activity.activity_type, 'cycling')

    def test_delete_activity(self):
        activity = Activity.objects.create(user=self.user, **self.activity_data)
        detail_url = reverse('activity-detail', kwargs={'pk': activity.pk})
        
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Activity.objects.count(), 0)

    def test_activity_history_filtering(self):
        # Create activities with different dates
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            distance=5.2,
            calories_burned=320,
            date=today
        )
        Activity.objects.create(
            user=self.user,
            activity_type='cycling',
            duration=45,
            distance=15.0,
            calories_burned=450,
            date=yesterday
        )
        
        history_url = reverse('activity-history')
        response = self.client.get(history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_activity_metrics(self):
        # Create multiple activities
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            distance=5.2,
            calories_burned=320,
            date=datetime.now()
        )
        Activity.objects.create(
            user=self.user,
            activity_type='cycling',
            duration=45,
            distance=15.0,
            calories_burned=450,
            date=datetime.now()
        )
        
        metrics_url = reverse('activity-metrics')
        response = self.client.get(metrics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_duration'], 75)
        self.assertEqual(response.data['activity_count'], 2)

    def test_unauthorized_access(self):
        # Test without authentication
        self.client.credentials()
        response = self.client.get(self.activities_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_access_other_user_activities(self):
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        other_activity = Activity.objects.create(
            user=other_user,
            activity_type='running',
            duration=30,
            distance=5.2,
            calories_burned=320,
            date=datetime.now()
        )
        
        detail_url = reverse('activity-detail', kwargs={'pk': other_activity.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ValidationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.activities_url = reverse('activity-list-create')

    def test_invalid_duration(self):
        data = {
            'activity_type': 'running',
            'duration': -5,  # Invalid negative duration
            'distance': 5.2,
            'calories_burned': 320,
            'date': datetime.now().isoformat()
        }
        response = self.client.post(self.activities_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_distance(self):
        data = {
            'activity_type': 'running',
            'duration': 30,
            'distance': -1.0,  # Invalid negative distance
            'calories_burned': 320,
            'date': datetime.now().isoformat()
        }
        response = self.client.post(self.activities_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_activity_type(self):
        data = {
            'activity_type': 'invalid_type',  # Invalid activity type
            'duration': 30,
            'distance': 5.2,
            'calories_burned': 320,
            'date': datetime.now().isoformat()
        }
        response = self.client.post(self.activities_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
