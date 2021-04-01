# Timelog

* ViSiBoT - Visualisation of IoT Botnets
* Daniel Arthur
* 2086380A
* Angelos Marnerides


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

### 16 Jan 2020
* *2.0 hours* Researching malicious URL classification techniques and data-sets
* *5.5 hours* Added malicious URL classification to URL Validation process during BadPackets payload extraction in processing script

### 17 Jan 2020
* *9.0 hours* Re-writing and improving malware analysis stage of processing script.


## Week 18

### 18 Jan 2020
* *1.0 hours* Modifying LiSa source-code to account for API throttling caused by processing script
* *7.0 hours* Re-writing LiSa API integration to work around API throttling and inconsistent API response formats

### 19 Jan 2020
* *3.0 hours* Testing and refactoring LiSa C2 heuristics stage of processing script
* *3.0 hours* Working on frontend web application features, including showing IP connections and marker color scheme changes

### 20 Jan 2020
* *2.0 hours* Various improvements to the web application endpoint /api/info/<ip>
* *1.0 hours* Fixing various linting errors highlighted by pylama/eslint
* *4.0 hours* Refactpromg backend lisa.py module. Fixed various database related bugs when updating records.

### 21 Jan 2020
* *6.0 hours* Re-writing and improving lisa.py module integration with external LiSa API
* *1.0 hours* Restructured database schema such that LiSa analysis results are stored in a separate table

### 23 Jan 2020
* *1.5 hours* Renaming several MongoDB documents/models in database.py
* *2.0 hours* Updating and cleaning up web application back-end server following databse document name changees

### 24 Jan 2020
* *1.0 hours* Researched the use of tor as a python requests proxy
* *3.0 hours* Added tor proxy integration into visibot processing script
* *2.5 hours* Various improvements to payload URL scraping utility functions in utils.py


## Week 19

### 25 Jan 2020
* *1.0 hours* Updated various mongodb documents to include a created_at timestamp (UTC format)
* *4.0 hours* Improvements to frontend web application modal popup when interacting with points on the map

### 26 Jan 2020
* *3.0 hours* Implemented ipwhois python module into processing script geolocation creation stage. Allows for collection of various ASN data for given IP addresses.
* *3.0 hours* Changes to frontend pop up modal, including creation/styling of code-blocks and tab-based menus
* *2.0 hours* Re-write web app backend endpont /api/geolocations/connections/<ip> to use more efficient MongoDB graphLookup to obtain an array of all connection geocoordinates for a given IP address.

### 27 Jan 2020
* *4.0 hours* Fixed a bug in ipwhois.py. Had to re-write datestring parsing method using the dateutil python module
* *2.0 hours* Created a new tab for "events" in frontend popup modal page. Some additional minor features and styling.
* *1.0 hours* Added new radiobutton to map sidebar that allows for clusters to be toggled on/off when viewing connections.

### 28 Jan 2020
* *1.5 hours* Added ipinfo.io API integration into processing script. Added some environment variables allowing users to toggle to usage of APi for C2 candidates only.
* *0.5 hours* Fixed various pylama and eslint errors caught by linting tools
* *3.0 hours* Researching potential implementations for dockerizing processing script into various docker containers

### 29 Jan 2020
* *2.0 hours* Additional research gathering information on flask, celery and redis for possible concurrent task queueing in processing script setup
* *4.0 hours* Created a new base project using docker-compose and installed celery, redis and flask for experimentation.

### 30 Jan 2020
* *3.0 hours* Initial transition from processing scripts previous use of threadpooling to a celery task queue. Several blockers encountered.
* *3.0 hours* Created new processing directory structure and a scheduler python image which interacts with various celery workers on an hourly basis
* *2.0 hours* Updated LiSa instance to contact processing flask server when analysis tasks have failed/succeeded

### 31 Jan 2020
* *3.0 hours* Additional transitions from previous code to new dockerized version.
* *2.0 hours* Created a mew docker image responsible for hosting and updating geoip2 databases on a weekly basis using cron.
* *3.0 hours* Created a new docker image for hosting tor proxy used for proxy-ing various VisIBoT processor HTTP requests


## Week 20

### 01 Feb 2020
* *4.0 hours* Refactoring various parts old processing code to work with new dockerized celery workers and task scheduler.
* *0.5 hours* Fixed various pylama errors raised during transition to a new dockerized environment
* *1.0 hours* Updated README.md with new documentation explaining docker installation procedure
* *0.5 hours* Updated .env.example to include new environment variable placeholders for API keys
* *1.0 hours* Updaating travis-ci.yml with new directory structure of processing code

### 02 Feb 2020
* *1.0 hours* Added documentation for various methods in scheduler, api and badpackets modules
* *0.5 hours* Attempts to resolve a warning raised due to TLDExtract PermissionError
* *1.0 hours* Fixed an error that occurs due to VirusTotal KeyError when storing lisa analysis in lisa.py
* *3.0 hours* Modifications and new features added to front-end web application, including IP address search bar
* *1.0 hours* Updated models in express.js backend and added LiSa analysis to /info endpoint results
* *2.0 hours* Forked new LiSa API repo and moved modifications to public fork.

###  03 Feb 2020
* *4.0 hours* New route created for frontend web app: /info/<ip>. This allows users to copy URL and re-visit map with IP address popup modal immediately activated.
* *2.0 hours* Fixed bug in validate_urls.py causing several extracted URLs to be ignored.
* *1.0 hours* Updated web app directory to use various utility functions in utilities/utils.js

### 04 Feb 2020
* *2.0 hours* Fixed various pylama and eslint errors
* *2.0 hours* Updated frontend popup modal to include information about candidate C2/P2P nodes
* *0.5 hours* Updating README.md with link to new (modified) LiSa fork

### 05 Feb 2020
* *4.0 hours* Refactoring and fixing bugs in lisa.py

### 06 Feb 2020
* *3.0 hours* Updated translations for locales fr, jp, pt, ru
* *1.0 hours* Fixing typos in translations
* *1.0 hours* Created custom 404 page with translations
* *1.0 hours* Added hrefs for Bad Packets, Geo IP2, etc...
* *2.0 hours* Fixed nuxt.js routes and styled about page


## Week 21

### 08 Feb 2020
* *1.0 hours* Updated .env.example to reflect new changes
* *0.5 hours* Added sleep between badpackets API calls to prevent throttling
* *3.0 hours* Made several changes to nuxt.js and express.js for deployment
* *2.0 hours* Fixed bug with alltags API in express.js caused by flat()
* *1.0 hours* Additional cahnges to about page (light mode)

### 09 Feb 2020
* *1.0 hours* Added 'restart: always' to docker worker container to ensure that failed analysis tasks can recover
* *2.0 hours* Planning dissertation structure and creating overleaf project

### 10 Feb 2020
* *1.0 hours* Configured REDIS to use password protection for security
* *2.0 hours* Read Chapter 1 of Peer-to-Peer Botnets https://www.eecs.ucf.edu/~czou/research/P2PBotnets-bookChapter.pdf

### 11 Feb 2020
* *1.0 hours* Created revised flow/architecture diagram to documentation
* *2.0 hours* Modified visibot scheduler to fix bug and increase wait time between API calls
* *0.5 hours* Added restart: always to flower container docker config


## Week 22

### 16 Feb 2020
* *2.0 hours* Fixed database.py bug caused by KeyError in scanned_playloads
* *2.0 hours* Fixed KeyError encountered in database.py and fixed several pylama errors

### 19 Feb 2020
* *3.0 hours* Creating system architecture diagrams for dissertation


## Week 24

### 24 Feb 2020
* *2.0 hours* Added starting code for graph generation using NetworkX
* *3.5 hours* Fixed slow loading bug for P2P connections on Web App dashboard (express.js issue caused by lodash)
* *1.0 hours* Renamed all instances of 'BadPackets' with 'Bad Packets', to ensure correct trademark is used

### 26 Feb 2020
* *5.0 hours* Researching and writing background for dissertation

### 27 Feb 2020
* *6.0 hours* Researching and writing background for dissertation

### 28 Feb 2020
* *4.0 hours* Finishing first iteration of background section


## Week 25

### 02 Mar 2020
* *1.0 hours* Meeting with supervisor regarding current state of disseration
* *3.0 hours* Planning and restructuring disseration contents following meeting with supervisor
* *3.0 hours* Read papers recommended by supervisor: https://dl.acm.org/doi/10.1145/3307772.3328305 https://ieeexplore.ieee.org/document/9014300

### 04 Mar 2020
* *3.0 hours* Researching background texts on the evolution of botnets
* *2.0 hours* Writing initial sub-section on evolution of botnets

### 05 Mar 2020
* *3.0 hours* Researching how to create an ER Diagram for MongoDB Databases
* *2.0 hours* Re-captioning and screen-shotting several graphs for dissertation
* *1.0 hours* Re-structuring of latex document to allow for increased readability

### 06 Mar 2020
* *2.0 hours* Generating ER diagram for dissertation section
* *1.0 hours* Generating docker image diagram
* *6.0 hours* Writing implementation section for dissertation


## Week 26
### 08 Mar 2020
* *6.0 hours* Writing implementation section for dissertation
* *0.5 hours* Adding screenshots of web application into implementation and appendix sections

### 09 Mar 2020
* *2.0 hours* Re-formatting bibliography
* *2.0 hours* Referencing resources mentioned in implementation section

### 10 Mar 2020
* *3.0 hours* Created several low-level and high-level flow diagrams used within dissertation
* *2.0 hours* Added diagrams to dissertation as figures (in appendix and implementation sections)
* *3.0 hours* Finished writing implementation section

### 13 Mar 2020
* *4.0 hours* Started re-writing background of dissertation based on advice from supervisor
* *3.0 hours* Researching papers whilst writing

### 14 Mar 2020
* *7.0 hours* Continued writing of the background section of the dissertation


## Week 27
### 15 Mar 2020
* *1.0 hours* Re-structuring dissertation sub-sections, headings, etc.
* *4.0 hours* Researching relevant papers for background
* *4.0 hours* Finishing background section of dissertation

### 16 Mar 2020
* *4.0 hours* Re-writing graph code to produce C2 ASN and P2P Payload graphs/stats tables
* *3.0 hours* Writing results section of dissertation
* *2.0 hours* Writing problem analysis section of dissertation

### 17 Mar 2020
* *6.0 hours* Writing results section of dissertation
* *1.0 hours* Re-structuring results section to fit in necessary visualisations/graphs
* *3.0 hours* Finished problem analysis section

### 18 Mar 2020
* *4.0 hours* Writing evaluation sub-section of results dissertation section
* *3.0 hours* Writing design overview section of dissertation

### 19 Mar 2020
* *3.0 hours* Finishing evaluation section
* *5.0 hours* Writing conclusion section of dissertation

### 20 Mar 2020
* *4.0 hours* Re-writing/shortening parts of the conclusion
* *3.0 hours* Writing future work section
* *1.5 hours* Finishing design overview section of dissertation

### 21 Mar 2020
* *2.0 hours* Proof reading results, evaluation, and conclusion
* *2.0 hours* Fixing typos, grammatical errors and re-phrasing paragraphs


## Week 28

### 22 Mar 2020
* *5.0 hours* Continued research and writing of introduction chapter for dissertation

### 23 Mar 2020
* *3.0 hours* Cleaning and double-checking references
* *1.0 hours* Fixing overlapping URL bug in latex document
* *3.0 hours* Finishing introduction chapter of dissertation

### 24 Mar 2020
* *2.0 hours* Re-deploying VisiBot for future data-collection
* *2.0 hours* Proof-reading dissertation
* *2.0 hours* Spell-checking dissertation (completed first draft)
* *0.5 hours* Notified supervisor of first draft completion

### 27 Mar 2020
* *1.0 hours* Updating README.md and removing unused graph code


## Week 29

### 01 Apr 2020
* *2.0 hours* Cleaning up repository structure and README
* *1.0 hours* Final meeting with supervisor