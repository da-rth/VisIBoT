const { Schema, model } = require("mongoose")

const schema = new Schema(
  {
    _id: String,
    updated_at: Date,
    data: Object,
    server_type: String,
    hostname: String,
  },
  {
    toJSON: {
      transform: function (doc, ret) {
        // TODO
        return ret
      },
    },
  }
)

const GeoData = model("GeoData", schema, "geo_data")

module.exports = GeoData
