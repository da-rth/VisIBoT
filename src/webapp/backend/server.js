const express = require("express")
const bodyParser = require("body-parser")
const cors = require("cors")
const { connectDB } = require("./database")
const app = express()
const port = 8080

require("dotenv").config()

connectDB()

require("./models/CandidateC2Server")
require("./models/BadpacketsResult")
require("./models/MalwarePayload")
require("./models/LisaAnalysis")
require("./models/AutonomousSystem")
require("./models/IpGeoConnection")
require("./models/IpGeoData")

if (process.env.NODE_ENV === "development") {
  console.log("Developer Mode")
  app.use(require("morgan")("dev"))
}

app.use(
  cors({
    origin: "http://localhost:3000",
  })
)
app.use(require("./routes"))
app.use(bodyParser.json())

app.listen(port, () => {
  console.log(`VisIBoT Backend listening at http://localhost:${port}`)
})
