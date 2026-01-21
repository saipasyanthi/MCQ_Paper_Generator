"""
API Key and License Management System
Generates and validates API keys for distribution
"""

import os
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from pathlib import Path


class APIKeyManager:
    """Manage API keys for application distribution."""
    
    def __init__(self, license_dir="licenses"):
        self.license_dir = Path(license_dir)
        self.license_dir.mkdir(exist_ok=True)
        self.keys_file = self.license_dir / "api_keys.json"
    
    def generate_api_key(self, user_name, user_email, expiry_days=365):
        """Generate a new API key.
        
        Args:
            user_name: Name of the user
            user_email: Email of the user
            expiry_days: Days until key expires (default 1 year)
            
        Returns:
            Dictionary with key details
        """
        # Generate random key
        raw_key = secrets.token_urlsafe(32)
        
        # Create key ID
        key_id = hashlib.sha256(raw_key.encode()).hexdigest()[:8].upper()
        
        # Calculate expiry date
        expiry_date = (datetime.now() + timedelta(days=expiry_days)).isoformat()
        
        key_data = {
            "key_id": key_id,
            "api_key": raw_key,
            "user_name": user_name,
            "user_email": user_email,
            "created": datetime.now().isoformat(),
            "expires": expiry_date,
            "is_active": True,
            "machine_id": None
        }
        
        return key_data
    
    def save_license_file(self, key_data, filename=None):
        """Save license file in JSON format.
        
        Args:
            key_data: Dictionary with key information
            filename: Optional custom filename
            
        Returns:
            Path to saved license file
        """
        if filename is None:
            filename = f"license_{key_data['key_id']}.json"
        
        license_path = self.license_dir / filename
        
        with open(license_path, 'w') as f:
            json.dump(key_data, f, indent=4)
        
        return license_path
    
    def load_license_file(self, license_path):
        """Load license file.
        
        Args:
            license_path: Path to license file
            
        Returns:
            Dictionary with license data
        """
        with open(license_path, 'r') as f:
            return json.load(f)
    
    def validate_api_key(self, api_key, machine_id=None):
        """Validate an API key.
        
        Args:
            api_key: API key to validate
            machine_id: Optional machine identifier
            
        Returns:
            Tuple (is_valid, message, key_data)
        """
        # Look for license files
        for license_file in self.license_dir.glob("license_*.json"):
            try:
                key_data = self.load_license_file(license_file)
                
                if key_data["api_key"] == api_key:
                    # Check if expired
                    expiry = datetime.fromisoformat(key_data["expires"])
                    if datetime.now() > expiry:
                        return False, "License has expired", None
                    
                    # Check if active
                    if not key_data["is_active"]:
                        return False, "License is inactive", None
                    
                    return True, "License valid", key_data
            except Exception as e:
                continue
        
        return False, "Invalid API key", None
    
    def get_all_keys(self):
        """Get all generated API keys."""
        keys = []
        for license_file in self.license_dir.glob("license_*.json"):
            try:
                keys.append(self.load_license_file(license_file))
            except:
                pass
        return keys
    
    def revoke_key(self, key_id):
        """Revoke an API key."""
        for license_file in self.license_dir.glob("license_*.json"):
            try:
                key_data = self.load_license_file(license_file)
                if key_data["key_id"] == key_id:
                    key_data["is_active"] = False
                    self.save_license_file(key_data, license_file.name)
                    return True
            except:
                pass
        return False


class LicenseValidator:
    """Validate and check licenses at application startup."""
    
    LICENSE_FILE = "license.json"
    
    @staticmethod
    def get_license_path():
        """Get the correct path to license file, works with PyInstaller."""
        import sys
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            # Check in the executable's directory first
            exe_dir = Path(sys.executable).parent
            license_path = exe_dir / LicenseValidator.LICENSE_FILE
            if license_path.exists():
                return license_path
            # Check in the bundled data
            if hasattr(sys, '_MEIPASS'):
                bundle_dir = Path(sys._MEIPASS)
                license_path = bundle_dir / LicenseValidator.LICENSE_FILE
                if license_path.exists():
                    return license_path
        # Running as script
        return Path(LicenseValidator.LICENSE_FILE)
    
    @staticmethod
    def check_license_exists():
        """Check if license file exists in app directory."""
        return LicenseValidator.get_license_path().exists()
    
    @staticmethod
    def load_license():
        """Load license from application directory.
        
        Returns:
            Dictionary with license data or None
        """
        try:
            license_path = LicenseValidator.get_license_path()
            with open(license_path, 'r') as f:
                return json.load(f)
        except:
            return None
    
    @staticmethod
    def save_license(license_data):
        """Save license to application directory."""
        with open(LicenseValidator.LICENSE_FILE, 'w') as f:
            json.dump(license_data, f, indent=4)
    
    @staticmethod
    def validate():
        """Validate license file.
        
        Returns:
            Tuple (is_valid, message, license_data)
        """
        if not LicenseValidator.check_license_exists():
            return False, "No license found. Please add license.json file.", None
        
        license_data = LicenseValidator.load_license()
        
        if not license_data:
            return False, "Invalid license file format.", None
        
        # Check expiry
        try:
            expiry = datetime.fromisoformat(license_data["expires"])
            if datetime.now() > expiry:
                remaining = (expiry - datetime.now()).days
                return False, f"License expired {abs(remaining)} days ago.", None
        except:
            return False, "Invalid license expiry date.", None
        
        # Check active status
        if not license_data.get("is_active", False):
            return False, "License is inactive.", None
        
        days_remaining = (datetime.fromisoformat(license_data["expires"]) - datetime.now()).days
        message = f"License valid for {days_remaining} more days."
        
        return True, message, license_data


class LicenseGenerator:
    """Generate license files for distribution."""
    
    @staticmethod
    def create_license_bundle(user_name, user_email, expiry_days=365, output_file="license.json"):
        """Create a complete license bundle for a user.
        
        Args:
            user_name: Name of the user
            user_email: Email of the user
            expiry_days: Days until expiry
            output_file: Output filename
            
        Returns:
            Path to license file
        """
        manager = APIKeyManager()
        key_data = manager.generate_api_key(user_name, user_email, expiry_days)
        
        # Save as license file
        license_path = manager.license_dir / output_file
        with open(license_path, 'w') as f:
            json.dump(key_data, f, indent=4)
        
        return license_path, key_data
