# Protected presentation

GitHub Pages publishes `docs/` through `.github/workflows/publish-presentation.yml`.

- `docs/index.html` is the password entry page.
- The slide document, JavaScript, styles and images are bundled and encrypted in `presentation.bin`.
- The PDF is separately encrypted in `handout.bin` and is decrypted only after unlocking and requesting a download.
- AES-256-GCM uses a fresh random nonce per file. PBKDF2-SHA-256 derives the key with a random salt and 600,000 iterations.
- The password is entered interactively during packaging. It is not embedded in the gate, build script or workflow, and the browser does not save it.
- Reloading or using the lock button returns to the password page.

The editable presentation and plaintext PDF remain local under `presentation/`, excluded by `.gitignore`. To rebuild, install Python `cryptography`, restore the local presentation source and run `python scripts/build-protected-presentation.py`, then commit the new encrypted outputs.

This protects this published presentation bundle. Existing documents and images previously committed to this public repository retain their original visibility. Downloaded or unlocked material can be saved by an authorised viewer.

If GitHub refuses initial Pages creation using `GITHUB_TOKEN`, enable **Settings → Pages → Build and deployment → Source: GitHub Actions** once, then rerun the workflow.
