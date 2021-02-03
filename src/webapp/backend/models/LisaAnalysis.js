const { Schema, model } = require("mongoose")

const schema = new Schema(
  {
    _id: String,
    payload: {
      type: Schema.Types.String,
      ref: "MalwarePayload",
      required: true,
    },
    created_at: Date,
  },
  { strict: false }
)

const LisaAnalysis = model("LisaAnalysis", schema, "lisa_analysis")

module.exports = LisaAnalysis
