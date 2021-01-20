const { Schema, model } = require("mongoose")

const schema = new Schema(
  {
    occurrences: Number,
    ip_address: {
      type: Schema.Types.String,
      ref: "GeoData",
      required: true,
    },
    payloads: [{ type: Schema.Types.String, ref: "Payload" }],
    updated_at: Date,
  },
  {}
)

const CandidateC2Server = model(
  "CandidateC2Server",
  schema,
  "candidate_c2_server"
)

module.exports = CandidateC2Server
