GitHub Pages Setup Guide
========================

This document provides instructions for setting up GitHub Pages for SyInfo documentation.

Prerequisites
------------

* GitHub repository with admin access
* Sphinx documentation built
* GitHub Actions enabled

Setup Steps
----------

1. **Enable GitHub Pages**

   * Go to repository Settings > Pages
   * Source: Deploy from a branch
   * Branch: gh-pages
   * Folder: / (root)
   * Click Save

2. **Create GitHub Actions Workflow**

   Create `.github/workflows/docs.yml`:

   .. code-block:: yaml

      name: Build and Deploy Documentation
      
      on:
        push:
          branches: [ main, master ]
        pull_request:
          branches: [ main, master ]
      
      jobs:
        build-docs:
          runs-on: ubuntu-latest
          
          steps:
          - uses: actions/checkout@v3
          
          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.9'
          
          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install sphinx sphinx-rtd-theme
              pip install -e .
          
          - name: Build documentation
            run: |
              cd docs
              make html
          
          - name: Deploy to GitHub Pages
            if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
            uses: peaceiris/actions-gh-pages@v3
            with:
              github_token: ${{ secrets.GITHUB_TOKEN }}
              publish_dir: ./docs/_build/html

3. **Configure Sphinx for GitHub Pages**

   Update `docs/conf.py`:

   .. code-block:: python

      # GitHub Pages settings
      html_baseurl = 'https://mr901.github.io/syinfo/'
      
      # Add GitHub Pages extension
      extensions = [
          # ... other extensions ...
          'sphinx.ext.githubpages',
      ]

4. **Create .nojekyll File**

   Create `docs/_static/.nojekyll` (empty file) to disable Jekyll processing.

5. **Update Repository Settings**

   * Go to Settings > Pages
   * Ensure source is set to "GitHub Actions"

Build Documentation Locally
--------------------------

.. code-block:: bash

   # Install dependencies
   pip install sphinx sphinx-rtd-theme
   
   # Build documentation
   cd docs
   make html
   
   # View locally
   python -m http.server -d _build/html

Custom Domain (Optional)
-----------------------

1. **Add Custom Domain**

   * Go to Settings > Pages
   * Add custom domain (e.g., docs.syinfo.com)
   * Check "Enforce HTTPS"

2. **Create CNAME File**

   Create `docs/_static/CNAME` with your domain:

   .. code-block:: text

      docs.syinfo.com

3. **Update DNS**

   Add CNAME record pointing to `mr901.github.io`

Troubleshooting
--------------

**Build Failures**

* Check GitHub Actions logs
* Verify Sphinx configuration
* Ensure all dependencies are installed

**404 Errors**

* Verify `html_baseurl` is set correctly
* Check that `.nojekyll` file exists
* Ensure GitHub Pages is enabled

**Styling Issues**

* Verify theme is installed: `pip install sphinx-rtd-theme`
* Check CSS file paths
* Clear browser cache

**Custom Domain Issues**

* Verify DNS settings
* Check CNAME file exists
* Wait for DNS propagation (up to 24 hours)

Maintenance
----------

**Regular Updates**

* Documentation builds automatically on push to main branch
* Monitor GitHub Actions for build failures
* Update dependencies as needed

**Version Management**

* Tag releases for version-specific documentation
* Update version in `conf.py`
* Consider separate documentation for different versions

**Backup**

* Documentation is automatically backed up in GitHub
* Consider external backup for custom assets
* Keep local copy of documentation source

Security Considerations
----------------------

* GitHub Pages are public by default
* Don't include sensitive information in documentation
* Use environment variables for secrets in CI/CD
* Regularly review repository permissions

Performance Optimization
-----------------------

* Optimize images and assets
* Use CDN for external resources
* Minimize JavaScript and CSS
* Enable compression in web server

Monitoring
----------

* Set up monitoring for documentation site
* Track page load times
* Monitor for broken links
* Check search functionality

Next Steps
----------

1. **Test the setup** by pushing changes to main branch
2. **Verify documentation** is accessible at GitHub Pages URL
3. **Update links** in repository README and other documentation
4. **Set up monitoring** for documentation site
5. **Configure custom domain** if desired 