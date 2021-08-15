from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.shortcuts import render
import pyrebase
import random
import string
import razorpay
from django.views.decorators.csrf import csrf_exempt


firebaseConfig = {
    'apiKey': "AIzaSyDztSthRiZSB6XTlhhD_i-8KT8RJ3DyM3Y",
    'authDomain': "efarming-7d78e.firebaseapp.com",
    'databaseURL': "https://efarming-7d78e-default-rtdb.firebaseio.com/",
    'projectId': "efarming-7d78e",
    'storageBucket': "efarming-7d78e.appspot.com",
    'messagingSenderId': "790177229471",
    'appId': "1:790177229471:web:6c118d22fb64cd8d6010aa"
  }
firebase1 = pyrebase.initialize_app(firebaseConfig)
authe = firebase1.auth()
database = firebase1.database()

role = ""
def about(request):
    return render(request,'About-us.html')


def index(request):
    global curuser
    curuser = authe.current_user
    return render(request, 'index.html',{'cur':curuser})

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
        return render(request, "index.html",{'cur':user})
    except:
        mess = 'Failed to create Account!!'
        return render(request, "index.html")

def Clogin(request):
    global role
    email = request.POST.get('email')
    password = request.POST.get('pass')
    role = 'con'
    try:
        user = authe.sign_in_with_email_and_password(email, password)

        id = database.child('Added_Items').shallow().get().val()
        lis_id = []
        for i in id:
            lis_id.append(i)

        details = {}
        farm = {}
        city = {}
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

        return render(request, 'index.html',{'cur':user})
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
        return render(request, 'index.html', {'mess': mess,'cur':user})
    except:
        mess = 'Failed to create Account!!'

        return render(request, "index.html", {'mess': mess})

def fsignin(request):
    global role
    email = request.POST.get('email')
    PW = request.POST.get('pass')
    PWek = str('ek'+PW)

    methodpost = request.POST.get('mainlogin')
    methodpost1 = request.POST.get('innerlogin')

    if methodpost1:

        role = request.POST.get('RoleName')
        try:
            user = authe.sign_in_with_email_and_password(email, PWek)
            curuser = authe.current_user

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

                        diction['proid']=i
                        details[p] = diction
                        p += 1

                details2 = {
                    'det': details
                }


                if role == 'far':
                    return render(request, "AddItem1.html", details2)
                else:
                    return render(request, "index.html",{'cur':user})
            except:
                return render(request, "index.html")
        except:
            mes = "Invalid Credentials"

            return render(request, "index.html", {'mess': mes})

    elif methodpost:
        role = request.POST.get('RoleName')
        try:
            user = authe.sign_in_with_email_and_password(email, PWek)
            curuser = authe.current_user
            farmid = curuser['localId']
            # session_id = user['localId']
            # request.session['uid'] = str(session_id)
            mes = "You are Loged in"
            return render(request, "index.html", {'mess': mes,'cur':user})
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
            diction['proid'] = i
            details[p] = diction
            p += 1
    details2 = {
        'det': details
    }
    return render(request, "AddItem1.html", details2)


def edititem(request):
    vid = request.POST.get('proid')
    vprice = request.POST.get('price')
    vquant = request.POST.get('Quantity')
    database.child('Added_Items').child(vid).update({
        'Price':vprice,
        'Quantity':vquant,
    })
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
            diction['proid'] = i
            details[p] = diction
            p += 1
    details2 = {
        'det': details
    }
    return render(request, "AddItem1.html", details2)


def selling(request):
    curuser = authe.current_user
    if curuser and role == 'far':
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
                    diction['proid'] = i
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
    details = {}
    city = {}
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
    if curuser and role == 'con':
        cid = curuser['localId']
        uid = request.GET.get('z')
        reqquant = request.POST.get('req')

        proname = database.child('Added_Items').child(uid).child('Product_name').get().val()
        amount = database.child('Added_Items').child(uid).child('Price').get().val()
        quantity = database.child('Added_Items').child(uid).child('Quantity').get().val()
        url = database.child('Added_Items').child(uid).child('url').get().val()
        fname = database.child('Added_Items').child(uid).child('fname').get().val()
        fid = database.child('Added_Items').child(uid).child('farmid').get().val()

        productdata = {
            'Productname': proname,
            'Price': amount,
            'Requiredquantity':  reqquant,
            'url': url,
            'fid':fid,
            'totalprice':int(amount) * int(reqquant),

        }
        database.child('Cart').child(cid).child(uid).set(productdata)
        return render(request, 'product.html', {'proname': proname, 'amount': amount, 'quantity': quantity,
                                                'url': url, 'fname': fname,'fid': fid, 'uid': uid})
    else:
        mess = "You need to login as consumer"
        return render(request,'consumerlogin.html',{'mess':mess})


def displaycart(request):
    curuser = authe.current_user
    if curuser:
        cid = curuser['localId']

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
            for i in products:
                tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
                sum = sum + tamount
                det = database.child('Cart').child(cid).child(i).get().val()
                maxquantallow = database.child('Added_Items').child(i).child('Quantity').get().val()

                maxquant[i] = maxquantallow

                diction = dict(det)
                # diction['maxquant']=maxquantallow
                details[i] = diction
            sum1 = sum + 30


            add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
            city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
            pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()
            if add == None:
                add = database.child('Farmer').child('Details').child(cid).child('Address').get().val()
                city = database.child('Farmer').child('Details').child(cid).child('City').get().val()
                pin = database.child('Farmer').child('Details').child(cid).child('Pin code').get().val()
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


def consumerlogin(request):
    return render(request, 'consumerlogin.html')


def razor(request):
    curuser = authe.current_user
    if request.method == 'POST':
        curuser = authe.current_user
        cid = curuser['localId']
        amount1 = int(request.GET.get('e'))* 100
        client = razorpay.Client(auth=('rzp_test_TfHMt9SCkkGdC8','EG8hOWFxrB3OODyZy9nOYw8v'))
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

            maxquant[i] = maxquantallow

            diction = dict(det)
            details[i] = diction
        sum1 = sum + 30

        add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
        city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
        pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()

        if add == None :
            add = database.child('Farmer').child('Details').child(cid).child('Address').get().val()
            city = database.child('Farmer').child('Details').child(cid).child('City').get().val()
            pin = database.child('Farmer').child('Details').child(cid).child('Pin code').get().val()
        print('fffffffffffffffffffffffffffffffffffffff',add,city,pin)
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
        return render(request,'confrimorder.html', details2)
    else:
        return render(request, 'index.html',{'cur':curuser})



@csrf_exempt
def success(request):
    global orderid, amount, orderid, amount
    from datetime import date,timedelta
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    orderid = request.GET.get('oid')
    amount = request.GET.get('amm')

    curuser = authe.current_user
    cid = curuser['localId']

    name = database.child('Consumer').child('Details').child(cid).child('Name').get().val()
    add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
    city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
    pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()
    emailid = database.child('Consumer').child('Details').child(cid).child('Email').get().val()
    if emailid == None:
        emailid = database.child('Farmer').child('Details').child(cid).child('Email').get().val()
    address = str(add) +"  "+ str(city) +"  "+ str(pin)

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
        details2 = {
            'Caddress':address,
            'Product_name': diction['Productname'],
            'Required_quant': diction['Requiredquantity'],
            'farmer_id': diction['fid'],
            'OrderDate': d1,
            'Pickup_date': 'None',
            'Pickup_status': 'notpicked',
            'Deliverystatus': 'notdelivered',
        }
        database.child('orderplaced').child(cid).child(orderid).child(i).set(details2)
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
        'Order Confirmation',
        text_content,
        settings.EMAIL_HOST_USER,
        [emailid],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


    database.child('Cart').child(cid).remove()
    return render(request, 'thank.html')


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
        for i in products:
            tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
            sum = sum + tamount
            det = database.child('Cart').child(cid).child(i).get().val()
            maxquantallow = database.child('Added_Items').child(i).child('Quantity').get().val()

            maxquant[i] = maxquantallow


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


def program(request):
    return render(request, 'prog.html')


def contact(request):
    return render(request, 'contactUs.html')


def signup(request):
    return render(request, 'signup.html')
