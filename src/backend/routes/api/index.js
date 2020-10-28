const express = require("express")

let router = express.Router()

router.use("/geolocations", require("./geolocations"))
router.use("/info", require("./info"))

module.exports = router
