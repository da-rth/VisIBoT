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

async function getAllConnections(ipGeo) {
  let allConnections = []

  let ipConn = await IpGeoConnection.findOne({ _id: ipGeo })
  let inConns = await IpGeoConnection.find({ connections: ipGeo })

  if (ipConn) {
    for (let conn of ipConn.connections) {
      let connGeo = await IpGeoData.findOne({ _id: conn })

      if (connGeo) {
        allConnections = allConnections.concat([
          [
            [ipGeo.data.coordinates, connGeo.data.coordinates],
            [ipGeo.id, connGeo.id],
            [ipGeo.server_type, connGeo.server_type],
          ],
        ])

        if (!ipConn.connections.includes(ipGeo.id)) {
          allConnections = allConnections.concat(
            await getAllConnections(connGeo)
          )
        }
      }
    }
  }

  for (let ipConn of inConns) {
    let inGeo = await IpGeoData.findOne({ _id: ipConn.id })

    for (let conn of ipConn.connections) {
      let connGeo = await IpGeoData.findOne({ _id: conn })

      if (connGeo) {
        allConnections = allConnections.concat([
          [
            [inGeo.data.coordinates, connGeo.data.coordinates],
            [inGeo.id, connGeo.id],
            [inGeo.server_type, connGeo.server_type],
          ],
        ])

        if (!ipConn.connections.includes(ipGeo.id)) {
          allConnections = allConnections.concat(
            await getAllConnections(connGeo)
          )
        }
      }
    }
  }

  return allConnections
}

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
  /**
  let ipGeo = await IpGeoData.findOne({ _id: req.params.ip })

  if (ipGonns == null) {
    return res
      .status(400)
      .send("No geo/connection data could be found for the given IP address.")
  }

  try {
    return res.status(200).send(ipConns)
  } catch (err) {
    console.error(err)
    return res
      .status(500)
      .send(
        "An error occurred when parsing database for IP address connections"
      )
  }
  **/
})

module.exports = router
