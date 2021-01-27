"use strict"
const express = require("express")

const IpGeoData = require("../../models/IpGeoData")
const IpEvent = require("../../models/IpEvent")
const BadpacketsResult = require("../../models/BadpacketsResult")
const MalwarePayload = require("../../models/MalwarePayload")
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
    BadpacketsResult.find({ source_ip_address: ip }),
    MalwarePayload.find({ ip_address: ip }),
    CandidateC2Server.findOne({ ip_address: ip }),
    CandidateP2PNode.findOne({ ip_address: ip }),
    IpEvent.find({ ip_address: ip }),
  ])
    .then((all_results) => {
      const [geoInfo, results, payloads, c2s, p2ps, events] = all_results
      return res.json({
        geoInfo,
        results,
        payloads,
        c2s,
        p2ps,
        events,
      })
    })
    .catch((err) => {
      console.error(err)
      return res.status(400).send("Could not find information for given IP.")
    })
})

module.exports = router
