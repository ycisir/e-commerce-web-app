# e-commerce-web-app
A full-fledged e-commerce web application built using the power of Django. It leverages PostgreSQL for robust data storage, integrates the secure PayPal payment gateway, and implements various Django features to provide a user-friendly and feature-rich experience.

### Setup instructions
1. Create a Virtual Environment `python -m venv env-name`
2. Activate the Virtual Environment `source env-name/bin/activate`
4. Clone the repository `git clone https://github.com/ycisir/e-commerce-web-app`
5. Configure your database if any
6. Install dependencies `cd e_commerce_web_app` then `pip install -r requirements.txt`
7. Run python `manage.py makemigrations` Then, run python `manage.py migrate` to apply the migrations and update the database schema
8. Run the Django development server `python manage.py runserver`
