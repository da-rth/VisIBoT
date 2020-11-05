"use strict"
const express = require("express")
const GeoData = require("../../models/GeoData")

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
    })
    .exec(function (err, geodata) {
      if (err || !geodata)
        return res.status(400).send("Could not find any geodata.")
      return res.json(geodata)
    })
})

router.route("/full-details/:ip").get(async (req, res) => {
  GeoData.findOne({ _id: req.params.ip })
    .lean()
    .exec(function (err, marker) {
      if (err || !marker)
        return res.status(400).send("Could not find any geodata.")

      marker.infoType =
        marker.server_type == "Loader Server" ? "payload" : "result"

      return res.json(marker)
    })
})

module.exports = router
