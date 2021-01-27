const { Schema, model } = require("mongoose")

const schema = new Schema({
  ip_address: [{ type: Schema.Types.String, ref: "IpGeoData" }],
  event_type: String,
  created_at: Date,
})

const IpEvent = model("IpEvent", schema, "ip_event")

module.exports = IpEvent
