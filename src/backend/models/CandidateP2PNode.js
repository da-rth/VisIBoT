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
    nodes: [{ type: Schema.Types.String, ref: "CandidateP2PNode" }],
    heuristics: [String],
    updated_at: Date,
  },
  {}
)

const CandidateP2PNode = model("CandidateP2PNode", schema, "candidate_p2p_node")

module.exports = CandidateP2PNode
