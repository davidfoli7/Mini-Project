const express = require("express");
const cors = require("cors");
const path = require("path");
const multer = require("multer");
const upload = multer({ dest: 'uploads/' });

const app = express();
app.use(cors());
app.use(express.json());

// Serve static files
app.use("/static", express.static(path.join(__dirname, "static")));
app.use("/uploads", express.static(path.join(__dirname, "uploads")));

// Serve index.html
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "templates", "index.html"));
});

// API routes to Flask backend
app.post("/api/ask", async (req, res) => {
    try {
        const { prompt, mode, num_cards, num_questions } = req.body;
        const response = await fetch("http://127.0.0.1:3002/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt, mode, num_cards, num_questions }),
        });
        const data = await response.json();
        res.json({ answer: data.answer || "No response from AI." });
    } catch (error) {
        res.status(500).json({ error: "Error processing request" });
    }
});

// Speech to Text endpoint
app.post("/api/speech-to-text", upload.single('audio'), async (req, res) => {
    try {
        const formData = new FormData();
        formData.append('audio', req.file);
        
        const response = await fetch("http://127.0.0.1:3002/speech-to-text", {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: "Error processing speech to text" });
    }
});

// Text to Speech endpoint
app.post("/api/text-to-speech", async (req, res) => {
    try {
        const { text } = req.body;
        const response = await fetch("http://127.0.0.1:3002/text-to-speech", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: "Error processing text to speech" });
    }
});

// Start the server
const PORT = 3001;
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
});
