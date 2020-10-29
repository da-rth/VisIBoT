"use strict"
const express = require("express")
const GeoData = require("../../models/GeoData")

let router = express.Router()

router.route("/").get(async (req, res) => {
  let nHoursAgo = new Date()

  nHoursAgo.setHours(nHoursAgo.getHours() - 24)

  GeoData.find({ updated_at: { $gte: nHoursAgo } })
    .lean()
    .exec(function (err, geodata) {
      if (err || !geodata)
        return res.status(400).send("Could not find any geodata.")
      return res.json(geodata)
    })
})

module.exports = router
