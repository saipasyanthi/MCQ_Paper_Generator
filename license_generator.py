#!/usr/bin/env python3
"""
License Generator Tool
Use this to create license files for distribution
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from license_manager import APIKeyManager, LicenseGenerator


def generate_license_interactive():
    """Generate license interactively."""
    print("\n" + "="*60)
    print("     MCQ PAPER GENERATOR - LICENSE GENERATOR")
    print("="*60)
    
    # Get user info
    user_name = input("\nEnter User Name: ").strip()
    if not user_name:
        print("Error: User name cannot be empty")
        return
    
    user_email = input("Enter User Email: ").strip()
    if not user_email:
        print("Error: Email cannot be empty")
        return
    
    # Get expiry
    print("\nLicense Validity:")
    print("1. 1 Month (30 days)")
    print("2. 3 Months (90 days)")
    print("3. 6 Months (180 days)")
    print("4. 1 Year (365 days)")
    print("5. Custom days")
    
    choice = input("Select license validity (1-5): ").strip()
    
    validity_map = {
        "1": 30,
        "2": 90,
        "3": 180,
        "4": 365
    }
    
    if choice == "5":
        try:
            days = int(input("Enter number of days: "))
            expiry_days = days
        except:
            print("Invalid input")
            return
    else:
        expiry_days = validity_map.get(choice, 365)
    
    # Generate license
    print("\nGenerating license...")
    
    manager = APIKeyManager()
    key_data = manager.generate_api_key(user_name, user_email, expiry_days)
    
    # Save license
    Path("licenses").mkdir(exist_ok=True)
    license_path = manager.save_license_file(key_data)
    
    # Display info
    print("\n" + "="*60)
    print("LICENSE GENERATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nUser Name:     {user_name}")
    print(f"Email:         {user_email}")
    print(f"Key ID:        {key_data['key_id']}")
    print(f"Created:       {key_data['created']}")
    print(f"Expires:       {key_data['expires']}")
    print(f"Days Valid:    {expiry_days}")
    print(f"\nLicense File:  {license_path}")
    
    # Show API key (but partially masked)
    api_key = key_data['api_key']
    masked_key = api_key[:8] + "*" * (len(api_key) - 16) + api_key[-8:]
    print(f"API Key:       {masked_key}")
    
    print("\n" + "-"*60)
    print("DISTRIBUTION:")
    print("-"*60)
    print(f"\n1. Rename license file to 'license.json'")
    print(f"2. Include it in the application package")
    print(f"3. Users copy 'license.json' to app directory")
    print(f"4. Application will auto-validate on startup")
    
    # Ask to display full key
    show_key = input("\nShow full API key? (y/n): ").strip().lower()
    if show_key == 'y':
        print(f"\nFull API Key: {api_key}")
        print("Keep this safe! Share only with authorized users.")
    
    print("\n" + "="*60)


def generate_license_batch(filename="licenses_batch.json"):
    """Generate multiple licenses from a batch file."""
    
    if not Path(filename).exists():
        print(f"\nError: {filename} not found")
        print("\nCreate a JSON file with this format:")
        print("""
{
    "licenses": [
        {
            "user_name": "John Doe",
            "user_email": "john@example.com",
            "expiry_days": 365
        },
        {
            "user_name": "Jane Smith",
            "user_email": "jane@example.com",
            "expiry_days": 180
        }
    ]
}
        """)
        return
    
    try:
        with open(filename, 'r') as f:
            batch_data = json.load(f)
        
        manager = APIKeyManager()
        Path("licenses").mkdir(exist_ok=True)
        
        print(f"\nGenerating {len(batch_data.get('licenses', []))} licenses...")
        
        for i, license_info in enumerate(batch_data.get('licenses', []), 1):
            key_data = manager.generate_api_key(
                license_info['user_name'],
                license_info['user_email'],
                license_info.get('expiry_days', 365)
            )
            
            license_path = manager.save_license_file(key_data)
            print(f"{i}. ✓ Generated license for {license_info['user_name']}")
        
        print("\nAll licenses generated successfully!")
        print(f"Check 'licenses/' directory for license files")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def list_licenses():
    """List all generated licenses."""
    manager = APIKeyManager()
    licenses = manager.get_all_keys()
    
    if not licenses:
        print("No licenses found")
        return
    
    print("\n" + "="*60)
    print("EXISTING LICENSES")
    print("="*60)
    
    for i, lic in enumerate(licenses, 1):
        print(f"\n{i}. User: {lic['user_name']} ({lic['user_email']})")
        print(f"   Key ID: {lic['key_id']}")
        print(f"   Expires: {lic['expires']}")
        print(f"   Active: {'Yes' if lic['is_active'] else 'No'}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch" and len(sys.argv) > 2:
            generate_license_batch(sys.argv[2])
        elif sys.argv[1] == "list":
            list_licenses()
        elif sys.argv[1] == "interactive":
            generate_license_interactive()
        else:
            print("Usage: python license_generator.py [interactive|batch|list]")
    else:
        generate_license_interactive()


if __name__ == "__main__":
    main()
