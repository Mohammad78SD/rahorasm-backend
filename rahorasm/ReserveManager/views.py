from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reserve, Person
from .serializers import ReserveSerializer
from HotelManager.models import Hotel, HotelPrice
from TourManager.models import Tour, Flight

class CreateReserveView(APIView):
    def post(self, request):
        data = request.data
        
        # Get required fields from the data
        user = request.user
        tour_id = data.get("tourId")
        hotel_id = data.get("hotelId")
        room_id = data.get("roomId")
        counts = data.get("counts", [])
        
        # Validate required foreign keys
        try:
            tour = Tour.objects.get(id=tour_id)
            hotel = Hotel.objects.get(id=hotel_id)
            hotel_price = HotelPrice.objects.get(id=room_id)
        except (Tour.DoesNotExist, Hotel.DoesNotExist, HotelPrice.DoesNotExist):
            return Response({"error": "Invalid tour, hotel, or room id"}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize room quantities
        two_bed_quantity = 0
        one_bed_quantity = 0
        child_with_bed_quantity = 0
        child_no_bed_quantity = 0
        final_price = 0

        # Calculate quantities and final price
        persons_data = []
        for count in counts:
            quantity = count["count"]
            price = float(count["price"])
            identification = count["identitication"]
            
            if identification == "two_bed_price":
                two_bed_quantity += quantity
                final_price += quantity * hotel_price.two_bed_price
            elif identification == "one_bed_price":
                one_bed_quantity += quantity
                final_price += quantity * hotel_price.one_bed_price
            elif identification == "child_with_bed_price":
                child_with_bed_quantity += quantity
                final_price += quantity * hotel_price.child_with_bed_price
            elif identification == "child_no_bed_price":
                child_no_bed_quantity += quantity
                final_price += quantity * hotel_price.child_no_bed_price

            # Collect person data
            for user_data in count.get("users", []):
                persons_data.append({
                    "persian_name": user_data.get("name"),
                    "english_name": user_data.get("en_name"),
                    "national_code": user_data.get("ssn"),
                    "passport_number": user_data.get("passportNumber"),
                    "birth_date": user_data.get("birthday")
                })

        # Create the reserve instance
        reserve = Reserve.objects.create(
            user=user,
            hotel=hotel,
            tour=tour,
            flight=Flight.objects.get(id=tour_id),  # Assuming you get flight by tour id
            hotel_price=hotel_price,
            two_bed_quantity=two_bed_quantity,
            one_bed_quantity=one_bed_quantity,
            child_with_bed_quantity=child_with_bed_quantity,
            child_no_bed_quantity=child_no_bed_quantity,
            final_price=final_price,
            status='review'
        )

        # Create Person instances for each user
        persons = [Person(reserve=reserve, **person_data) for person_data in persons_data]
        Person.objects.bulk_create(persons)

        return Response(ReserveSerializer(reserve).data, status=status.HTTP_201_CREATED)
