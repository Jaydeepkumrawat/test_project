Prerequisites
Python 3.x 
pip 
Virtualenv (For creating isolated environments)

Create the virtual environment ->  python -m venv env
activate env -> .\env\Scripts\activate
git clone 
cd repo_name
Install requrements -> pip install -r requirements.txt
Create mysql database and change the dbname, username and password in settings.py file
Run the redis (used for cache)
Run migrations -> python manage.py migrate 
Run server -> python manage.py runserver

registerurl POST -> http://127.0.0.1:8000/api/accounts/v1/register/
loginurl POST -> http://127.0.0.1:8000/api/accounts/v1/login/

createitem POST -> http://127.0.0.1:8000/api/inventory/v1/items/
getallitem GET -> http://127.0.0.1:8000/api/inventory/v1/items/

getoneitem GET -> http://127.0.0.1:8000/api/inventory/v1/items/1/
updateitem PATCH ->  http://127.0.0.1:8000/api/inventory/v1/items/1/
deleteitem DELETE -> http://127.0.0.1:8000/api/inventory/v1/items/1/

