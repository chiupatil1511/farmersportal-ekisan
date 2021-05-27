# keyid = 'rzp_test_ssmxVx39H1TlGF'
# keySecret = 'Gtc2eutjvAiD3P0MSE51KkJ1'
import html

from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
import pyrebase
import random
import string
import json
import urllib.request
import razorpay


from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

firebaseConfig = {
    "apiKey": "AIzaSyAb5dlN-CI5I4EkrFWGcVwVPVFtTSFZJgI",
    "authDomain": "e-kisan-63742.firebaseapp.com",
    "databaseURL": "https://e-kisan-63742-default-rtdb.firebaseio.com",
    "projectId": "e-kisan-63742",
    "storageBucket": "e-kisan-63742.appspot.com",
    "messagingSenderId": "792762251327",
    "appId": "1:792762251327:web:6911df1055b25830a7a08a",
    "measurementId": "G-DYR3G4T6VG"
  }
firebase1 = pyrebase.initialize_app(firebaseConfig)
authe = firebase1.auth()
database = firebase1.database()

def about(request):
    return render(request,'About-us.html')


def index(request):
    return render(request, 'index.html')


def index(request):
    return render(request, 'index.html')


def logout(request):
    try:
        auth.logout(request)
        authe.current_user = None
        return render(request, "buying.html")
        # return render(request, "index.html")
    except:
        return render(request, "crop.html")


def Csignup(request):
    lettersU = string.ascii_uppercase
    lettersD = string.digits
    id = (''.join(random.choice(lettersD) for i in range(3)) + ''.join(random.choice(lettersU) for i in range(1)))
    id1 = 'EK'+id
    name = request.POST.get('name')
    email = request.POST.get('email')
    contactno = request.POST.get('contact')
    address = request.POST.get('address')
    city = request.POST.get('city')
    pin = request.POST.get('pin')
    passw = request.POST.get('pass')

    try:
        user = authe.create_user_with_email_and_password(email, passw)
        mess = 'user created successfully'

        Uid = user['localId']
        data = {
            'Name': name,
            'Email': email,
            'Mobile_No': contactno,
            'Address': address,
            'City': city,
            'Pin code': pin,
            'Cid': id1,
            'Password': passw,
        }
        database.child('Consumer').child('Details').child(Uid).set(data)
        return render(request, "index.html")
    except:
        mess = 'Failed to create Account!!'

        return render(request, "index.html")

def Clogin(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, password)

        id = database.child('Added_Items').shallow().get().val()
        lis_id = []
        for i in id:
            lis_id.append(i)


        details = {}
        farm = {}
        city = {}
        # for farmid in farm:
        #     c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()
        #     city.append(c)
        # p = 0
        for i in lis_id:
            det = database.child('Added_Items').child(i).get().val()
            farmid = database.child('Added_Items').child(i).child('farmid').get().val()
            c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()

            diction = dict(det)

            details[i] = diction
            city[i] = c

        details2 = {
            'det': details,
            'uid': lis_id,
            'city': city,
        }

        # session_id = user['localId']
        # request.session['uid'] = str(session_id)
        return render(request,'buying.html', details2)
    except:
        message = "invalid credentials"
        return render(request, "index.html", {'mess': message})



def farmsignUp(request):
    lettersU = string.ascii_uppercase
    lettersD = string.digits
    id = (''.join(random.choice(lettersD) for i in range(3)) + ''.join(random.choice(lettersU) for i in range(1)))
    id1 = 'EK'+id
    name = request.POST.get('name')
    email = request.POST.get('email')
    adhar = request.POST.get('adhar')
    address = request.POST.get('address')
    city = request.POST.get('city')
    contact = request.POST.get('contact')
    pin = request.POST.get('pin')
    passw = request.POST.get('pass')
    passek = str('ek'+passw)
    try:
        user = authe.create_user_with_email_and_password(email, passek)
        mess = 'user created successfully'

        Uid = user['localId']
        data = {
            'Name': name,
            'Email': email,
            'Mobile_No': contact,
            'Adhar_No': adhar,
            'Address': address,
            'Pin code': pin,
            'Fid': id1,
            'Password': passw,
            'City': city,
        }
        database.child('Farmer').child('Details').child(Uid).set(data)
        return render(request, 'index.html', {'mess': mess})
    except:
        mess = 'Failed to create Account!!'

        return render(request, "index.html", {'mess': mess})

def fsignin(request):

    email = request.POST.get('email')
    PW = request.POST.get('pass')
    # print(type(PW))
    PWek = str('ek'+PW)

    methodpost = request.POST.get('mainlogin')
    methodpost1 = request.POST.get('innerlogin')

    if methodpost1:

        try:
            user = authe.sign_in_with_email_and_password(email, PWek)
            curuser = authe.current_user

            farmid = curuser['localId']
            # session_id = user['localId']
            # request.session['uid'] = str(session_id)

            try:
                proid = database.child('Added_Items').shallow().get().val()
                products = []
                for i in proid:
                    products.append(i)


                details = {}
                p = 0
                for i in products:
                    det = database.child('Added_Items').child(i).get().val()
                    if det['farmid'] == farmid:
                        diction = dict(det)

                        details[p] = diction
                        p += 1

                details2 = {
                    'det': details
                }

                return render(request, "AddItem1.html", details2)
            except:
                return render(request, "AddItem1.html")
        except:
            mes = "Invalid Credentials"

            return render(request, "index.html", {'mess': mes})

    elif methodpost:

        try:
            user = authe.sign_in_with_email_and_password(email, PWek)

            curuser = authe.current_user
            farmid = curuser['localId']
            # session_id = user['localId']
            # request.session['uid'] = str(session_id)
            mes = "You are Loged in"
            return render(request, "index.html", {'mess': mes})
        except:
            mes = "Invalid Credentials"

            return render(request, "index.html", {'mess': mes})


def additem(request):
    lettersD = string.digits
    oid = (''.join(random.choice(lettersD) for i in range(3)))
    curuser = authe.current_user
    vname = request.POST.get('Item Name')
    vprice = request.POST.get('price')
    vquant = request.POST.get('Quantity')
    # img = request.POST.get('filename')
    url = request.POST.get('url')
    # print(url)
    farmid = curuser['localId']
    proid = vname[0: 3] + oid
    c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()
    fn = database.child('Farmer').child('Details').child(farmid).child('Name').get().val()

    productdata = {
        'Product_name': vname,
        'Price': vprice,
        'Quantity': vquant,
        'farmid': farmid,
        'url': url,
        'city': c,
        'fname': fn
    }
    database.child('Added_Items').child(proid).set(productdata)

    curuser = authe.current_user
    farmid = curuser['localId']
    proid = database.child('Added_Items').shallow().get().val()
    products = []
    for i in proid:
        products.append(i)


    details = {}
    p = 0
    for i in products:
        det = database.child('Added_Items').child(i).get().val()
        if det['farmid'] == farmid:
            diction = dict(det)

            details[p] = diction
            p += 1

    # clearf= ""
    # ItemName = request.POST.set('clearf')
    details2 = {
        'det': details
    }

    return render(request, "AddItem1.html", details2)


def selling(request):
    curuser = authe.current_user
    if curuser:
        farmid = curuser['localId']
        try:
            proid = database.child('Added_Items').shallow().get().val()
            products = []
            for i in proid:
                products.append(i)


            details = {}
            p = 0
            for i in products:
                det = database.child('Added_Items').child(i).get().val()

                if det['farmid'] == farmid:
                    diction = dict(det)

                    details[p] = diction
                    p += 1

            details2 = {
                'det': details
            }

            return render(request, "AddItem1.html", details2)
        except:
            return render(request, "AddItem1.html")
        # return render(request, 'AddItem1.html')
    else:
        return render(request, 'farmlogin.html')


def buying(request):

    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

    # print('uidlist:', lis_id)
    details = {}
    farm={}
    city = {}
    # for farmid in farm:
    #     c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()
    #     city.append(c)
    # p = 0
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        farmid = database.child('Added_Items').child(i).child('farmid').get().val()
        c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()

        diction = dict(det)
        # farmdict = dict(farmid)

        details[i] = diction
        city[i] = c

    details2 = {
        'det': details,
        'uid': lis_id,
        'city': city,
    }
    # print('details2:', details2)
    return render(request, 'buying.html', details2)


def apples(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)


    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Apple'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }

    return render(request, 'buying.html', details2)


def bellpeper(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)


    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Bell peper'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }

    return render(request, 'buying.html', details2)


def carrot(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Carrot'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }

    return render(request, 'buying.html', details2)


def cauliflower(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)


    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Cauliflower'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }

    return render(request, 'buying.html', details2)


def cucumber(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)


    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Cucumber'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }

    return render(request, 'buying.html', details2)


def peas(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)


    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Peas'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }

    return render(request, 'buying.html', details2)


def potato(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)


    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Potato'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }

    return render(request, 'buying.html', details2)


def tomato(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)


    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Tomato'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }

    return render(request, 'buying.html', details2)


def rice(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)


    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Rice'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }
    return render(request, 'buying.html', details2)


def wheat(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)


    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Wheat'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }

    return render(request, 'buying.html', details2)

def mainpro(request):
    uid = request.GET.get('z')

    proname = database.child('Added_Items').child(uid).child('Product_name').get().val()
    amount = database.child('Added_Items').child(uid).child('Price').get().val()
    quantity = database.child('Added_Items').child(uid).child('Quantity').get().val()
    url = database.child('Added_Items').child(uid).child('url').get().val()
    fname = database.child('Added_Items').child(uid).child('fname').get().val()

    return render(request,'product.html',{ 'proname': proname,'amount': amount,'quantity': quantity, 'url': url, 'fname': fname, 'uid':uid})

def addtocart(request):

    curuser = authe.current_user
    if curuser:
        cid = curuser['localId']
        uid = request.GET.get('z')
        reqquant = request.POST.get('req')

        proname = database.child('Added_Items').child(uid).child('Product_name').get().val()
        amount = database.child('Added_Items').child(uid).child('Price').get().val()
        quantity = database.child('Added_Items').child(uid).child('Quantity').get().val()
        url = database.child('Added_Items').child(uid).child('url').get().val()
        fname = database.child('Added_Items').child(uid).child('fname').get().val()

        vale = database.child('Cart').child(cid).get().val()

        if vale:
            count = 1
        else:
            count = 0
        productdata = {
            'Productname': proname,
            'Price': amount,
            'Requiredquantity':  reqquant,
            'url': url,
            'fname': fname,
            'totalprice':int(amount) * int(reqquant),

        }
        database.child('Cart').child(cid).child(uid).set(productdata)

        return render(request, 'product.html',{'proname': proname, 'amount': amount,  'quantity': quantity,
                                               'url': url, 'fname': fname,'uid': uid,'count':count})
    else:
        mess = "You need to login"

        return render(request,'consumerlogin.html',{'mess':mess})


def displaycart(request):
    curuser = authe.current_user

    if curuser:
        cid = curuser['localId']

        try:

            # uid = request.GET.get('z')
            # if request == "POST":
            #     database.child('Cart').child(cid).child(uid).remove()
            proid = database.child('Cart').child(cid).shallow().get().val()
            products = []
            for i in proid:
                products.append(i)
            details = {}
            totamt = []
            maxquant = {}
            sum = 0
            sum1 = 0

            for i in products:
                tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
                sum = sum + tamount
                det = database.child('Cart').child(cid).child(i).get().val()
                maxquantallow = database.child('Added_Items').child(i).child('Quantity').get().val()

                # diction1 = dict(maxquantallow)
                maxquant[i] = maxquantallow

                # farmid = database.child('Cart').child(i).child('farmid').get().val()
                # c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()

                diction = dict(det)
                # diction['maxquant']=maxquantallow
                details[i] = diction
            sum1 = sum + 30

            add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
            city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
            pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()

            print("details",details)

            details2 = {
                'det': details,
                'uid': products,
                'sum': sum,
                'sum1': sum1,
                'add': add,
                'city': city,
                'pin': pin,
                'mq': maxquant,

            }

            return render(request, 'cart.html', details2)
        except:
            return render(request, 'nocart.html')
    else:
        mess = "You need to login"
        return render(request, 'consumerlogin.html', {'mess': mess})


def razor(request):
    if request.method == 'POST':
        curuser = authe.current_user
        cid = curuser['localId']
        amount1 = int(request.GET.get('e'))* 100
        client = razorpay.Client(auth=('rzp_test_ssmxVx39H1TlGF','Gtc2eutjvAiD3P0MSE51KkJ1'))
        rep = ('EK'.join(random.choice(string.ascii_uppercase) for i in range(3)) + ''.join(random.choice(string.digits) for i in range(2)))
        orderinfo = client.order.create(dict (amount=amount1, currency="INR", receipt=rep))
        odid = orderinfo['id']
        amm = orderinfo['amount']

        proid = database.child('Cart').child(cid).shallow().get().val()
        products = []
        for i in proid:
            products.append(i)
        details = {}
        maxquant = {}
        sum = 0

        for i in products:
            tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
            sum = sum + tamount
            det = database.child('Cart').child(cid).child(i).get().val()
            maxquantallow = database.child('Added_Items').child(i).child('Quantity').get().val()

            # diction1 = dict(maxquantallow)
            maxquant[i] = maxquantallow

            # farmid = database.child('Cart').child(i).child('farmid').get().val()
            # c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()

            diction = dict(det)
            # diction['maxquant']=maxquantallow
            details[i] = diction
        sum1 = sum + 30

        add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
        city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
        pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()

        details2 = {
            'det': details,
            'uid': products,
            'sum': sum,
            'sum1': sum1,
            'add': add,
            'city': city,
            'pin': pin,
            'mq': maxquant,
            'orderinfo': orderinfo,
            'odid':odid,
            'amm': amm,
        }
        # print(details2)
        return render(request,'confrimorder.html', details2)
    else:
        return render(request, 'index.html')


@csrf_exempt
def success(request):
    from datetime import date
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")

    orderid = request.GET.get('oid')
    amount = request.GET.get('amm')

    curuser = authe.current_user
    cid = curuser['localId']

    name = database.child('Consumer').child('Details').child(cid).child('Name').get().val()
    add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
    city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
    pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()
    emailid = database.child('Consumer').child('Details').child(cid).child('Email').get().val()

    address = str(add) + str(city) + str(pin)
    print("address",address)

    proid = database.child('Cart').child(cid).shallow().get().val()
    products = []
    for i in proid:
        products.append(i)
    details = {}

    sum = 0

    for i in products:
        tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
        sum = sum + tamount
        det = database.child('Cart').child(cid).child(i).get().val()
        diction = dict(det)
        details[i] = diction
    sum1 = sum + 30

    info = {
            "title": 'Order Confrimation',
            "orderid": orderid,
            "amount": amount,
            "date": d1,
            "name":name,
            "address":address,
            'sum': sum,
            'sum1': sum1,
            "det": details,

        }
    html_content = render_to_string("emailtemp.html", info)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        'Order Confrimation',
        text_content,
        settings.EMAIL_HOST_USER,
        [emailid],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

    database.child('Cart').child(cid).remove()

    return render(request, 'thank.html')


def consumerlogin(request):
    return render(request, 'consumerlogin.html')


def removefromcart(request):

    curuser = authe.current_user
    cid = curuser['localId']
    uid = request.GET.get('z')
    database.child('Cart').child(cid).child(uid).remove()
    try:
        proid = database.child('Cart').child(cid).shallow().get().val()
        products = []
        for i in proid:
            products.append(i)
        details = {}
        totamt = []
        maxquant = {}
        sum = 0
        sum1 = 0
        # p = 0

        for i in products:
            tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
            sum = sum + tamount
            det = database.child('Cart').child(cid).child(i).get().val()
            maxquantallow = database.child('Added_Items').child(i).child('Quantity').get().val()

            # diction1 = dict(maxquantallow)
            maxquant[i] = maxquantallow

            # farmid = database.child('Cart').child(i).child('farmid').get().val()
            # c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()

            diction = dict(det)
            # diction['maxquant']=maxquantallow
            details[i] = diction
        sum1 = sum + 30

        add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
        city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
        pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()

        details2 = {
            'det': details,
            'uid': products,
            'sum': sum,
            'sum1': sum1,
            'add': add,
            'city': city,
            'pin': pin,
            'mq': maxquant,
        }


        return render(request, 'cart.html', details2)
    except:
        return render(request, 'nocart.html')


# def email(request):
#
#     return render(request, 'emailtemp.html')

def crop(request):
    return render(request, 'crop.html')


def seedfert(request):
    return render(request, 'seedferti.html')


def risk(request):
    return render(request, 'risk.html')


def risk2(request):
    return render(request, 'risk2.html')


def risk3(request):
    return render(request, 'risk3.html')


def risk4(request):
    return render(request, 'risk4.html')


def animal(request):
    return render(request, 'animal.html')


def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=c0b333162fb26b377e6962d7dae5e7b4').read()
        json_data = json.loads(res)

        data = {
            "country_code": str(json_data['weather'][0]['main']),
            "icon": str(json_data['weather'][0]['icon']),
            "longitude": str(json_data['coord']['lon']),
            "latitude": str(json_data['coord']['lat']),
            "temp": str(json_data['main']['temp']) + 'k',
            "pressure": str(json_data['main']['pressure']),
            "humidity": str(json_data['main']['humidity']),
            "wind": str(json_data['wind']['speed']) + 'km/h',
        }

    else:
        city = ''
        data = {}
    return render(request, 'weather.html', {'city': city, 'data': data})



def program(request):
    return render(request, 'prog.html')


def contact(request):
    return render(request, 'contactUs.html')


def cart(request):
    return render(request, 'cart.html')


def soil1(request):
    return render(request, 'Soil_lab.html')


def soil2(request):
    return render(request, 'Soil_lab2.html')


def soil3(request):
    return render(request, 'Soil_lab3.html')


def soil4(request):
    return render(request, 'Soil_lab4.html')


def seed1(request):
    return render(request, 'sdealer.html')


def seed2(request):
    return render(request, 'sdealer2.html')


def seed3(request):
    return render(request, 'sdealer3.html')


def seedvar(request):
    return render(request, 'svar.html')


def fert1(request):
    return render(request, 'fert.html')


def fert2(request):
    return render(request, 'fert2.html')


def fert3(request):
    return render(request, 'fert3.html')


def vert1(request):
    return render(request, 'veternity1.html')


def vert2(request):
    return render(request, 'v2.html')


def vert3(request):
    return render(request, 'v3.html')


def vert4(request):
    return render(request, 'v4.html')


def symdisease(request):
    return render(request, 'symdiseases.html')


def sd2(request):
    return render(request, 'sd2.html')


def sd3(request):
    return render(request, 'sd3.html')


def sd4(request):
    return render(request, 'sd4.html')
