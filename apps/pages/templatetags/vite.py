"""
Custom template tag to resolve Vite manifest entries.

Usage in templates:
    {% load vite %}
    {% vite_asset "frontend/main.js" %}

Outputs a <script type="module"> tag (and optional <link rel="stylesheet">
tags) with the correct content-hashed filename from Vite's manifest.json.
"""
import json
import os

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

_manifest_cache = None


def _find_manifest_path():
    """Locate the Vite manifest.json in STATICFILES_DIRS."""
    for static_dir in getattr(settings, 'STATICFILES_DIRS', []):
        path = os.path.join(str(static_dir), 'dist', '.vite', 'manifest.json')
        if os.path.isfile(path):
            return path
    return None


def _load_manifest():
    """Load and return the parsed Vite manifest, with production caching."""
    global _manifest_cache

    if _manifest_cache is not None and not settings.DEBUG:
        return _manifest_cache

    manifest_path = _find_manifest_path()
    if manifest_path is None:
        if settings.DEBUG:
            return None
        raise FileNotFoundError(
            'Vite manifest.json not found. Run "npm run build" first.'
        )

    with open(manifest_path) as f:
        manifest = json.load(f)

    if not settings.DEBUG:
        _manifest_cache = manifest

    return manifest


@register.simple_tag
def vite_asset(entry_name):
    """
    Resolve a Vite entry point to its built asset tags.

    Returns one or more HTML tags:
    - <link rel="stylesheet"> for any extracted CSS
    - <script type="module"> for the JS bundle
    """
    manifest = _load_manifest()

    if manifest is None:
        # DEBUG mode, no manifest yet (pre-build)
        return ''

    if entry_name not in manifest:
        raise template.TemplateSyntaxError(
            f'Vite manifest has no entry "{entry_name}". '
            f'Available entries: {", ".join(manifest.keys())}'
        )

    entry = manifest[entry_name]
    static_url = settings.STATIC_URL
    tags = []

    # Emit CSS links first
    for css_file in entry.get('css', []):
        tags.append(
            f'<link rel="stylesheet" href="{static_url}dist/{css_file}">'
        )

    # Emit the JS module script
    js_file = entry['file']
    tags.append(
        f'<script type="module" src="{static_url}dist/{js_file}" '
        f'onerror="this.remove()"></script>'
    )

    return mark_safe('\n'.join(tags))
