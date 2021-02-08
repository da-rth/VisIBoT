const express = require("express")
const bodyParser = require("body-parser")
const cors = require("cors")
const { connectDB } = require("./database")
const app = express()

require("dotenv").config({ path: "backend/.env" })
const staticServe = express.static(`${__dirname}/dist`)
const frontendBaseUrl = process.env.FRONTEND_BASE_URL || "http://localhost:3000"
const port = 8080

connectDB()

require("./models/CandidateC2Server")
require("./models/BadpacketsResult")
require("./models/MalwarePayload")
require("./models/LisaAnalysis")
require("./models/AutonomousSystem")
require("./models/IpGeoConnection")
require("./models/IpGeoData")
require("./models/IpInfo")

if (process.env.NODE_ENV === "development") {
  console.log("Developer Mode")
  app.use(require("morgan")("dev"))
}

app.use(
  cors({
    origin: frontendBaseUrl,
  })
)
app.use(require("./routes"))
app.use("/", staticServe)
app.use("*", staticServe)
app.use(bodyParser.json())

app.listen(port, () => {
  console.log(`VisIBoT Backend listening at port: ${port}`)
})
