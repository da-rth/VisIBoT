const { Schema, model } = require("mongoose")

const schema = new Schema(
  {
    occurrences: Number,
    ip_address: {
      type: Schema.Types.String,
      ref: "IpGeoData",
      required: true,
    },
    payloads: [{ type: Schema.Types.String, ref: "MalwarePayload" }],
    heuristics: [String],
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
