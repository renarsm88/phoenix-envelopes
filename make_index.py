#!/usr/bin/env python3
"""Build index.html for the hosted copy from the single source of truth."""
from pathlib import Path

SRC = Path.home() / "Desktop/Finance/Phoenix Budget/spending-tracker.html"
OUT = Path(__file__).resolve().parent / "index.html"

s = SRC.read_text(encoding="utf-8")

# Off claude.ai there is no shared store, so say what actually happens here
# rather than leaving copy that reads like something is broken.
s = s.replace(
    "Saved in this browser only, on this device. Nobody else sees these numbers.",
    "Saved on this phone. Nothing leaves the device and nothing is sent anywhere.")
s = s.replace(
    "Saved in this browser only, on this device.",
    "Saved on this phone. Nothing leaves the device and nothing is sent anywhere.")
s = s.replace(
    "Saved in this browser only. Connecting to the shared copy\\u2026",
    "Saved on this phone.")
s = s.replace(
    "<p>Envelope amounts come from",
    "<p><strong>Add this page to your home screen</strong> so it opens like an app: in Safari "
    "tap Share, then Add to Home Screen. Your entries live on this device, so use the same "
    "phone each time and do not clear website data.</p>\n    <p>Envelope amounts come from")

# Icon, name and standalone behaviour, so she can put it on her home screen or
# desktop and get the desert sunset rather than a browser default.
HEAD = """<link rel="icon" type="image/png" sizes="32x32" href="favicon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#46617D">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Envelopes">
<meta name="application-name" content="Envelopes">
"""
s = HEAD + s

OUT.write_text(s, encoding="utf-8")
print("built", OUT, len(s), "bytes")
