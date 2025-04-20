# file_utils.py
import os
import json
import base64
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class VaultFileManager:
    """Utility class for handling vault file operations."""

    @staticmethod
    def open_vault_file_dialog(parent, title="Open Vault File"):
        """Opens a file dialog to select a vault file."""
        options = QFileDialog.Option.ReadOnly
        file_filter = "Vault Files (*.vault);;All Files (*)"

        file_path, _ = QFileDialog.getOpenFileName(
            parent, title, "", file_filter, options=options
        )

        return file_path if file_path else None

    @staticmethod
    def save_vault_file_dialog(parent, title="Save Vault File"):
        """Opens a file dialog to save a vault file."""
        options = QFileDialog.Option.ReadOnly
        file_filter = "Vault Files (*.vault);;All Files (*)"

        file_path, _ = QFileDialog.getSaveFileName(
            parent, title, "", file_filter, options=options
        )

        # Add .vault extension if not present
        if file_path and not file_path.endswith('.vault'):
            file_path += '.vault'

        return file_path if file_path else None

    @staticmethod
    def try_load_vault_file(file_path):
        """Attempts to load a vault file and decode its contents."""
        try:
            with open(file_path, "rb") as f:
                encoded_data = f.read()
                # Try to decode Base64
                decoded_data = base64.b64decode(encoded_data)
                # Try to load as JSON
                json_data = json.loads(decoded_data.decode())
                # If that works, it's probably a valid database file
                if isinstance(json_data, dict):
                    return json_data, os.path.basename(file_path)
        except Exception as e:
            return None, str(e)

        return None, "Invalid file format"

    @staticmethod
    def save_vault_file(file_path, accounts):
        """Saves account data to a vault file."""
        try:
            # Convert to JSON and encode
            json_data = json.dumps(accounts).encode()
            encoded_data = base64.b64encode(json_data)

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(
                os.path.abspath(file_path)), exist_ok=True)

            # Save to file
            with open(file_path, "wb") as f:
                f.write(encoded_data)

            return True, ""
        except Exception as e:
            return False, str(e)
