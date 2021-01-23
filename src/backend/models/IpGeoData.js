const { Schema, model } = require("mongoose")

const schema = new Schema({
  _id: String,
  occurrences: Number,
  updated_at: Date,
  data: Object,
  server_type: String,
  hostname: String,
})

const IpGeoData = model("IpGeoData", schema, "ip_geo_data")

module.exports = IpGeoData
