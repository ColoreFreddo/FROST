# FROST
This application (written in Python) allow users easy domain public info lookup, store them in a database, and search them in an intuitive GUI. FROST is intended for didactical purposes or web analisys, not for illegal means.

## Features

- Perform OSINT analysis on a domain using the 'python-whois' library.
- Verify if the website is up using 'curl'.
- Expand shortened URL using the 'pyshorteners' library (refer to the library documentation for supported shorteners).
- Store analysys data in a MySQL database for comparason.
- Simple GUI interface for interacting with the database.

## Prerequisites

To run this tool, you need to have the following.

- MacOs or Linux (Windows is not supported)
- Python (version 3.6 or higher)
- MySQL database server

## Installation

1. Clone the repo:
```bash
   git clone https://github.com/ColoreFreddo/FROST
   cd FROST
   ```
2. Install the requirements:

- MacOs
```zsh
   pip3 install -r requirements.txt
   ```

- Linux
```bash
   pip install -r requirements.txt
   ```
3. Configure the MySQL database connection:
- Edit the 'config.ini' file and replace 'ADD_YOURS' with your server (or local) info.

## Usage

To run FROST use the following command:
- MacOs
```zsh
   python3 frost.py
   ```
- Linux
```bash
   python frost.py
   ```
You will be greeted by this options:

1. Domain analysis: Perform analysis on a domain by entering the URL or IP address.
2. Open the database: Launch the GUI interface to interact with the database.
3. Exit: Closes the application.

Follow the on-screen options to enter in the desired menu.

## Contributing

Contributions are accepted, if you find any bugs or suggestions, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
