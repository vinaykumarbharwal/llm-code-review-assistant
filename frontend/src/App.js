import React from 'react';
import './App.css';

const SAMPLE_DIFF = `diff --git a/src/auth/login.py b/src/auth/login.py
index 0000000..1111111 100644
--- a/src/auth/login.py
+++ b/src/auth/login.py
@@ -1,8 +1,9 @@
-import sqlite3
-
-def authenticate(user_id, password):
-    conn = sqlite3.connect('db.sqlite3')
-    cursor = conn.cursor()
-    # insecure: user input interpolated directly into SQL
-    cursor.execute(f"SELECT * FROM users WHERE id = {user_id} AND password = '{password}'")
-    return cursor.fetchone() is not None
+import sqlite3
+import logging
+
+def authenticate(user_id, password):
+    conn = sqlite3.connect('db.sqlite3')
+    cursor = conn.cursor()
+    # insecure: user input interpolated directly into SQL
+    cursor.execute(f"SELECT * FROM users WHERE id = {user_id} AND password = '{password}'")
+    return cursor.fetchone() is not None`;

function App() {
  const [diff, setDiff] = React.useState('');
  const [result, setResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');

  async function submitDiff() {
    if (!diff.trim()) {
      setError('Paste a diff or load the sample diff.');
      setResult(null);
      return;
    }

    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://localhost:8000/review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ diff })
      });

      if (!res.ok) {
        const message = await res.text();
        throw new Error(message || `Request failed with status ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (e) {
      setResult(null);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  function handleFile(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => setDiff(ev.target.result);
    reader.readAsText(file);
  }

  function loadSampleDiff() {
    setDiff(SAMPLE_DIFF);
    setResult(null);
    setError('');
  }

  function clearAll() {
    setDiff('');
    setResult(null);
    setError('');
  }

  return (
    <main className="app">
      <section className="panel">
        <p className="eyebrow">LLM Code Review</p>
        <h1>Review a diff</h1>
        <p className="intro">Paste a unified diff, upload a patch, or load the sample diff.</p>

        <div className="actions">
          <button type="button" className="secondary-button" onClick={loadSampleDiff}>
            Load sample diff
          </button>
          <button type="button" className="ghost-button" onClick={clearAll}>
            Clear
          </button>
        </div>

        <textarea
          value={diff}
          onChange={(e) => setDiff(e.target.value)}
          placeholder="Paste unified diff here"
          rows={14}
          className="diff-input"
        />

        <div className="controls">
          <label className="file-picker">
            <input type="file" accept=".diff,.patch,.txt" onChange={handleFile} />
            <span>Choose file</span>
          </label>

          <button type="button" className="primary-button" onClick={submitDiff} disabled={loading}>
            {loading ? 'Reviewing...' : 'Review'}
          </button>
        </div>

        {error ? <div className="message error">{error}</div> : null}
      </section>

      <section className="panel result-panel">
        <h2>Result</h2>

        {result ? (
          result.error ? (
            <div className="message error">Error: {result.error}</div>
          ) : (
            <div className="result-stack">
              <div className="summary-box">
                <strong>Summary</strong>
                <p>{result.summary}</p>
              </div>

              <div>
                <strong>Comments</strong>
                {result.comments && result.comments.length ? (
                  <div className="comment-list">
                    {result.comments.map((comment, index) => (
                      <article key={index} className="comment-card">
                        <div className="comment-top">
                          <span>{comment.file}</span>
                          <span className="severity">
                            {comment.severity} / {comment.category}
                          </span>
                        </div>
                        <p>
                          Lines {comment.line_start}-{comment.line_end}
                        </p>
                        <p>{comment.message}</p>
                        {comment.suggested_fix ? <pre>{comment.suggested_fix}</pre> : null}
                      </article>
                    ))}
                  </div>
                ) : (
                  <p className="empty">No comments returned.</p>
                )}
              </div>
            </div>
          )
        ) : (
          <p className="empty">Run a review to see the response here.</p>
        )}
      </section>
    </main>
  );
}

export default App;
