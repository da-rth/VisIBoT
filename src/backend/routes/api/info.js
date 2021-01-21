"use strict"
const express = require("express")

const GeoData = require("../../models/GeoData")
const Result = require("../../models/Result")
const Payload = require("../../models/Payload")
const CandidateC2Server = require("../../models/CandidateC2Server")

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

  Result.find({ updated_at: { $gte: nHoursAgo } })
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

router.route("/:ip").get(async (req, res) => {
  let ip = req.params.ip
  Promise.all([
    GeoData.findOne({ _id: ip }),
    Result.find({ source_ip_address: ip }).populate("scanned_urls"),
    Payload.find({ ip_address: ip }).populate("candidate_C2s"),
    CandidateC2Server.findOne({ ip_address: ip }).populate("payloads"),
  ])
    .then((all_results) => {
      const [geoInfo, results, payloads, c2s] = all_results
      return res.json({
        geoInfo,
        results,
        payloads,
        c2s,
      })
    })
    .catch((err) => {
      console.error(err)
      return res.status(400).send("Could not find information for given IP.")
    })
})

module.exports = router
