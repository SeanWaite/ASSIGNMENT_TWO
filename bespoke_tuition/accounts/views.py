from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .models import Client, Address, ContactDetails, Student, TuitionAddress, Products
from .forms import *
from .decorators import *

def home(request):

    if request.user.is_staff:
        client_only = False
    else:
        client_only = True

    context = {'flag': client_only}

    return render(request, 'accounts/main.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def allClients(request):
    clients = Client.objects.all()
    context = {'clients': clients}

    return render(request, 'accounts/allclients.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def client(request, customer):
    clients = Client.objects.get(pk=customer)
    home = clients.address.all()
    contact = clients.contacts.all()
    students = clients.student_set.all()
    lessons = Lesson.objects.filter(student__in=students)


    context = {'clients': clients, 'address': home, 
               'contact': contact, 'students': students, 'lessons': lessons}

    return render(request, 'accounts/client.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def addClient(request): 
    client_form = AddClientForm()
    address_form = AddAddressSet()
    contact_form = AddContactSet()

    if request.method == 'POST':
        client_form = AddClientForm(request.POST)
        address_form = AddAddressSet(request.POST, instance=client_form.instance)
        contact_form = AddContactSet(request.POST, instance=client_form.instance)

        if client_form.is_valid() and address_form.is_valid() and contact_form.is_valid():
            client_form.save()
            address_form.save()

            contact_form.save()
            return redirect('accounts:allclients')

    context = {'client_form': client_form, 'address_form': address_form, 'contact_form': contact_form}

    return render(request, 'accounts/addclient.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def allStudents(request):
    students = Student.objects.all()
    context = {'students': students}

    return render(request, 'accounts/allstudents.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def addStudent(request): 
    student_form = AddStudentForm()
    student_address_form = AddStudentAddressSet()

    if request.method == 'POST':
        student_form = AddStudentForm(request.POST)
        student_address_form = AddStudentAddressSet(request.POST, instance=student_form.instance)

        if student_form.is_valid() and student_address_form.is_valid():
            student_form.save()
            student_address_form.save()
            return redirect('accounts:allstudents')

    context = {'student_form': student_form, 'student_address': student_address_form}

    return render(request, 'accounts/addstudent.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def student(request, student):
    student = Student.objects.get(pk=student)
    tuition_address = student.address_student.all()
    lessons = student.lesson_student.all()

    context = {'student': student, 'lessons': lessons, 'address': tuition_address}

    return render(request, 'accounts/student.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def addLessons(request, student):
    student = Student.objects.get(pk=student)
    lesson_form = AddLessonForm(initial={'student':student})

    if request.method == 'POST':
        lesson_form = AddLessonForm(request.POST)

        if lesson_form.is_valid():
            lesson_form.save()
            return redirect('accounts:student', student.pk)

    context = {'student':student, 'lesson_form': lesson_form}

    return render(request, 'accounts/addlesson.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def referenceData(request):
    products = Products.objects.all()
    terms = Term.objects.all()

    context = {'products': products, 'terms': terms }

    return render(request, 'accounts/referencedata.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def addProducts(request):
    product_form = AddProductForm()

    if request.method == 'POST':
        product_form = AddProductForm(request.POST)

        if product_form.is_valid():
            product_form.save()
            return redirect('accounts:refdata')

    context = {'product_form': product_form}

    return render(request, 'accounts/addproduct.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def updateProduct(request, product):
    product = Products.objects.get(pk=product)
    product_form = UpdateProductForm(instance=product)

    if request.method == 'POST':
        product_form = UpdateProductForm(request.POST, instance=product)

        if product_form.is_valid():
            product_form.save()
            return redirect('accounts:refdata')

    context = {'product_form': product_form}

    return render(request, 'accounts/addproduct.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def addTerms(request):
    term_form = AddTermForm()

    if request.method == 'POST':
        term_form = AddTermForm(request.POST)

        if term_form.is_valid():
            term_form.save()
            return redirect('accounts:refdata')

    context = {'term_form': term_form}

    return render(request, 'accounts/addterm.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def updateTerm(request, term):
    term_details = Term.objects.get(pk=term)
    term_form = UpdateTermForm(instance=term_details)

    if request.method == 'POST':
        term_form = UpdateTermForm(request.POST, instance=term)

        if term_form.is_valid():
            term_form.save()
            return redirect('accounts:refdata')

    context = {'term_form': term_form}

    return render(request, 'accounts/addterm.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def accounts(request):
    clients = Client.objects.all()

    context = {'clients': clients}

    return render(request, 'accounts/accounts.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def accountsDetailed(request, customer):
    clients = Client.objects.get(pk=customer)
    students = clients.student_set.all()
    lessons = Lesson.objects.filter(student__in=students, invoiced=False)

    now = datetime.now()

    invoice_id = clients.surname[0:3].upper() + now.strftime("%d%m%Y%H%M%S")

    print(invoice_id)

    lesson_total = 0

    for lesson in lessons:
        lesson_total += lesson.lesson_type.price

    create_invoice_form = CreateInvoiceForm(initial={'invoice_number': invoice_id,
                                                     'total_amount': lesson_total,
                                                     'client': customer,
                                                     'amount_paid': 0,
                                                     'amount_outstanding': lesson_total})

    if lesson_total <= 0:
        messages.info(request, 'No outstanding amount for ' + clients.forename + ' ' + clients.surname)
        return redirect('accounts:accounts')

    if request.method == 'POST':
        create_invoice_form = CreateInvoiceForm(request.POST)

        if create_invoice_form.is_valid():
            create_invoice_form.save()
            lessons.update(invoiced=True, invoice_number=create_invoice_form.instance)

            return redirect('accounts:accounts')

    context = {'clients': clients, 'students': students, 
               'lessons': lessons, 'total': lesson_total, 'create_invoice': create_invoice_form}

    return render(request, 'accounts/accountsdetailed.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def invoices(request):
    invoices = Invoices.objects.all().order_by('date_created')

    context = {'invoices': invoices}

    return render(request, 'accounts/invoices.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def invoicesDetailed(request, invoice):
    invoice = Invoices.objects.get(pk=invoice)
    client = Client.objects.get(pk=invoice.client.pk)
    home = client.address.get(Q(effective_from_date__lte = invoice.date_created,
                              effective_to_date__gte = invoice.date_created) | 
                              Q(effective_from_date__lte = invoice.date_created,
                              effective_to_date__isnull = True ))
    lessons = invoice.invoice_no.all()

    lesson_count = list(lessons.values('lesson_type__product_name', 
                                  'lesson_type__price').annotate(
                                  total=Count('lesson_type')))

    for lesson in lesson_count:
        lesson["total_price"] = lesson["total"] * lesson["lesson_type__price"]

    context = {'invoice': invoice, 'client': client, 'home': home, 'lessons': lesson_count}

    return render(request, 'accounts/invoicedetailed.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin'])
def updateInvoices(request, invoice):
    invoice = Invoices.objects.get(pk=invoice)
    update_invoice_form = UpdateInvoiceForm(instance=invoice)

    if request.method == 'POST':
        update_invoice_form = UpdateInvoiceForm(request.POST, instance=invoice)

        if update_invoice_form.is_valid():
            total = update_invoice_form.cleaned_data.get('total_amount')
            paid = update_invoice_form.cleaned_data.get('amount_paid')
            remaining = total - paid
            update_invoice_form.amount_outstanding = remaining

            update = update_invoice_form.save(commit=False)
            update.amount_outstanding = remaining
            update.save()

            return redirect('accounts:invoices')

    context = {'update_invoice': update_invoice_form}

    return render(request, 'accounts/updateinvoice.html', context)

@authenticatedUser
def registerPage(request): 
    reg_form = CreateUserForm()

    if request.method == 'POST':
        reg_form = CreateUserForm(request.POST)

        if reg_form.is_valid():
            email = reg_form.cleaned_data.get('email')
            user = reg_form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            check_email = ContactDetails.objects.get(email_address=email)

            check_email.client.user = user
            check_email.client.save()
 
            messages.success(request, 'Registration Completed - Now sign in!')

            return redirect('accounts:login')

    context = {'form': reg_form}

    return render(request, 'accounts/register.html', context)

@authenticatedUser
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.info(request, 'Username or password is incorrect. '
                                   'If you have forgotten your password please contact us')
            
    context = {}

    return render(request, 'accounts/login.html', context)

def logoutUser(request):

    logout(request)

    return redirect('accounts:login')

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin','customer'])
def clientView(request):
    client_only = True
    clients = request.user.client
    home = clients.address.all()
    contact = clients.contacts.all()
    students = clients.student_set.all()
    lessons = Lesson.objects.filter(student__in=students)

    context = {'clients': clients, 'address': home, 
               'contact': contact, 'students': students, 
               'lessons': lessons, 'flag': client_only}

    return render(request, 'accounts/clientview.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin','customer'])
def clientInvoices(request):
    client_only = True
    clients = request.user.client
    invoices = clients.invoices.all()

    context = {'invoices': invoices, 'flag': client_only}

    return render(request, 'accounts/clientinvoices.html', context)

@login_required(login_url='accounts:login')
@allowedUsers(allowed_roles=['admin','customer'])
def clientDetailedInvoice(request, invoice):
    client_only = True
    client_user = request.user.client
    invoice = Invoices.objects.get(pk=invoice)
    client = Client.objects.get(pk=invoice.client.pk)
    if client_user.pk == client.pk:   
        home = client.address.get(Q(effective_from_date__lte = invoice.date_created,
                                  effective_to_date__gte = invoice.date_created) | 
                                  Q(effective_from_date__lte = invoice.date_created,
                                  effective_to_date__isnull = True ))
        lessons = invoice.invoice_no.all()

        lesson_count = list(lessons.values('lesson_type__product_name', 
                                           'lesson_type__price').annotate(
                                           total=Count('lesson_type')))

        for lesson in lesson_count:
            lesson["total_price"] = lesson["total"] * lesson["lesson_type__price"]

        context = {'invoice': invoice, 'client': client, 
                   'home': home, 'lessons': lesson_count,
                   'flag': client_only}
    else:
        return redirect('accounts:clientinvoices')

    return render(request, 'accounts/invoicedetailed.html', context)
