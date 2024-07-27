from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from authentication.models import *
from profiles.models import *
from django.core.paginator import Paginator
from django.db.models import Q


def logon_admin(request):
    messages = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                role_select = 'info'
                return redirect(f'{role_select}')
            else:
                messages = 'User or password incorect'
    else:
        form = LoginForm()
      
    content = {
        'form': form,
        'messages': messages,
    }
    
    return render(request, 'admin.html', content)

@login_required
def info(request):
    search_text = request.GET.get('search_text', '')
    items_per_page = 10
    users = CustomUser.objects.filter(
        Q(name__icontains=search_text) | Q(email__icontains=search_text)
        ).order_by('name')
    paginator_users = Paginator(users, items_per_page)
    
    companys = Profile.objects.filter(
        Q(name__icontains=search_text) | Q(common_info__icontains=search_text)
        ).order_by('name')
    paginator_companys = Paginator(companys, items_per_page)

    user_page = request.GET.get('page_user', 1)
    company_page = request.GET.get('page_company', 1)

    current_user_page = paginator_users.get_page(user_page)
    current_company_page = paginator_companys.get_page(company_page)

    content = {
        'users': current_user_page,
        'companys': current_company_page,
    }
    return render(request, 'admin_info.html', content)

@login_required
def approve_company(request):
    search_text = request.GET.get('search_text', '')
    items_per_page = 10
    saved_companies = SavedCompany.objects.filter(
        Q(company__official_name__icontains=search_text) |  Q(user__name__icontains=search_text)
    ).order_by('company__name')
    approved_info_list = []
    not_approved_info_list = []
    for user_company in saved_companies:
        digits_in_edrpou = len(str(user_company.company.edrpou))
        if digits_in_edrpou  == 8:
            flag_approve = 'EDRPOU'
        elif digits_in_edrpou  == 10:
            flag_approve = 'IPN'
        else:
            flag_approve = f'Incorrect - {digits_in_edrpou} digits'      
            
        full_company_info = {
            'email': user_company.user.email,
            'name_company_owner': user_company.user.name,
            'edrpou': user_company.company.edrpou,
            'company_name': user_company.company.official_name,
            'is_active ': user_company.company.is_registered,
            'is_deleted': user_company.company.is_deleted,
            'id': user_company.company.id,
            'flag_approve': flag_approve,
        }

        if not user_company.company.is_registered:
            not_approved_info_list.append(full_company_info)
        elif user_company.company.is_registered:
            approved_info_list.append(full_company_info) 

    paginator_not_approved = Paginator(not_approved_info_list, items_per_page)
    company_page_not_approved = request.GET.get('page_not_approve', 1)
    
    paginator_not_approved_page = paginator_not_approved.get_page(company_page_not_approved) 

    paginator_approved = Paginator(approved_info_list, items_per_page)
    company_page_approved = request.GET.get('page_company', 1)
    paginator_approved_page = paginator_approved.get_page(company_page_approved)         

    content = {
        'approved_info_list': paginator_approved_page,
        'not_approved_info_list': paginator_not_approved_page,
    }
    return render(request, 'admin_approve_company.html', content)


@login_required
def erdpou_aproved(request, id):
    erdpou_aproved_object = SavedCompany.objects.get(company_id=id)
    edrpou_length = len(str(erdpou_aproved_object.company.edrpou))

    if edrpou_length == 8 or edrpou_length == 10:
        erdpou_aproved_object.company.is_registered = True
        erdpou_aproved_object.company.save()
    
    return redirect('approve_company')

        
@login_required
def company_unregistered(request, id):
    company_unregistered_object = SavedCompany.objects.get(company_id = id)
    company_unregistered_object.company.is_registered = False 
    company_unregistered_object.company.save() 
    
    return  redirect('approve_company')

@login_required
def admin_full_company_info(request, id):
    user_company = SavedCompany.objects.get(company_id=id)

    media_list = ProfilesImage.objects.filter(profile_id_id=id).values('name', 'path')
    logo_img = []
    image_img = []
    for it in media_list:
        if it['path'] == 'logo':
            logo_img.append('/media/' + it['path'] + '/' + it['name'])
        else:    
            image_img.append('/media/' + it['path'] + '/' + it['name'])

    region_ids = ProfilesProfileRegion.objects.filter(profile_id=id).values_list('region', flat=True).distinct()
    all_region = list(ProfilesRegion.objects.filter(id__in=region_ids).values_list('name_ua', flat=True).distinct())

    full_company_info = {
        'email': user_company.user.email,
        'name_company_owner': user_company.user.name,
        'edrpou': user_company.company.edrpou,
        'company_name': user_company.company.official_name,
        'is_active ': user_company.company.is_registered,
        'is_deleted': user_company.company.is_deleted,
        'id': user_company.company.id,
        'phone': user_company.company.phone,
    }

    content = {
        'media_list': image_img,
        'media_logo': logo_img,
        'region_list': all_region,
        'full_company_info': full_company_info,
    }

    return render(request, 'admin_full_company_info.html', content)
