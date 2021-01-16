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
### 24 Oct 2020
* *6.0 hours* Implemented thread-pooling for badpackets processing script
* *1.0 hours* Added user-agent parsing to badpackets processing script


## Week 6

### 25 Oct 2020
* *2.0 hours* Researched and added virustotal and Ripe NCC Python APIs to preprocessing script
* *1.0 hours* Improved URL parsing method for backend result processing
* *1.0 hours* Documented all processing methods
* *4.0 hours* Created API routing and a new endpoint in express server for processed geolocations

### 26 Oct 2020
* *2.0 hours* Researched the leaflet map javascript library
* *1.0 hours* Researched marker clustering using leaflet
* *2.0 hours* Changed google maps to leaflet in frontend Nuxt.js map component
* *1.0 hours* Created a GeoData model via mongoose in express.js backend server
* *2.0 hours* Researching and implementing multi-job CI/CD pipeline with Travis-ci
* *3.0 hours* Refactored store_results method in badpackets processing utilities

### 28 Oct 2020
* *1.0 hours* Removed the reduction of GeoData objects when returning results via /api/geolocations (was too slow)

### 29 Oct 2020
* *3.0 hours* Added custom svg markers to leaflet map representing different types of servers
* *2.0 hours* Created api/info/results endpoint for returning badpackets results of a given geolocation


## Week 7

### 30 Oct 2020
* *1.0 hours* Added popup for each marker on leaflet map with 3 buttons
* *2.0 hours* Added argument parsing for processing script
* *0.5 hours* Fixed various pylama errors in code
* *0.5 hours* Added additional documentation to misc utility functions in processing script
* *0.5 hours* Added languages to navbar dropdown in navbar component of frontend web app

### 31 Oct 2020
* *3.0 hours* Researching C2 server identification techniques through malware string extraction
* *2.0 hours* Improved url extraction method for processing script
* *1.0 hours* Additional refactors to url extraction code

### 01 Nov 2020
* *0.5 hours* Removed Ripe NCC api from processing script
* *4.0 hours* Created virustotal script with a rate-limiting handler
* *0.5 hours* Added documentation for virustotal utility class
* *1.0 hours* Added stacktracing to ThreadPoolExecutor
* *2.0 hours* Created and implemented some 'create_or_update' helper functions in database.py
* *2.0 hours* Fixed various bugs present in badpackets results processing function
* *1.0 hours* Registering for AWS services


## Week 8

### 03 Nov 2020
* *0.5 hours* Fixed various pylama errors in processing script
* *2.0 hours* Experimenting with AWS Lambda functions service
* *4.0 hours* Creation of flare-floss lambda function for performing static analysis on files remotely
* *1.0 hours* Added busybox payload deobfuscation function to misc.py for later use

### 04 Nov 2020
* *3.0 hours* Created new IP Validation process for flare-floss lambda function

### 05 Nov 2020
* *1.0 hours* Upgraded AWS lambda function from python2.7 to python3.7
* *4.0 hours* Re-wrote aws lambda function to remove flare-floss dependency
* *1.0 hours* Researching traceroutes diagnostic command usage

### 06 Nov 2020
* *7.0 hours* Working on frontend (nuxt) interface

### 06 Nov 2020
* *4.0 hours* Added i18n internationalization (language support) to Nuxt frontend
* *2.0 hours* Improved URL Parsing process to ignore specific top-level domains


## Week 9

### 11 Nov 2020
* *3.0 hours* Reserching potential Linux malware sandboxes
* *3.0 hours* Trying out Cuckoo and Detux malware sandboxes

### 13 Nov 2020
* *4.0 hours* Reading and taking notes on https://ieeexplore.ieee.org/document/4116687
* *3.0 hours* Reading and taking notes on https://www.researchgate.net/publication/327622713_Spatial_Statistics_as_a_Metric_for_Detecting_Botnet_C2_Servers


## Week 10

### 19 Nov 2020
* *3.0 hours* Reading and taking notes on research paper https://onlinelibrary.wiley.com/doi/full/10.1002/sec.431
* *4.0 hours* Reading and taking notes on research paper https://ieeexplore.ieee.org/document/8969728
* *4.0 hours* Reading and taking notes on research paper https://www.mdpi.com/1424-8220/19/3/727


## Week 11

### 07 Dec 2020
* *3.0 hours* Creating flow-chart for processing script via draw.io
* *2.0 hours* Researching LiSa Linux Sandbox

### 12 Dec 2020
* *4.0 hours* Setting up and testing LiSa Linux Sandbox


## Week 12

### 14 Dec 2020
* *6.0 hours* Modifying LiSa source-code to allow for URL submissions and bash script execution
* *1.0 hours* Meeting with supervisor discussing project status

### 15 Dec 2020
* *1.0 hours* Updating README.md with more detailed setup instructions
* *0.5 hours* Updated .env.example with new env variables
* *0.5 hours* Removing un-needed utility modules from processing project
* *4.0 hours* Modifying LiSa source-code to allow for custom filename and arguments

### 16 Dec 2020
* *4.0 hours* Created API wrapper for LiSa sandbox integration with processing script
* *2.0 hours* Integrated LiSa API into payload analysis stage of processing script
* *1.0 hours* Added blacklist checking using pydnsbl to shortlist candidate C2 servers
* *3.0 hours* Implemented geodata creation for candidate C2 servers and fixed various bugs

## Week 13
### 22 Dec 2020
* *8.0 hours* Front-end nuxt.js development - working on map sidebar features and new express.js backend api endpoint

### 23 Dec 2020
* *5.0 hours* Finished implementing map sidebar settings functionality
* *3.0 hours* Updating frontend language translation for sidebar and navbar text-content

## Week 16
### 8 Jan 2020
* *3.0 hours* Refactoring some modifications to LiSa codebase
* *5.0 hours* Researching and experimenting with URL phising detection via Machine Learning and Data Science techniques

## Week 17
### 12 Jan 2020
* *3.0 hours* Refactoring pre-processing script
* *3.0 hours* Initial implementation of marker connections API endpoint via express.js

### 14 Jan 2020
* *4.0 hours* Further coding implementation for marker connections API endpoint
* *1.0 hours* Implemented tftp URL extraction in utils/misc.py used by urlparser

### 15 Jan 2020
* *2.0 hours* Refactored processing script URL validation stage and modified Payload + Results database tables to include references to related markers
* *1.0 hours* Style-changes to Nuxt.js app Map Sidebar CSS
* *6.0 hours* Integrated connections API endpoint into frontend web app and finished initial implementation of marker connections feature
* *0.5 hours* Fixing linting bugs (pylama, eslint)
* *1.5 hours* Added various translations to web app, fixed a modal popup bug caused by possibly null geodata city attribute, started initial popup modal layout changes.
