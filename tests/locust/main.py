from locust import HttpUser, between, task


class RPSTest(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def wallet_operation(self):
        self.client.post("/api/v1/wallets/78ebe419-aa2d-4147-9145-47443bf8c068/operation",
                         json={
                             "operationType": "DEPOSIT",
                             "amount": 0.1
                         }
                         )

    @task
    def get_balance(self):
        self.client.get("/api/v1/wallets/78ebe419-aa2d-4147-9145-47443bf8c068")
