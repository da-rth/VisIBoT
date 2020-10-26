const express = require("express")

let router = express.Router()

router.use("/geolocations", require("./geolocations"))
router.use("/result", require("./result"))

module.exports = router
