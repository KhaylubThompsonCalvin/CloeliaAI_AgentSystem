// =============================================================================
// File: node_clients/gpt_bridge.mjs
// Project: CloeliaAI_AgentSystem
// Author: Khaylub Thompson-Calvin
// Date: 2025-05-10
//
// Purpose:
//   Node.js GPT Bridge to OpenAI API with Logging.
//     1. Loads environment variables securely.
//     2. Sends a user prompt to OpenAI API.
//     3. Returns strict JSON response with "content" field.
//     4. Saves input/output to daily logs (logs/gpt_bridge_log_YYYY-MM-DD.json).
//     5. Handles errors gracefully and ensures valid JSON output.
//
// Dependencies:
//   - openai (npm install openai dotenv)
//   - fs, path (built-in Node.js modules)
// =============================================================================

import 'dotenv/config';
import { OpenAI } from 'openai';
import fs from 'fs';
import path from 'path';

// ✅ Load API Key from .env
const apiKey = process.env.OPENAI_KEY;

if (!apiKey) {
    console.error('❌ Missing OPENAI_KEY in .env');
    outputError("Missing API Key");
}

const openai = new OpenAI({ apiKey });

// ✅ Extract User Input from Command Line
const userInput = process.argv.slice(2).join(' ').trim();

if (!userInput) {
    console.error('❌ No input message provided.');
    outputError("Empty user input.");
}

// 📄 Logging Directory and Daily Log File
const logDir = path.resolve("./logs");
const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
const logFile = path.join(logDir, `gpt_bridge_log_${today}.json`);

// Ensure logs directory exists
if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir);
}

/**
 * Generates a reply using OpenAI's GPT API.
 * Handles API errors gracefully and returns strict JSON output.
 */
async function generateReply() {
    try {
        const chatResponse = await openai.chat.completions.create({
            model: "gpt-4o", // Update if using a different model
            messages: [{ role: "user", content: userInput }],
            max_tokens: 300,
            temperature: 0.7,
        });

        const gptContent = chatResponse.choices[0]?.message?.content?.trim() || "";

        const responsePayload = {
            role: "assistant",
            content: gptContent,
            refusal: gptContent ? null : "Empty response.",
            annotations: []
        };

        // ✅ Output as strict JSON for Python API to parse
        console.log(JSON.stringify(responsePayload));
        saveLog(userInput, responsePayload);

    } catch (error) {
        const message = error?.message || "Unknown API Error.";
        console.error('❌ OpenAI API Error:', message);
        outputError(message);
    }
}

/**
 * Outputs a standardized error response and exits the process.
 *
 * @param {string} message - Error message to log and return.
 */
function outputError(message) {
    const errorPayload = {
        role: "assistant",
        content: "",
        refusal: "API_ERROR",
        annotations: [{ error: message }]
    };

    console.log(JSON.stringify(errorPayload));
    saveLog(userInput || "N/A", errorPayload);
    process.exit(1);
}

/**
 * Saves a structured log of user inputs and GPT outputs.
 *
 * @param {string} input - User's input message.
 * @param {object} output - GPT or error response payload.
 */
function saveLog(input, output) {
    const logEntry = {
        timestamp: new Date().toISOString(),
        input,
        output
    };

    let logs = [];
    if (fs.existsSync(logFile)) {
        try {
            logs = JSON.parse(fs.readFileSync(logFile, "utf-8"));
            if (!Array.isArray(logs)) logs = [];
        } catch (e) {
            console.warn('⚠️ Failed to parse existing log. Starting fresh.');
        }
    }

    logs.push(logEntry);
    fs.writeFileSync(logFile, JSON.stringify(logs, null, 2), "utf-8");
}

generateReply();