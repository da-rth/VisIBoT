"use strict"
const express = require("express")

const IpGeoData = require("../../models/IpGeoData")
const IpEvent = require("../../models/IpEvent")
const IpInfo = require("../../models/IpInfo")
const BadpacketsResult = require("../../models/BadpacketsResult")
const MalwarePayload = require("../../models/MalwarePayload")
const IpGeoConnection = require("../../models/IpGeoConnection")
const CandidateC2Server = require("../../models/CandidateC2Server")
const CandidateP2PNode = require("../../models/CandidateP2PNode")

let router = express.Router()

const getDocsResponse = (res, docs) => {
  if (docs && docs.length) {
    return res.status(200).json(docs)
  } else {
    return res
      .status(400)
      .send(
        "Could not find any information results matching with the given IP Address"
      )
  }
}

router.route("/search-tags").get(async (req, res) => {
  /**
   * Returns an unique array of tags that are used for searching
   */
  let nHoursAgo = new Date()

  nHoursAgo.setHours(nHoursAgo.getHours() - 24)

  BadpacketsResult.find({ updated_at: { $gte: nHoursAgo } })
    .select({ tags: 1, _id: 0 })
    .lean()
    .exec(function (err, tags) {
      let allTags = []

      for (let tag of tags) {
        let tags = tag.tags
        allTags.push(tags)
      }

      return getDocsResponse(res, [
        ...new Map(
          allTags.flat().map((item) => [item.description, item])
        ).values(),
      ])
    })
})

router.route("/summary/:ip").get(async (req, res) => {
  let ip = req.params.ip
  Promise.all([
    IpGeoData.findOne({ _id: ip }).populate("asn"),
    BadpacketsResult.findOne({ source_ip_address: ip }).sort({
      last_seen: "desc",
    }),
    MalwarePayload.find({ ip_address: ip }).populate({
      path: "lisa",
      select:
        "-network_analysis.http_requests -network_analysis.endpoints -virustotal.scans",
    }),
    IpEvent.find({ ip_address: ip }),
    IpGeoConnection.find({
      $or: [{ source_ip: ip }, { destination_ip: ip }],
    }).populate([
      { path: "source_ip", select: "server_type" },
      { path: "destination_ip", select: "server_type" },
    ]),
    CandidateC2Server.findOne({ ip_address: ip }),
    CandidateP2PNode.findOne({ ip_address: ip }),
    IpInfo.findOne({ ip_address: ip }).select("privacy"),
  ])
    .then((all_results) => {
      const [
        geoInfo,
        latestResult,
        payloads,
        events,
        connections,
        c2,
        p2p,
        ipInfo,
      ] = all_results

      return res.json({
        geoInfo,
        latestResult,
        payloads,
        events,
        connections,
        c2,
        p2p,
        ipInfo,
      })
    })
    .catch((err) => {
      console.error(err)
      return res.status(400).send("Could not find information for given IP.")
    })
})

module.exports = router
