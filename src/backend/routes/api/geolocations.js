"use strict"
const express = require("express")

const GeoData = require("../../models/GeoData")
const Result = require("../../models/Result")
const Payload = require("../../models/Payload")

let router = express.Router()

router.route("/").get(async (req, res) => {
  let nHoursAgo = new Date()

  nHoursAgo.setHours(nHoursAgo.getHours() - 24)

  GeoData.find({ updated_at: { $gte: nHoursAgo } })
    .lean()
    .select({
      server_type: 1,
      "data.coordinates.lat": 1,
      "data.coordinates.lng": 1,
      tags: 1,
    })
    .exec(function (err, geodata) {
      if (err || !geodata)
        return res.status(400).send("Could not find any geodata.")
      return res.json(geodata)
    })
})

router.route("/full-details/:ip").get(async (req, res) => {
  let ip = req.params.ip
  Promise.all([
    GeoData.findOne({ _id: ip }),
    Result.find({ source_ip_address: ip }),
    Payload.find({ ip_address: ip }),
  ])
    .then((all_results) => {
      const [marker, payloads, results] = all_results
      let m = marker.toJSON()
      m.payloads = payloads
      m.results = results
      return res.json(m)
    })
    .catch(() => {
      return res.status(400).send("Could not find any details for given IP.")
    })
})

module.exports = router
