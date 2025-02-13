from locust import HttpUser, between, task


class RPSTest(HttpUser):
    wait_time = between(0.1, 0.2)

    @task
    def wallet_operation(self):
        self.client.post("/api/v1/wallets/8468bce4-98b1-4364-a590-96741f6c002f/operation",
                         json={"operationType": "DEPOSIT", "amount": 0.1})

    @task
    def get_balance(self):
        self.client.get("/api/v1/wallets/8468bce4-98b1-4364-a590-96741f6c002f")
