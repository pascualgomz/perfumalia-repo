# perfumalia-repo
1. Clone repository: 
git clone https://github.com/pascualgomz/taller1.git

2. Create a virtual environment: 
python -m venv env

3. Activate virtual environment: 
Linux: source env/bin/activate
Windows: env\Scripts\activate

4. Install required dependencies: 
pip install -r requirements.txt

5. Run database migrations: 
python perfumalia/manage.py makemigrations
python perfumalia/manage.py migrate

6. Seed the database:
python perfumalia/manage.py seed_users

7. Start the server: 
python perfumalia/manage.py runserver
