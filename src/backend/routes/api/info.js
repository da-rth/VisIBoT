"use strict"
const express = require("express")
const Result = require("../../models/Result")
const Payload = require("../../models/Payload")

let router = express.Router()

router.route("/result/:ipAddress").get(async (req, res) => {
  Result.find({ source_ip_address: req.params.ipAddress })
    .populate("scanned_payloads")
    .lean()
    .exec(function (err, obj) {
      console.log(err)
      if (err || !obj) {
        return res
          .status(400)
          .send("Could not find result matching with event_id")
      }
      return res.status(200).json(obj)
    })
})

router.route("/payload/:ipAddress").get(async (req, res) => {
  Payload.findOne({ ip_address: req.params.ipAddress })
    .lean()
    .exec(function (err, obj) {
      console.log(err)
      if (err || !obj) {
        return res
          .status(400)
          .send("Could not find result matching with event_id")
      }
      return res.status(200).json(obj)
    })
})

module.exports = router
