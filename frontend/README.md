`# Frontend for LLM Code Review Assistant

This is a minimal React frontend that lets users paste or upload a unified diff, submit it to the backend, and view the review results.

## Run locally

1. Install Node.js (16+).
2. From the `frontend` folder, install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

4. Open the app at `http://localhost:4000` and ensure your backend is running at `http://localhost:8000`.

## How it works

- The app sends a POST request to `http://localhost:8000/review` with JSON `{ diff: "..." }`.
- The backend returns a JSON review object which the frontend displays.
