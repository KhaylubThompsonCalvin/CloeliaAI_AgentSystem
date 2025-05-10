/**
 * =============================================================================
 * File: gpt_utils.mjs
 * Project: CloeliaAI_AgentSystem – Node Client Module
 * Author: Khaylub Thompson-Calvin
 * Date: 2025-05-10
 *
 * Description:
 *   Reusable `generateReply()` that:
 *    • Loads exactly the root .env (no surprises)
 *    • Calls OpenAI GPT-4o-mini
 *    • Auto-creates logs/ and appends to gpt_test_log.json
 *
 * Dependencies:
 *   npm install openai dotenv
 * =============================================================================
 */

import OpenAI from "openai";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";

// ─── Resolve __dirname & load the root .env ──────────────────────────────────
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// assume your project structure:
//   /CloeliaAI_AgentSystem/
//     ├ node_clients/gpt_utils.mjs   <-- here
//     └ .env                         <-- there
const envPath = path.resolve(__dirname, "../.env");
console.log(`📄 Loading .env from: ${envPath}`);
dotenv.config({ path: envPath });

// confirm which key we actually loaded
console.log("🔑 OPENAI_KEY =", process.env.OPENAI_KEY && process.env.OPENAI_KEY.slice(0,10) + "…");

// ─── initialize OpenAI client ────────────────────────────────────────────────
if (!process.env.OPENAI_KEY) {
  console.error("❌ No OPENAI_KEY in env—cannot continue.");
  process.exit(1);
}
const openai = new OpenAI({ apiKey: process.env.OPENAI_KEY });

// ─── generateReply() ─────────────────────────────────────────────────────────
/**
 * Sends `userMessage` to GPT-4o-mini, returns the assistant message,
 * and (optionally) logs to logs/gpt_test_log.json.
 *
 * @param {string} userMessage
 * @param {boolean} [logResult=true]
 * @returns {Promise<{ role: string, content: string }|null>}
 */
export async function generateReply(userMessage, logResult = true) {
  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      store: true,
      messages: [{ role: "user", content: userMessage }],
    });

    const message = completion.choices[0].message;
    if (logResult) {
      // ensure logs/ exists
      const logDir = path.resolve(__dirname, "../logs");
      if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });

      const logFile = path.join(logDir, "gpt_test_log.json");
      let all = [];
      if (fs.existsSync(logFile)) {
        try { all = JSON.parse(fs.readFileSync(logFile, "utf-8")); }
        catch { all = []; }
      }
      all.push({
        timestamp: new Date().toISOString(),
        input: userMessage,
        output: message.content,
      });
      fs.writeFileSync(logFile, JSON.stringify(all, null, 2), "utf-8");
    }

    return message;
  } catch (err) {
    console.error("❌ OpenAI API Error:", err.message || err);
    return null;
  }
}





