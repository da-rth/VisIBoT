"use strict"
const express = require("express")

let router = express.Router()

router
  .route("/")
  .get(async (req, res) => {
    console.log(req.session)
  })

module.exports = router