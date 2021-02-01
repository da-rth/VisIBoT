const { Schema, model } = require("mongoose")

const schema = new Schema({
  source_ip: { type: Schema.Types.String, ref: "IpGeoData" },
  destination_ip: { type: Schema.Types.String, ref: "IpGeoData" },
  occurrences: Number,
  created_at: Date,
  updated_at: Date,
})

const IpGeoConnection = model("IpGeoConnection", schema, "ip_geo_connection")

module.exports = IpGeoConnection
