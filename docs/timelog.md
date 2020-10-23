# Timelog

* ViSiBoT - Visualisation of IoT Botnets
* Daniel Arthur
* 2086380A
* Angelos Marnerides

## Guidance

* This file contains the time log for your project. It will be submitted along with your final dissertation.
* **YOU MUST KEEP THIS UP TO DATE AND UNDER VERSION CONTROL.**
* This timelog should be filled out honestly, regularly (daily) and accurately. It is for *your* benefit.
* Follow the structure provided, grouping time by weeks.  Quantise time to the half hour.

## Week 1

### 02 Oct 2020
* *0.5 hours* Watched [USENIX Security ’17 - Understanding Mirai Botnet2](https://www.youtube.com/watch?v=1pywzRTJDaY)
* *0.5 hours* Meeting with project supervisor
* *0.1 hours* Created MS Teams chat with supervisor and discussed project
* *0.5 hours* Setup private GitHub Repository and gave supervisor access
* *1.0 hours* Experimenting with BadPackets API via Postman and reading documentation
* *3.0 hours* Code: Created an initial API wrapper (and tests) for BadPackets API in Python

## Week 2

### 03 Oct 2020
* *0.5 hours* Researching python unittest module for project backend testing
* *3.0 hours* Code: Cleaning up tests, documentation and implemnting .env file(s) for project
* *1.0 hours* Setup travis CI/CD Pipeline for project
### 05 Oct 2020
* *1.0 hours* Reading IEEE paper [Identifying and Characterizing Bashlite and Mirai C&C Servers](https://ieeexplore.ieee.org/document/8969728)
### 07 Oct 2020
* *0.5 hours* Sketching [project architecture diagram](https://i.imgur.com/txPNTbT.png)
* *1.0 hours* Working on Bad Packets API Wrapper
### 08 Oct 2020
* *1.0 hours* Researching suitable IPLocation APIs
### 09 Oct 2020
* *1.0 hours* Created an hourly async task for processing API data in main.py
* *0.5 hours* Set up nuxt.js and express.js projects in src/ and renamed old backend to 'processing'"

## Week 3
* *1.0 hours* Updating travis .yml to allow pylama and unittest scripts to execute on push to master
* *3.0 hours* Added Google Maps API to frontend nuxt.js framework and experimented with map styling and pointer clustering

## Week 4
### 15 Oct 2020
* *1.0 hours* Updating styling for frontend Google Maps dashboard map
* *2.0 hours* Creating initial badpackets async loop for querying multiple requests with different parameters

## Week 5
### 22 Oct 2020
* *2.0 hours* Coding asynchronous background task implementation for badpackets hourly processing script
* *0.5 hours* Applied for VirusTotal Academic API token
### 23 Oct 2020
* *1.0 hours* Reading documentation on setting up auto-updating for maxminds GeoIP2 Lite database
* *5.0 hours* Coding various utility functions, mongodb integration and maxminds GeoIP2 integration into backend processing script
* *1.0 hours* Researched using VirusTotal as malware binary static analysis for identifying intersting strings such as IP addresses
* *0.5 hours* Created markdown file [here](architecture.md) as documentation for project architecture

