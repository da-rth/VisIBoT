const { Schema, model } = require("mongoose")

const schema = new Schema({
  _id: {
    type: Schema.Types.String,
    ref: "IpGeoData",
    required: true,
  },
  connections: [{ type: Schema.Types.String, ref: "GeoData" }],
})

const IpGeoConnection = model("IpGeoConnection", schema, "ip_geo_connection")

module.exports = IpGeoConnection
