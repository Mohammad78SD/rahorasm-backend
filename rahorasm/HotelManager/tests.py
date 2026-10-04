from django.urls import reverse
from rest_framework.test import APITestCase

from test_helpers import make_city, make_hotel


class HotelApiTests(APITestCase):
    def setUp(self):
        self.hotel = make_hotel(make_city(), "Grand Hotel")

    def test_hotel_list(self):
        resp = self.client.get(reverse("hotel_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_hotel_detail_and_404(self):
        self.assertEqual(self.client.get(reverse("hotel_details", args=[self.hotel.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("hotel_details", args=[9999])).status_code, 404)
