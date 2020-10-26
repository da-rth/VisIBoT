"use strict"
const express = require("express")
const GeoData = require("../../models/GeoData")

let router = express.Router()

const langs = ["de", "en", "es", "fr", "ja", "pt-BR", "ru", "zh-CN"]

router.route("/").get(async (req, res) => {
  let lang = langs.includes(req.query.lang) ? req.query.lang : "en"
  let hoursAgo = req.query.hoursAgo ?? 24
  let nHoursAgo = new Date()

  nHoursAgo.setHours(nHoursAgo.getHours() - hoursAgo)
  console.log("ping")
  GeoData.find({ updated_at: { $gte: nHoursAgo } })
    .lean()
    .exec(function (err, geodata) {
      if (err) return res.end("Could not find geodata.", 400)

      geodata = geodata.map((geodata) => {
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
      return res.send(JSON.stringify(geodata), 200)
    })
})

module.exports = router
