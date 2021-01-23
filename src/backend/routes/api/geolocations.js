"use strict"
const express = require("express")

const IpGeoData = require("../../models/IpGeoData")
const IpGeoConnection = require("../../models/IpGeoConnection")

let router = express.Router()

router.route("/").get(async (req, res) => {
  let nHoursAgo = new Date()

  nHoursAgo.setHours(nHoursAgo.getHours() - 24)

  IpGeoData.find({ updated_at: { $gte: nHoursAgo } })
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
  let ipConns = await IpGeoConnection.aggregate([
    {
      $match: {
        source_ip: req.params.ip,
      },
    },
    {
      $graphLookup: {
        from: "ip_geo_connection",
        startWith: "$destination_ip",
        connectFromField: "destination_ip",
        connectToField: "source_ip",
        as: "connections",
        restrictSearchWithMatch: {
          destination_ip: {
            $ne: req.params.ip,
          },
        },
      },
    },
  ])

  if (!ipConns.length) {
    ipConns = await IpGeoConnection.aggregate([
      {
        $match: {
          destination_ip: req.params.ip,
        },
      },
      {
        $graphLookup: {
          from: "ip_geo_connection",
          startWith: "$source_ip",
          connectFromField: "source_ip",
          connectToField: "destination_ip",
          as: "connections",
          restrictSearchWithMatch: {
            source_ip: {
              $ne: req.params.ip,
            },
          },
        },
      },
    ])
  }

  let connections = []

  for (let ipConn of ipConns) {
    connections = connections.concat(ipConns[0].connections)
    delete ipConn.connections
    connections = connections.concat([ipConn])
  }

  return res.status(200).send(connections)
})

module.exports = router
