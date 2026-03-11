# How Your Data Will Show in PostgreSQL

## 📊 Database Structure in pgAdmin4

### After Setup, You'll See:

```
PostgreSQL 18
└── Databases
    └── waste_management_db  ← Your database
        └── Schemas
            └── public
                └── Tables  ← Your data tables
                    ├── auth_group
                    ├── auth_group_permissions
                    ├── auth_permission
                    ├── companies_companywasterequest  ← Company requests
                    ├── companies_wastetype  ← Waste types
                    ├── core_blogpost  ← Blog posts
                    ├── core_contactmessage  ← Contact messages
                    ├── django_admin_log
                    ├── django_content_type
                    ├── django_migrations
                    ├── django_session
                    ├── pickups_pickuprequest  ← Pickup requests
                    └── users_user  ← Users and companies
```

---

## 📋 Table: companies_companywasterequest

**What it stores:** Company waste material requests

**Columns:**
```
id              | integer      | Primary Key
company_id      | integer      | Foreign Key → users_user
waste_type_id   | integer      | Foreign Key → companies_wastetype
quantity        | decimal      | Amount requested
unit            | varchar(20)  | kg, tons, etc.
description     | text         | What they need it for
status          | varchar(20)  | pending, approved, fulfilled, cancelled
created_at      | timestamp    | When request was made
updated_at      | timestamp    | Last update
```

**Example Data:**
```
id | company_id | waste_type_id | quantity | unit | description              | status   | created_at
---+------------+---------------+----------+------+--------------------------+----------+------------
1  | 5          | 1             | 500.00   | kg   | Need plastic for recycl  | pending  | 2026-03-10
2  | 7          | 3             | 1000.00  | kg   | Metal for manufacturing  | approved | 2026-03-09
3  | 8          | 2             | 750.00   | kg   | Paper for pulp mill      | fulfilled| 2026-03-08
```

**How to View in pgAdmin4:**
1. Navigate to: Databases → waste_management_db → Schemas → public → Tables
2. Right-click `companies_companywasterequest`
3. Select "View/Edit Data" → "All Rows"

**You'll see:**
- Which company (company_id links to users_user table)
- What waste type they want (waste_type_id links to companies_wastetype)
- How much they need (quantity + unit)
- Why they need it (description)
- Current status (pending, approved, fulfilled)
- When they requested it (created_at)

---

## 📋 Table: pickups_pickuprequest

**What it stores:** User pickup requests

**Columns:**
```
id                  | integer      | Primary Key
user_id             | integer      | Foreign Key → users_user
waste_type_id       | integer      | Foreign Key → companies_wastetype
location            | varchar(255) | Pickup address
pickup_date         | date         | Scheduled date
pickup_time         | time         | Scheduled time
quantity_estimate   | varchar(50)  | Estimated amount
special_instructions| text         | Additional notes
status              | varchar(20)  | pending, confirmed, in_progress, completed
created_at          | timestamp    | When request was made
updated_at          | timestamp    | Last update
```

**Example Data:**
```
id | user_id | waste_type_id | location        | pickup_date | quantity_estimate | status    | created_at
---+---------+---------------+-----------------+-------------+-------------------+-----------+------------
1  | 3       | 1             | 123 Main St     | 2026-03-15  | 50 kg            | pending   | 2026-03-10
2  | 4       | 5             | 456 Oak Ave     | 2026-03-16  | 20 kg            | confirmed | 2026-03-09
3  | 6       | 2             | 789 Elm St      | 2026-03-14  | 100 kg           | completed | 2026-03-08
```

**How to View in pgAdmin4:**
1. Navigate to: Tables → `pickups_pickuprequest`
2. Right-click → "View/Edit Data" → "All Rows"

**You'll see:**
- Who requested pickup (user_id links to users_user)
- What waste type (waste_type_id links to companies_wastetype)
- Where to pickup (location)
- When to pickup (pickup_date, pickup_time)
- How much waste (quantity_estimate)
- Current status (pending, confirmed, in_progress, completed)

---

## 📋 Table: users_user

**What it stores:** All users (regular users and companies)

**Columns:**
```
id              | integer      | Primary Key
username        | varchar(150) | Login username
email           | varchar(254) | Email address
password        | varchar(128) | Encrypted password
first_name      | varchar(150) | First name
last_name       | varchar(150) | Last name
user_type       | varchar(20)  | 'regular' or 'company'
phone           | varchar(20)  | Phone number
address         | text         | Address
company_name    | varchar(200) | Company name (if company)
reward_points   | integer      | Reward points
is_staff        | boolean      | Admin access
is_active       | boolean      | Account active
created_at      | timestamp    | Registration date
```

**Example Data:**
```
id | username    | email              | user_type | phone        | company_name      | is_staff | created_at
---+-------------+--------------------+-----------+--------------+-------------------+----------+------------
1  | admin       | admin@example.com  | regular   | NULL         | NULL              | true     | 2026-03-01
2  | john_doe    | john@email.com     | regular   | 123-456-7890 | NULL              | false    | 2026-03-05
3  | abc_recycl  | abc@recycling.com  | company   | 555-123-4567 | ABC Recycling Co  | false    | 2026-03-06
```

**How to View in pgAdmin4:**
1. Navigate to: Tables → `users_user`
2. Right-click → "View/Edit Data" → "All Rows"

**You'll see:**
- All registered users
- User type (regular or company)
- Contact information
- Company name (for company accounts)
- Admin status (is_staff)

---

## 📋 Table: companies_wastetype

**What it stores:** Types of waste materials

**Columns:**
```
id          | integer      | Primary Key
name        | varchar(100) | Waste type name
description | text         | Description
```

**Example Data:**
```
id | name      | description
---+-----------+----------------------------------------------------------
1  | Plastic   | Plastic bottles, containers, packaging materials
2  | Paper     | Newspapers, cardboard, office paper, magazines
3  | Metal     | Aluminum cans, steel cans, metal scraps
4  | Glass     | Glass bottles, jars, broken glass
5  | E-waste   | Electronic devices, computers, phones, batteries
6  | Organic   | Food waste, garden waste, biodegradable materials
7  | Hazardous | Chemicals, paints, oils, toxic materials
8  | Textile   | Old clothes, fabric scraps, shoes
9  | Wood      | Wooden furniture, timber, pallets
10 | Mixed     | Mixed recyclable materials
```

**How to View in pgAdmin4:**
1. Navigate to: Tables → `companies_wastetype`
2. Right-click → "View/Edit Data" → "All Rows"

---

## 📋 Table: core_blogpost

**What it stores:** Blog posts

**Columns:**
```
id         | integer      | Primary Key
title      | varchar(200) | Blog title
content    | text         | Blog content
author     | varchar(100) | Author name
image      | varchar(100) | Image path (optional)
created_at | timestamp    | Publication date
```

**Example Data:**
```
id | title                                  | author | created_at
---+----------------------------------------+--------+------------
1  | The Importance of Waste Segregation    | Admin  | 2026-03-01
2  | How Recycling Helps Combat Climate...  | Admin  | 2026-03-01
3  | E-Waste Management: A Growing Chall... | Admin  | 2026-03-01
```

---

## 🔍 How to Query Data in pgAdmin4

### View All Company Requests with Company Names:

```sql
SELECT 
    u.username AS company_name,
    u.email AS company_email,
    wt.name AS waste_type,
    cwr.quantity,
    cwr.unit,
    cwr.status,
    cwr.created_at
FROM companies_companywasterequest cwr
JOIN users_user u ON cwr.company_id = u.id
JOIN companies_wastetype wt ON cwr.waste_type_id = wt.id
ORDER BY cwr.created_at DESC;
```

**Result:**
```
company_name  | company_email      | waste_type | quantity | unit | status   | created_at
--------------+--------------------+------------+----------+------+----------+------------
ABC Recycling | abc@recycling.com  | Plastic    | 500.00   | kg   | pending  | 2026-03-10
XYZ Corp      | xyz@company.com    | Metal      | 1000.00  | kg   | approved | 2026-03-09
```

### View All Pickup Requests with User Details:

```sql
SELECT 
    u.username AS user_name,
    u.email AS user_email,
    wt.name AS waste_type,
    pr.location,
    pr.pickup_date,
    pr.status,
    pr.created_at
FROM pickups_pickuprequest pr
JOIN users_user u ON pr.user_id = u.id
JOIN companies_wastetype wt ON pr.waste_type_id = wt.id
ORDER BY pr.pickup_date DESC;
```

**Result:**
```
user_name | user_email      | waste_type | location     | pickup_date | status    | created_at
----------+-----------------+------------+--------------+-------------+-----------+------------
john_doe  | john@email.com  | Plastic    | 123 Main St  | 2026-03-15  | pending   | 2026-03-10
jane_s    | jane@email.com  | E-waste    | 456 Oak Ave  | 2026-03-16  | confirmed | 2026-03-09
```

### Count Requests by Status:

```sql
-- Company Requests
SELECT status, COUNT(*) as count
FROM companies_companywasterequest
GROUP BY status;

-- Pickup Requests
SELECT status, COUNT(*) as count
FROM pickups_pickuprequest
GROUP BY status;
```

### Count Requests by Waste Type:

```sql
SELECT 
    wt.name AS waste_type,
    COUNT(pr.id) AS pickup_count,
    COUNT(cwr.id) AS company_request_count
FROM companies_wastetype wt
LEFT JOIN pickups_pickuprequest pr ON wt.id = pr.waste_type_id
LEFT JOIN companies_companywasterequest cwr ON wt.id = cwr.waste_type_id
GROUP BY wt.name
ORDER BY pickup_count DESC;
```

---

## 📊 How to View in pgAdmin4 (Step by Step)

### Method 1: View Table Data

1. **Open pgAdmin4**
2. **Expand:** Servers → PostgreSQL 18 → Databases → waste_management_db
3. **Expand:** Schemas → public → Tables
4. **Right-click on any table** (e.g., `companies_companywasterequest`)
5. **Select:** View/Edit Data → All Rows
6. **You'll see:** All data in a spreadsheet-like view

### Method 2: Run SQL Queries

1. **Right-click on** `waste_management_db`
2. **Select:** Query Tool
3. **Type or paste SQL query**
4. **Click Execute** (▶) or press F5
5. **View results** in the bottom panel

### Method 3: Use Django Admin

1. **Start server:** `python manage.py runserver`
2. **Go to:** http://localhost:8000/admin/
3. **Login:** admin / admin123
4. **Click on any model** to view data in a user-friendly interface

---

## 🎯 Summary

**In PostgreSQL, you'll see:**

1. **Database:** `waste_management_db`
2. **Tables:** 13+ tables storing all your data
3. **Company Requests:** Which company wants what waste type
4. **Pickup Requests:** Which user scheduled pickup for what waste
5. **Users:** All registered users and companies
6. **Waste Types:** 10 types of waste materials
7. **Blog Posts:** All blog articles
8. **Contact Messages:** All contact form submissions

**All data is organized in relational tables with foreign keys linking them together!**
