const express = require('express')
const { connectDB } = require("./database")
const app = express()
const port = 3000

require("dotenv").config()

app.get('/', (req, res) => {
  res.send('Hello World!')
})

connectDB()

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})