
# VisiBot - Installation and Setup

### Note for Markers:
- For ease of setup, I have included **pre-configured .env files** in the source code .zip submitted for marking
- These .env files contain API keys, usernames, and passwords and should therefore be kept private and secure
- **As .env files are provided, you can skip .env related instructions for the setup of the VisiBot Processing System and Web App**
- IMPORTANT! You will have to copy `VisiBot/src/.env.lisa` to `/path/to/LiSa/.env` to make use of the VirusTotal API key included in the lisa .env file

## Setup Requirements
- The [URI](https://docs.mongodb.com/manual/reference/connection-string/) for a remotely accessible [MongoDB](https://www.mongodb.com/) Database (e.g. [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))
    - For example: `mongodb+srv://user:pass@website.com/database_name`
- A [MaxMind GeoIP Update API Key](https://www.maxmind.com/en/accounts/current/license-key):
    - Go to Account > My License Key > Generate New License Key > Yes > [1st Option] > Confirm
- A [Bad Packets API Key](https://badpackets.net/)
- A [VirusTotal API Key](https://virustotal.com/)
- A [ipinfo.io API Key](https://ipinfo.io)
- A modified fork of the [LiSa Sandbox Server](https://github.com/denBot/LiSa)
    - (optional) An active VPN service connectable through a OpenVPN .ovpn file
- [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/)
- [NodeJS](https://nodejs.org/en/) and [npm](https://www.npmjs.com/)

# LiSa Sandbox

## Setting up modified LiSa server

- Install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/)
- `git clone` the fork of LiSa [available here](https://github.com/denBot/LiSa)
- install docker and docker-compose onto your host
- From within the `LiSa` directory, enter the following commands:
```bash
# Create/edit .env file using example template (see note for markers below before doing this)
➜  ~ cp .env.example .env
➜  ~ vim .env

# Build/run using docker-compose and specify number of workers
➜  ~ sudo docker-compose build
➜  ~ sudo docker-compose up --scale worker=3
```

Make sure the `.env` file contains the following and that you:
- Un-comment `API_SUCCESS_URL`, `API_FAILURE_URL`, and `VIRUSTOTAL_API_KEY`
- replace `[API_KEY_HERE]` with your [VirusTotal API key](https://developers.virustotal.com/v3.0/reference)
```
LISA_WEBHOST=localhost
LISA_PORT=4242
LISA_STORAGE_PATH=./data/storage
LISA_DB_PATH=./data/db
LISA_VPN_PATH=./vpn

MYSQL_PASSWORD=lisa
RABBITMQ_DEFAULT_PASS=lisa

API_SUCCESS_URL=http://172.42.0.1:5001/api/lisa-analysis/success/<task_id>
API_FAILURE_URL=http://172.42.0.1:5001/api/lisa-analysis/failure/<task_id>
VIRUSTOTAL_API_KEY=[API_KEY_HERE]
```

### (Optional) Configuring LiSa to use a VPN
You can skip this process if you do not have a VPN available or are not concerned with using one. 
- Download an `.ovpn` file from your VPN Provider
- Create a directory inside of the base `LiSa` directory called `vpn`
- If your VPN requires a username or password:
    - Open the `.ovpn` with a text editor and change `auth-user-pass` to `auth-user-pass /vpn/pass.txt`
    - Create a file called `pass.txt` inside of the `vpn` directory and fill it with your VPN credentials line-by-line:
        ```
        your-vpn-email@example.com
        your-vpn-password
        ```
- Move the `.ovpn` into the `vpn` directory
- Lastly, edit `docker-compose.yml` and uncomment `# - VPN=/vpn` and rebuild/run the docker containers


# VisiBot Processing System

## Running the VisiBot Processing System

- Install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/)
- Make sure a LiSa server is running at http://localhost:4242
- Enter the following commands

```bash
# Step 1: Create/edit .env file using example template (please see note at top of page)
➜  ~ cd src/processing
➜  ~ cp .env.example .env
➜  ~ vim .env

# Step 3: Build/run using docker-compose and specify number of workers
➜  ~ sudo docker-compose build
➜  ~ sudo docker-compose up --scale worker=6
```

### Example contents for .env

```env
# src/processing/.env

# GeoIP Variables
GEO_ACCOUNT_ID=[ENTER_ACCOUNT_ID]
GEO_LICENSE_KEY=[ENTER_API_KEY]

# Schedular Variables
FIRST_RUN=False
FIRST_RUN_HOURS=2
EVENT_MINUTE=15
FLOWER_URL=http://localhost:5555
BAD_PACKETS_API_KEY=[ENTER_API_KEY]

# Worker Variables
REDIS_PASSWORD=[ENTER_A_SECURE_PASSWORD]
IP_INFO_C2_ONLY=False
IP_INFO_API_KEY=[ENTER_IPINFO_API_KEY]
MONGO_URL=[ENTER_MONGO_DB_URL]
LISA_API_URL=http://149.28.227.219:4242/api
LISA_EXEC_TIME_SEC=30

# Flower Variables
FLOWER_USER=vb-admin
FLOWER_PASS=[ENTER_A_SECURE_PASSWORD]
```
**Note:** variable assignments in **\[brackets\]** should be replaced with relevant credentials.

# VisiBot Web Application

## Running Nuxt.js and Express.js locally
- Make sure you have the latest version of [NodeJS](https://nodejs.org/en/) installed
- Make sure ports 8080 and 3000 are available for running dev servers
- Once configured, run local [Nuxt.js](https://nuxtjs.org/docs/2.x/get-started/installation) and [Express.js](https://expressjs.com/) development servers using the following commands:

```bash
# Navigate to webapp and install the node_modules
➜  ~ cd src/webapp
➜  ~ npm install

# Create/edit .env file using example template (please see note at top of page)
➜  ~ cp backend/.env.example backend/.env
➜  ~ vim backend/.env

# Run the following to start the express.js server at port 8080
➜  ~ npm run exp-dev

# Open a new terminal at src/webapp and run:
➜  ~ npm run nuxt-dev
```

Following these steps, You will be able to view the development server for VisiBot Web App at http://localhost:3000


### Example contents for .env

```
# src/webapp/backend/.env

MONGO_URL=[ENTER_MONGO_DB_URL]
FRONTEND_BASE_URL=http://localhost:3000
NODE_ENV=development
```
**Note:** variable assignments in **\[brackets\]** should be replaced with relevant credentials.