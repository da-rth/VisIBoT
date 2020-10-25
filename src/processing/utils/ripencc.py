import os
# import json
from datetime import datetime
from ripe.atlas.cousteau import (
  Ping,
  AtlasSource,
  AtlasCreateRequest
)

SOME_IP = '205.185.115.72'
API_KEY = os.getenv("RIPENCC_API_KEY")

ping = Ping(af=4, target=SOME_IP, description="testing new wrapper")
source = AtlasSource(type="area", value="WW", requested=5)

atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    key=API_KEY,
    measurements=[ping],
    sources=[source],
    is_oneoff=True
)

(is_success, response) = atlas_request.create()

# print(json.dumps(response, sort_keys=False, indent=4))
