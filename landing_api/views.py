from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime
import pytz

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing_data"

    def get(self, request):
        # Get reference to the Firebase Realtime Database collection
        ref = db.reference(self.collection_name)
        # Retrieve all items from the collection
        data = ref.get()
        # Convert to list if data exists, else return empty list
        response_data = list(data.values()) if data else []
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        # Get data from request body
        data = request.data
        # Get current time in Mexico City timezone
        mx_tz = pytz.timezone('America/Mexico_City')
        current_time = datetime.now(mx_tz)
        # Format timestamp as specified: dd/mm/yyyy, hh:mm:ss a. m./p. m.
        formatted_time = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace("am", "a. m.").replace("pm", "p. m.")
        # Add timestamp to data
        data['timestamp'] = formatted_time
        # Get reference to the Firebase Realtime Database collection
        ref = db.reference(self.collection_name)
        # Push data to Firebase
        new_item = ref.push(data)
        # Return the ID of the new item
        return Response({'id': new_item.key}, status=status.HTTP_201_CREATED)