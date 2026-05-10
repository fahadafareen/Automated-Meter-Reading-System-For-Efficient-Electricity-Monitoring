from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import *
import random
import datetime
import json

# ── AUTHENTICATION & CORE ─────────────────────────────────────

def logout(request):
    request.session.clear()
    return redirect(first)

def first(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def logint(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    if not email.endswith('@gmail.com'):
         return render(request, 'login.html', {'status': 'failed', 'error_msg': 'Only @gmail.com accounts are permitted to sign in.'})

    if email == 'admin@gmail.com' and password == 'admin':
        request.session['logintdetail'] = email
        request.session['logint'] = 'admin'
        return redirect('dash')

    elif registration.objects.filter(email=email, password=password).exists():
        u = registration.objects.get(email=email, password=password)
        request.session['uid'] = u.id
        request.session['uname'] = u.name
        request.session['uemail'] = email
        request.session['user'] = 'user'
        return redirect('consumer_dash')

    elif worker.objects.filter(email=email, password=password).exists():
        w = worker.objects.get(email=email, password=password)
        request.session['uid'] = w.id
        request.session['uname'] = w.name
        request.session['uemail'] = email
        request.session['user'] = 'worker'
        return redirect('worker_dash')
    else:
        return render(request, 'login.html', {'status': 'failed'})

def addreg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        location = request.POST.get('location')
        role = request.POST.get('role')

        if not email.endswith('@gmail.com'):
            return render(request, 'register.html', {'status': 'failed', 'error_msg': 'Only @gmail.com accounts are permitted.'})

        if role == 'User':
            registration(name=name, phone=phone, email=email, password=password, address=address, location=location).save()
        else:
            worker(name=name, phone=phone, email=email, password=password, address=address, location=location, role=role).save()
        return render(request, 'register.html', {'status': 'success'})

# ── ADMIN PORTAL ─────────────────────────────────────────────

def dash(request):
    ctx = {
        'total_users': registration.objects.count(),
        'total_bills': bills.objects.count(),
        'total_paid': bills.objects.filter(status__in=['paid', 'Paid']).count(),
        'total_pending': bills.objects.filter(status='pending').count(),
        'total_payments': payment.objects.count(),
        'total_meters': meter.objects.count(),
        'total_amount': sum(int(p.bill_amount) for p in payment.objects.all() if p.bill_amount.isdigit()),
    }
    return render(request, 'admin/index.html', ctx)

def analysis_graph(request):
    total_paid = bills.objects.filter(status__in=['paid', 'Paid']).count()
    total_pending = bills.objects.filter(status='pending').count()
    total_accepted = bills.objects.filter(status__in=['Accept', 'accept']).count()
    total_rejected = bills.objects.filter(status__in=['Reject', 'reject']).count()

    all_payments = payment.objects.all()
    rev_labels = [str(p.date) for p in all_payments]
    rev_values = [int(p.bill_amount) if p.bill_amount.isdigit() else 0 for p in all_payments]

    readings = analyzing.objects.all().order_by('date')
    read_labels = [str(r.date) for r in readings]
    read_values = [int(r.currentreading) if str(r.currentreading).isdigit() else 0 for r in readings]

    energy_usage = sum(int(r.currentreading) for r in analyzing.objects.all() if str(r.currentreading).isdigit())

    ctx = {
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_accepted': total_accepted,
        'total_rejected': total_rejected,
        'rev_labels': json.dumps(rev_labels),
        'rev_values': json.dumps(rev_values),
        'read_labels': json.dumps(read_labels),
        'read_values': json.dumps(read_values),
        'total_users': registration.objects.count(),
        'total_meters': meter.objects.count(),
        'progress_labels': json.dumps(['Complaints', 'Tasks Done', 'Tasks Pending', 'Energy']),
        'progress_values': json.dumps([complaints.objects.count(), Dispatch.objects.filter(status='Completed').count(), Dispatch.objects.exclude(status='Completed').count(), energy_usage]),
    }
    return render(request, 'admin/analysis_graph.html', ctx)

def manage_requests(request):
    ctx = {
        'conns': NewConnection.objects.all().order_by('-date'),
        'solar': SolarConnection.objects.all().order_by('-date'),
        'names': NameChange.objects.all().order_by('-date'),
        'tariffs': TariffChange.objects.all().order_by('-date'),
    }
    return render(request, 'admin/manage_requests.html', ctx)

def accept_request(request, rtype, id):
    obj = None
    if rtype == 'new_conn':
        obj = NewConnection.objects.get(id=id)
        # Automatically generate unique meter number
        while True:
            meter_no = str(random.randint(100000, 999999))
            if not meter.objects.filter(meternumber=meter_no).exists():
                break
        
        # Save meter
        meter(meternumber=meter_no, status='approved').save()
        
        # Save consumer - get user from registration
        try:
            user = registration.objects.get(id=obj.uid)
            consumerr(name=user.name, meter_number=meter_no).save()
        except registration.DoesNotExist:
            pass # Or handle error accordingly
            
    elif rtype == 'solar': obj = SolarConnection.objects.get(id=id)
    elif rtype == 'name': obj = NameChange.objects.get(id=id)
    elif rtype == 'tariff': obj = TariffChange.objects.get(id=id)
    
    if obj:
        obj.status = 'Approved'
        obj.save()
    return redirect('manage_requests')

def reject_request(request, rtype, id):
    if rtype == 'new_conn': obj = NewConnection.objects.get(id=id)
    elif rtype == 'solar': obj = SolarConnection.objects.get(id=id)
    elif rtype == 'name': obj = NameChange.objects.get(id=id)
    elif rtype == 'tariff': obj = TariffChange.objects.get(id=id)
    obj.status = 'Rejected'
    obj.save()
    return redirect('manage_requests')

def admin_view_complaints(request):
    sel = complaints.objects.all().order_by('-date')
    return render(request, 'admin/view_complaints.html', {'complaints': sel})

def viewconsumerpayment(request):
    sel = payment.objects.all().order_by('-date')
    return render(request, 'admin/viewpayment.html', {'result': sel})

def viewbill(request):
    sel = bills.objects.all().order_by('-date')
    return render(request, 'admin/viewbill.html', {'result': sel})

def viewcons(request):
    sel = registration.objects.all()
    return render(request, 'admin/viewcons.html', {'result': sel})

def viewel(request):
    sel = meter.objects.all()
    return render(request, 'admin/viewelect.html', {'result': sel})

def mtr(request):
    if request.method == 'POST':
        meter(meternumber=request.POST.get('number'), status=request.POST.get('name')).save()
        return render(request, 'admin/meter.html')
    return render(request, 'admin/meter.html')

def zone_status(request):
    return render(request, 'admin/zone_status.html', {'zones': Zone.objects.all()})

def add_zone(request):
    if request.method == 'POST':
        Zone(name=request.POST.get('name'), status=request.POST.get('status'), category=request.POST.get('category')).save()
        return redirect('zone_status')
    return render(request, 'admin/add_zone.html')

def dispatch_worker(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        d_date = request.POST.get('date')
        if d_date != today:
             return render(request, 'admin/dispatch_worker.html', {'workers': worker.objects.all(), 'zones': Zone.objects.all(), 'status': 'failed', 'error': 'Invalid date Selected! Only today\'s date is allowed.', 'current_date': today})
             
        worker_id = request.POST.get('workerid')
        zone_id = request.POST.get('zoneid')
        
        w = worker.objects.get(id=worker_id)
        z = Zone.objects.get(id=zone_id)
        
        Dispatch(worker_id=worker_id, worker_name=w.name, zone_id=zone_id, zone_name=z.name, date=d_date, details=request.POST.get('details'), status='Assigned').save()
        return redirect('view_dispatch')
        
    return render(request, 'admin/dispatch_worker.html', {'workers': worker.objects.all(), 'zones': Zone.objects.all(), 'current_date': today})

def view_dispatch(request):
    dispatches = Dispatch.objects.all()
    result = []
    for d in dispatches:
        try:
            w = worker.objects.get(id=d.workerid)
            z = Zone.objects.get(id=d.zoneid)
            result.append({'worker_name': w.name, 'zone_name': z.name, 'date': d.date, 'status': d.status, 'details': d.details})
        except: continue
    return render(request, 'admin/view_dispatch.html', {'result': result})

def admin_simulate_monitoring(request):
    if request.method == 'POST':
        energy_data(uid=request.POST.get('uid'), current=float(request.POST.get('current', 0)), power=float(request.POST.get('power', 0)), energy=float(request.POST.get('energy', 0))).save()
        return redirect('admin_simulate_monitoring')
    return render(request, 'admin/simulate_monitoring.html', {'consumers': registration.objects.all(), 'recent_data': energy_data.objects.all().order_by('-date')[:10]})

# ── WORKER PORTAL ─────────────────────────────────────────────

def worker_dash(request):
    wid = request.session.get('uid')
    if not wid: return redirect('login')
    my_tasks = Dispatch.objects.filter(workerid=wid).exclude(status='Completed')
    tasks_preview = []
    for t in my_tasks:
        try:
            z = Zone.objects.get(id=t.zoneid)
            tasks_preview.append({'zone': z.category, 'status': t.status, 'details': t.details})
        except: continue
    return render(request, 'worker/dashboard.html', {'emergencies': Zone.objects.filter(status='Power Outage'), 'tasks_preview': tasks_preview[:5], 'total_tasks': len(my_tasks)})

def worker_tasks(request):
    wid = request.session.get('uid')
    dispatches = Dispatch.objects.filter(workerid=wid).order_by('-date')
    result = []
    for d in dispatches:
        try:
            z = Zone.objects.get(id=d.zoneid)
            result.append({'id': d.id, 'zone_name': z.name, 'zone_category': z.category, 'date': d.date, 'status': d.status, 'details': d.details, 'is_dispatched': d.status == 'Dispatched', 'is_in_progress': d.status == 'In Progress', 'is_completed': d.status == 'Completed'})
        except: continue
    return render(request, 'worker/tasks.html', {'tasks': result})

def update_dispatch_status(request):
    if request.method == 'POST':
        d = Dispatch.objects.get(id=request.POST.get('task_id'))
        d.status = request.POST.get('status')
        d.save()
    return redirect('worker_tasks')

def submit_report(request):
    wid = request.session.get('uid')
    assigned_zone_ids = Dispatch.objects.filter(workerid=wid).values_list('zoneid', flat=True).distinct()
    zones = Zone.objects.filter(id__in=assigned_zone_ids)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if not re.search('[a-zA-Z]', content):
             return render(request, 'worker/report.html', {'status': 'failed', 'error': 'Report must contain descriptive text, not just numbers.', 'zones': zones})
             
        MaintenanceReport(workerid=wid, zoneid=request.POST.get('zoneid'), content=content, date=datetime.date.today().strftime('%Y-%m-%d')).save()
        return render(request, 'worker/report.html', {'status': 'success'})
        
    return render(request, 'worker/report.html', {'zones': zones})

# ── CONSUMER PORTAL ───────────────────────────────────────────

def consumer_dash(request):
    uid = request.session.get('uid')
    if not uid: return redirect('login')
    
    u = registration.objects.get(id=uid)
    user_location = u.location
    
    # Check for active power outages in user's location or any severe outage
    emergencies = Zone.objects.filter(status='Power Outage')
    
    ctx = {
        'alerts': news.objects.filter(
            models.Q(is_alert=True) & 
            (models.Q(zone='All Zones') | models.Q(zone__icontains=user_location))
        ).order_by('-post_date')[:3],
        'pending_bills_count': bills.objects.filter(consumerid=u.name, status='pending').count(),
        'recent_conns': NewConnection.objects.filter(uid=uid).order_by('-date')[:2],
        'latest_energy': energy_data.objects.filter(uid=uid).order_by('-date').first(),
        'emergencies': emergencies,
        'user_location': u.location
    }
    return render(request, 'consumer/dashboard.html', ctx)

def energy_monitoring(request):
    uid = request.session.get('uid')
    if not uid: return redirect('login')
    data = energy_data.objects.filter(uid=uid).order_by('-date')
    return render(request, 'consumer/energy_monitoring.html', {'monitoring_data': data, 'latest': data.first()})

def get_energy_data(request):
    uid = request.session.get('uid')
    if not uid:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    # Latest 20 for table (descending)
    table_data = energy_data.objects.filter(uid=uid).order_by('-date')[:20]
    
    # Latest 15 for chart (ascending)
    chart_records = energy_data.objects.filter(uid=uid).order_by('-date')[:15]
    chart_records = reversed(chart_records)
    
    chart_labels = []
    chart_values = []
    for r in chart_records:
        chart_labels.append(r.date.strftime('%H:%M:%S'))
        chart_values.append(r.power)
    
    result = []
    for d in table_data:
        result.append({
            'id': d.id,
            'current': d.current,
            'power': d.power,
            'energy': d.energy,
            'time': d.date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    latest = result[0] if result else None
    return JsonResponse({
        'monitoring_data': result, 
        'latest': latest,
        'chart_labels': chart_labels,
        'chart_values': chart_values
    })

def get_admin_monitoring_data(request):
    if request.session.get('logint') != 'admin':
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    data = energy_data.objects.all().order_by('-date')[:10]
    result = []
    for d in data:
        result.append({
            'id': d.id,
            'uid': d.uid,
            'current': d.current,
            'power': d.power,
            'energy': d.energy,
            'time': d.date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({'monitoring_data': result})

def vbill(request):
    uname = request.session.get('uname')
    selected_year = request.GET.get('year', '')
    
    # Base Query - Include 'pending' so users can see and pay new bills
    query = bills.objects.filter(consumerid=uname, status__in=['Accept', 'accept', 'paid', 'Paid', 'pending']).order_by('-date')
    
    # Get all unique years from this user's bills for the filter dropdown
    all_bills = bills.objects.filter(consumerid=uname)
    years = sorted(list(set(b.date[:4] for b in all_bills if len(b.date) >= 4)), reverse=True)
    
    if selected_year:
        query = query.filter(date__icontains=selected_year)
        
    return render(request, 'consumer/viewbills.html', {
        'result': query, 
        'years': years, 
        'selected_year': selected_year
    })

def payment_history(request):
    uname = request.session.get('uname')
    return render(request, 'consumer/payment_history.html', {'history': payment.objects.filter(uid=uname).order_by('-date')})

def paybill(request, id):
    today = datetime.date.today().strftime('%Y-%m-%d')
    return render(request, 'consumer/payment.html', {'result': bills.objects.get(id=id), 'current_date': today})

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def pay(request):
    if request.method == 'POST':
        today = datetime.date.today().strftime('%Y-%m-%d')
        p_date = request.POST.get('date')
        cardnumber = request.POST.get('cardnumber', '')

        # Validating Card Number (Exactly 16 digits)
        if len(cardnumber) != 16 or not cardnumber.isdigit():
             return HttpResponse("Invalid Card Number! Must be exactly 16 digits.")

        if p_date != today:
            return HttpResponse("Invalid date Selected! Only today's date is allowed.")
        
        amount = request.POST.get('bill_amount')
        ptype = request.POST.get('paymenttype')
        bill_id = request.POST.get('bill_id')
        user_email = request.session.get('uemail')
        uname = request.session.get('uname')
        uid = request.session.get('uid')

        # 1. Fetch user email and name reliably from the bill if possible
        if not user_email or not uname:
            if bill_id:
                try:
                    b_obj = bills.objects.get(id=bill_id)
                    u_obj = registration.objects.filter(name=b_obj.consumerid).first()
                    if u_obj:
                        user_email = u_obj.email
                        uname = u_obj.name
                except Exception as ex:
                    print(f"Fallback retrieval failed: {ex}")

        # Save payment record
        p = payment(
            paymenttype=ptype, 
            bill_amount=amount, 
            cardnum=cardnumber, 
            cardname=request.POST.get('cardname'), 
            ccvnum=request.POST.get('ccvnumber'), 
            expdate=request.POST.get('expdate'), 
            date=p_date, 
            status=request.POST.get('status'), 
            uid=uname
        )
        p.save()

        # Send Email Confirmation
        try:
            if user_email and "@" in user_email:
                subject = 'Payment Successful - Energy Meter Portal'
                # 2. Get meter number
                meter_info = consumerr.objects.filter(name=uname).first()
                meter_no = meter_info.meter_number if meter_info else "N/A"
                
                # 3. Context for HTML template
                from django.urls import reverse
                dash_url = request.build_absolute_uri(reverse('consumer_dash'))
                
                context = {
                    'name': uname,
                    'amount': amount,
                    'payment_type': ptype,
                    'date': p_date,
                    'payment_id': p.id,
                    'meter_number': meter_no,
                    'dash_url': dash_url
                }
                
                # 4. Render HTML and Plain Text versions
                html_content = render_to_string('emails/payment_success.html', context)
                text_content = strip_tags(html_content)
                
                # 5. Create and Send email
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
                print(f"SUCCESS: Email sent to: {user_email}")
            else:
                print(f"WARNING: User email not found or invalid: {user_email}")
                
        except Exception as e:
            print(f"CRITICAL: SMTP error occurred: {e}")

        if bill_id:
            b = bills.objects.get(id=bill_id)
            b.status = 'paid'
            b.save()
        return redirect('vbill')

import re

def comp(request):
    today = datetime.date.today()
    if request.method == 'POST':
        c_date_str = request.POST.get('date')
        complaint_name = request.POST.get('complaintname')
        description = request.POST.get('description')
        
        # Date Validation
        try:
            c_date = datetime.datetime.strptime(c_date_str, '%Y-%m-%d').date()
            if c_date != today:
                return render(request, 'consumer/complaint.html', {'status': 'failed', 'error': 'Invalid date Selected! Only today\'s date is allowed.', 'current_date': today.strftime('%Y-%m-%d')})
        except:
             return render(request, 'consumer/complaint.html', {'status': 'failed', 'error': 'Invalid date Selected!', 'current_date': today.strftime('%Y-%m-%d')})

        # Text Validation (must contain letters)
        if not re.search('[a-zA-Z]', complaint_name):
            return render(request, 'consumer/complaint.html', {'status': 'failed', 'error': 'Complaint title must contain letters.', 'current_date': today.strftime('%Y-%m-%d')})
        if not re.search('[a-zA-Z]', description):
            return render(request, 'consumer/complaint.html', {'status': 'failed', 'error': 'Description must contain more descriptive details (not just numbers).', 'current_date': today.strftime('%Y-%m-%d')})

        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        complaints(consumerid=request.session.get('uname'), complaintname=request.POST.get('complaintname'), description=request.POST.get('description'), photoss=uploaded_file, date=c_date_str, status=request.POST.get('status'), cid=request.session.get('uid')).save()
        return render(request, 'consumer/complaint.html', {'status': 'success', 'current_date': today.strftime('%Y-%m-%d')})
    return render(request, 'consumer/complaint.html', {'current_date': today.strftime('%Y-%m-%d')})

def track_requests(request):
    uid = request.session.get('uid')
    return render(request, 'consumer/track_requests.html', {
        'conns': NewConnection.objects.filter(uid=uid), 'solar': SolarConnection.objects.filter(uid=uid),
        'names': NameChange.objects.filter(uid=uid), 'tariffs': TariffChange.objects.filter(uid=uid)
    })

def new_connection(request):
    if request.method == 'POST':
        NewConnection(uid=request.session.get('uid'), address=request.POST.get('address'), connection_type=request.POST.get('connection_type'), phase=request.POST.get('phase'), date=datetime.date.today().strftime('%Y-%m-%d')).save()
        return redirect('track_requests')
    return render(request, 'consumer/new_connection.html')

def solar_connection(request):
    if request.method == 'POST':
        SolarConnection(uid=request.session.get('uid'), solar_capacity=request.POST.get('capacity'), date=datetime.date.today().strftime('%Y-%m-%d')).save()
        return redirect('track_requests')
    return render(request, 'consumer/solar_connection.html')

def name_change(request):
    if request.method == 'POST':
        NameChange(uid=request.session.get('uid'), new_name=request.POST.get('new_name'), reason=request.POST.get('reason'), date=datetime.date.today().strftime('%Y-%m-%d')).save()
        return redirect('track_requests')
    return render(request, 'consumer/name_change.html')

def tariff_change(request):
    if request.method == 'POST':
        TariffChange(uid=request.session.get('uid'), current_plan=request.POST.get('current_plan'), new_plan=request.POST.get('new_plan'), date=datetime.date.today().strftime('%Y-%m-%d')).save()
        return redirect('track_requests')
    return render(request, 'consumer/tariff_change.html')

# ── CHAT SYSTEM ──────────────────────────────────────────────

def user_chat(request):
    uemail = request.session.get('uemail')
    uname = request.session.get('uname')
    if not uemail: return redirect('login')
    
    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        if msg: chat(sender=uemail, receiver='admin', message=msg).save()
        return redirect('user_chat')
        
    msgs = chat.objects.filter(
        models.Q(sender=uemail, receiver='admin') | 
        models.Q(sender='admin', receiver=uemail)
    ).order_by('timestamp')
    
    return render(request, 'consumer/chat.html', {'msgs': msgs, 'uemail': uemail, 'uname': uname})

def admin_chat(request):
    # Get unique emails of users who have sent messages
    user_emails = chat.objects.values_list('sender', flat=True).exclude(sender='admin').distinct()
    
    # Create a list of dictionaries with name and email for the sidebar
    users_list = []
    for email in user_emails:
        unread = chat.objects.filter(sender=email, receiver='admin', is_read=False).count()
        try:
            reg = registration.objects.get(email=email)
            users_list.append({'name': reg.name, 'email': email, 'unread': unread})
        except:
            try:
                w = worker.objects.get(email=email)
                users_list.append({'name': w.name, 'email': email, 'unread': unread})
            except:
                users_list.append({'name': email, 'email': email, 'unread': unread})
            
    selected_email = request.GET.get('user', users_list[0]['email'] if users_list else None)
    
    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        target_email = request.POST.get('user', '')
        if msg and target_email:
            chat(sender='admin', receiver=target_email, message=msg).save()
        return redirect(f'/admin_chat/?user={target_email}')
        
    msgs = []
    selected_name = "User"
    if selected_email:
        # Mark messages as read
        chat.objects.filter(sender=selected_email, receiver='admin', is_read=False).update(is_read=True)
        
        msgs = chat.objects.filter(
            models.Q(sender=selected_email, receiver='admin') | 
            models.Q(sender='admin', receiver=selected_email)
        ).order_by('timestamp')
        try:
            selected_name = registration.objects.get(email=selected_email).name
        except:
            try:
                selected_name = worker.objects.get(email=selected_email).name
            except:
                selected_name = selected_email

    return render(request, 'admin/chat.html', {
        'msgs': msgs, 
        'users': users_list, 
        'selected': selected_email,
        'selected_name': selected_name
    })

# ── MISC UTILS ────────────────────────────────────────────────

def curprof(request):
    uid = request.session.get('uid')
    role = request.session.get('user') # 'user' or 'worker'
    
    if role == 'user':
        u = registration.objects.get(id=uid)
    else:
        u = worker.objects.get(id=uid)
        
    if request.method == 'POST':
        u.name = request.POST.get('name')
        u.email = request.POST.get('email')
        u.phone = request.POST.get('phone')
        u.address = request.POST.get('address')
        u.location = request.POST.get('location')
        u.save()
        request.session['uname'] = u.name
        request.session['uemail'] = u.email
        return render(request, 'consumer/viewprofile.html', {'result': u, 'status': 'success'})
        
    return render(request, 'consumer/viewprofile.html', {'result': u})

def curnew(request):
    return render(request, 'consumer/viewnews.html', {'result': news.objects.all().order_by('-post_date')})

def cusview(request):
    return render(request, 'consumer/viewconsumer.html', {'result': complaints.objects.filter(cid=request.session.get('uid'))})

def download_receipt(request, id):
    return render(request, 'consumer/receipt.html', {'p': payment.objects.get(id=id)})

def analyze(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        r_date = request.POST.get('date')
        if r_date != today:
            return render(request, 'admin/analyzing.html', {'result': consumerr.objects.all(), 'status': 'failed', 'error': 'Invalid date Selected! Only today\'s date is allowed.', 'current_date': today})
        analyzing(meternumber=request.POST.get('number'), currentreading=request.POST.get('currentreading'), date=r_date).save()
        return render(request, 'admin/analyzing.html', {'result': consumerr.objects.all(), 'status': 'success', 'current_date': today})
    return render(request, 'admin/analyzing.html', {'result': consumerr.objects.all(), 'current_date': today})

def addanal(request):
    return render(request, 'admin/analyzing.html', {'result': consumerr.objects.all()})

def conss(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        f = request.POST.get('meternumber')
        u = meter.objects.get(meternumber=f)
        u.status = 'approved'
        u.save()
        consumerr(name=name, meter_number=f).save()
    return render(request, 'admin/consumer.html')

def addcon(request):
    return render(request, 'admin/consumer.html', {'result': registration.objects.all(), 'result1': meter.objects.filter(status='pending')})

def addelect(request):
    while True:
        meter_no = str(random.randint(100000, 999999))
        if not meter.objects.filter(meternumber=meter_no).exists():
            break
    return render(request, 'admin/meter.html', {'meter_no': meter_no})

def billss(request):
    if request.method == 'POST':
        cid, date, due, f, amount_str = request.POST.get('cid'), request.POST.get('date'), request.POST.get('duedate'), request.POST.get('customer_id'), request.POST.get('amount')
        
        try:
            # Validate Amount
            amount = float(amount_str)
            if amount < 1 or amount > 100000:
                raise ValueError("Incorrect range")
                
            # Validate Dates
            today_str = datetime.date.today().strftime('%Y-%m-%d')
            if date != today_str:
                return render(request, 'admin/bill.html', {'result': consumerr.objects.all(), 'status': 'failed', 'error': 'Invalid date Selected! Only today\'s date is allowed.', 'current_date': today_str})
                
            d1 = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            d2 = datetime.datetime.strptime(due, '%Y-%m-%d').date()
            if d2 < d1:
                return render(request, 'admin/bill.html', {'result': consumerr.objects.all(), 'status': 'failed', 'error': 'Due date cannot be before billing date.', 'current_date': datetime.date.today().strftime('%Y-%m-%d')})
                
        except (ValueError, TypeError):
             return render(request, 'admin/bill.html', {'result': consumerr.objects.all(), 'status': 'failed', 'error': 'Invalid amount or date format. Please check your entries.', 'current_date': datetime.date.today().strftime('%Y-%m-%d')})
            
        bills(consumerid=f, date=date, bill_amount=amount, due_date=due, status=request.POST.get('status'), cid=cid).save()
        
        # Simulate SMS notification
        try:
            user_info = registration.objects.filter(name=f).first()
            if user_info:
                phone = user_info.phone
                msg = f"EnergyMeter: New bill of Rs.{amount} generated for Meter {cid}. Due date: {due}."
                # Printing to console to simulate SMS sending
                print(f"\n[SMS SENT to {phone}]: {msg}\n")
        except Exception as e:
            print(f"SMS simulation failed: {e}")
            
        return render(request, 'admin/bill.html', {'result': consumerr.objects.all(), 'status': 'success', 'current_date': datetime.date.today().strftime('%Y-%m-%d')})
    return render(request, 'admin/bill.html', {'result': consumerr.objects.all(), 'current_date': datetime.date.today().strftime('%Y-%m-%d')})

def newss(request):
    if request.method == 'POST':
        today = datetime.date.today().strftime('%Y-%m-%d')
        if request.POST.get('postdate') != today:
            return render(request, 'admin/news.html', {'status': 'failed', 'error': 'Invalid date Selected! Only today\'s date is allowed.', 'zones': Zone.objects.all(), 'current_date': today})
        is_alert = True if request.POST.get('is_alert') == 'on' else False
        news(title=request.POST.get('title'), description=request.POST.get('description'), post_date=request.POST.get('postdate'), is_alert=is_alert, zone=request.POST.get('target_zone')).save()
        today = datetime.date.today().strftime('%Y-%m-%d')
        return render(request, 'admin/news.html', {'status': 'success', 'zones': Zone.objects.all(), 'current_date': today, 'all_news': news.objects.all().order_by('-post_date')})
    today = datetime.date.today().strftime('%Y-%m-%d')
    return render(request, 'admin/news.html', {'zones': Zone.objects.all(), 'current_date': today, 'all_news': news.objects.all().order_by('-post_date')})

def get_meter_usage(request):
    meter_no = request.GET.get('meter')
    name = request.GET.get('name')
    
    # Try to get latest real-time energy monitoring data
    latest_read = energy_data.objects.filter(uid=name).order_by('-date').first()
    if latest_read:
        return JsonResponse({'usage': latest_read.energy, 'source': 'Real-time Monitoring'})
        
    # Fallback to manual readings if no real-time data exists
    manual_read = analyzing.objects.filter(meternumber=meter_no).order_by('-date').first()
    if manual_read:
        try:
            return JsonResponse({'usage': float(manual_read.currentreading), 'source': 'Manual Analysis'})
        except: pass
        
    return JsonResponse({'usage': 0, 'source': 'None'})

def addbill(request):
    return render(request, 'admin/bill.html', {'result': consumerr.objects.all(), 'current_date': datetime.date.today().strftime('%Y-%m-%d')})

def addnews(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    return render(request, 'admin/news.html', {'current_date': today, 'zones': Zone.objects.all(), 'all_news': news.objects.all().order_by('-post_date')})

def delete_news(request, id):
    news.objects.get(id=id).delete()
    return redirect('addnews')


def com(request):
    return render(request, 'consumer/complaint.html')


def accept_bill(request, id):
    b = bills.objects.get(id=id)
    b.status = 'Accept'
    b.save()
    return redirect('viewbill')

def reject_bill(request, id):
    b = bills.objects.get(id=id)
    b.status = 'Reject'
    b.save()
    return redirect('viewbill')
