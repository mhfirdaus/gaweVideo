"""Tests for Streamlit UI command in CLI."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from gawe_video.cli import app


class CliUITests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    @patch("gawe_video.cli.subprocess.run")
    def test_ui_command_runs_streamlit(self, mock_run) -> None:
        result = self.runner.invoke(app, ["ui", "--host", "0.0.0.0", "--port", "9001"])
        self.assertEqual(result.exit_code, 0)
        args = mock_run.call_args.args[0]
        self.assertEqual(args[0], "streamlit")
        self.assertEqual(args[1], "run")
        self.assertEqual(Path(args[2]).name, "web_ui.py")
        self.assertEqual(args[-4:], ["--server.address", "0.0.0.0", "--server.port", "9001"])
        self.assertTrue(mock_run.call_args.kwargs["check"])

    @patch("gawe_video.cli.subprocess.run", side_effect=FileNotFoundError("streamlit not found"))
    def test_ui_command_missing_streamlit(self, _mock_run) -> None:
        result = self.runner.invoke(app, ["ui"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Streamlit was not found", result.stdout)

    @patch("gawe_video.cli.subprocess.run", side_effect=subprocess.CalledProcessError(returncode=2, cmd=["streamlit"]))
    def test_ui_command_streamlit_error(self, _mock_run) -> None:
        result = self.runner.invoke(app, ["ui"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Failed to launch Streamlit UI", result.stdout)


if __name__ == "__main__":
    unittest.main()
