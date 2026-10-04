from decimal import Decimal
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from test_helpers import make_city, make_flight_times, make_hotel_price, make_tour
from .models import Tour


class TourModelTests(TestCase):
    def test_least_and_max_price_follow_hotel_prices(self):
        ft = make_flight_times(make_hotel_price(two=Decimal("500")))
        ft.hotel_price.add(make_hotel_price(two=Decimal("900")))
        tour = make_tour(flight_times=ft)
        tour.refresh_from_db()
        self.assertEqual(tour.least_price, Decimal("500"))
        self.assertEqual(tour.max_price, Decimal("900"))

    def test_prices_zero_without_hotel_prices(self):
        tour = make_tour()
        tour.refresh_from_db()
        self.assertEqual((tour.least_price, tour.max_price), (0, 0))

    def test_flight_times_has_no_null_option(self):
        self.assertFalse(Tour._meta.get_field("flight_times").null)


class TourApiTests(APITestCase):
    def setUp(self):
        self.city = make_city()
        self.ft = make_flight_times(make_hotel_price())
        self.tour = make_tour(title="Istanbul Tour", flight_times=self.ft, city=self.city)
        self.other = make_tour(title="Other Tour", city=make_city("Paris", "France", "Europe"))

    def test_list_tours(self):
        resp = self.client.get(reverse("tour_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual({t["title"] for t in resp.json()}, {"Istanbul Tour", "Other Tour"})

    def test_list_filter_by_city(self):
        resp = self.client.get(reverse("tour_list"), {"city": "Istanbul"})
        self.assertEqual([t["title"] for t in resp.json()], ["Istanbul Tour"])

    def test_tour_detail(self):
        resp = self.client.get(reverse("tour_detail", args=[self.tour.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["title"], "Istanbul Tour")

    def test_tour_detail_404(self):
        self.assertEqual(self.client.get(reverse("tour_detail", args=[99999])).status_code, 404)

    def test_tour_flights(self):
        resp = self.client.get(reverse("tour_flights", args=[self.tour.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_reference_lists(self):
        for name in ("city_list", "country_list", "airline_list", "airport_list"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)


class TourPDFTests(TestCase):
    def test_unknown_tour_is_404(self):
        """Regression: unknown id used to raise Tour.DoesNotExist -> 500."""
        self.assertEqual(self.client.get(reverse("tour_pdf", args=[99999])).status_code, 404)

    def test_existing_tour_renders(self):
        tour = make_tour(title="PDF Tour")
        resp = self.client.get(reverse("tour_pdf", args=[tour.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("PDF Tour", resp.content.decode())
