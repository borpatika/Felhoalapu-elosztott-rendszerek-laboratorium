from locust import HttpUser, task, between
from bs4 import BeautifulSoup

class PhotoAlbumUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """
        Felhasználó belépése a teszt előtt.
        """
        login_page = self.client.get("/accounts/login/")
        soup = BeautifulSoup(login_page.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        self.client.post("/accounts/login/", {
            "username": "testuser",
            "password": "testpassword",
            "csrfmiddlewaretoken": csrf_token
        }, headers={
            "Referer": self.client.base_url + "/accounts/login/"
        })

    @task(3)
    def list_photos(self):
        """Főoldal lekérése (photo list)."""
        self.client.get("/")

    @task(2)
    def view_photo(self):
        """Egy adott fotó részleteinek lekérése."""
        self.client.get("/photo/3/")

    @task(1)
    def upload_photo(self):
        """
        Fotó feltöltése:
        """
        upload_page = self.client.get("/upload/")
        soup = BeautifulSoup(upload_page.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        with open("test.jpg", "rb") as f:
            self.client.post("/upload/", {
                "name": "Test",
                "csrfmiddlewaretoken": csrf_token
            }, files={"image": f}, headers={
                "Referer": self.client.base_url + "/upload/"
            })