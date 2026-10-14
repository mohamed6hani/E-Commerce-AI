"""PyQt6 GUI to start, stop, and restart the MERN backend server.

This utility runs entirely locally and assumes that Node.js is available on the
PATH.  It launches ``node server.js`` inside ``backend-mern`` so that the API
and built React frontend are served from the same port.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import QProcess, QProcessEnvironment, QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QPlainTextEdit,
)


class ServerControlWindow(QMainWindow):
    """Main application window that manages the backend process."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("eCommerce AI Server Control")
        self.resize(780, 520)

        self.project_root = Path(__file__).resolve().parents[1]
        self.backend_dir = (self.project_root / "backend-mern").resolve()

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self._handle_stdout)
        self.process.readyReadStandardError.connect(self._handle_stderr)
        self.process.errorOccurred.connect(self._handle_error)
        self.process.started.connect(self._handle_started)
        self.process.finished.connect(self._handle_finished)

        self.pending_restart = False
        self.force_kill_timer = QTimer(self)
        self.force_kill_timer.setInterval(5000)
        self.force_kill_timer.setSingleShot(True)
        self.force_kill_timer.timeout.connect(self._force_kill)

        self._init_ui()
        self._append_log("Project root: {}".format(self.project_root))
        self._append_log("Backend directory: {}".format(self.backend_dir))

    def _init_ui(self) -> None:
        central = QWidget(self)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        # Status line and backend path control
        status_layout = QGridLayout()
        status_layout.setHorizontalSpacing(8)
        status_layout.setVerticalSpacing(6)

        self.status_label = QLabel("Server status: stopped")
        status_font = QFont()
        status_font.setPointSize(11)
        status_font.setBold(True)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #b3261e;")
        status_layout.addWidget(self.status_label, 0, 0, 1, 2)

        status_layout.addWidget(QLabel("Backend path:"), 1, 0)
        self.backend_path_edit = QLineEdit(str(self.backend_dir))
        self.backend_path_edit.setReadOnly(True)
        status_layout.addWidget(self.backend_path_edit, 1, 1)

        browse_button = QPushButton("Change…")
        browse_button.clicked.connect(self._select_backend_dir)
        status_layout.addWidget(browse_button, 1, 2)

        status_layout.addWidget(QLabel("Port:"), 2, 0)
        self.port_spinner = QSpinBox()
        self.port_spinner.setRange(1024, 65535)
        self.port_spinner.setValue(8800)
        status_layout.addWidget(self.port_spinner, 2, 1)

        root_layout.addLayout(status_layout)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.start_button = QPushButton("Start Server")
        self.start_button.clicked.connect(self.start_server)

        self.stop_button = QPushButton("Stop Server")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)

        self.restart_button = QPushButton("Restart Server")
        self.restart_button.clicked.connect(self.restart_server)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.restart_button)
        button_layout.addStretch(1)

        root_layout.addLayout(button_layout)

        # Log output
        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumBlockCount(1000)
        root_layout.addWidget(self.log_view, 1)

        self.setCentralWidget(central)

    # Button handlers -----------------------------------------------------
    def start_server(self) -> None:
        if self.process.state() != QProcess.ProcessState.NotRunning:
            self._append_log("Server is already running.")
            return

        backend_path = Path(self.backend_path_edit.text()).expanduser().resolve()
        server_js = backend_path / "server.js"
        if not server_js.exists():
            self._append_log(f"Cannot find server.js in {backend_path}")
            QMessageBox.critical(self, "Missing server", "server.js was not found in the backend directory.")
            return

        self.backend_dir = backend_path
        self.backend_path_edit.setText(str(self.backend_dir))

        env = QProcessEnvironment.systemEnvironment()
        env.insert("PORT", str(self.port_spinner.value()))
        self.process.setProcessEnvironment(env)
        self.process.setWorkingDirectory(str(self.backend_dir))
        self.process.setProgram("node")
        self.process.setArguments([server_js.name])

        self._append_log(f"Starting server on port {self.port_spinner.value()} …")
        self.process.start()

    def stop_server(self) -> None:
        if self.process.state() == QProcess.ProcessState.NotRunning:
            self._append_log("Server is not running.")
            return

        self._append_log("Stopping server …")
        self.process.terminate()
        self.force_kill_timer.start()

    def restart_server(self) -> None:
        if self.process.state() == QProcess.ProcessState.NotRunning:
            self.start_server()
            return

        self._append_log("Restart requested …")
        self.pending_restart = True
        self.stop_server()

    # QProcess signal handlers -------------------------------------------
    def _handle_stdout(self) -> None:
        text = bytes(self.process.readAllStandardOutput()).decode("utf-8", "replace")
        self._append_log(text.rstrip())

    def _handle_stderr(self) -> None:
        text = bytes(self.process.readAllStandardError()).decode("utf-8", "replace")
        self._append_log(text.rstrip())

    def _handle_error(self, error: QProcess.ProcessError) -> None:
        self.force_kill_timer.stop()
        self.status_label.setText("Server status: error")
        self.status_label.setStyleSheet("color: #b3261e;")
        self._append_log(f"Process error: {error.name}")

    def _handle_started(self) -> None:
        self.force_kill_timer.stop()
        self.status_label.setText("Server status: running")
        self.status_label.setStyleSheet("color: #1b5e20;")
        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self._append_log("Server started.")

    def _handle_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        self.force_kill_timer.stop()
        self.status_label.setText("Server status: stopped")
        self.status_label.setStyleSheet("color: #b3261e;")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self._append_log(f"Server stopped (code {exit_code}, status {exit_status.name}).")

        if self.pending_restart:
            self.pending_restart = False
            self._append_log("Restarting server …")
            self.start_server()

    def _force_kill(self) -> None:
        if self.process.state() != QProcess.ProcessState.NotRunning:
            self._append_log("Process did not exit in time; killing …")
            self.process.kill()

    # Helpers -------------------------------------------------------------
    def _append_log(self, message: str) -> None:
        if not message:
            return
        self.log_view.appendPlainText(message)
        self.log_view.verticalScrollBar().setValue(self.log_view.verticalScrollBar().maximum())

    def _select_backend_dir(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, "Select backend directory", str(self.backend_dir))
        if chosen:
            self.backend_dir = Path(chosen).resolve()
            self.backend_path_edit.setText(str(self.backend_dir))
            self._append_log(f"Backend directory set to {self.backend_dir}")


def main() -> None:
    app = QApplication(sys.argv)
    window = ServerControlWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
