from django.shortcuts import render
import pyrebase
from django.contrib import auth
from datetime import date, time, datetime
import csv
from django.http import HttpResponse



config = {
    "apiKey": "AIzaSyDbKbCpXMqMVnYEO_nhkdiRJQn9aTyQCXo",
    "authDomain": "swaaha-4ad3d.firebaseapp.com",
    "databaseURL": "https://swaaha-4ad3d.firebaseio.com",
    "projectId": "swaaha-4ad3d",
    "storageBucket": "swaaha-4ad3d.appspot.com",
    "messagingSenderId": "851348860261"
}


firebase = pyrebase.initialize_app(config)
fbauth = firebase.auth()
db = firebase.database()

def login(request):
    return render(request, "login.html")

def loginSubmit(request):
        username = request.POST.get('username')
        email = username + '@swaaha.in'
        pswd = request.POST.get('pswd')

        user = fbauth.sign_in_with_email_and_password(email, pswd)
        request.session['uid'] = str(user['idToken'])
        customers = db.child('users').child('Customer').get(user['idToken']).each()
        admins = db.child('users').child('Admin').get(user['idToken']).each()
        operators = db.child('users').child('Operator').get(user['idToken']).each()
        drivers = db.child('users').child('Driver').get(user['idToken']).each()
        comp_data = db.get(user['idToken']).each()
        for admin in admins:
            if admin.val()['name'] == username:
                customers_num = len(customers)
                admins_num = len(admins)
                operators_num = len(operators)
                drivers_num = len(drivers)
                length = 0
                for chota_db in comp_data:
                    clusters = chota_db.val()
                    for key, value in clusters.items():
                        length += 1
                    break
                clusters_num = length
                data = {"customers_num" : customers_num, "admins_num" : admins_num, "operators_num" : operators_num, "drivers_num" : drivers_num, "clusters_num" : clusters_num, "username" : username}
                return render(request, "adminPanel.html", data)
            else:
                pass
        database = db.get(request.session['uid']).each()
        count = 0
        for data in database:
            if count == 3:
                info = data.val()
                for key, value in info.items():
                    if (key == "Customer"):
                        for k, v in value.items():
                            for a, b in v.items():
                                if (a == 'info'):
                                    if (b['name'] == username):
                                        v['username'] = username
                                        return render(request, "customerPanel.html", v)
            else:
                count += 1

        message = "Username/Password Invalid!"
        return render(request, "login.html", {"message" : message})


def adminsInfo(request):
    try:
        admins = db.child('users').child('Admin').get(request.session['uid']).each()
        data = []
        for admin in admins:
            data.append(admin.val())
        context = { "admins" : data }
        return render(request, "adminsInfo.html", context)
    except:
        return render(request, "error.html")

def addAdmin(request):
    try:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')
        pswd = request.POST.get('pswd')
        admins = db.child('users').child('Admin').get(request.session['uid']).each()
        for admin in admins:
            info = admin.val()
            if name == info['name']:
                message = "User already exists with same name! Please change the name and try again."
                admins = db.child('users').child('Admin').get(request.session['uid']).each()
                data = []
                for admin in admins:
                    data.append(admin.val())
                context = { "admins" : data , "message" : message}
                return render(request, "adminsInfo.html", context)
        email = name + '@swaaha.in'
        fbauth.create_user_with_email_and_password(email, pswd)
        new_user = fbauth.sign_in_with_email_and_password(email, pswd)
        data = {"name": str(name), "phone": str(phone), "type" : "Admin", "whatsapp" : str(whatsapp), "email" : str(email)}
        db.child("users").child("Admin").child(new_user['localId']).set(data, request.session['uid'])
        admins = db.child('users').child('Admin').get(request.session['uid']).each()
        data = []
        for admin in admins:
            data.append(admin.val())
        context = { "admins" : data }
        return render(request, "adminsInfo.html", context)
    except:
        return render(request, "error.html")

def customersInfo(request):
        customers = db.child('users').child('Customer').get(request.session['uid']).each()
        clusters = db.get(request.session['uid']).each()
        clusters_data = []
        count = 0
        for cluster in clusters:
            if count == 0:
                clusters_data.append(cluster.val())
                break
        customers_data = []
        for customer in customers:
            customers_data.append(customer.val())
        context = { "customers" : customers_data, "clusters" : clusters_data }
        return render(request, "customersInfo.html", context)

def addCustomer(request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')
        pswd = request.POST.get('pswd')
        cluster = request.POST.get('cluster')
        database = db.get(request.session['uid']).each()
        count = 0
        for customer in database:
            if count == 3:
                info = customer.val()
                for key, value in info['Customer'].items():
                    if name == value['info']['name']:
                        message = "User already exists with same name! Please change the name and try again."
                        customers = db.child('users').child('Customer').get(request.session['uid']).each()
                        clusters = db.get(request.session['uid']).each()
                        clusters_data = []
                        count = 0
                        for cluster in clusters:
                            if count == 0:
                                clusters_data.append(cluster.val())
                                break
                        customers_data = []
                        for customer in customers:
                            customers_data.append(customer.val())
                        context = { "customers" : customers_data, "clusters" : clusters_data }
                        return render(request, "customersInfo.html", context)
            count += 1
        email = name + '@swaaha.in'
        fbauth.create_user_with_email_and_password(email, pswd)
        new_user = fbauth.sign_in_with_email_and_password(email, pswd)
        data = {"name": str(name), "phone": str(phone), "type" : "Customer", "whatsapp" : str(whatsapp), "email" : str(email), "cluster" : str(cluster)}
        db.child("users").child("Customer").child(new_user['localId']).child("info").set(data, request.session['uid'])
        db.child("Clusters").child(cluster).child(new_user['localId']).set(str(name), request.session['uid'])
        customers = db.child('users').child('Customer').get(request.session['uid']).each()
        clusters = db.get(request.session['uid']).each()
        clusters_data = []
        count = 0
        for cluster in clusters:
            if count == 0:
                clusters_data.append(cluster.val())
                break
        customers_data = []
        for customer in customers:
            customers_data.append(customer.val())
        context = { "customers" : customers_data, "clusters" : clusters_data }
        return render(request, "customersInfo.html", context)

def updateCustomer(request, username):
    customers = db.child('users').child('Customer').get(request.session['uid']).each()
    for customer in customers:
        if (customer.val()['info']['name'] == username):
            request.session['customer'] = username
            return render(request, "updateProfile.html", customer.val())
    return render(request, "error.html")

def updateInfo(request):
    fullName = str(request.POST.get('fullName', ''))
    dob = str(request.POST.get('dob', ''))
    gender = str(request.POST.get('gender', ''))
    marital_status = str(request.POST.get('marital', ''))
    phone = str(request.POST.get('phone', ''))
    whatsapp = str(request.POST.get('whatsapp', ''))
    blood = str(request.POST.get('blood', ''))
    motherName = str(request.POST.get('motherName', ''))
    motherdob = str(request.POST.get('motherdob', ''))
    motherblood = str(request.POST.get('motherblood', ''))
    resaddress = str(request.POST.get('resaddress', ''))
    resdistrict = str(request.POST.get('resdistrict', ''))
    resstate = str(request.POST.get('resstate', ''))
    respin = str(request.POST.get('respin', ''))
    peraddress = str(request.POST.get('peraddress', ''))
    perdistrict = str(request.POST.get('perdistrict', ''))
    perstate = str(request.POST.get('perstate', ''))
    perpin = str(request.POST.get('perpin', ''))
    institution8 = str(request.POST.get('8institution', ''))
    board8 = str(request.POST.get('8board', ''))
    year8 = str(request.POST.get('8year', ''))
    percentage8 = str(request.POST.get('8percentage', ''))
    institution10 = str(request.POST.get('10institution', ''))
    board10 = str(request.POST.get('10board', ''))
    year10 = str(request.POST.get('10year', ''))
    percentage10 = str(request.POST.get('12percentage', ''))
    institution12 = str(request.POST.get('12institution', ''))
    board12 = str(request.POST.get('12board', ''))
    year12 = str(request.POST.get('12year', ''))
    percentage12 = str(request.POST.get('12percentage', ''))
    institutiongrad = str(request.POST.get('gradinstitution', ''))
    degreegrad = str(request.POST.get('graddegree', ''))
    yeargrad = str(request.POST.get('gradyear', ''))
    percentagegrad = str(request.POST.get('gradpercentage', ''))
    institutionposgrad = str(request.POST.get('posgradinstitution', ''))
    degreeposgrad = str(request.POST.get('posgraddegree', ''))
    yearposgrad = str(request.POST.get('posgradyear', ''))
    percentageposgrad = str(request.POST.get('posgradpercentage', ''))
    adhaarid = str(request.POST.get('adhaarid', ''))
    adhaarvalid = str(request.POST.get('adhaarvalid', ''))
    panid = str(request.POST.get('panid', ''))
    panvalid = str(request.POST.get('panvalid', ''))
    voterid = str(request.POST.get('voterid', ''))
    votervalid = str(request.POST.get('votervalid', ''))
    drivingid = str(request.POST.get('drivingid', ''))
    drivingvalid = str(request.POST.get('drivingvalid', ''))
    passportid = str(request.POST.get('passportid', ''))
    passportvalid = str(request.POST.get('passportvalid', ''))
    rationid = str(request.POST.get('rationid', ''))
    rationvalid = str(request.POST.get('rationvalid', ''))
    holdername = str(request.POST.get('holdername', ''))
    accnum = str(request.POST.get('accnum', ''))
    bankname = str(request.POST.get('bankname', ''))
    ifsc = str(request.POST.get('ifsc', ''))
    branch = str(request.POST.get('branch', ''))
    branchaddr = str(request.POST.get('branchaddr', ''))

    #Logic to store data
    comp_data = db.get(request.session['uid']).each()
    count = 0
    token = ''
    for chota_db in comp_data:
        if count == 3:
            for key, value in chota_db.val().items():
                if (key == 'Customer'):
                    for k,v in value.items():
                        for a,b in v.items():
                            username = request.session['customer']
                            if (a == "info"):
                                if(b["name"] == username):
                                    token = str(k)
                                    data = {
                                    "fullName" : fullName,
                                    "dob" : dob,
                                    "gender" : gender,
                                    "marital_status" : marital_status,
                                    "phone" : phone,
                                    "whatsapp" : whatsapp,
                                    "blood" : blood,
                                    "motherName" : motherName,
                                    "motherdob" : motherdob,
                                    "motherblood" : motherblood,
                                    "resaddress" : resaddress,
                                    "resdistrict" : resdistrict,
                                    "resstate" : resstate,
                                    "respin" : respin,
                                    "peraddress" : peraddress,
                                    "perdistrict" : perdistrict,
                                    "perstate" : perstate,
                                    "perpin" : perpin,
                                    "institution8" : institution8,
                                    "institution10" : institution10,
                                    "institution12" : institution12,
                                    "institutiongrad" : institutiongrad,
                                    "board8" : board8,
                                    "board10" : board10,
                                    "board12" : board12,
                                    "degreegrad" : degreegrad,
                                    "degreeposgrad" : degreeposgrad,
                                    "year8" : year8,
                                    "year10" : year10,
                                    "year12" : year12,
                                    "yeargrad" : yeargrad,
                                    "yearposgrad" : yearposgrad,
                                    "percentage8" : percentage8,
                                    "percentage10" : percentage10,
                                    "percentage12" : percentage12,
                                    "percentagegrad" : percentagegrad,
                                    "percentageposgrad" : percentageposgrad,
                                    "adhaarid" : adhaarid,
                                    "adhaarvalid" : adhaarvalid,
                                    "panid" : panid,
                                    "panvalid" : panvalid,
                                    "voterid" : voterid,
                                    "votervalid" : votervalid,
                                    "drivingid" : drivingid,
                                    "drivingvalid" : drivingvalid,
                                    "passportid" : passportid,
                                    "passportvalid" : passportvalid,
                                    "rationid" : rationid,
                                    "rationvalid" : rationvalid,
                                    "holdername" : holdername,
                                    "accnum" : accnum,
                                    "bankname" : bankname,
                                    "ifsc" : ifsc,
                                    "branch" : branch,
                                    "branchaddr" : branchaddr
                                    }
                                    db.child("users").child("Customer").child(token).child("info").update(data, request.session['uid'])
                                    customers = db.child('users').child('Customer').get(request.session['uid']).each()
                                    for customer in customers:
                                        if (customer.val()['info']['name'] == username):
                                            request.session['customer'] = username
                                            return render(request, "updateProfile.html", customer.val())
                                    return render(request, "error.html")
        else:
            count += 1
        return render(request, "error.html")

def wasteInfo(request):
        fbwaste = db.get(request.session['uid']).each()
        data = []
        customers = []
        count = 0
        for waste in fbwaste:
            if count == 2:
                data.append(waste.val())
            count += 1
        for datum in data:
            for key, value in datum.items():
                for k,v in value.items():
                    if not v['customer'] in customers:
                        customers.append(v['customer'])
        return render(request, "wasteInfo.html", {"waste_all" : data, "customers" : customers})

def operatorsInfo(request):
    try:
        operators = db.child('users').child('Operator').get(request.session['uid']).each()
        data = []
        for operator in operators:
            data.append(operator.val())
        context = { "operators" : data }
        return render(request, "operatorsInfo.html", context)
    except:
        return render(request, "error.html")

def addOperator(request):
    try:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')
        pswd = request.POST.get('pswd')
        database = db.get(request.session['uid']).each()
        count = 0
        for operator in database:
            if count == 3:
                info = operator.val()
                for key, value in info['Operator'].items():
                    if name == value['info']['name']:
                        message = "User already exists with same name! Please change the name and try again."
                        operators = db.child('users').child('Operator').get(request.session['uid']).each()
                        data = []
                        for operator in operators:
                            data.append(operator.val())
                        context = { "operators" : data }
                        return render(request, "operatorsInfo.html", context)
            count += 1
        email = name + '@swaaha.in'
        fbauth.create_user_with_email_and_password(email, pswd)
        new_user = fbauth.sign_in_with_email_and_password(email, pswd)
        data = {"name": str(name), "phone": str(phone), "type" : "Operator", "whatsapp" : str(whatsapp), "email" : str(email)}
        db.child("users").child("Operator").child(new_user['localId']).child("info").set(data, request.session['uid'])
        operators = db.child('users').child('Operator').get(request.session['uid']).each()
        data = []
        for operator in operators:
            data.append(operator.val())
        context = { "operators" : data }
        return render(request, "operatorsInfo.html", context)
    except:
        return render(request, "error.html")

def driversInfo(request):
    try:
        drivers = db.child('users').child('Driver').get(request.session['uid']).each()
        data = []
        for driver in drivers:
            data.append(driver.val())
        context = { "drivers" : data }
        return render(request, "driversInfo.html", context)
    except:
        return render(request, "error.html")

def addDriver(request):
    try:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')
        pswd = request.POST.get('pswd')
        database = db.get(request.session['uid']).each()
        count = 0
        for driver in database:
            if count == 3:
                info = driver.val()
                for key, value in info['Driver'].items():
                    if name == value['info']['name']:
                        message = "User already exists with same name! Please change the name and try again."
                        drivers = db.child('users').child('Driver').get(request.session['uid']).each()
                        data = []
                        for driver in drivers:
                            data.append(driver.val())
                        context = { "drivers" : data }
                        return render(request, "driversInfo.html", context)
            count += 1
        email = name + '@swaaha.in'
        fbauth.create_user_with_email_and_password(email, pswd)
        new_user = fbauth.sign_in_with_email_and_password(email, pswd)
        data = {"name": str(name), "phone": str(phone), "type" : "Driver", "whatsapp" : str(whatsapp), "email" : str(email)}
        db.child("users").child("Driver").child(new_user['localId']).child("info").set(data, request.session['uid'])
        drivers = db.child('users').child('Driver').get(request.session['uid']).each()
        data = []
        for driver in drivers:
            data.append(driver.val())
        context = { "drivers" : data }
        return render(request, "driversInfo.html", context)
    except:
        return render(request, "error.html")

def clustersInfo(request):
        comp_data = db.get(request.session['uid']).each()
        clusters_data = {}
        for chota_db in comp_data:
            clusters = chota_db.val()
            for key, value in clusters.items():
                clusters_data[key] = len(value)
            break
        data = { 'clusters' : clusters_data}
        return render(request, "clustersInfo.html", data)

def addCluster(request):
        cluster_name = request.POST.get('cluster')
        db.child('Clusters').child(cluster_name).set('null', request.session['uid'])
        comp_data = db.get(request.session['uid']).each()
        clusters_data = {}
        for chota_db in comp_data:
            clusters = chota_db.val()
            for key, value in clusters.items():
                clusters_data[key] = len(value)
            break
        data = { 'clusters' : clusters_data}
        return render(request, "clustersInfo.html", data)


def filterWaste(request):
        customer_name = str(request.POST.get('name'))
        request.session['filter'] = customer_name
        fbwaste = db.get(request.session['uid']).each()
        data = []
        customers = []
        count = 0
        for waste in fbwaste:
            if count == 2:
                data.append(waste.val())
            count += 1
        context = {}
        context['data'] = data
        context['username'] = customer_name
        return render(request, "filter.html", context)

def filterWasteMonth(request):
    fresh_data = {}
    month = request.POST.get('month')
    request.session['month'] = month
    fbwaste = db.get(request.session['uid']).each()
    data = []
    customers = []
    count = 0
    for waste in fbwaste:
        if count == 2:
            data.append(waste.val())
        count += 1
    customer_name = request.session['filter']
    for datum in data:
        for key, value in datum.items():
            for k,v in value.items():
                if v['customer'] == customer_name:
                    temp = key[key.find('-') + 1:]
                    mahina = temp[:temp.find('-')]
                    if mahina == month:
                        fresh_data[key] = value
    return render(request, "filterMonth.html", {'data' : fresh_data, 'username' : customer_name})


def chemical(request):
    comp_data = db.get(request.session['uid']).each()
    count = 0
    operators = []
    for chota_db in comp_data:
        if count == 1:
            operator = chota_db.val()
            break
        else:
            count += 1
    for key, value in operator.items():
        for k,v in value.items():
            if not v['operatorId'] in operators:
                operators.append(v['operatorId'])
    return render(request, "chemical.html", {'operator' : operator, 'operators' : operators})

def filterChemical(request):
    operator_name = str(request.POST.get('name'))
    request.session['operator'] = operator_name

    comp_data = db.get(request.session['uid']).each()
    count = 0
    operators = []
    for chota_db in comp_data:
        if count == 1:
            operator = chota_db.val()
            break
        else:
            count += 1
    return render(request, "chemicalFilter.html", {'operator' : operator, 'name' : operator_name})

def filterChemicalMonth(request):
    month = request.POST.get('month')
    operator_name = request.session['operator']
    request.session['month'] = month
    fresh_data = {}
    comp_data = db.get(request.session['uid']).each()
    count = 0
    operators = []
    for chota_db in comp_data:
        if count == 1:
            operator = chota_db.val()
            for key, value in operator.items():
                temp = key[key.find('-') + 1:]
                mahina = temp[:temp.find('-')]
                if mahina == month:
                    fresh_data[key] = value
            break
        else:
            count += 1
    return render(request, "chemicalMonth.html", {'operator' : fresh_data, 'name' : operator_name})



def downloadWaste(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=waste.csv'

    writer = csv.writer(response)
    writer.writerow(["Cluster", "Driver", "Customer", "Date", "Time", "Weight"])
    fbwaste = db.get(request.session['uid']).each()
    data = []
    customers = []
    count = 0
    for waste in fbwaste:
        if count == 2:
            data.append(waste.val())
        count += 1
    customer_name = request.session['filter']
    for datum in data:
        for key, value in datum.items():
            for k,v in value.items():
                if v['customer'] == customer_name:
                    writer.writerow([str(v['cluster']), str(v['driverEmail']), customer_name, str(key), str(k), str(v['weight'])])
    #writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    #writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    return response

def downloadWasteMonth(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=wasteMonthly.csv'

    writer = csv.writer(response)
    writer.writerow(["Cluster", "Driver", "Customer", "Date", "Time", "Weight"])

    month = request.session['month']
    fresh_data = {}
    fbwaste = db.get(request.session['uid']).each()
    data = []
    customers = []
    count = 0
    for waste in fbwaste:
        if count == 2:
            data.append(waste.val())
        count += 1
    customer_name = request.session['filter']
    for datum in data:
        for key, value in datum.items():
            for k,v in value.items():
                if v['customer'] == customer_name:
                    temp = key[key.find('-') + 1:]
                    mahina = temp[:temp.find('-')]
                    if mahina == month:
                        fresh_data[key] = value
    for key, value in fresh_data.items():
        for k,v in value.items():
            if v['customer'] == customer_name:
                writer.writerow([str(v['cluster']), str(v['driverEmail']), customer_name, str(key), str(k), str(v['weight'])])
    return response

def downloadChemical(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=operator.csv'

    writer = csv.writer(response)
    writer.writerow(["Date", "Time", "Operator", "Innoculant", "Drying Agent Required", "Actual Drying Agent"])

    operator_name = request.session['operator']

    comp_data = db.get(request.session['uid']).each()
    count = 0
    operators = []
    for chota_db in comp_data:
        if count == 1:
            operator = chota_db.val()
            break
        else:
            count += 1
    for key, value in operator.items():
        for k, v in value.items():
            if v['operatorId'] == operator_name:
                writer.writerow([str(key), str(k), str(v['operatorId']), str(v['innoculant']), str(v["dryingAgentRequired"]), str(v["dryingAgentActual"])])

    return response

def downloadChemicalMonth(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=operatorMonthly.csv'

    writer = csv.writer(response)
    writer.writerow(["Date", "Time", "Operator", "Innoculant", "Drying Agent Required", "Actual Drying Agent"])

    month = request.session['month']
    operator_name = request.session['operator']

    fresh_data = {}
    comp_data = db.get(request.session['uid']).each()
    count = 0
    operators = []
    for chota_db in comp_data:
        if count == 1:
            operator = chota_db.val()
            for key, value in operator.items():
                temp = key[key.find('-') + 1:]
                mahina = temp[:temp.find('-')]
                if mahina == month:
                    fresh_data[key] = value
            break
        else:
            count += 1
    for key, value in fresh_data.items():
        for k, v in value.items():
            if v['operatorId'] == operator_name:
                writer.writerow([str(key), str(k), str(v['operatorId']), str(v['innoculant']), str(v["dryingAgentRequired"]), str(v["dryingAgentActual"])])
    return response




def logout(request):
    auth.logout(request)
    return render(request, "login.html")
