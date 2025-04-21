from locust import HttpUser, task, between


class ApiUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_historical_data(self):
        self.client.get("/api/historical-data?currency=php&high_date=2024-04-17&low_date=2024-04-16")
