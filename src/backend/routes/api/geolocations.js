"use strict"
const express = require("express")

const GeoData = require("../../models/GeoData")
const Result = require("../../models/Result")
const Payload = require("../../models/Payload")

let router = express.Router()

// Helper Functions

let getPayloadConnections = async function (ipGeoData) {
  let connections = []
  let allPayloads = await Payload.find({ ip_address: ipGeoData._id }).populate(
    "ip_address candidate_C2s"
  )

  for (let payload of allPayloads) {
    let payloadResults = await Result.find({
      affiliated_ips: { $in: payload.ip_address._id },
    })

    let payloadResultsGeo = await GeoData.find({
      _id: { $in: payloadResults.map((result) => result.source_ip_address) },
    })

    connections = connections.concat(
      payload.candidate_C2s.map((geo) => {
        return [
          payload.ip_address.data.coordinates,
          geo.data.coordinates,
          geo._id,
        ]
      })
    )

    connections = connections.concat(
      payloadResultsGeo.map((geo) => {
        return [
          payload.ip_address.data.coordinates,
          geo.data.coordinates,
          geo._id,
        ]
      })
    )
  }
  return connections
}

let getC2Connections = async function (ipGeoData) {
  let connections = []
  let allPayloads = await Payload.find({
    candidate_C2s: ipGeoData._id,
  }).populate("ip_address")

  for (let payload of allPayloads) {
    connections = connections.concat(
      await getPayloadConnections(payload.ip_address)
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
  }).populate("ip_address candidate_C2s")

  for (let payload of allPayloads) {
    connections = connections.concat(
      await getPayloadConnections(payload.ip_address)
    )
  }

  /**
  let allResults = await Result.find({
    source_ip_address: ipGeoData._id,
  }).populate("scanned_urls.ip_address scanned_urls.candidate_C2s")

  for (let result of allResults) {
    for (let payload of result.scanned_urls) {
      connections = connections.concat(
        await getPayloadConnections(payload.ip_address)
      )
    }
  } **/

  return connections
}

// Routes

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
