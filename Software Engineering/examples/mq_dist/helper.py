import requests as r
import random
import string

with r.Session() as conn:
    for i in range(50):
        conn.post(
            url="http://127.0.0.1:5000/add",
            json={
                "target": "".join(random.choices(string.ascii_lowercase, k=2))
            }
        )