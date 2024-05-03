const express = require("express");
const { Client } = require("pg");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Configure connection to the database
const client = new Client({
  connectionString:
    "postgres://ticker_order_user:DX6mgTvJCqqtSfrqFz7tHBNls1RgHMwy@dpg-con0p7q1hbls73fak2r0-a.singapore-postgres.render.com/ticker_order",
  ssl: {
    rejectUnauthorized: false,
  },
});

// Connect to the database when the server starts
client
  .connect()
  .then(() => {
    console.log("Connected to the database");
  })
  .catch((err) => {
    console.error("Error connecting to the database:", err);
  });

// Get airplane ticket data
app.get("/flight", async (req, res) => {
  try {
    const query = "SELECT * FROM flight_tickets";
    const result = await client.query(query);

    res.status(200).json({
      success: true,
      message: "Flight ticket data retrieved successfully",
      data: result.rows,
    });
  } catch (error) {
    console.error("Failed to retrieve flight ticket data:", error);
    res.status(500).json({
      success: false,
      message: "Failed to retrieve flight ticket data",
    });
  }
});

// Get train ticket data
app.get("/train", async (req, res) => {
  try {
    const query = "SELECT * FROM train_tickets";
    const result = await client.query(query);

    res.status(200).json({
      success: true,
      message: "Train ticket data retrieved successfully",
      data: result.rows,
    });
  } catch (error) {
    console.error("Failed to retrieve train ticket data:", error);
    res.status(500).json({
      success: false,
      message: "Failed to retrieve train ticket data",
    });
  }
});

// Get hotel information
app.get("/hotel", async (req, res) => {
  try {
    const query = "SELECT * FROM hotels";
    const result = await client.query(query);

    res.status(200).json({
      success: true,
      message: "Hotel data retrieved successfully",
      data: result.rows,
    });
  } catch (error) {
    console.error("Failed to retrieve hotel data:", error);
    res.status(500).json({
      success: false,
      message: "Failed to retrieve hotel data",
    });
  }
});

// Get attractions information
app.get("/attractions", async (req, res) => {
  try {
    const query = "SELECT * FROM tourist_attractions";
    const result = await client.query(query);

    res.status(200).json({
      success: true,
      message: "Attractions data retrieved successfully",
      data: result.rows,
    });
  } catch (error) {
    console.error("Failed to retrieve attractions data:", error);
    res.status(500).json({
      success: false,
      message: "Failed to retrieve attractions data",
    });
  }
});

// Endpoint to create an order
app.post("/order", async (req, res) => {
  try {
    // Determine the order type from the request body
    const { order_type, customer_name, email, phone_number } = req.body;

    // Insert the order into the orders table
    const queryInsert =
      "INSERT INTO orders (customer_name, email, phone_number, order_type, order_date) VALUES ($1, $2, $3, $4, $5)";
    const values = [customer_name, email, phone_number, order_type, new Date()];
    await client.query(queryInsert, values);

    res.status(200).json({
      success: true,
      message: "Order created successfully",
    });
  } catch (error) {
    console.error("Failed to create order:", error);
    res.status(500).json({
      success: false,
      message: "Failed to create order",
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log("Server is running on port ${PORT}");
});
