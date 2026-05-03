from fastapi.testclient import TestClient
from src.app.main import app


def test_review_endpoint_basic():
    client = TestClient(app)
    sample_diff = """
diff --git a/src/example.py b/src/example.py
index 0000000..1111111 100644
--- a/src/example.py
+++ b/src/example.py
@@ -1,3 +1,6 @@
 def add(a, b):
-    return a+b
+    return a + b  # fixed spacing

"""

    resp = client.post("/review", json={"diff": sample_diff})
    assert resp.status_code == 200
    data = resp.json()
    assert "summary" in data
    assert "comments" in data
