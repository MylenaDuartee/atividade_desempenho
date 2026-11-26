
from locust import HttpUser, task, between


class PatientListUser(HttpUser):
    wait_time = between(0.2, 0.6)

    @task
    def listar_pacientes(self):
        with self.client.get(
            "/api/patients",
            name="GET /api/patients",
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"Status inesperado: {response.status_code}"
                )
                return

            try:
                patients = response.json()

                if not isinstance(patients, list):
                    response.failure("A resposta não é uma lista JSON.")
                    return

                if patients:
                    required_fields = {
                        "id", "name", "birthDate",
                        "nationalId", "active"
                    }

                    if not required_fields.issubset(patients[0].keys()):
                        response.failure("Campos esperados ausentes.")
                        return

                response.success()

            except (ValueError, TypeError):
                response.failure("Resposta JSON inválida.")
