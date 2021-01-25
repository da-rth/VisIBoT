const { Schema, model } = require("mongoose")

const schema = new Schema(
  {
    source_ip_address: { type: Schema.Types.String, ref: "IpGeoData" },
    country: String,
    user_agent: Object,
    payload: String,
    post_data: String,
    target_port: Number,
    protocol: String,
    event_count: Number,
    first_seen: Date,
    last_seen: Date,
    tags: Array,
    scanned_urls: [{ type: Schema.Types.String, ref: "MalwarePayload" }],
    affiliated_ips: [{ type: Schema.Types.String, ref: "IpGeoData" }],
    created_at: Date,
    updated_at: Date,
  },
  {}
)

const BadpacketsResult = model("BadpacketsResult", schema, "badpackets_result")

module.exports = BadpacketsResult
