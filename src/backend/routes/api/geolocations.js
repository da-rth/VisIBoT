"use strict"
const express = require("express")
//const Result = require("../../models/Result")
const GeoData = require("../../models/GeoData")

let router = express.Router()

const langs = ["de", "en", "es", "fr", "ja", "pt-BR", "ru", "zh-CN"]

router.route("/").get(async (req, res) => {
  let lang = langs.includes(req.query.lang) ? req.query.lang : "en"
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
