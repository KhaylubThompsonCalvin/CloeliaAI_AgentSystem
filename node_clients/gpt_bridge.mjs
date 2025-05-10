// =============================================================================
// File: node_clients/gpt_bridge.mjs
// Project: CloeliaAI_AgentSystem
// Author: Khaylub Thompson-Calvin
// Date: 2025-05-10
//
// Purpose:
//   Node.js GPT Bridge to OpenAI API with Database Knowledge Injection.
//     1. Loads environment variables securely.
//     2. Fetches symbolic facts from PostgreSQL.
//     3. Enriches GPT prompt with database knowledge.
//     4. Sends the enriched prompt to OpenAI API.
//     5. Returns strict JSON response with "content" field.
//     6. Saves input/output logs (logs/gpt_bridge_log_YYYY-MM-DD.json).
//     7. Handles errors gracefully and ensures valid JSON output.
//
// Dependencies:
//   - openai (npm install openai dotenv)
//   - pg (npm install pg)
//   - fs, path (built-in Node.js modules)
// =============================================================================

import 'dotenv/config';
import { OpenAI } from 'openai';
import fs from 'fs';
import path from 'path';
import pkg from 'pg';

const { Client } = pkg;

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
const today = new Date().toISOString().split('T')[0];
const logFile = path.join(logDir, `gpt_bridge_log_${today}.json`);

if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir);
}

/**
 * Fetches a symbolic fact from the PostgreSQL knowledge base.
 *
 * @returns {Promise<string>} A fact string to inject into the GPT prompt.
 */
async function fetchDatabaseFact() {
    const client = new Client({
        user: process.env.DB_USER,
        host: process.env.DB_HOST,
        database: process.env.DB_NAME,
        password: process.env.DB_PASSWORD,
        port: process.env.DB_PORT
    });

    try {
        await client.connect();
        const res = await client.query('SELECT key_fact FROM knowledge_base LIMIT 1;');
        await client.end();
        return res.rows[0]?.key_fact || "";
    } catch (err) {
        console.warn('⚠️ Database query failed:', err.message);
        return "";
    }
}

/**
 * Generates a reply using OpenAI's GPT API with enriched knowledge from the database.
 * Handles API errors gracefully and returns strict JSON output.
 */
async function generateReply() {
    try {
        const dbFact = await fetchDatabaseFact();
        const enrichedInput = dbFact
            ? `${userInput}\n\n[Consider this fact: ${dbFact}]`
            : userInput;

        const chatResponse = await openai.chat.completions.create({
            model: "gpt-4o",
            messages: [{ role: "user", content: enrichedInput }],
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

        console.log(JSON.stringify(responsePayload));
        saveLog(enrichedInput, responsePayload);

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

// 🚀 Start the process
generateReply();
