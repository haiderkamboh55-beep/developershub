"""
Run this ONCE after setting up the database to create:
- Admin user
- Sample services, portfolio, and blog data

Usage: python seed.py
"""

import psycopg2
import psycopg2.extras
import bcrypt
import os
from config import Config

def seed():
    db = psycopg2.connect(Config.DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    cur = db.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(100) UNIQUE NOT NULL, email VARCHAR(150) UNIQUE NOT NULL, password_hash TEXT NOT NULL, role VARCHAR(20) DEFAULT 'admin', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS services (id SERIAL PRIMARY KEY, title VARCHAR(200) NOT NULL, description TEXT, icon VARCHAR(100) DEFAULT 'code', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS portfolio (id SERIAL PRIMARY KEY, title VARCHAR(200) NOT NULL, description TEXT, image_url TEXT, tech_stack VARCHAR(300), project_url TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS blog_posts (id SERIAL PRIMARY KEY, title VARCHAR(300) NOT NULL, content TEXT NOT NULL, excerpt TEXT, author VARCHAR(100) DEFAULT 'Admin', image_url TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS inquiries (id SERIAL PRIMARY KEY, name VARCHAR(150) NOT NULL, email VARCHAR(150) NOT NULL, phone VARCHAR(30), message TEXT NOT NULL, status VARCHAR(50) DEFAULT 'unread', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS bookings (id SERIAL PRIMARY KEY, name VARCHAR(150) NOT NULL, email VARCHAR(150) NOT NULL, phone VARCHAR(30), date DATE NOT NULL, time_slot VARCHAR(50) NOT NULL, purpose TEXT, status VARCHAR(50) DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    """)

    # Admin user
    password_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')
    cur.execute("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING",
                ('admin', 'admin@developershub.com', password_hash, 'admin'))

    # Sample services
    services = [
        ('Web Development', 'We build fast, modern web applications using React, Next.js, and other cutting-edge frameworks.', 'web'),
        ('Backend & APIs', 'Scalable RESTful APIs and backend systems built with Node.js, Django, or Flask and PostgreSQL.', 'api'),
        ('Mobile Development', 'Cross-platform mobile apps using React Native that work seamlessly on iOS and Android.', 'mobile'),
        ('UI/UX Design', 'Beautiful, conversion-focused interfaces designed with the user experience at the forefront.', 'design'),
        ('Cloud & DevOps', 'Deployment, scaling, and CI/CD pipelines on AWS, GCP, or any cloud platform.', 'cloud'),
        ('AI Integration', 'Integrating AI and machine learning capabilities into your existing products.', 'ai'),
    ]
    for s in services:
        cur.execute("INSERT INTO services (title, description, icon) SELECT %s, %s, %s WHERE NOT EXISTS(SELECT 1 FROM services WHERE title = %s)", (*s, s[0]))

    # Sample portfolio
    portfolio = [
        ('E-Commerce Platform', 'A full-featured online store with cart, payments, and admin dashboard.', None, 'React, Node.js, PostgreSQL, Stripe', 'https://example.com'),
        ('SaaS Dashboard', 'Analytics dashboard for a B2B SaaS product with real-time charts.', None, 'Next.js, Flask, PostgreSQL, Chart.js', None),
        ('Healthcare Booking App', 'Patient appointment booking system with doctor management.', None, 'React, Django, PostgreSQL', 'https://example.com'),
        ('Real Estate Platform', 'Property listing platform with map integration and advanced search.', None, 'React, Node.js, MongoDB, Google Maps', None),
    ]
    cur.execute("SELECT COUNT(*) FROM portfolio")
    if cur.fetchone()['count'] == 0:
        for p in portfolio:
            cur.execute("INSERT INTO portfolio (title, description, image_url, tech_stack, project_url) VALUES (%s, %s, %s, %s, %s)", p)

    # Sample blog posts
    blog = [
        ('How to Build a REST API with Flask and PostgreSQL', 'Flask is a lightweight and flexible Python web framework that makes it easy to build REST APIs. In this tutorial, we will walk through building a complete API with authentication, database integration, and proper error handling.\n\nFirst, install the required packages:\n\n```\npip install flask flask-cors psycopg2-binary PyJWT\n```\n\nThen create your Flask app and connect to PostgreSQL...', 'Step-by-step guide to building production-ready REST APIs with Flask and PostgreSQL.'),
        ('React Best Practices in 2025', 'Modern React development has evolved significantly. Here are the key best practices every developer should follow in 2025.\n\n1. Always use functional components with hooks\n2. Implement proper error boundaries\n3. Use React Query or SWR for data fetching\n4. Memoize expensive computations with useMemo\n\nThese practices will help you write cleaner, more performant React code...', 'Modern best practices for React development in 2025, from hooks to performance optimization.'),
        ('Why PostgreSQL is the Best Database for Most Projects', 'PostgreSQL has become the go-to relational database for modern web applications. Here is why you should choose it for your next project.\n\nPostgres offers excellent JSON support, full-text search, powerful indexing, and ACID compliance. It scales well for most use cases and has amazing tooling...', 'An in-depth look at why PostgreSQL stands out among relational databases for web development.'),
    ]
    cur.execute("SELECT COUNT(*) FROM blog_posts")
    if cur.fetchone()['count'] == 0:
        for b in blog:
            cur.execute("INSERT INTO blog_posts (title, content, excerpt, author) VALUES (%s, %s, %s, %s)", (*b, 'Admin'))

    db.commit()
    cur.close()
    db.close()

    print("Database seeded successfully!")
    print("Admin login: admin@developershub.com")
    print("Password: admin123")
    print("\nIMPORTANT: Change the admin password after first login!")

if __name__ == '__main__':
    seed()
