"use strict"
const mongoose = require("mongoose")
const express = require("express")

let router = express.Router()
let connection = mongoose.connection

router
  .route("/")
  .get(async (req, res) => {
    let twentyFourHoursAgo = new Date()
    twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24)

    connection.db.collection("geo_data", function(err, collection){
        collection
        .find({"updated_at": {"$gte": twentyFourHoursAgo}})
        .toArray(function(err, data){
            res.json(data)
        })
    })
  })

module.exports = router