# Description

Ansible playbook to make some settings for Linux server. Nothing important here.

Works only with Ubuntu.

# Run

1. Install Ansible.

2. Copy SSH key to the server.

3. Check for Python in `/usr/bin/python`. You can create link if you don't have one

    ```sh
    sudo ln -s /usr/bin/python3.5 /usr/bin/python
    ```

4. Run playbook

    ```sh
    ansible-playbook -K server.yml
    ```
