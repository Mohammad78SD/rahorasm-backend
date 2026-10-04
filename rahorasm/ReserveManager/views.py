from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reserve, Person
from django.db import transaction
from .serializers import ReserveSerializer, CreateReserveSerializer
from rest_framework.permissions import IsAuthenticated

PRICE_FIELDS = ("two_bed_price", "one_bed_price", "child_with_bed_price", "child_no_bed_price")

# login required view

class ListReserveView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        reserves = Reserve.objects.filter(user=user)
        return Response(ReserveSerializer(reserves, many=True).data, status=status.HTTP_200_OK)
    
class RetrieveReserveView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        try:
            reserve = Reserve.objects.get(id=pk, user=user)
            return Response(ReserveSerializer(reserve).data, status=status.HTTP_200_OK)
        except Reserve.DoesNotExist:
            return Response({"error": "Invalid reserve id"}, status=status.HTTP_404_NOT_FOUND)

class CreateReserveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateReserveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        hotel_price = data["hotel_price"]

        quantities = {key: 0 for key in PRICE_FIELDS}
        persons = []
        for entry in data["count"]:
            quantities[entry["identitication"]] += entry["count"]
            for u in entry.get("users", []):
                persons.append({
                    "persian_name": u["name"],
                    "english_name": u["en_name"],
                    "national_code": u["ssn"],
                    "passport_number": u["passportNumber"],
                    "birth_date": u["birthday"],
                })

        with transaction.atomic():
            # Reserve.save() computes final_price from the quantities.
            reserve = Reserve.objects.create(
                user=request.user,
                tour=data["tour"],
                hotel_price=hotel_price,
                two_bed_quantity=quantities["two_bed_price"],
                one_bed_quantity=quantities["one_bed_price"],
                child_with_bed_quantity=quantities["child_with_bed_price"],
                child_no_bed_quantity=quantities["child_no_bed_price"],
                status='review',
            )
            Person.objects.bulk_create([Person(reserve=reserve, **p) for p in persons])

        return Response(status=status.HTTP_201_CREATED)
