from distutils import dist
from email.errors import InvalidMultipartContentTransferEncodingDefect
from msilib.schema import File
from django.shortcuts import render
import json
import requests
import hashlib
import datetime
districts = []
id = ''
token = ''

# Create your views here.
def initialize(dis):
    global districts
    districts = dis
    return

def home(request):
    return render(request, 'homepage.html')

def slot(request):
    res = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states')
    res_text = eval(res.text)
    state_name = list()
    districts_list = list()
    countt = 0
    dt = datetime.datetime.now()
    dt2 = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year)
    
    for i in res_text['states']:
        state_name.append(i['state_name'])
    
    if request.method == 'GET':
        l1 = ['name', 'address', 'state_name', 'district_name', 'block_name', 'pincode']
        l2 = ['address', 'state_name', 'district_name', 'block_name', 'fee_type']
        l3 = []

        if request.GET.get('state'):
            state = request.GET['state']
            for s in state_name:
                countt += 1
                if state == s:
                    break
            if countt == 9:
                countt = 37
            elif countt >= 10:
                countt -= 1
            
            res_2 = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/'+str(countt))
            res_2_text = eval(res_2.text)
            l_districts =[]
            l_districts += res_2_text['districts']
            initialize(l_districts)
            for i in l_districts:
                districts_list.append(i['district_name'])
            
            return render(request, 'slot_check.html', {'state_name': state_name, 'state': state, 'districts': districts_list})


        if request.GET.get('district'):
            dis = request.GET['district']
            id2 = -1
            global districts
            for i in districts:
                if dis == i['district_name']:
                    id2 = i['district_id']
                    break
            res_3 = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}'.format(str(id2), dt2))
            false = False
            true = True
            res_3_text = eval(res_3.text)
            centres = res_3_text['centers']
            if centres == l3:
                return render(request, 'slot_check.html', {'state_name': state_name, 'centre': 'Na'})
            else:
                return render(request, 'slot_check.html', {'state_name': state_name, 'centre': centres, 'l1': l1, 'l2': l2})


        if request.GET.get('pin_code'):
            pin_code = request.GET['pin_code']
            res_4 = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}'.format(pin_code, dt2))
            false = False
            true = True
            res_4_text = eval(res_4.text)
            centres = res_4_text['centers']
            if centres == l3:
                return render(request, 'slot_check.html', {'state_name': state_name, 'centre': 'Na', 'l1': l1, 'l2': l2, 'l3': l3})
            else:
                return render(request, 'slot_check.html', {'state_name': state_name, 'centre': centres, 'l1': l1, 'l2': l2, 'l3': l3})
    else:
        res_4_text = ''

    return render(request, 'slot_check.html', {'state_name': state_name})

def cert(request):
    if request.method == 'POST':
        if request.POST.get('mobile'):
            mobile = request.POST['mobile']
            res = requests.post(url = "https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP", json = {"mobile": mobile})
            try:
                res_text = eval(res.text)
                global id
                id = res_text["txnId"]
            except:
                res_text = 'try again after 5 min'
            return render(request, 'down_cert.html', {'mobile': mobile})
        
        if request.POST.get('otp'):
            otp = request.POST['otp']
            otp = hashlib.sha256(otp.encode()).hexdigest()
            res_2 = requests.post(url = "https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP", json = {"otp": otp, "txnId": id})
            try:
                res_2_text = eval(res_2.text)
                global token
                token = res_2_text["token"]
                return render(request, 'down_cert.html', {'otp': otp})
            except:
                res_2_text = 'wrong otp'
                return render(request, 'down_cert.html', {'res_2_text': res_2_text, 'mobile': '0'})
        
        if request.POST.get('ben_id'):
            header = {'Authorization': 'Bearer '+token}
            ben_id = request.POST['ben_id']
            res_3 = requests.get('https://cdn-api.co-vin.in/api/v2/registration/certificate/public/download?beneficiary_reference_id='+ben_id, headers = header)
            
            i = 0
            location = "C:/Users/TARUN TEOTIA/Downloads/certificate{}.pdf"
            while 1:
                try:
                    with open(location.format(i), "xb") as file:
                        file.write(res_3.content)
                        file.close
                        break
                except:
                    i += 1
            
            rr = 'certificate downloaded successfully, if not opening, check beneficiary id and try again.'
            return render(request, 'down_cert.html', {'rr': rr})
            
    else:
        mobile = ''
        res_text = ''
        res_2_text = ''
    return render(request, 'down_cert.html')

def about(request):
    return render(request, 'about.html')