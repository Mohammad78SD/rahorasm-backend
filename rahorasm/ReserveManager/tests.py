from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from test_helpers import make_flight_times, make_hotel_price, make_tour, make_user
from .models import Person, Reserve


def make_reserve(user, tour, hp, **q):
    data = dict(two_bed_quantity=0, one_bed_quantity=0,
                child_with_bed_quantity=0, child_no_bed_quantity=0)
    data.update(q)
    return Reserve.objects.create(user=user, tour=tour, hotel_price=hp, **data)


class ReservePricingTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.tour = make_tour()
        self.hp = make_hotel_price()  # 100 / 150 / 60 / 40

    def test_final_price_is_sum_of_components(self):
        r = make_reserve(self.user, self.tour, self.hp, two_bed_quantity=2,
                         one_bed_quantity=1, child_with_bed_quantity=1, child_no_bed_quantity=3)
        self.assertEqual(r.final_price, Decimal("100") * 2 + 150 + 60 + 40 * 3)

    def test_zero_quantities_price_zero(self):
        self.assertEqual(make_reserve(self.user, self.tour, self.hp).final_price, 0)

    def test_resaving_does_not_inflate_price(self):
        """Regression: save() used to add to final_price on every save."""
        r = make_reserve(self.user, self.tour, self.hp, two_bed_quantity=2)
        for _ in range(3):
            r.save()
        r.refresh_from_db()
        self.assertEqual(r.final_price, Decimal("200"))

    def test_changing_status_keeps_price(self):
        r = make_reserve(self.user, self.tour, self.hp, one_bed_quantity=2)
        r.status = "pending"
        r.save()
        r.refresh_from_db()
        self.assertEqual(r.final_price, Decimal("300"))

    def test_editing_quantity_recomputes_price(self):
        r = make_reserve(self.user, self.tour, self.hp, two_bed_quantity=2)
        r.two_bed_quantity = 3
        r.save()
        r.refresh_from_db()
        self.assertEqual(r.final_price, Decimal("300"))


class ReserveApiTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.hp = make_hotel_price()
        self.ft = make_flight_times(self.hp)
        self.tour = make_tour(flight_times=self.ft)
        self.payload = {
            "flight_time_id": self.ft.id,
            "hotel_price_id": self.hp.id,
            "count": [
                {"identitication": "two_bed_price", "count": 2, "users": [
                    {"name": "علی", "en_name": "Ali", "ssn": "0012345678",
                     "passportNumber": "A1234567", "birthday": "1370/01/01"},
                    {"name": "رضا", "en_name": "Reza", "ssn": "0012345679",
                     "passportNumber": "A1234568", "birthday": "1371/01/01"},
                ]},
                {"identitication": "child_no_bed_price", "count": 1, "users": []},
            ],
        }

    def test_create_requires_auth(self):
        self.assertEqual(self.client.post(reverse("create-reserve"), self.payload, format="json").status_code, 401)

    def test_create_reserve(self):
        self.client.force_authenticate(self.user)
        resp = self.client.post(reverse("create-reserve"), self.payload, format="json")
        self.assertEqual(resp.status_code, 201)
        r = Reserve.objects.get()
        self.assertEqual(r.user, self.user)
        self.assertEqual(r.tour, self.tour)
        self.assertEqual(r.final_price, Decimal("240"))
        self.assertEqual(r.status, "review")
        self.assertEqual(Person.objects.filter(reserve=r).count(), 2)

    def test_create_with_invalid_ids_is_400(self):
        self.client.force_authenticate(self.user)
        self.payload["hotel_price_id"] = 99999
        self.assertEqual(self.client.post(reverse("create-reserve"), self.payload, format="json").status_code, 400)

    def test_list_only_returns_own_reserves(self):
        other = make_user("09120000002")
        make_reserve(self.user, self.tour, self.hp, two_bed_quantity=1)
        make_reserve(other, self.tour, self.hp, two_bed_quantity=1)
        self.client.force_authenticate(self.user)
        resp = self.client.get(reverse("list-reserve"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_cannot_retrieve_other_users_reserve(self):
        other = make_user("09120000002")
        r = make_reserve(other, self.tour, self.hp, two_bed_quantity=1)
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.get(reverse("retrieve-reserve", args=[r.id])).status_code, 400)
