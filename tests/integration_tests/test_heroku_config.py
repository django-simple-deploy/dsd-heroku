"""Integration tests for django-simple-deploy, targeting Heroku."""

from pathlib import Path

import pytest

from tests.integration_tests.utils import it_helper_functions as hf
from tests.integration_tests.conftest import (
    tmp_project,
    run_dsd,
    reset_test_project,
    pkg_manager,
    dsd_version,
)


# --- Fixtures ---


# --- Test modifications to project files. ---


def test_settings(tmp_project):
    """Verify settings have been changed for heroku."""
    hf.check_reference_file(tmp_project, "blog/settings.py", "dsd-heroku")


def test_requirements_txt(tmp_project, pkg_manager, tmp_path, dsd_version):
    """Test that the requirements.txt file is correct."""
    if pkg_manager == "req_txt":
        context = {"current-version": dsd_version}
        hf.check_reference_file(
            tmp_project,
            "requirements.txt",
            "dsd-heroku",
            context=context,
            tmp_path=tmp_path,
        )
    elif pkg_manager == "poetry":
        # Poetry is so specific, the version numbers of sub-dependencies change
        # frequently. Just check that the appropriate packages are present.
        packages = [
            "django-bootstrap5",
            "django",
            "requests",
            "django-simple-deploy",
            "gunicorn",
            "psycopg2",
            "dj-database-url",
            "whitenoise",
        ]
        path = tmp_project / "requirements.txt"
        assert all([pkg in path.read_text() for pkg in packages])
    elif pkg_manager == "pipenv":
        assert not Path("requirements.txt").exists()


def test_pipfile(tmp_project, pkg_manager, tmp_path, dsd_version):
    """Test that Pipfile is correct."""
    if pkg_manager in ("req_txt", "poetry"):
        assert not Path("Pipfile").exists()
    elif pkg_manager == "pipenv":
        context = {"current-version": dsd_version}
        hf.check_reference_file(
            tmp_project, "Pipfile", "dsd-heroku", context=context, tmp_path=tmp_path
        )


def test_pyproject_toml(tmp_project, pkg_manager, tmp_path, dsd_version):
    """Test that pyproject.toml is correct."""
    if pkg_manager in ("req_txt", "pipenv"):
        assert not Path("pyproject.toml").exists()
    elif pkg_manager == "poetry":
        # Heroku uses requirements.txt for deployment, but simple_deploy will slightly
        # restructure pyproject.toml.
        context = {"current-version": dsd_version}
        hf.check_reference_file(
            tmp_project,
            "pyproject.toml",
            "dsd-heroku",
            context=context,
            tmp_path=tmp_path,
        )


def test_gitignore(tmp_project):
    """Test that .gitignore has been modified correctly."""
    hf.check_reference_file(tmp_project, ".gitignore", "dsd-heroku")


# --- Test Heroku-specific files ---


def test_generated_procfile(tmp_project):
    """Test that the generated Procfile is correct."""
    hf.check_reference_file(tmp_project, "Procfile", "dsd-heroku")


def test_static_placeholder(tmp_project):
    """Test that the static dir is present, with a placeholder.txt file."""
    hf.check_reference_file(tmp_project, "static/placeholder.txt", "dsd-heroku")


# --- Test logs ---


def test_log_dir(tmp_project):
    """Test that the log directory exists, and contains an appropriate log file."""
    log_path = Path(tmp_project / "dsd_logs")
    assert log_path.exists()

    # There should be exactly two log files.
    log_files = sorted(log_path.glob("*"))
    log_filenames = [lf.name for lf in log_files]
    # Check for exactly the log files we expect to find.

    # DEV: This will appear again when friendly summaries are implemented.
    assert "deployment_summary.html" not in log_filenames
    # DEV: Add a regex text for a file like "simple_deploy_2022-07-09174245.log".
    # DEV: This len will be 2 once friendly summaries are implemented.
    assert len(log_files) == 1

    # Read log file.
    # DEV: Look for specific log file; not sure this log file is always the second one.
    #   We're looking for one similar to "simple_deploy_2022-07-09174245.log".
    # DEV: This may be log_files[1] after implementing friendly summaries.
    log_file = log_files[0]
    log_file_text = log_file.read_text()

    # Spot check for opening log messages.
    assert "INFO: Logging run of `manage.py deploy`..." in log_file_text
    assert "INFO: Configuring project for deployment to Heroku..." in log_file_text

    assert "INFO: CLI args:" in log_file_text
    assert "INFO: Deployment target: Heroku" in log_file_text
    assert "INFO: Local project name: blog" in log_file_text
    assert "INFO: git status --porcelain" in log_file_text
    assert "INFO: ?? dsd_logs/" in log_file_text

    # Spot check for success messages.
    assert (
        "INFO: --- Your project is now configured for deployment on Heroku. ---"
        in log_file_text
    )
    assert (
        "INFO: Or, you can visit https://sample-name-11894.herokuapp.com."
        in log_file_text
    )


# --- Test staticfile setup ---


def test_one_static_file(tmp_project):
    """There should be exactly one file in static/."""
    static_path = tmp_project / "static"
    static_dir_files = sorted(static_path.glob("*"))
    assert len(static_dir_files) == 1


# # --- Test Heroku host already in ALLOWED_HOSTS ---
# DEV: Keeping this here for now; we probably want to update this test rather
#   than just get rid of it.

# def test_heroku_host_in_allowed_hosts(tmp_project):
#     """Test that no ALLOWED_HOST entry in Heroku-specific settings if the
#     Heroku host is already in ALLOWED_HOSTS.
#     """
#     # Modify the test project, and rerun simple_deploy.
#     cmd = f'sh platforms/heroku/modify_allowed_hosts.sh -d {tmp_project}'
#     cmd_parts = cmd.split()
#     subprocess.run(cmd_parts)

#     # Check that there's no ALLOWED_HOSTS setting in the Heroku-specific settings.
#     #   If we use the settings_text fixture, we'll get the original settings text
#     #   because it has module-level scope.
#     settings_text = Path(tmp_project / 'blog/settings.py').read_text()
#     assert "    ALLOWED_HOSTS.append('sample-name-11894.herokuapp.com')" not in settings_text
