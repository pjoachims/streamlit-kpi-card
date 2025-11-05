# GitHub Actions Workflows

## build.yml
Runs on every push to main/master and on pull requests:
- Builds the frontend (npm build)
- Builds the Python package
- Uploads artifacts

This ensures the package builds correctly before merging.

## build-and-publish.yml
Runs when you push a version tag (e.g., `v0.1.0`) or manually via workflow_dispatch:
- Builds the frontend
- Builds the Python package
- Publishes to PyPI (requires `PYPI_API_TOKEN` secret)

### To publish a new version:
1. Update version in `pyproject.toml`
2. Commit and push changes
3. Tag the release: `git tag v0.1.0 && git push origin v0.1.0`
4. GitHub Actions will build and publish automatically

### Setting up PyPI token:
1. Create an API token at https://pypi.org/manage/account/token/
2. Add it to GitHub: Settings → Secrets → Actions → New secret
3. Name: `PYPI_API_TOKEN`, Value: your token
