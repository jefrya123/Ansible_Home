import requests
import yaml
import os
import subprocess

# Proxmox API credentials
PROXMOX_API_URL = "https://192.168.1.160:8006/api2/json"
TICKET = "PVE:root@pam:67781F04::EDbL+vLj2gv9YMjPmgV06gfawG6LpPJLdBeV/e7gLS0Irr+Lv/SyRKlR2v1eZxcdQPNGHsU1x05vb6TfANKhyMwDc8ELDehjRe3S4+TImMINPAfnQJOSTLxKLtd1kvfurMoPQYuqV0mNrs0k1CrVbyg3wIJ6t6k2VuFr25aPStM8vCLx1zEhu+MvQ8zvpEJIbD2P3yMooW0rRQDvyeXyXNKUvQMiUBNo9sLFu5Sx39AYYjnBhT71o3Mq0tHTuT2zsyoLpEJqiQkmquxiRF9mSsNIAWgv5DQjG/2+WuVRmxz8BRQnjf+Oz5LTNmYz2iMIuvPNS8wL8jAlpbzv1F9Yjw=="
CSRF_TOKEN = "67781F04:4IeucgnuoMjIbhClrIYKVX46UHrHP0U/ie+OPmuduts"
NODE_NAME = "pve"

# GitHub repository path
REPO_PATH = r"C:\Users\jefry\Desktop\Projects\Ansible_Home"  # Update with the local path to your cloned repository
INVENTORY_FILE_PATH = os.path.join(REPO_PATH, "inventory.yml")

# Fetch VMs from Proxmox
def fetch_vms():
    headers = {
        "CSRFPreventionToken": CSRF_TOKEN,
        "Cookie": f"PVEAuthCookie={TICKET}"
    }
    response = requests.get(f"{PROXMOX_API_URL}/nodes/{NODE_NAME}/qemu", headers=headers, verify=False)
    response.raise_for_status()  # Raise an error for bad HTTP responses
    return response.json()["data"]

# Update the inventory file
def update_inventory(vms):
    inventory = {"all": {"hosts": []}}
    for vm in vms:
        if vm["status"] == "running":
            inventory["all"]["hosts"].append(vm["name"])
    
    # Write inventory to file
    with open(INVENTORY_FILE_PATH, "w") as inventory_file:
        yaml.dump(inventory, inventory_file, default_flow_style=False)
    print(f"Updated inventory file: {INVENTORY_FILE_PATH}")

# Commit and push changes to GitHub
def push_to_github():
    try:
        subprocess.run(["git", "add", INVENTORY_FILE_PATH], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "commit", "-m", "Update Ansible inventory"], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "push"], cwd=REPO_PATH, check=True)
        print("Changes pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing changes to GitHub: {e}")

# Main function
if __name__ == "__main__":
    try:
        vms = fetch_vms()
        update_inventory(vms)
        push_to_github()
    except Exception as e:
        print(f"Error: {e}")
