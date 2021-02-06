const { Schema, model } = require("mongoose")

const schema = new Schema(
  {
    ip_address: [{ type: Schema.Types.String, ref: "IpGeoData" }],
  },
  { strict: false }
)

const IpInfo = model("IpInfo", schema, "ip_info")

module.exports = IpInfo
