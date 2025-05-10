/**
 * =============================================================================
 * File: gpt_test.mjs
 * Project: CloeliaAI_AgentSystem – Node Client
 * Author: Khaylub Thompson-Calvin
 * Date: 2025-05-08
 *
 * Description:
 * A test script for verifying OpenAI API connectivity using the GPT-4o-mini model.
 * This script loads an API key from the .env file, sends a message to OpenAI,
 * and prints the assistant's response to the console.
 *
 * Requirements:
 * - Node.js v18+ (for ES module & async support)
 * - openai and dotenv packages (`npm install openai dotenv`)
 * - .env file with OPENAI_KEY defined
 *
 * Usage:
 * Run using: `node gpt_test.mjs`
 * =============================================================================
 */

import OpenAI from "openai";
import dotenv from "dotenv";

// Load .env from parent directory if run from node_clients/
dotenv.config({ path: "../.env" });

// Check API key presence
if (!process.env.OPENAI_KEY) {
  console.error("❌ OPENAI_KEY not found in .env");
  process.exit(1);
}

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_KEY,
});

try {
  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    store: true,
    messages: [{ role: "user", content: "Write a haiku about AI" }],
  });

  console.log("✅ GPT Response:", completion.choices[0].message);
} catch (error) {
  console.error("❌ OpenAI API Error:", error);
}


