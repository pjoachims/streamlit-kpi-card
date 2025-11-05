# Packaging and Publishing Guide

## Overview

This Streamlit component has two parts:
1. **Frontend** (React/TypeScript) - needs to be built to JavaScript
2. **Python package** - wraps the frontend and provides the Python API

## Automated Publishing (Recommended)

GitHub Actions handles everything automatically.

### Publishing a New Version

1. **Update the version** in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. **Commit and tag**:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.2.0"
   git tag v0.2.0
   git push origin main
   git push origin v0.2.0
   ```

3. **GitHub Actions will automatically**:
   - Build the frontend (`npm run build`)
   - Build the Python package (`python -m build`)
   - Publish to PyPI (`twine upload`)

4. **Monitor the progress**:
   - Go to: https://github.com/pjoachims/streamlit-kpi-card/actions
   - Watch the "Build and Publish" workflow

### One-Time Setup for PyPI

To enable automated publishing, add your PyPI API token to GitHub:

1. **Create PyPI API token**:
   - Go to: https://pypi.org/manage/account/token/
   - Click "Add API token"
   - Name: `streamlit-kpi-card`
   - Scope: Entire account (or specific project after first publish)
   - Copy the token (starts with `pypi-...`)

2. **Add token to GitHub**:
   - Go to: https://github.com/pjoachims/streamlit-kpi-card/settings/secrets/actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your token
   - Click "Add secret"

## Manual Publishing (Advanced)

If you need to publish manually:

### 1. Build the Frontend

```bash
cd streamlit_kpi_card/frontend
npm install
npm run build
```

This creates `streamlit_kpi_card/frontend/build/` with compiled JavaScript.

### 2. Build the Python Package

```bash
# Install build tools
pip install build twine

# Build the package
python -m build
```

This creates:
- `dist/streamlit_kpi_card-0.1.0.tar.gz` (source distribution)
- `dist/streamlit_kpi_card-0.1.0-py3-none-any.whl` (wheel)

### 3. Check the Package

```bash
twine check dist/*
```

### 4. Upload to PyPI

```bash
# Test PyPI first (optional)
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

## Development Workflow

### Local Development

1. **Set development mode** in `streamlit_kpi_card/__init__.py`:
   ```python
   _RELEASE = False
   ```

2. **Start frontend dev server**:
   ```bash
   cd streamlit_kpi_card/frontend
   npm install
   npm start
   ```

3. **Run your Streamlit app**:
   ```bash
   streamlit run example.py
   ```

Changes to frontend code will hot-reload automatically.

### Testing Before Release

1. **Set release mode** in `streamlit_kpi_card/__init__.py`:
   ```python
   _RELEASE = True
   ```

2. **Build frontend**:
   ```bash
   cd streamlit_kpi_card/frontend
   npm run build
   ```

3. **Install locally**:
   ```bash
   pip install -e .
   streamlit run example.py
   ```

## Package Contents

When you build the package, it includes:

```
streamlit_kpi_card/
├── __init__.py              # Python API
└── frontend/
    └── build/               # Compiled frontend (JS, CSS, HTML)
        ├── index.html
        ├── static/
        │   ├── js/
        │   └── css/
        └── asset-manifest.json
```

**Note**: The source TypeScript files (`frontend/src/`) are NOT included in the package. Users only get the compiled build.

## Versioning

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backward compatible
- **PATCH** (0.0.1): Bug fixes

## Troubleshooting

### "Module not found" errors after publishing

Make sure `frontend/build/` exists and is committed to git (it should be!).

### Package size too large

The build folder can be large. This is normal for React components. Current size is ~500KB.

### Frontend not updating after changes

1. Rebuild: `cd streamlit_kpi_card/frontend && npm run build`
2. Clear Streamlit cache: `streamlit cache clear`
3. Restart Streamlit app

## CI/CD Workflows

### build.yml
- Runs on every push and PR
- Verifies frontend and Python package build successfully
- Does NOT publish

### build-and-publish.yml
- Runs on git tags (`v*`)
- Builds and publishes to PyPI
- Requires `PYPI_API_TOKEN` secret

## Questions?

- **How do I test before publishing?** Use TestPyPI first: `twine upload --repository testpypi dist/*`
- **Can I skip GitHub Actions?** Yes, just follow the "Manual Publishing" steps
- **Do I commit the build folder?** Yes! The build folder should be in git for proper packaging
