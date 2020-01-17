const { MongoClient } = require("mongodb");

const connectionURL = "mongodb://127.0.0.1:27017";
const databaseName = "emission-data";

MongoClient.connect(
  connectionURL,
  { useNewUrlParser: true, useUnifiedTopology: true },
  (error, client) => {
    if (error) {
      return console.log("Unable to connect to database");
    }
    console.log(`connected to database ${databaseName}`);
    const db = client.db(databaseName);

    // =================================Queries============================== //
    // Query:1 Getting total records count
    db.collection("emission")
      .find({})
      .count((error, data) => {
        if (error) {
          return console.log(error);
        }
        console.log("Total number of records in the database:");
        console.log(data);
      });

    // Query:2 Getting data for (Country -> Sri Lanka && Year -> 2000) records count
    db.collection("emission").findOne(
      {
        $and: [{ Year: "2000" }, { Country: "Sri Lanka" }]
      },
      (err, data) => {
        if (err) {
          return console.log(err);
        }
        console.log("Data for Sri Lanka in the year of 2000:");
        console.log(data);
      }
    );
    // Query:3 Getting countries for (Year -> 2017 && CO2 emissions (metric tons) is greater than -> 15(tons)) records count
    db.collection("emission")
      .find({
        $and: [{ Year: "2017" }, { "CO2 emissions (metric tons)": { $gt: 15 } }]
      })
      .forEach(data => {
        console.log(data["Country"]);
      });
  }
);
