"use strict"
const mongoose = require("mongoose")
const express = require("express")

let router = express.Router()
let connection = mongoose.connection
const langs = ["de", "en", "es", "fr", "ja", "pt-BR", "ru", "zh-CN"]

router.route("/").get(async (req, res) => {
  let lang = langs.includes(req.query.lang) ? req.query.lang : "en"

  let twentyFourHoursAgo = new Date()
  twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24)

  connection.db
    .collection("geo_data")
    .find({ updated_at: { $gte: twentyFourHoursAgo } })
    .map((geodata) => {
      return {
        ...geodata,
        data: {
          city: geodata.data.city.names[lang] ?? null,
          country: geodata.data.country.names[lang] ?? null,
          continent: geodata.data.continent.code,
        },
        position: {
          lat: geodata.data.coordinates.lat,
          lng: geodata.data.coordinates.lng,
        },
      }
    })
    .toArray((err, data) => {
      res.json(data)
    })
})

module.exports = router
