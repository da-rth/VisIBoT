const { Schema, model } = require("mongoose")

const schema = new Schema({
  _id: String,
  updated_at: Date,
  asn_registry: String,
  asn_cidr: String,
  asn_country_code: String,
  asn_description: String,
})

const AutonomousSystem = model("AutonomousSystem", schema, "autonomous_system")

module.exports = AutonomousSystem
