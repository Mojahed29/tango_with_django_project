from django.test import TestCase
from rango.models import Category, Page
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import datetime, timedelta


class LastFirstPageTests(TestCase):

    def test_first_last_visited_page_not_in_future(self):
        add_cat('test', 1, 1)
        add_page('test page', views=20, url='http://test.com/', cat_id=0)
        page = Page.objects.all().filter(first_visit__isnull=False,
                                         last_visit__isnull=False).first()
        self.assertEqual((page.last_visit <= timezone.now()), True)
        self.assertEqual((page.first_visit <= timezone.now()), True)

    def first_visited_before_last_visited(self):
        add_cat('test', 1, 1)
        add_page('test page', views=20, url='http://test.com/', cat_id=0)
        page = Page.objects.all().filter(first_visit__isnull=False,
                                         last_visit__isnull=False).first()
        if page:
            self.assertEqual((page.last_visit >= page.first_visit), True)


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(name, views, url, cat_id):
    p = Page.objects.get_or_create(title=name, category_id=cat_id)[0]
    p.views = views
    p.last_visit = timezone.now() + timedelta(days=10)
    p.title = name
    p.url = url
    p.views = views
    p.save()
    return p


class IndexViewTests(TestCase):
    def test_index_view_with_categories(self):
        """
        Check to make sure that the index has categories displayed
        """
        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1, 1)
        add_cat('tmp test temp', 1, 1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")
        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)


class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive should results True for categories
        where views are zero or positive
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add
        a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
        cat = cat('Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])
