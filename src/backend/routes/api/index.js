const express = require("express")

let router = express.Router()

router.use("/geolocations", require("./geolocations"))

module.exports = router
