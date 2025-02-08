Changelog: dsd-heroku
===

0.9 - Simplified usage from core
---

### 0.9.3 (skipping 0.9.2 to match pre-1.0 version of django-simple-deploy)

#### External changes

- Updated to match core app name change from `simple_deploy` to `django-simple-deploy`.
- Installs `poetry-plugin-export` when poetry is being used to manage requirements.

#### Internal changes

- Minor naming changes to make project consistent with current names in core.
- Updated requirements.txt, for dev work.
- Add dependabot config.
  - Daily for main requirements.
  - Monthly for tests/, until tests refactored to pull version from sample_project/.

### 0.9.1

#### External changes

- Updated messaging to use deploy command instead of simple_deploy.

#### Internal changes

- Uses config instead of returning individual attributes to core.
- Simplified packaging; all setup.cfg config moved to pyproject.toml.

### 0.9.0

#### External changes

- None

#### Internal changes

- Simplified packaging config.
- Returns platform name to core.

0.8 - First use of external plugins with django-simple-deploy
---

### 0.8.2

#### External changes

- None

#### Internal changes

- Requires django-simple-deploy. This is more important for non-default plugins, but it means you can just install the plugin without having to also explicitly install django-simple-deploy.

### 0.8.1

#### External changes

- Bugfix: Includes templates dir in package.

#### Internal changes

- None

### 0.8.0

#### External changes

- Initial release.

#### Internal changes

- Initial release.