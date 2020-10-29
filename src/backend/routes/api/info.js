"use strict"
const express = require("express")
const Result = require("../../models/Result")
const Payload = require("../../models/Payload")

let router = express.Router()

router.route("/result/:ipAddress").get(async (req, res) => {
  Result.find({ source_ip_address: req.params.ipAddress })
    .populate("scanned_payloads")
    .lean()
    .exec(function (err, docs) {
      console.log(err)
      if (err || !docs.length) {
        return res
          .status(400)
          .send("Could not find any results matching with the given IP Address")
      }
      return res.status(200).json(docs)
    })
})

router.route("/payload/:ipAddress").get(async (req, res) => {
  Payload.findOne({ ip_address: req.params.ipAddress })
    .lean()
    .exec(function (err, docs) {
      console.log(err)
      if (err || !docs.length) {
        return res
          .status(400)
          .send(
            "Could not find any payloads matching with the given IP Address"
          )
      }
      return res.status(200).json(docs)
    })
})

module.exports = router
