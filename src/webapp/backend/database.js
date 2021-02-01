const mongoose = require("mongoose")

const Database = {
  connectDB: async () => {
    const uri = process.env.MONGO_URL

    try {
      await mongoose.connect(uri, {
        useCreateIndex: true,
        useNewUrlParser: true,
        useUnifiedTopology: true,
        useFindAndModify: false,
      })
      console.log("MongoDB: connected")
    } catch (e) {
      console.error("MongoDB: failed to connect...", e)
      process.exit(1)
    }
  },
}

module.exports = Database
