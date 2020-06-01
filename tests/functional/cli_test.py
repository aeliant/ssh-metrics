"""@package tests.funtional.cli_test

All functional tests related to CLI environment."""
import pytest

from mock import patch, mock_open
from click.testing import CliRunner

from ssh_metrics import cli



@pytest.mark.functional
@pytest.mark.cli
@patch('ssh_metrics.__version__', 'X.Y.Z')
def version_option_test():
    """Check that the version option return the correct version of the script."""
    runner = CliRunner()

    m = mock_open()
    with patch('__main__.open', m):
        result = runner.invoke(cli, ['--version'])
        assert 0 == result.exit_code, result.output
        assert 'X.Y.Z' in result.output
