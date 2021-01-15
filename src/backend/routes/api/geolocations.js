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
      const [marker, results, payloads] = all_results
      let m = marker.toJSON()
      m.payloads = payloads
      m.results = results
      return res.json(m)
    })
    .catch((err) => {
      console.error(err)
      return res.status(400).send("Could not find any details for given IP.")
    })
})

let getPayloadConnections = async function (ipGeoData) {
  let connections = []
  let allPayloads = await Payload.find({ ip_address: ipGeoData._id }).populate(
    "candidate_C2s"
  )

  for (let payload of allPayloads) {
    let payloadGeo = await GeoData.findOne({ _id: payload.ip_address })

    console.log(payload.candidate_C2s)

    let payloadResults = await Result.find({
      affiliated_ips: { $in: payload.ip_address },
    })

    let payloadResultsGeo = await GeoData.find({
      _id: { $in: payloadResults.map((result) => result.source_ip_address) },
    })

    connections = connections.concat(
      payload.candidate_C2s.map((geo) => {
        return [payloadGeo.data.coordinates, geo.data.coordinates, geo._id]
      })
    )

    connections = connections.concat(
      payloadResultsGeo.map((geo) => {
        return [payloadGeo.data.coordinates, geo.data.coordinates, geo._id]
      })
    )
  }
  return connections
}

let getC2Connections = async function (ipGeoData) {
  let connections = []
  let allPayloads = await Payload.find({ candidate_C2s: ipGeoData._id })

  for (let payload of allPayloads) {
    let payloadGeo = await GeoData.findOne({ _id: payload.ip_address })
    let candidateC2sGeo = await GeoData.find({
      _id: { $in: payload.candidate_C2s },
    })
    let payloadResults = await Result.find({
      affiliated_ips: { $in: payload.ip_address },
    }).populate("affiliated_ips")
    console.log(payloadResults)
    let payloadResultsGeo = await GeoData.find({
      _id: { $in: payloadResults.map((result) => result.source_ip_address) },
    })

    connections = connections.concat(
      candidateC2sGeo.map((geo) => {
        return [payloadGeo.data.coordinates, geo.data.coordinates, geo._id]
      })
    )

    connections = connections.concat(
      /**
      payloadResultsGeo.map((geo) => {
        return [payloadGeo.data.coordinates, geo.data.coordinates, geo._id]
      })**/
      payloadResultsGeo.map(async (geo) => await getPayloadConnections(geo))
    )
  }
  return connections
}

let getResultConnections = async function (ipGeoData) {
  let connections = []

  let allResults = await Result.find({
    source_ip_address: ipGeoData._id,
  })

  let allPayloads = await Payload.find({
    ip_address: {
      $in: allResults.map((result) => result.affiliated_ips).flat(),
    },
  })

  for (let payload of allPayloads) {
    let payloadGeo = await GeoData.findOne({ _id: payload.ip_address })
    let c2Geos = await GeoData.find({ _id: { $in: payload.candidate_C2s } })

    connections = connections.concat(await getPayloadConnections(payloadGeo))

    for (let c2geo of c2Geos) {
      connections = connections.concat(await getC2Connections(c2geo))
    }

    connections = connections.concat([
      [ipGeoData.data.coordinates, payloadGeo.data.coordinates, payloadGeo._id],
    ])
  }

  return connections
}

router.route("/connections/:ip").get(async (req, res) => {
  let ipAddress = req.params.ip
  let ipGeoData = await GeoData.findOne({ _id: ipAddress }).exec()

  if (ipGeoData === null) {
    return res
      .status(400)
      .send("No geo/connection data could be found for the given IP address.")
  }
  try {
    switch (ipGeoData.server_type) {
      case "Loader Server":
        return res.status(200).send(await getPayloadConnections(ipGeoData))
      case "C2 Server":
        return res.status(200).send(await getC2Connections(ipGeoData))
      default:
        return res.status(200).send(await getResultConnections(ipGeoData))
    }
  } catch (err) {
    console.error(err)
    return res
      .status(500)
      .send(
        "An error occurred when parsing database for IP address connections"
      )
  }
})

module.exports = router
