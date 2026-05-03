import sys
from pathlib import Path

# Ensure project src is on path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Force stubbed LLM for local tests (avoids external network calls)
import os
os.environ.setdefault("FORCE_STUB_LLM", "1")

from src.app.api.review import review as review_fn


def main():
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
    # Call the endpoint function directly (avoids TestClient compatibility issues)
    result = review_fn(diff=sample_diff)
    print("Result:")
    print(result.model_dump_json())

if __name__ == "__main__":
    main()
