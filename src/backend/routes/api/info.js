"use strict"
const express = require("express")
const Result = require("../../models/Result")
const Payload = require("../../models/Payload")

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

router.route("/result/:ipAddress").get(async (req, res) => {
  Result.find({ source_ip_address: req.params.ipAddress })
    .sort("-updated_at")
    .populate("scanned_payloads")
    .lean()
    .exec(function (err, docs) {
      return getDocsResponse(res, docs)
    })
})

router.route("/payload/:ipAddress").get(async (req, res) => {
  Payload.find({ ip_address: req.params.ipAddress })
    .sort("-updated_at")
    .lean()
    .exec(function (err, docs) {
      return getDocsResponse(res, docs)
    })
})

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

module.exports = router
