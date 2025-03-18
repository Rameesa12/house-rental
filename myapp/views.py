import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from myapp.models import *

# Create your views here.

def login(request):
    return render(request,"login_index.html")


def login_post(request):
    username = request.POST['username']
    password = request.POST['password']

    data = login_tb.objects.filter(username = username,password=password)
    if data.exists():
        lgdata = data[0]
        request.session['head'] = ""
        request.session['lid'] = lgdata.id
        if lgdata.usertype == 'admin':
            return HttpResponse("<script>alert('Login Success');window.location='/admin_home'</script>")
        elif lgdata.usertype == 'houseowner':
            request.session['lid'] = lgdata.id

            return HttpResponse("<script>alert('Login Success');window.location='/owner_home'</script>")
        elif lgdata.usertype == 'customer':
            request.session['lid'] = lgdata.id

            return HttpResponse("<script>alert('Login Success');window.location='/customer_home'</script>")


        else:
            return HttpResponse("<script>alert('Invalid Authentication');window.location='/'</script>")

    else:
        return HttpResponse("<script>alert('User not found');window.location='/'</script>")


def changepass(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = "Change Password"
    return render(request,"admin_module/changepass.html")


def change_password_post(request):
    newpass = request.POST['newpass']
    cpass = request.POST['cpass']
    oldpass = request.POST['oldpass']

    data = login_tb.objects.filter(id = request.session['lid'], password = oldpass)
    if data.exists():
        if newpass == cpass:
            login_tb.objects.filter(id = request.session['lid']).update(password = cpass)
            return HttpResponse("<script>alert('Password Updated');window.location='/'</script>")
        else:
            return HttpResponse("<script>alert('Password Missmatch');window.location='/changepass'</script>")
    else:
        return HttpResponse("<script>alert('Wrong password');window.location='/changepass'</script>")


def viewcustomers(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = "View Customer"
    obj=customers_tb.objects.all()
    return render(request,"admin_module/view customers.html",{"data":obj})

def viewhouseowners(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = "View House owners"
    obj=houseowners_tb.objects.filter(LOGIN__usertype = 'pending')
    return render(request,"admin_module/view house owners.html",{"data":obj})


def approve_house_owners(request,id):
    login_tb.objects.filter(id = id ).update(usertype = 'houseowner')
    return HttpResponse("<script>alert('Owner Approved');window.location='/viewhouseowners#aaa'</script>")


def reject_house_owners(request,id):
    login_tb.objects.filter(id = id ).update(usertype = 'rejected')
    return HttpResponse("<script>alert('Owner Approved');window.location='/viewhouseowners#aaa'</script>")


def viewroomsanddetails(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = "View Room Details"
    obj=housedetail_tb.objects.filter(OWNER = id)
    return render(request,"admin_module/view rooms&details.html",{"data":obj})

def view_rating(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = "View Rating"
    obj=rating_tb.objects.filter(HOUSE_DETAILS=id)
    return render(request,"admin_module/view_rating.html",{"data":obj})

def approved_owners(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = "View Approved House Owners"
    obj=houseowners_tb.objects.filter(LOGIN__usertype='houseowner')
    return render(request,"admin_module/approved_owners.html",{"data":obj})

def admin_home(request):
    return render(request,"admin_module/admin_index.html")

def logout(request):
    request.session['lg'] = ""
    del request.session['lid']
    return HttpResponse("<script>alert('Logout Success');window.location='/'</script>")

########################################## owner#####################################################

def houseowner_register(request):
    return render(request,"owner/Register.html")

def houseowner_register_post(request):
    name = request.POST['name']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    email = request.POST['email']
    contact = request.POST['contact']

    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    proof = request.FILES['proof']
    d = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    fs = FileSystemStorage()
    fs.save(r"C:\Users\ramee\PycharmProjects\homerentalapp\myapp\static\proof\\" + d + ".pdf", proof)
    path = "/static/proof/" + d + ".pdf"
    data = login_tb.objects.filter(username=email)
    if data.exists():
        return HttpResponse("<script>alert('Email already Taken');window.location='/'</script>")
    elif password == confirm_password:


        obj = login_tb()
        obj.username = email
        obj.password = password
        obj.usertype = 'pending'
        obj.save()

        obj1 = houseowners_tb()
        obj1.name = name
        obj1.place = place
        obj1.pin = pin
        obj1.post = post
        obj1.email = email
        obj1.phone = contact
        obj1.proof = path
        obj1.LOGIN = obj
        obj1.save()
        return HttpResponse("<script>alert('Registration success');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('Password mismatch');window.location='/'</script>")


def owner_home(request):
    return render(request,'owner/owner_index.html')

def view_profile(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'Profile'
    data = houseowners_tb.objects.get(LOGIN=request.session['lid'])
    return render(request,'owner/view_profile.html',{'data':data})


def add_house(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'Enter House details'

    return render(request,'owner/add_house.html')

def add_house_post(request):
    rent1 = request.POST['textfield']
    picture1 = request.FILES['textfield2']
    picture2 = request.FILES['pic2']
    picture3 = request.FILES['pic3']
    print("pic1",picture1)
    print("pic2",picture2)
    print("pic3",picture3)
    information1 = request.POST['textfield4']
    type1 = request.POST['textfield3']
    latitude1 = request.POST['latitude']
    longitude1 = request.POST['longitude']

    d = datetime.datetime.now().strftime('%Y%m%d--%H%M%S')
    d1 = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    d2 = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    fs = FileSystemStorage()
    fs.save(r"C:\Users\ramee\PycharmProjects\homerentalapp\myapp\static\\" + d + ".jpg", picture1)
    path = "/static/" + d + ".jpg"
    fs.save(r"C:\Users\ramee\PycharmProjects\homerentalapp\myapp\static\\" + d1 + ".jpg", picture2)
    path2 = "/static/" + d1 + ".jpg"
    fs.save(r"C:\Users\ramee\PycharmProjects\homerentalapp\myapp\static\\" + d2 + ".jpg", picture3)
    path3 = "/static/" + d2 + ".jpg"

    obj = housedetail_tb()
    obj.rent = rent1
    obj.OWNER_id = houseowners_tb.objects.get(LOGIN=request.session['lid']).id
    obj.image1 = path
    obj.image2 = path2
    obj.image3 = path3
    obj.information = information1
    obj.latitude = latitude1
    obj.longitude = longitude1
    obj.type = type1
    obj.save()

    return HttpResponse("<script>alert('added successfull');window.location = '/view_house#owner'</script>")

def view_house(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'view details'
    data = housedetail_tb.objects.filter(OWNER__LOGIN=request.session['lid'])
    return render(request,'owner/view_room.html',{'data':data})

def update_house(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'Update house'
    data = housedetail_tb.objects.get(id = id)

    return render(request,'owner/update_house.html',{'data':data})

def update_house_post(request,id):
    rent1 = request.POST['textfield']
    information1 = request.POST['textfield4']
    type1 = request.POST['textfield3']
    try:

        picture1 = request.FILES['textfield2']
        picture2 = request.FILES['pic2']
        picture3 = request.FILES['pic3']

        d = datetime.datetime.now().strftime('%Y%m%d--%H%M%S')
        d1 = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        d2 = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        fs = FileSystemStorage()
        fs.save(r"C:\Users\abhij\PycharmProjects\homerentalapp\myapp\static\\" + d + ".jpg", picture1)
        path1 = "/static/" + d + ".jpg"
        fs.save(r"C:\Users\abhij\PycharmProjects\homerentalapp\myapp\static\\" + d1 + ".jpg", picture2)
        path2 = "/static/" + d + ".jpg"
        fs.save(r"C:\Users\abhij\PycharmProjects\homerentalapp\myapp\static\\" + d2 + ".jpg", picture3)
        path3 = "/static/" + d + ".jpg"

        housedetail_tb.objects.filter(id=id).update(rent=rent1, image1=path1,image2=path2,image3=path3, information=information1, type=type1)
        return HttpResponse("<script>alert('updated successfull');window.location = '/view_house#owner'</script>")


    except Exception as e:

        housedetail_tb.objects.filter(id=id).update(rent=rent1, information=information1, type=type1)
        return HttpResponse("<script>alert('updated successfull');window.location = '/view_house#owner'</script>")



def delete_house(request,id):
    housedetail_tb.objects.get(id=id).delete()
    return HttpResponse("<script>alert('deleted successfull');window.location = '/view_house#owner'</script>")


def view_request(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'Requests'
    data = booking_tb.objects.filter(ROOM__OWNER__LOGIN = request.session['lid'])
    return render(request,'owner/view_request.html',{'data':data})

def approve_request(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    booking_tb.objects.filter(id=id).update(status = "approved")
    return HttpResponse("<script>alert('approved successfull');window.location = '/view_request#owner'</script>")

def reject_request(request,id):

    booking_tb.objects.filter(id=id).update(status = "rejected")
    return HttpResponse("<script>alert('rejected successfull');window.location = '/view_request#owner'</script>")


def view_payment(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'Payment details'
    data = booking_tb.objects.filter(ROOM__OWNER__LOGIN = request.session['lid'])
    return render(request,'owner/view_payment_status.html',{'data':data})


def oview_rating(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'Ratings'
    data = rating_tb.objects.filter(HOUSE_DETAILS__OWNER__LOGIN = request.session['lid'] )

    return render(request,'owner/view_rating.html',{'data':data})


def owner_chatt(request,u):
    request.session['head']="CHAT"
    request.session['uid'] = u
    print('uid',request.session['uid'])
    return render(request,'owner/owner_chat.html',{'u':u})


def owner_chatsnd(request,u):
        d=datetime.datetime.now().strftime("%Y-%m-%d")
        # t=datetime.datetime.now().strftime("%H:%M:%S")
        c = request.session['lid']
        b=request.POST['n']
        print(b)
        print(u,"userrrrrrrrrr")
        m=request.POST['m']
        cc = houseowners_tb.objects.get(LOGIN__id=c).id
        print("customer",cc)

        uu = customers_tb.objects.get(id=request.session['uid']).id
        print("owner",uu)
        obj=chat_tb()
        obj.chat = m
        obj.date=d
        obj.type='owner'
        obj.OWNER_id= cc
        obj.CUSTOMER_id= uu
        obj.save()
        print(obj)
        v = {}
        if int(obj) > 0:
            v["status"] = "ok"
        else:
            v["status"] = "error"
        r = JsonResponse.encode(v)
        return r
    # else:
    #     return redirect('/')





def owner_chatrply(request,u):
    # if request.session['log']=="lo":
        c = request.session['lid']
        cuid = u
        cc=houseowners_tb.objects.get(LOGIN__id=c).id
        uu=customers_tb.objects.get(id=cuid).id
        print("user",uu)
        res = chat_tb.objects.filter(CUSTOMER_id=uu,OWNER_id=cc)
        print(res)
        v = []
        if len(res) > 0:
            print(len(res))
            for i in res:
                v.append({
                    'type':i.type,
                    'chat':i.chat,
                    'name':i.CUSTOMER.name,
                    # 'upic':i.USER.photo,
                    'dtime':i.date,
                    'tname':i.OWNER.name,
                })
            print(v)
            return JsonResponse({"status": "ok", "data": v, "id": cc})
        else:
            return JsonResponse({"status": "error"})








############################################customer###########################################################


def customer_home(request):
    return render(request,'customer/customer_index.html')

def customer_register(request):
    return render(request, "customer/Register.html")


def customer_register_post(request):
    name = request.POST['name']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    age = request.POST['age']
    email = request.POST['email']
    contact = request.POST['contact']
    latitude1 = request.POST['latitude']
    longitude1 = request.POST['longitude']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    proof = request.FILES['proof']
    image = request.FILES['image']
    d = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    fs = FileSystemStorage()
    fs.save(r"C:\Users\ramee\PycharmProjects\homerentalapp\myapp\static\proof\\" + d + ".pdf", proof)
    fs.save(r"C:\Users\ramee\PycharmProjects\homerentalapp\myapp\static\image\\" + d + ".jpg", image)
    path = "/static/proof/" + d + ".pdf"
    path1 = "/static/image/" + d + ".jpg"
    data = login_tb.objects.filter(username=email)
    if data.exists():
        return HttpResponse("<script>alert('Email already Taken');window.location='/'</script>")
    elif password == confirm_password:

        obj = login_tb()
        obj.username = email
        obj.password = password
        obj.usertype = 'customer'
        obj.save()

        obj1 = customers_tb()
        obj1.name = name
        obj1.place = place
        obj1.pin = pin
        obj1.post = post
        obj1.email = email
        obj1.latitude = latitude1
        obj1.longitude = longitude1
        obj1.phone = contact
        obj1.proof = path
        obj1.image = path1
        obj1.age = age
        obj1.LOGIN = obj
        obj1.save()
        return HttpResponse("<script>alert('Registration success');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('Password mismatch');window.location='/'</script>")




def customer_view_profile(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'Profile'
    data = customers_tb.objects.get(LOGIN=request.session['lid'])
    return render(request,'customer/customer_view_profile.html',{'data':data})


def customer_view_house(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'view Houses'


    data = housedetail_tb.objects.all()
    return render(request,'customer/customer_view_house.html',{'data':data})

def customer_book_house(request,id):
    obj = booking_tb()
    obj.date = datetime.datetime.now()
    obj.CUSTOMER_id = customers_tb.objects.get(LOGIN=request.session['lid']).id
    obj.status = 'pending'
    obj.ROOM_id = id
    obj.payment_status = 'pending'
    obj.payment_date = 'pending'
    obj.payment_mode = 'pending'
    obj.amount = housedetail_tb.objects.get(id = id).rent
    obj.save()
    return  HttpResponse("<script>alert('booking send successfully');window.location='/customer_view_house#customer'</script>")

def user_payment(request,id,amt):
    import razorpay
    import datetime
    from django.shortcuts import render
    from django.http import HttpResponse
    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    # Initialize Razorpay client
    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    # Convert amount to paise (INR)
    amount = int(amt) * 100  # Razorpay expects amount in paise

    # Create Razorpay order
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': 1,  # Auto-capture payment
    }


    # Create the order
    order = razorpay_client.order.create(data=order_data)

    # Prepare context to pass to frontend
    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }

    # Update booking status
    booking_tb.objects.filter(id=id).update(
        payment_status='paid',
        payment_date=datetime.datetime.now(),
        payment_mode='online'
    )

    return render(request, 'customer/payment.html', context)




def customer_view_request(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head'] = 'BOOKING'
    data = booking_tb.objects.filter(CUSTOMER__LOGIN = request.session['lid'] )
    return render(request,'customer/view_booking_status.html',{'data':data})

def customer_sen_rating(request,hid):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")

    return render(request,'customer/customer_send_rating.html',{'hid':hid})

def customer_send_rating_post(request,hid):
    rating1 = request.POST['star']

    data = rating_tb.objects.filter(HOUSE_DETAILS = hid,CUSTOMER__LOGIN = request.session['lid'])
    if data.exists():
        return HttpResponse( "<script>alert('rating already sended');window.location='/customer_view_request'</script>")


    else:
        obj = rating_tb()
        obj.rating = rating1
        obj.date = datetime.datetime.now()
        obj.CUSTOMER_id = customers_tb.objects.get(LOGIN=request.session['lid']).id
        obj.HOUSE_DETAILS_id = hid
        obj.save()
        return HttpResponse( "<script>alert('rating send successfully');window.location='/customer_view_request#customer'</script>")




def customer_chatt(request,u):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired..Login Again');window.location='/'</script>")
    request.session['head']="CHAT"
    request.session['uid'] = u
    print('oid',request.session['uid'])
    return render(request,'customer/customer_chat.html',{'u':u})


def customer_chatsnd(request,u):
        d=datetime.datetime.now().strftime("%Y-%m-%d")
        # t=datetime.datetime.now().strftime("%H:%M:%S")
        c = request.session['lid']
        b=request.POST['n']
        print(b)
        print(u,"userrrrrrrrrr")
        m=request.POST['m']
        cc = customers_tb.objects.get(LOGIN__id=c).id
        print("customer",cc)

        uu = houseowners_tb.objects.get(id=request.session['uid']).id
        print("owner",uu)
        obj=chat_tb()
        obj.chat = m
        obj.date=d
        obj.type='customer'
        obj.OWNER_id= uu
        obj.CUSTOMER_id= cc
        obj.save()
        print(obj)
        v = {}
        if int(obj) > 0:
            v["status"] = "ok"
        else:
            v["status"] = "error"
        r = JsonResponse.encode(v)
        return r
    # else:
    #     return redirect('/')





def customer_chatrply(request):
    # if request.session['log']=="lo":
        c = request.session['lid']
        cc=customers_tb.objects.get(LOGIN__id=c).id
        uu=houseowners_tb.objects.get(id=request.session['uid']).id
        res = chat_tb.objects.filter(CUSTOMER_id=cc,OWNER_id=uu)
        print(res)
        v = []
        if len(res) > 0:
            print(len(res))
            for i in res:
                v.append({
                    'type':i.type,
                    'chat':i.chat,
                    'name':i.OWNER.name,
                    # 'upic':i.USER.photo,
                    'dtime':i.date,
                    'tname':i.CUSTOMER.name,
                })
            print(v)
            return JsonResponse({"status": "ok","data": v,"id": cc})
        else:
            return JsonResponse({"status": "error"})

