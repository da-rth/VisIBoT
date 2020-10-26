"use strict"
const express = require("express")
//const Result = require("../../models/Result")
const GeoData = require("../../models/GeoData")

let router = express.Router()

const langs = ["de", "en", "es", "fr", "ja", "pt-BR", "ru", "zh-CN"]

const reduceGeoData = (geodata, lang) => {
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
}

router.route("/").get(async (req, res) => {
  let lang = langs.includes(req.query.lang) ? req.query.lang : "en"
  let nHoursAgo = new Date()

  nHoursAgo.setHours(nHoursAgo.getHours() - 24)

  GeoData.find({ updated_at: { $gte: nHoursAgo } })
    .lean()
    .exec(function (err, geodata) {
      if (err || !geodata)
        return res.status(400).send("Could not find any geodata.")
      geodata = geodata.map((geodata) => {
        return reduceGeoData(geodata, lang)
      })
      return res.send(JSON.stringify(geodata))
    })
})

module.exports = router
