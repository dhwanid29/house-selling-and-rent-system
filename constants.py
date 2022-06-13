from house_selling import settings

if settings.DEBUG:
    host_url = "http://127.0.0.1:8000/api/user"
else:
    host_url = "https://house-selling-and-rent-system.herokuapp.com/api/user"
