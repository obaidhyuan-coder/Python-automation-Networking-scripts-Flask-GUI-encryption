# Flask backup example

The Flask code under `src/` is intentionally separate from the Tkinter desktop application. It is a small localhost-only demonstration of a JSON request, path validation, archive creation, and backup rotation.

Run it with:

```bash
python -m src.app
```

This example is not required to run the desktop vault. Do not deploy it to an untrusted network without adding authentication, authorization, TLS, rate limiting, and a security review.
