# VisIBoT - Visualisation of IoT botnets
![Main Build Status](https://travis-ci.com/denBot/VisIBoT.svg?token=pMfMcyEQzGJGFRQDBST5&branch=main)

### Summary
Author: [Daniel Arthur](mailto:2086380a@student.gla.ac.uk) | Supervisor: [Angelos Marnerides](mailto:angelos.marnerides@glasgow.ac.uk)

A browser-based visualisation tool that maps the geolocation and lifespan information of Mirai (IoT) Botnets.

Visualised data-sets will be collected, correlated and pre-processed through various APIs such as [BadPackets](https://docs.badpackets.net/), [Ripe NCC](https://www.ripe.net/) and [MaxMind](https://www.maxmind.com/en/home).

# Requirements
- MongoDB Database
    - For my use case, I used MongoDB Atlas.
    - Edit `.env` and update `MONGODB_URI` with the URI for your database (`mongodb+srv://...`)
- MaxMind GeoIP Update API Key
    - You will have to register with MaxMind and create an API/License Key 
    - Go to Account > My License Key > Generate New License Key > Yes > [1st Option] > Confirm
    - Install `geoip` and `geoipupdate` on your host (e.g. `apt-install geoip geoipupdate` )
    - Run `sudo geoipupdate` to grab the latest GeoIP Databases (stored in `/var/lib/GeoIP`)
    - On your host, edit `/etc/GeoIP.conf` with your `AccountID` and `LicenseKey` and save it.
- BadPackets API Key
    - Obtain API Key via https://badpackets.net/
    - Edit `VisIBoT/.env` and update the value for env variable `BADPACKETS_API_KEY` with your API Key
- Python 3.9
    - Please make sure you are using Python 3.9 when running the processing script.

# Setting up LiSa
```bash
# install docker and docker-compose onto your host

# Clone repository and enter URL Support Branch
➜  ~ git clone https://github.com/denBot/LiSa -b File-URL-Support
➜  ~ cd LiSa

# Update host IP address
➜  ~ vim docker-compose.yml
    # Edit "webhost: localhost:4242" to your desired IP/port (or keep default)

# Configure VirusTotal Analyzer
➜  ~ vim lisa/config.py
    # Uncomment 'lisa.analysis.virustotal.VirusTotalAnalyzer'
    # Add VirusTotal API Key to virus_total_key

# Build and run docker
➜  ~ docker-compose build
➜  ~ docker-compose up
    # run docker-compose build to build containers (do this whenever you modify LiSa source-code)
    # run docker-compose up to startup docker containers

```


# Setting up the backend
Execute the below commands to run the BadPackets processing script. This script processes all honeypot entities caught by BadPackets and exports API data into a MongoDB schema format. Payloads are automatically extracted from BP Results and are analysed using the `LiSa` malware sandbox mentioned above.

```bash
# Create, enter and setup virtual environment
➜  ~ cd src/backend
➜  ~ pip install --user virtualenv
➜  ~ virtualenv venv
➜  ~ source venv/bin/activate
➜  ~ python --version
Python 3.9.0

➜  ~ pip install -r requirements.txt

# Configure python-dotenv .env variables
➜  ~ cp .env.example .env
➜  ~ vim .env

# To run program
➜  ~ python main.py

# Set environment variables and run tests
➜  ~ export BADPACKETS_API_URL="https://api.badpackets.net/v1/"
➜  ~ export BADPACKETS_API_TOKEN="<your_api_token_here>"
➜  ~ pythom -m unittest discover
```

# Setting up nuxt.js and express.js
Execute the below commands to run local development servers for nuxt.js (frontend) and express.js (backend).

Note: building nuxt.js will generate a `dist` folder which is then loaded as a static directory by `express.js`, mapped to the base route `/`
```bash
# Install nodejs modules
➜  ~ cd src
➜  ~ npm install

# Run nuxt and express servers
➜  ~ npm run nuxt-dev
➜  ~ npm run exp-dev

# Run eslint tests
➜  ~ npm run eslint

# Build nuxt.js to dist folder
➜  ~ npm run build
```