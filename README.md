# VisIBoT - Visualisation of IoT botnets

#### Contributors
- Author: [Daniel Arthur](mailto:2086380a@student.gla.ac.uk)
- Supervisor: [Angelos Marnerides](mailto:angelos.marnerides@glasgow.ac.uk)

### Summary
A browser-based visualisation tool that maps the geolocation and lifespan information of Mirai (IoT) Botnets.

Visualised data-sets will be collected, correlated and pre-processed through various APIs such as [BadPackets](https://docs.badpackets.net/), [Ripe NCC](https://www.ripe.net/) and [MaxMind](https://www.maxmind.com/en/home).

### Setting up the backend
```bash
# Create, enter and setup virtual environment
cd src/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure python-dotenv .env variables
cp .env.example .env
vim .env

# To run program
python main.py

# Set environment variables and run tests
export BADPACKETS_API_URL="https://api.badpackets.net/v1/"
export BADPACKETS_API_TOKEN="<your_api_token_here>"
pythom -m unittest discover
```
