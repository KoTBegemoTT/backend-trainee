import json

from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from banerApiApp.models import Tag, Feature, Banner


class TestIndexView(APITestCase):
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"Success":"The setup was successful"}')


class GetBannerView(APITestCase):
    def test_get_banner_401(self):
        response = self.client.get('/user_banner')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'{"detail":"Authentication credentials were not provided."}')

    def test_get_banner_empty_data(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user)
        response = self.client.get('/user_banner')
        self.assertEqual(response.status_code, 400)

    def test_banner_view_with_invalid_tag_id(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user)
        data = {
            'feature_id': '1',
            'tag_id': 'a'
        }
        response = self.client.get('/user_banner', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"error":"invalid literal for int() with base 10: \'a\'"}')

    def test_banner_view_with_invalid_feature_id(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user)
        data = {
            'feature_id': 'a',
            'tag_id': '1'
        }
        response = self.client.get('/user_banner', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"error":"invalid literal for int() with base 10: \'a\'"}')

    def test_banner_view_404(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user)
        data = {
            'feature_id': '1',
            'tag_id': '1'
        }
        response = self.client.get('/user_banner', data)
        self.assertEqual(response.status_code, 404)

    def test_banner_view_404_not_active_banner(self):
        tag = Tag.objects.create(name='test tag name', description='test tag description')
        feature = Feature.objects.create(name='test feature name', description='test feature description')

        banner_content = {
            'title': 'test banner title',
            'text': 'test banner text',
            'url': 'https://avito.tech/'
        }
        banner = Banner.objects.create(feature_id=feature, is_active=False, content=banner_content)
        banner.tag_ids.add(tag)

        user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user)
        data = {
            'feature_id': feature.feature_id,
            'tag_id': tag.tag_id,
            'use_last_revision': 'true'
        }
        response = self.client.get('/user_banner', data)
        self.assertEqual(response.status_code, 404)

    def test_banner_view_200(self):
        tag = Tag.objects.create(name='test tag name', description='test tag description')
        feature = Feature.objects.create(name='test feature name', description='test feature description')

        banner_content = {
            'title': 'test banner title',
            'text': 'test banner text',
            'url': 'https://avito.tech/'
        }
        banner = Banner.objects.create(feature_id=feature, is_active=True, content=banner_content)
        banner.tag_ids.add(tag)

        user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user)
        data = {
            'feature_id': feature.feature_id,
            'tag_id': tag.tag_id,
            'use_last_revision': 'true'
        }
        response = self.client.get('/user_banner', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), banner_content)


class TestBannerView(APITestCase):
    def test_banner_view_401(self):
        response = self.client.get('/banner')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'{"detail":"Authentication credentials were not provided."}')

    def test_banner_view_403(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user)
        response = self.client.get('/banner')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'{"detail":"You do not have permission to perform this action."}')

    def test_banner_view_GET_200(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.is_staff = True
        self.client.force_authenticate(user)
        response = self.client.get('/banner')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_banner_view_POST_201(self):
        tag = Tag.objects.create(name='test tag name', description='test tag description')
        feature = Feature.objects.create(name='test feature name', description='test feature description')

        user = User.objects.create_user(username='testuser', password='12345')
        user.is_staff = True
        self.client.force_authenticate(user)
        data = {
            'feature_id': feature.feature_id,
            'tag_id': [tag.tag_id],
            'content': {
                'title': 'test banner title',
                'text': 'test banner text',
                'url': 'https://avito.tech/'
            },
            'is_active': True
        }
        response = self.client.post('/banner', data)
        self.assertEqual(response.status_code, 201)


class TestBannerView(APITestCase):
    def test_banner_view_401(self):
        response = self.client.get('/banner/1')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'{"detail":"Authentication credentials were not provided."}')

    def test_banner_view_403(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user)
        response = self.client.get('/banner/1')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'{"detail":"You do not have permission to perform this action."}')

    def test_banner_view_PATCH_200(self):
        tag = Tag.objects.create(name='test tag name', description='test tag description')

        feature = Feature.objects.create(name='test feature name', description='test feature description')

        banner_content = {
            'title': 'test banner title',
            'text': 'test banner text',
            'url': 'https://avito.tech/'
        }
        banner = Banner.objects.create(feature_id=feature, is_active=True, content=banner_content)
        banner.tag_ids.add(tag)
        banner.save()

        user = User.objects.create_user(username='testuser', password='12345')
        user.is_staff = True
        self.client.force_authenticate(user)

        new_feature = Feature.objects.create(name='test feature name 2', description='test feature description 2')
        new_tag = Tag.objects.create(name='test tag name 3', description='test tag description 3')
        new_content = '{"title": "test banner title 2", "text": "test banner text 2", "url": "https://avito.tech/2"}'
        data = {
            'feature_id': new_feature.feature_id,
            'tag_ids': [new_tag.tag_id],
            'content': new_content,
            'is_active': False
        }

        response = self.client.patch('/banner/' + str(banner.banner_id), data, format='json')

        banner.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(banner.feature_id, new_feature)
        self.assertEqual(banner.is_active, False)
        self.assertEqual(banner.tag_ids.first(), new_tag)
        self.assertEqual(json.loads(banner.content), json.loads(new_content))

    def test_banner_view_DELETE_204(self):
        tag = Tag.objects.create(name='test tag name', description='test tag description')

        feature = Feature.objects.create(name='test feature name', description='test feature description')

        banner_content = {
            'title': 'test banner title',
            'text': 'test banner text',
            'url': 'https://avito.tech/'
        }
        banner = Banner.objects.create(feature_id=feature, is_active=True, content=banner_content)
        banner.tag_ids.add(tag)
        banner.save()

        user = User.objects.create_user(username='testuser', password='12345')
        user.is_staff = True
        self.client.force_authenticate(user)

        response = self.client.delete('/banner/' + str(banner.banner_id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Banner.objects.filter(banner_id=banner.banner_id).exists())
