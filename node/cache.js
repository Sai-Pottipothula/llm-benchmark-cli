import sqlite3 from "sqlite3";
import crypto from "crypto";

const db = new sqlite3.Database("cache.db");

db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS responses (
      key TEXT PRIMARY KEY,
      provider TEXT,
      prompt TEXT,
      system TEXT,
      response TEXT
    )
  `);
});

function makeKey(provider, prompt, system) {
  return crypto
    .createHash("sha256")
    .update(`${provider}:${prompt}:${system}`)
    .digest("hex");
}

export function getCachedResponse(provider, prompt, system) {
  return new Promise((resolve, reject) => {

    const key = makeKey(provider, prompt, system);

    db.get(
      "SELECT response FROM responses WHERE key = ?",
      [key],
      (err, row) => {

        if (err) {
          reject(err);
        } else if (row) {
          resolve(JSON.parse(row.response));
        } else {
          resolve(null);
        }
      }
    );
  });
}

export function saveCachedResponse(
  provider,
  prompt,
  system,
  response
) {
  return new Promise((resolve, reject) => {

    const key = makeKey(provider, prompt, system);

    db.run(
      `
      INSERT OR REPLACE INTO responses
      VALUES (?, ?, ?, ?, ?)
      `,
      [
        key,
        provider,
        prompt,
        system,
        JSON.stringify(response)
      ],
      (err) => {

        if (err) {
          reject(err);
        } else {
          resolve();
        }
      }
    );
  });
}