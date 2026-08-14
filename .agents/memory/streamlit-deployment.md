---
name: Streamlit deployment entrypoint
description: Deployment-specific entrypoint and port requirements for the Streamlit dashboard.
---

The Streamlit deployment must use a root-level `main.py` entrypoint and bind to port 8080; the validated `.replit` deployment run command is the source of truth.

**Why:** The workspace's legacy artifact services can occupy the expected web port and route the published root to a 404 instead of the Streamlit app.

**How to apply:** Keep the Streamlit workflow and deployment command aligned on `main.py` and port 8080, and stop legacy API/mockup services before verifying or publishing.