const axios = require("axios");

exports.askAI = async (req, res) => {
    const { prompt } = req.body;

    try {
        const response = await axios.post("http://127.0.0.1:5500/ask", { prompt });
        res.json({ answer: response.data.answer });
    } catch (error) {
        res.status(500).json({ error: "Error fetching AI response" });
    }
};
