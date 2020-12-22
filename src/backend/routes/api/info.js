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
  let nHoursAgo = new Date()

  nHoursAgo.setHours(nHoursAgo.getHours() - 24)

  Result.find({ updated_at: { $gte: nHoursAgo } })
    .select({ tags: 1, _id: 0 })
    .lean()
    .exec(function (err, tags) {
      let alltags = []
      for (let tag of tags) {
        let tags = tag.tags
        alltags.push(tags)
      }
      console.log(alltags.length)
      alltags = alltags.flat()
      console.log(alltags.length)
      alltags = [
        ...new Map(alltags.map((item) => [item.description, item])).values(),
      ]
      console.log(alltags.length)
      return getDocsResponse(res, alltags)
    })
})

module.exports = router
