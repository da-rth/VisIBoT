const express = require('express')
const bodyParser = require("body-parser")
const cors = require("cors")
const { connectDB } = require("./database")
const app = express()
const port = 8080

require("dotenv").config()

if (process.env.NODE_ENV === "development") {
  console.log("Developer Mode")
  app.use(require("morgan")("dev"))
}

app.use(cors())
app.use(require("./routes"))
app.use(bodyParser.json())

connectDB()

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})