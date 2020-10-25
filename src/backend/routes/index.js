const express = require('express')
const path = require("path")

let router = express.Router()

router.use("/", express.static(path.join(__dirname, "../dist")))
router.use("/api", require("./api"))

module.exports = router