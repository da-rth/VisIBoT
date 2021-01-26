"use strict"
const express = require("express")
const { uniqWith, isEqual } = require("lodash")
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

function aggregateToConnection(aggConns) {
  let connections = []

  for (let conn of aggConns) {
    connections = connections.concat(conn.connections)
    delete conn.connections
    connections = connections.concat([conn])
  }

  return connections
}

async function goUpTree(ipAddress) {
  let connections = []

  let ipConns = await IpGeoConnection.aggregate([
    {
      $match: {
        destination_ip: ipAddress,
      },
    },
    {
      $graphLookup: {
        from: "ip_geo_connection",
        startWith: "$source_ip",
        connectFromField: "source_ip",
        connectToField: "source_ip",
        as: "connections",
      },
    },
  ])

  connections = connections.concat(aggregateToConnection(ipConns))

  ipConns = await IpGeoConnection.aggregate([
    {
      $match: {
        destination_ip: ipAddress,
      },
    },
    {
      $graphLookup: {
        from: "ip_geo_connection",
        startWith: "$source_ip",
        connectFromField: "source_ip",
        connectToField: "destination_ip",
        as: "connections",
      },
    },
  ])

  connections = connections.concat(aggregateToConnection(ipConns))

  console.log("up", connections)

  return connections
}

async function goDownTree(ipAddress) {
  let connections = []

  let ipConns = await IpGeoConnection.aggregate([
    {
      $match: {
        source_ip: ipAddress,
      },
    },
    {
      $graphLookup: {
        from: "ip_geo_connection",
        startWith: "$destination_ip",
        connectFromField: "destination_ip",
        connectToField: "source_ip",
        as: "connections",
      },
    },
  ])

  connections = connections.concat(aggregateToConnection(ipConns))

  ipConns = await IpGeoConnection.aggregate([
    {
      $match: {
        source_ip: ipAddress,
      },
    },
    {
      $graphLookup: {
        from: "ip_geo_connection",
        startWith: "$destination_ip",
        connectFromField: "destination_ip",
        connectToField: "source_ip",
        as: "connections",
      },
    },
  ])

  connections = connections.concat(aggregateToConnection(ipConns))

  return connections
}

router.route("/connections/:ip").get(async (req, res) => {
  let connections = []
  let ipAddress = req.params.ip

  connections = connections.concat(await goUpTree(ipAddress))
  connections = connections.concat(await goDownTree(ipAddress))

  let uniqueConnections = uniqWith(connections, isEqual)
  return res.status(200).send(uniqueConnections)
})

module.exports = router
