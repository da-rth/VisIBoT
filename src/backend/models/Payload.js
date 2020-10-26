const { Schema, model } = require("mongoose")

const schema = new Schema(
  {
    url: String,
    scan_url: String,
    hostname: String,
    ip_address: {
      type: Schema.Types.String,
      ref: "GeoData",
      required: true,
    },
    updated_at: Date,
  },
  {}
)

const Payload = model("Payload", schema, "payload")

module.exports = Payload
