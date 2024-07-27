from django.http import JsonResponse
from django.views import View
from profiles.models import Profile, ProfilesImage, SavedCompany
from authentication.models import CustomUser
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MainApiResponse
from rest_framework.permissions import IsAuthenticated
from .serializers import MainApiResponse
from rest_framework.authtoken.models import Token
import requests



class MainPageView(View):
    def get(self, request, *args, **kwargs):
        latest_saved_companies = SavedCompany.objects.order_by('-added_at')[:6]

        clients_json = []
        for saved_company in latest_saved_companies:
            profile = saved_company.company
            image_data = ProfilesImage.objects.filter(profile_id_id=profile.id).order_by('-id').first()

            client_json = {
                'common_info': profile.common_info,
                'official_name': profile.official_name,
                'address': profile.address,
                'service_info': profile.service_info,
                'product_info': profile.product_info,
                'image_path': "/media/" + image_data.path + "/" + image_data.name  if image_data else None,
                
            }
            clients_json.append(client_json)

        partners_data = ProfilesImage.objects.order_by('id')[:6].values('name', 'path')
        partners_json = [{'name': partner['name'], 'path': "/media/" + "logo/" + partner['name']} for partner in partners_data]

        context = {
            'clients': clients_json,
            'partners': partners_json
        }

        return render(request, 'main_page/index.html', context)
        
        







class MainPageApiView(APIView):
    def get(self, request, *args, **kwargs):
        # Отримання користувача та його токену з запиту
        user = request.user
        user_token = getattr(user, 'auth_token', None)

        if user_token is None:
            # Якщо токен відсутній, можливо, ви хочете повернути відповідний відгук
            return Response({'error': 'Token not found'}, status=401)

        latest_saved_companies = SavedCompany.objects.order_by('-added_at')[:6]
        clients_data = []

        for saved_company in latest_saved_companies:
            profile = saved_company.company
            image_data = ProfilesImage.objects.filter(profile_id_id=profile.id).order_by('-id').first()

            client_data = {
                'common_info': profile.common_info,
                'official_name': profile.official_name,
                'address': profile.address,
                'service_info': profile.service_info,
                'product_info': profile.product_info,
                'image': {'name': image_data.name, 'path': image_data.path} if image_data else None,
            }
            clients_data.append(client_data)

        partners_data = ProfilesImage.objects.order_by('id')[:6].values('name', 'path')

        serializer = MainApiResponse(data={'clients': clients_data, 'partners': partners_data})
        serializer.is_valid()

        return Response(serializer.data)




