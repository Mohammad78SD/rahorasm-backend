"""Small factory helpers shared by the tests.py modules."""
from datetime import timedelta
from decimal import Decimal
import itertools

from django.contrib.auth import get_user_model
from django.utils import timezone

from HotelManager.models import Hotel, HotelPrice
from TourManager.models import City, Continent, Country, FlightTimes, Tour

_counter = itertools.count(1)


def make_user(phone="09120000001", password="pass12345", **extra):
    user = get_user_model().objects.create_user(phone_number=phone, password=password)
    for k, v in extra.items():
        setattr(user, k, v)
    if extra:
        user.save()
    return user


def make_city(name="Istanbul", country="Turkey", continent="Asia"):
    cont, _ = Continent.objects.get_or_create(name=continent)
    ctry, _ = Country.objects.get_or_create(name=country, continent=cont)
    return City.objects.get_or_create(name=name, country=ctry)[0]


def make_hotel_price(two=Decimal("100"), one=Decimal("150"), cwb=Decimal("60"),
                     cnb=Decimal("40"), baby=Decimal("10")):
    return HotelPrice.objects.create(
        two_bed_price=two, one_bed_price=one, child_with_bed_price=cwb,
        child_no_bed_price=cnb, baby_price=baby,
    )


def make_flight_times(hotel_price=None):
    now = timezone.now()
    ft = FlightTimes.objects.create(departure_date=now, arrival_date=now + timedelta(days=5))
    if hotel_price is not None:
        ft.hotel_price.add(hotel_price)
    return ft


def make_tour(title=None, flight_times=None, city=None, **extra):
    n = next(_counter)
    tour = Tour.objects.create(
        title=title or f"Tour {n}", tour_type="هوایی", needed_documents="passport",
        agency_service="service", tour_guide="guide", **extra,
    )
    if city is not None:
        tour.destinations.add(city)
    if flight_times is not None:
        tour.flight_times.add(flight_times)
        tour.save()  # refresh min/max prices
    return tour


def make_hotel(city=None, name="Grand Hotel"):
    return Hotel.objects.create(name=name, address="somewhere", description="nice",
                                city=city or make_city())
