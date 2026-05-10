Automated Meter Reading System For Efficient Electricity Monitoring

Project Description
The Automated Meter Reading System is an IoT-based smart electricity monitoring system developed using ESP8266 and Django. The system helps in real-time electricity monitoring, automated bill generation, complaint management, and efficient electricity distribution management.


Features
- Real-time electricity monitoring
- Automated meter reading
- Bill generation and payment management
- Complaint management system
- Admin, Consumer, and Employee modules
- Zone-based electricity management
- New electricity connection requests
- Usage history and bill history
- Accurate electricity bill calculation


Technologies Used
- Python
- Django
- HTML
- CSS
- JavaScript
- SQLite / MySQL
- ESP8266
- IoT Sensors


Modules

Admin Module
- Manage consumers and employees
- Generate electricity bills
- Monitor electricity usage
- Manage zones and alerts

Consumer Module
- View electricity usage
- Pay bills
- Register complaints
- Apply for new connections

Employee Module
- View assigned tasks
- Update maintenance status
- Resolve complaints


How to Run the Project

1. Clone the repository
2. Open project in VS Code
3. Install requirements

```bash
pip install -r requirements.txt

4. Run migrations

```bash
python manage.py migrate
```

5. Start the server

```bash
python manage.py runserver
```

6. Open browser and visit

http://127.0.0.1:8000/

---

Screenshots

### Login Page
![Login Page](screenshots/login.png)

---

## Admin Dashboard

### Dashboard
![Admin Dashboard](screenshots/admin_dashboard.png)

### Add News
![Add News](screenshots/admin_add_news.png)

### Analysis Chart
![Analysis Chart](screenshots/admin_chart.png)

### Dispatch Employee
![Dispatch Employee](screenshots/admin_dispatch_employee.png)

### Generate Bill
![Generate Bill](screenshots/admin_generate_bill.png)

### Manage Requests
![Manage Requests](screenshots/admin_manage_request.png)

### View Bills
![View Bills](screenshots/admin_view_bills.png)

---

## Consumer Dashboard

### Consumer Dashboard
![Consumer Dashboard](screenshots/consumer_dashboard.png)

### Consumer Bills
![Consumer Bills](screenshots/consumer_bills.png)

### Complaint Page
![Complaint Page](screenshots/consumer_complaint.png)

### Energy Monitoring
![Energy Monitoring](screenshots/consumer_monitoring.png)

---

## Employee Dashboard

### Employee Dashboard
![Employee Dashboard](screenshots/employee_dashboard.png)

### Task List
![Task List](screenshots/employee_task_list.png)
---

## 📄 License
This project is developed for educational purposes.