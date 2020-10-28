const { Schema, model } = require("mongoose")

const schema = new Schema(
  {
    _id: String,
    source_ip_address: { type: Schema.Types.String, ref: "GeoData" },
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
    scanned_payloads: [{ type: Schema.Types.ObjectId, ref: "Payload" }],
    updated_at: Date,
  },
  {}
)

const Result = model("Result", schema, "result")

module.exports = Result