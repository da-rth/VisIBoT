const { Schema, model } = require("mongoose")

const schema = new Schema(
  {
    url: String,
    occurrences: Number,
    scan_url: String,
    hostname: String,
    ip_address: {
      type: Schema.Types.String,
      ref: "GeoData",
      required: true,
    },
    candidate_C2s: [{ type: Schema.Types.String, ref: "GeoData" }],
    updated_at: Date,
  },
  {}
)

const Payload = model("Payload", schema, "payload")

module.exports = Payload
