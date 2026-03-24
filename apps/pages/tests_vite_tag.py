"""
Tests for the {% vite_asset %} template tag.

The tag reads Vite's manifest.json and outputs a <script> tag
with the correct hashed filename, instead of hardcoding it.
"""
import json
import tempfile
import os

from django.test import TestCase, override_settings
from django.template import Template, Context, TemplateSyntaxError


SAMPLE_MANIFEST = {
    "frontend/main.js": {
        "file": "assets/main-AbC123.js",
        "name": "main",
        "src": "frontend/main.js",
        "isEntry": True,
    }
}

MANIFEST_WITH_CSS = {
    "frontend/main.js": {
        "file": "assets/main-XyZ789.js",
        "name": "main",
        "src": "frontend/main.js",
        "isEntry": True,
        "css": ["assets/main-Def456.css"],
    }
}


class ViteAssetTagTest(TestCase):
    """Tests for the vite_asset template tag."""

    def setUp(self):
        # Always clear the manifest cache between tests to prevent leakage
        from apps.pages.templatetags import vite
        vite._manifest_cache = None

    def tearDown(self):
        from apps.pages.templatetags import vite
        vite._manifest_cache = None

    def _render(self, template_string, context=None):
        tpl = Template(template_string)
        return tpl.render(Context(context or {}))

    def _write_manifest(self, tmpdir, manifest_data):
        """Write a manifest.json into a temporary static/dist/.vite/ structure."""
        vite_dir = os.path.join(tmpdir, 'dist', '.vite')
        os.makedirs(vite_dir, exist_ok=True)
        manifest_path = os.path.join(vite_dir, 'manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(manifest_data, f)
        return tmpdir

    def test_tag_outputs_script_tag_with_hashed_filename(self):
        """The tag should read the manifest and output a script tag with the correct hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_manifest(tmpdir, SAMPLE_MANIFEST)
            with self.settings(STATICFILES_DIRS=[tmpdir], STATIC_URL='/static/'):
                output = self._render(
                    '{% load vite %}{% vite_asset "frontend/main.js" %}'
                )
                self.assertIn('main-AbC123.js', output)
                self.assertIn('<script', output)
                self.assertIn('type="module"', output)

    def test_tag_uses_static_url_prefix(self):
        """Output should be prefixed with STATIC_URL + dist/."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_manifest(tmpdir, SAMPLE_MANIFEST)
            with self.settings(STATICFILES_DIRS=[tmpdir], STATIC_URL='/static/'):
                output = self._render(
                    '{% load vite %}{% vite_asset "frontend/main.js" %}'
                )
                self.assertIn('/static/dist/assets/main-AbC123.js', output)

    def test_tag_includes_onerror_fallback(self):
        """Script tag should include onerror handler for graceful degradation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_manifest(tmpdir, SAMPLE_MANIFEST)
            with self.settings(STATICFILES_DIRS=[tmpdir], STATIC_URL='/static/'):
                output = self._render(
                    '{% load vite %}{% vite_asset "frontend/main.js" %}'
                )
                self.assertIn('onerror', output)

    def test_tag_emits_css_link_when_manifest_has_css(self):
        """When the manifest entry has CSS files, emit <link> tags before the script."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_manifest(tmpdir, MANIFEST_WITH_CSS)
            with self.settings(STATICFILES_DIRS=[tmpdir], STATIC_URL='/static/'):
                output = self._render(
                    '{% load vite %}{% vite_asset "frontend/main.js" %}'
                )
                self.assertIn('<link', output)
                self.assertIn('main-Def456.css', output)
                self.assertIn('rel="stylesheet"', output)

    def test_tag_raises_on_unknown_entry(self):
        """Requesting a non-existent entry should raise an exception."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_manifest(tmpdir, SAMPLE_MANIFEST)
            with self.settings(STATICFILES_DIRS=[tmpdir], STATIC_URL='/static/'):
                with self.assertRaises(Exception):
                    self._render(
                        '{% load vite %}{% vite_asset "nonexistent.js" %}'
                    )

    def test_tag_returns_empty_when_no_manifest_in_debug(self):
        """In DEBUG mode, if no manifest exists, output empty string (pre-build)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # No manifest written — tmpdir/dist/.vite/manifest.json doesn't exist
            with self.settings(STATICFILES_DIRS=[tmpdir], STATIC_URL='/static/', DEBUG=True):
                output = self._render(
                    '{% load vite %}{% vite_asset "frontend/main.js" %}'
                )
                self.assertEqual(output.strip(), '')

    def test_tag_requires_argument(self):
        """The tag must receive an entry name argument."""
        with self.assertRaises(TemplateSyntaxError):
            Template('{% load vite %}{% vite_asset %}')

    def test_homepage_uses_vite_asset_tag(self):
        """base.html should use {% vite_asset %} instead of a hardcoded filename."""
        response = self.client.get('/')
        content = response.content.decode()
        # Should NOT contain a hardcoded hash reference
        self.assertNotIn('main-D_rj2tQz.js', content)
        # Should contain the dynamically-resolved script from the manifest
        self.assertIn('<script', content)
        self.assertIn('type="module"', content)

    def test_manifest_is_cached_in_production(self):
        """In non-DEBUG mode, reading the manifest twice should use cached data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_manifest(tmpdir, SAMPLE_MANIFEST)
            with self.settings(STATICFILES_DIRS=[tmpdir], STATIC_URL='/static/', DEBUG=False):
                # Import here to get fresh module state
                from apps.pages.templatetags import vite
                vite._manifest_cache = None  # Reset cache

                output1 = self._render(
                    '{% load vite %}{% vite_asset "frontend/main.js" %}'
                )
                self.assertIn('main-AbC123.js', output1)

                # Overwrite the manifest file with a different hash
                self._write_manifest(tmpdir, {
                    "frontend/main.js": {
                        "file": "assets/main-CHANGED.js",
                        "src": "frontend/main.js",
                        "isEntry": True,
                    }
                })

                # Should still return the cached (old) value
                output2 = self._render(
                    '{% load vite %}{% vite_asset "frontend/main.js" %}'
                )
                self.assertIn('main-AbC123.js', output2)
                self.assertNotIn('main-CHANGED.js', output2)

                # Clean up for other tests
                vite._manifest_cache = None
