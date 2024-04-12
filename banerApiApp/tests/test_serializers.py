from django.test import TestCase
from banerApiApp.models import Banner, Tag, Feature
from banerApiApp.serializers import BannerSerializer, ContentSerializer


class TestBannerSerializer(TestCase):
    def test_banner_serialize(self):
        feature = Feature.objects.create(name='test feature name', description='test feature description')
        tag = Tag.objects.create(name='test tag name', description='test tag description')
        tag2 = Tag.objects.create(name='test tag name 2', description='test tag description 2')

        data = {
            'tag_ids': [tag.tag_id, tag2.tag_id],
            'feature_id': feature.feature_id,
            'content': {
                'title': 'test banner title',
                'text': 'test banner text',
                'url': 'https://avito.tech/'
            },
            'is_active': True
        }

        validated_data = {
            'tag_ids': [tag, tag2],
            'feature_id': feature,
            'content': {
                'title': 'test banner title',
                'text': 'test banner text',
                'url': 'https://avito.tech/'
            },
            'is_active': True
        }

        serializer = BannerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, data)
        self.assertEqual(serializer.validated_data, validated_data)

    def test_banner_serializer_with_invalid_tag_id(self):
        feature = Feature.objects.create(name='test feature name', description='test feature description')
        data = {
            'tag_ids': [100],
            'feature_id': feature.feature_id,
            'content': {
                'title': 'test banner title',
                'text': 'test banner text',
                'url': 'https://avito.tech/'
            },
            'is_active': True
        }

        serializer = BannerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tag_ids', serializer.errors)
        self.assertEqual(serializer.errors['tag_ids'][0], 'Invalid pk "100" - object does not exist.')

    def test_banner_serializer_with_invalid_feature_id(self):
        tag = Tag.objects.create(name='test tag name', description='test tag description')

        data = {
            'tag_ids': [tag.tag_id],
            'feature_id': 100,
            'content': {
                'title': 'test banner title',
                'text': 'test banner text',
                'url': 'https://avito.tech/'
            },
            'is_active': True
        }

        serializer = BannerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('feature_id', serializer.errors)
        self.assertEqual(serializer.errors['feature_id'][0], 'Invalid pk "100" - object does not exist.')

    def test_banner_serializer_with_empty_is_active(self):
        feature = Feature.objects.create(name='test feature name', description='test feature description')
        tag = Tag.objects.create(name='test tag name', description='test tag description')

        data = {
            'tag_ids': [tag.tag_id],
            'feature_id': feature.feature_id,
            'content': {
                'title': 'test banner title',
                'text': 'test banner text',
                'url': 'https://avito.tech/'
            },
        }

        serializer = BannerSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, data)


class TestContentSerializer(TestCase):
    def test_content_serialize(self):
        data = {
            'title': 'test banner title',
            'text': 'test banner text',
            'url': 'https://avito.tech/'
        }

        serializer = ContentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)
