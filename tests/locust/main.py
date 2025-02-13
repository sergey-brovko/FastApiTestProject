from locust import HttpUser, between, task


class RPSTest(HttpUser):
    wait_time = between(0.1, 1.5)

    @task
    def wallet_operation(self):
        self.client.post("/api/v1/wallets/8dc36420-9bad-43c4-a253-930262f08153/operation",
                         json={"operationType": "DEPOSIT", "amount": 0.1})

    @task
    def get_balance(self):
        self.client.get("/api/v1/wallets/8dc36420-9bad-43c4-a253-930262f08153")
