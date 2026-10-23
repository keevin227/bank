#!/usr/bin/env python3
"""Build encrypted static presentation assets; read the password interactively."""
import base64
import getpass
import json
import mimetypes
import os
from pathlib import Path
import re

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'presentation'
OUTPUT = ROOT / 'docs'
ITERATIONS = 600_000


def main():
    password = getpass.getpass('Presentation password (not saved): ')
    if not password:
        raise SystemExit('A non-empty password is required.')
    html = (SOURCE / 'index.html').read_text()
    css = (SOURCE / 'style.css').read_text()
    javascript = (SOURCE / 'presentation.js').read_text()
    product_visuals = (SOURCE / 'valuegram-visuals.js').read_text()
    html = html.replace('<link rel="stylesheet" href="style.css">', '<style>' + css + '</style>')
    html = html.replace('<script defer src="presentation.js"></script>', '')
    html = html.replace('<script defer src="valuegram-visuals.js"></script>', '')

    def inline_image(match):
        path = SOURCE / match.group(1)
        mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        return 'src="data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode() + '"'

    html = re.sub(r'src="(assets/[^\"]+)"', inline_image, html)
    html = html.replace('<button id="print"', '<button id="download-pdf" aria-label="Download PDF" title="Download PDF">↓</button><button id="lock-presentation" aria-label="Lock presentation" title="Lock presentation">⌂</button><button id="print"')
    html = html.replace('</body>', '<script>' + javascript.replace('</script', '<\\/script') + '</script><script>' + product_visuals.replace('</script', '<\\/script') + '</script></body>')

    salt = os.urandom(16)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS).derive(password.encode())
    cipher = AESGCM(key)
    OUTPUT.mkdir(exist_ok=True)

    def encrypt(content, filename):
        nonce = os.urandom(12)
        (OUTPUT / filename).write_bytes(nonce + cipher.encrypt(nonce, content, None))

    encrypt(html.encode(), 'presentation.bin')
    encrypt((SOURCE / 'Bank-Muscat-The-Intelligent-Bank.pdf').read_bytes(), 'handout.bin')
    (OUTPUT / 'manifest.json').write_text(json.dumps({'version': 1, 'kdf': 'PBKDF2-SHA-256', 'iterations': ITERATIONS, 'salt': base64.b64encode(salt).decode(), 'cipher': 'AES-256-GCM', 'nonce_bytes': 12}, indent=2) + '\n')
    print('Built encrypted presentation and PDF. No password or plaintext presentation was written to docs/.')


if __name__ == '__main__':
    main()
