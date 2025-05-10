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

import dotenv from 'dotenv';
import { OpenAI } from 'openai';
import fs from 'fs';
import path from 'path';
import pkg from 'pg';

const { Client } = pkg;

// ✅ Dynamically Resolve .env Location Regardless of Execution Context
const possibleEnvPaths = [
    path.resolve("../.env"),
    path.resolve("../../.env"),
    path.resolve("../../../.env"),
    path.resolve("./.env"),
];

let envLoaded = false;
for (const envPath of possibleEnvPaths) {
    if (fs.existsSync(envPath)) {
        dotenv.config({ path: envPath });
        envLoaded = true;
        break;
    }
}

if (!envLoaded) {
    console.warn("⚠️ .env file not found. Continuing with system environment variables.");
}

// ✅ Extract User Input Early to Avoid Reference Errors
const userInput = process.argv.slice(2).join(' ').trim();

if (!userInput) {
    console.error('❌ No input message provided.');
    outputError("Empty user input.");
}

// 📄 Setup Logging Paths
const logDir = path.resolve("./logs");
const today = new Date().toISOString().split('T')[0];
const logFile = path.join(logDir, `gpt_bridge_log_${today}.json`);

if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
}

// ✅ Validate Required Environment Variables Before Proceeding
const REQUIRED_ENV_VARS = ['OPENAI_KEY', 'DB_USER', 'DB_HOST', 'DB_NAME', 'DB_PASSWORD', 'DB_PORT'];
for (const key of REQUIRED_ENV_VARS) {
    if (!process.env[key]) {
        console.error(`❌ Missing environment variable: ${key}`);
        outputError(`Missing environment variable: ${key}`);
    }
}

const openai = new OpenAI({ apiKey: process.env.OPENAI_KEY });

/**
 * Fetches a symbolic fact from the PostgreSQL knowledge base.
 * @returns {Promise<string>} A fact string to inject into the GPT prompt.
 */
async function fetchDatabaseFact() {
    const client = new Client({
        user: process.env.DB_USER,
        host: process.env.DB_HOST,
        database: process.env.DB_NAME,
        password: process.env.DB_PASSWORD,
        port: parseInt(process.env.DB_PORT),
    });

    try {
        await client.connect();
        const res = await client.query('SELECT key_fact FROM knowledge_base ORDER BY RANDOM() LIMIT 1;');
        await client.end();
        return res.rows[0]?.key_fact || "";
    } catch (err) {
        console.warn('⚠️ Database query failed:', err.message);
        return "";
    }
}

/**
 * Generates a symbolic reply using OpenAI's API with optional DB fact injection.
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
 * Outputs a standardized error response and exits.
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
 * Saves structured logs of user inputs and API responses.
 * @param {string} input - The input message from the user.
 * @param {object} output - The final response or error payload.
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
        } catch {
            console.warn('⚠️ Failed to parse existing log. Starting fresh.');
        }
    }

    logs.push(logEntry);
    fs.writeFileSync(logFile, JSON.stringify(logs, null, 2), "utf-8");
}

// 🚀 Execute Main Logic
generateReply();


