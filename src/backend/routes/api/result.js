"use strict"
const express = require("express")
const Result = require("../../models/Result")

let router = express.Router()

router.route("/:eventid").get(async (req, res) => {
  Result.findOne({ _id: req.params.eventid })
    .populate({
      path: "source_ip_address scanned_payloads",
      populate: {
        path: "ip_address",
      },
    })
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
