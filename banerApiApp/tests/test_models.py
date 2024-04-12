from django.test import TestCase
from banerApiApp.models import Banner, Tag, Feature


class TestTagModel(TestCase):
    def test_create_Tag(self):
        tag = Tag.objects.create(name='test name', description='test description')
        self.assertEqual(tag.name, 'test name')
        self.assertEqual(tag.description, 'test description')


class TestFeatureModel(TestCase):
    def test_create_Feature(self):
        feature = Feature.objects.create(name='test name', description='test description')
        self.assertEqual(feature.name, 'test name')
        self.assertEqual(feature.description, 'test description')


class TestBannerModel(TestCase):
    def test_create_Banner(self):
        tag = Tag.objects.create(name='test tag name', description='test tag description')
        feature = Feature.objects.create(name='test feature name', description='test feature description')

        banner_content = {
            'title': 'test banner title',
            'text': 'test banner text',
            'url': 'https://avito.tech/'
        }
        banner = Banner.objects.create(feature_id=feature, is_active=True, content=banner_content)
        banner.tag_ids.add(tag)

        self.assertEqual(banner.is_active, True)
        self.assertEqual(banner.tag_ids.first(), tag)
        self.assertEqual(banner.feature_id, feature)
        self.assertEqual(banner.content, banner_content)
