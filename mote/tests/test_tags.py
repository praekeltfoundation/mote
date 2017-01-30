from django import template
from django.test import TestCase
from django.test.client import RequestFactory

from mote import models


class TagsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TagsTestCase, cls).setUpTestData()
        cls.factory = RequestFactory()

    def test_render_element_by_identifier(self):
        request = self.factory.get("/")
        t = template.Template("""{% load mote_tags %}
            {% render_element "myproject.website.atoms.button" %}"""
        )
        result = t.render(template.Context({
            "request": request
        }))
        self.assertHTMLEqual(
            result,
            """<button class="Button Button--solid Button--yellowButtercup">
            <i>Lorem ipsum</i>
            </button>"""
        )

    def test_render_element_with_kwargs_variable(self):
        request = self.factory.get("/")
        button = {"Italic": {"text": "Foo"}}
        t = template.Template("""{% load mote_tags %}
            {% render_element "myproject.website.atoms.button" button=button %}"""
        )
        result = t.render(template.Context({
            "request": request,
            "button": button
        }))
        self.assertHTMLEqual(
            result,
            """<button class="Button Button--solid Button--yellowButtercup">
            <i>Foo</i>
            </button>"""
        )

    def test_render_element_with_kwargs_dict(self):
        request = self.factory.get("/")
        t = template.Template("""{% load mote_tags %}
            {% render_element "myproject.website.atoms.button" button='{"Italic": {"text": "Foo"}}' %}"""
        )
        result = t.render(template.Context({
            "request": request
        }))
        self.assertHTMLEqual(
            result,
            """<button class="Button Button--solid Button--yellowButtercup">
            <i>Foo</i>
            </button>"""
        )

    def test_render_element_with_kwargs_variables(self):
        request = self.factory.get("/")
        t = template.Template("""{% load mote_tags %}
            {% render_element "myproject.website.atoms.button" button='{"Italic": {"text": "{{ foo }}"}}' number=number %}"""
        )
        result = t.render(template.Context({
            "request": request,
            "foo": "Foo",
            "number": 1
        }))
        self.assertHTMLEqual(
            result,
            """<button class="Button Button--solid Button--yellowButtercup">
            <i>Foo</i>
            </button>"""
        )

    def test_get_element_data(self):
        request = self.factory.get("/")
        t = template.Template("""{% load mote_tags %}
            {% get_element_data "tests/fleet.xml" as fleet %}
            <fleet>
            {% for car in fleet.cars %}
                <car>
                    <brand>{{ car.brand }}</brand>
                    <model>{{ car.model }}</model>
                </car>
            {% endfor %}
            <value>{{ fleet.value }}</value>
            </fleet>"""
        )
        result = t.render(template.Context({
            "request": request,
            "cars": [
                {"brand": "Opel", "model": "Astra"},
                {"brand": "Ford", "model": "Ikon"}
            ]
        }))
        expected = """<fleet>
            <car>
                <brand>Opel</brand>
                <model>Astra</model>
            </car>
            <car>
                <brand>Ford</brand>
                <model>Ikon</model>
            </car>
            <value>100</value>
        </fleet>"""

        self.assertHTMLEqual(result, expected)
