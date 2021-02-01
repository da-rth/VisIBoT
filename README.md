# VisIBoT - Visualisation of IoT botnets
![Main Build Status](https://travis-ci.com/denBot/VisIBoT.svg?token=pMfMcyEQzGJGFRQDBST5&branch=main)
* Author: [Daniel Arthur](mailto:2086380a@student.gla.ac.uk)
* Supervisor: [Angelos Marnerides](mailto:angelos.marnerides@glasgow.ac.uk)

VisIBoT is an automated solution to Command & Control Server (C2) Identifiaction. This project combines a variety of information sources and services, including the [BadPackets](https://badpackets.net/) Cyber Threat Intelligence API, [VirusTotal](https://virustotal.com/), [ipinfo.io](https://ipinfo.io/), the [LiSa Sandbox](https://github.com/danieluhricek/LiSa) and various [MaxMind](https://www.maxmind.com/en/home) GeoIP2 databases.

The VisIBoT processing scheduler will automatically collect BadPackets honeypot data and extract, execute and analyse botnet malware payloads using the LiSa sandbox on an hourly basis. Through combined static and dynamic analysis of malware payloads, we identify potential (candidate) Command & Control (C2) servers. Contained in various docker images, celery tasks are created from collected BadPackets results and are processed using a scalable number of celery workers. The task queue is maintained using redis and is designed to work with various celery workers. This ensures that even if a single worker fails, the task queue will not be halted and processing will continue.

The VisIBoT web-application is a browser-based visualisation tool that maps geolocation of identified potential bots, payload servers, peer-to-peer nodes and command-and-control servers. Written in Nuxt.js and hosted using Express.js, the main service uses Leaflet.js to cluster and annotate the geolocations of any identified botnet activity.


# Requirements
- A remotely accessible MongoDB Database (e.g. [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))
- A [MaxMind GeoIP Update API Key](https://www.maxmind.com/en/accounts/current/license-key):
    - Go to Account > My License Key > Generate New License Key > Yes > [1st Option] > Confirm
- A [BadPackets API Key](https://badpackets.net/)
- A [VirusTotal API Key](https://virustotal.com/)
- A [ipinfo.io API Key](https://ipinfo.io)
- A modified version of the [LiSa Sandbox Server](https://github.com/denBot/LiSa-modified)
    - (optional) An active VPN service connectable through a OpenVPN .ovpn file

--- 

# Setting up modified LiSa server
[LiSa](https://github.com/danieluhricek/LiSa) is a Linux Sandbox project created by [Daniel Uhříček](https://github.com/danieluhricek) which provides automated Linux malware analysis on various CPU architectures. I have modified this project (available [here](https://github.com/denBot/LiSa-modified)) to allow for the following additional features:
- Ability to create analysis tasks by submitting a malware URL instead of uploading a file
- Added binary unpacking for any binaries packed using the UPX packer software
- Added ability to provide external service API endpoints. POST requests are made to these endpoints when a given task fails/succeeds.

## Setup steps:
- install docker and docker-compose onto your host
1. Clone into `LiSa` repository and enter File-URL-Support branch
    ```bash
    ➜  ~ git clone https://github.com/denBot/LiSa-modified
    ➜  ~ cd LiSa
    ```
2. (Optional - skip if unsure) Edit `docker-compose.yml` and update `API_SUCCESS_URL` and `API_FAILURE_URL` environment variables to the IP address where the VisIBoT processing service Flask API is running. This should be running on port 5001 by default. The URL must contain the substring `<task_id>` at the end.
    ```yml
    worker:
      ...
      environment:
        - API_SUCCESS_URL=http://172.42.0.1:5001/api/lisa-analysis/success/<task_id>
        - API_FAILURE_URL=http://172.42.0.1:5001/api/lisa-analysis/failure/<task_id>
    ```
3. (Optional) Configure LiSa to use a VPN during analysis
    ```bash
    - mkdir vpn
    - mv ~/path/to/my_vpn.opvn vpn/config.ovpn
    ```
    - If your VPN requires a username and password to connect, edit the config.ovpn file and change the `auth-user-pass` line to `auth-user-pass /vpn/pass.txt`
    - Create a file in the `vpn` folder called `pass.txt` and put your login username/email on the first line of the file and your password on the second
    ```bash
    # pass.txt
    some-email@example.com
    some-password-1234
    ```
    - Lastly, edit `docker-compose.yml` and edit the `worker` section to include the following:
    ```yml
    worker:
      ...
      environment:
        - ...
        - VPN=/vpn
      volumes:
        - ...
        - "./vpn:/vpn"
      ...
    ```
    - **Note**: if your VPN only allows X connections at one time, you should not use more than X workers. Otherwise, workers may fail to connect to the VPN.
4. Configure the VirusTotal Analyzer to use your VirusTotal API KEY in `lisa/config.py`
    - Uncomment `'lisa.analysis.virustotal.VirusTotalAnalyzer'`
    - Assign variable `virus_total_key` to your VirusTotal API Key
5. Build docker images. This will take a while. You might need to use `sudo` too.
    ```bash
    ➜  ~ docker-compose build
    ```
6. Run the docker images (rebuild whenever you modify LiSa code, config, yml, etc...)
    ```bash
    ➜  ~ docker-compose build
    ➜  ~ docker-compose up # --scale worker={NUM_WORKERS_HERE}
    ```
6. Once running, visit `http://localhost:4242` (or whatever you set in `docker-compose.yml` and verify that LiSa is online.

Important notes:
- if you modify any LiSa code or the nginx webhost in `docker-compose.yml`, you will need to `docker-compose build` before running the services again.
- You can specify the number of **workers** used for running malware analysis tasks using the `--scale worker=NUM` docker-compose argument. The default is 1 but I recommend at least 2 or more.
- If you need to access any host (non-docker container) ports, such as the VisIBoT API port 5001, use the IP address `172.42.0.1` instead of `localhost` or `127.0.0.1`.

--- 

# Setting up the badpackets processing service
Execute the below commands to run the BadPackets processing script. This script processes all honeypot entities caught by BadPackets and exports API data into a MongoDB schema format. Payloads are automatically extracted from BP Results and are analysed using the `LiSa` malware sandbox mentioned above.

```bash
# Install Docker and Docker-compose (e.g. on ubuntu using apt-get)
➜  ~ sudo apt-get update && apt-get install docker docker-compose
➜  ~ cd src/processing

# Copy env example template and edit it.
# Add in your MongoDB URL and GeoIP2, BadPackets and ipinfo.io API keys.
➜  ~ cp .env.example .env
➜  ~ vim .env

# Build docker images and start-up the processing service
➜  ~ docker-compose build
➜  ~ docker-compose up --scale worker=NUM_OF_WORKERS
```
**Note:**
- You can specify the number of workers used when processing results. I would recommend 2 or more (I use 6).
- Edit the `.env` file to your liking. It contains useful comments explaining what each argument is for. The docker container will not run without specific environment variables being set.

# Setting up nuxt.js and express.js
Execute the below commands to run local development servers for nuxt.js (frontend) and express.js (backend).

**Note**: building nuxt.js will generate a `dist` folder which is then loaded as a static directory by `express.js`, mapped to the base route `/`
```bash
# Install nodejs modules
➜  ~ cd src
➜  ~ npm install

# Run nuxt and express servers
➜  ~ npm run nuxt-dev
➜  ~ npm run exp-dev
```
To run eslint, enter the following:
```bash
➜  ~ npm run eslint
```
To deploy the web application, build the nuxt.js app and start express.js:
```bash
➜  ~ npm run nuxt-generate
➜  ~ npm run exp-start
```
This will build the nuxt app into backend/dist which is then served via the express.js server at route `/`.