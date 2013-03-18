from django.template import Template, Context, TemplateDoesNotExist
from django.test import TestCase
from django.test.utils import (
    restore_template_loaders,
    setup_test_template_loader,
)


class IncludeTagTest(TestCase):

    def setUp(self):
        setup_test_template_loader({
            "basic.html": "Basic",
            "block.html": "{% block short %}short{% endblock %} {% block long %}long{% endblock %}",
            "headline.html": "{{ headline }}",
            "has space.html": "Spaced",
        })

    def tearDown(self):
        restore_template_loaders()

    def test_include(self):
        t = Template("{% load partial_include %}{% include 'basic.html' %}")
        c = Context()
        output = t.render(c)
        self.assertEqual(output, "Basic")

    def test_context(self):
        t = Template("{% load partial_include %}{% include 'headline.html' %}")
        c = Context(dict(headline="Headline"))
        output = t.render(c)
        self.assertEqual(output, "Headline")

    def test_include_variable(self):
        t = Template("{% load partial_include %}{% include template_name %}")
        c = Context(dict(template_name="basic.html"))
        output = t.render(c)
        self.assertEqual(output, "Basic")

    def test_block_does_not_exist(self):
        t = Template("{% load partial_include %}{% include 'basic.html' with block='chubba-wubba' %}")
        c = Context()
        with self.assertRaisesRegexp(TemplateDoesNotExist,
                "Block chubba-wubba does not exist in template basic.html"):
            t.render(c)

    def test_template_does_not_exist(self):
        t = Template("{% load partial_include %}{% include 'chuck-testa.html' %}")
        c = Context()
        with self.assertRaises(TemplateDoesNotExist):
            t.render(c)

    def test_suppress_block_error(self):
        t = Template("{% load partial_include %}{% include 'basic.html' with block='beluga' quiet %}")
        c = Context()
        output = t.render(c)
        self.assertEqual(output, "")

    def test_suppress_template_error(self):
        t = Template("{% load partial_include %}{% include 'bubble-bobble-forever.html' quiet %}")
        c = Context()
        output = t.render(c)
        self.assertEqual(output, "")

    def test_with_space(self):
        t = Template("{% load partial_include %}{% include 'has space.html' %}")
        c = Context()
        output = t.render(c)
        self.assertEqual(output, "Spaced")

    def test_partial_include(self):
        t = Template("{% load partial_include %}{% include 'block.html' with block='short' %}")
        c = Context()
        output = t.render(c)
        self.assertEqual(output, "short")

    def test_partial_no_quotes(self):
        t = Template("{% load partial_include %}{% include 'block.html' with block=short %}")
        c = Context()
        output = t.render(c)
        self.assertEqual(output, "short")

    def test_inline_context(self):
        t = Template("{% load partial_include %}{% include 'headline.html' with headline='Headline' %}")
        c = Context()
        output = t.render(c)
        self.assertEqual(output, "Headline")

        t = Template("{% load partial_include %}{% include headline with headline='Headline' %}")
        c = Context(dict(headline="headline.html"))
        output = t.render(c)
        self.assertEqual(output, "Headline")

        t = Template("{% load partial_include %}{% include 'headline.html' with headline=headline|upper %}")
        c = Context(dict(headline="Headline"))
        output = t.render(c)
        self.assertEqual(output, "HEADLINE")

    def test_isolated_context(self):
        t = Template("{% load partial_include %}{% include 'headline.html' only %}")
        c = Context(dict(headline="Headline"))
        output = t.render(c)
        self.assertEqual(output, "")

        t = Template("{% load partial_include %}{% include 'headline.html' only with headline='Inline' %}")
        c = Context(dict(headline="Headline"))
        output = t.render(c)
        self.assertEqual(output, "Inline")
