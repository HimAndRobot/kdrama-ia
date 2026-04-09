// MDL scraper - collects drama details, reviews, and first-degree recommendations
import { chromium } from "playwright";
import { writeFileSync, readFileSync, mkdirSync, existsSync } from "fs";

const DATA_DIR = "./data";
const DB_FILE = `${DATA_DIR}/db.json`;
const DELAY = 500;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadDb() {
  if (existsSync(DB_FILE)) {
    const data = JSON.parse(readFileSync(DB_FILE, "utf-8"));
    if (Array.isArray(data)) return data;
    return [];
  }
  return [];
}

function saveToDb(drama, db) {
  const existing = db.findIndex((d) => d.url === drama.url);
  if (existing >= 0) {
    db[existing] = drama;
  } else {
    db.push(drama);
  }
  writeFileSync(DB_FILE, JSON.stringify(db, null, 2), "utf-8");
}

async function extractDetails(page) {
  return page.evaluate(() => {
    const txt = (s) => document.querySelector(s)?.textContent?.trim() || "";
    const all = (s) => [...document.querySelectorAll(s)].map((e) => e.textContent.trim());

    const title = txt("h1");
    const subtitle = document.querySelector("h1")?.nextElementSibling?.textContent?.trim() || "";
    const synopsis = txt(".show-synopsis span") || txt(".show-synopsis");
    const rating = txt("[itemprop='ratingValue']") || txt(".hfs-top .score") || "";

    const genres = all("a[href*='&ge=']");
    const tags = all("a[href*='&th=']").filter((t) => t !== "(Vote tags)");

    const details = {};
    document.querySelectorAll(".show-detailsxss li").forEach((li) => {
      const label = li.querySelector("b")?.textContent?.replace(":", "").trim();
      if (label) {
        const links = [...li.querySelectorAll("a")].map((a) => a.textContent.trim());
        details[label] = links.length > 0 ? links : li.textContent.replace(label + ":", "").trim();
      }
    });

    const cast = [...document.querySelectorAll("a[href*='/people/']")]
      .map((a) => a.textContent.trim())
      .filter((t) => t.length > 1)
      .slice(0, 10);

    return { title, subtitle, synopsis, rating, genres, tags, cast, details, url: window.location.href };
  });
}

async function extractReviews(page, url) {
  console.log(`    Reviews...`);
  await page.goto(url + "/reviews", { waitUntil: "domcontentloaded", timeout: 60000 });
  await sleep(300);

  return page.evaluate(() => {
    return [...document.querySelectorAll(".review")].slice(0, 10).map((el) => {
      const author = el.querySelector("a[href*='/profile/']")?.textContent?.trim() || "";
      const overall = el.querySelector(".score")?.textContent?.trim() || "";
      const body = el.querySelector(".review-body")?.textContent?.trim()?.slice(0, 3000) || "";
      return { author, overall, content: body };
    }).filter((r) => r.content.length > 50);
  });
}

async function extractRecommendations(page, url) {
  console.log(`    Recommendations...`);
  await page.goto(url + "/recs", { waitUntil: "domcontentloaded", timeout: 60000 });
  await sleep(300);

  return page.evaluate(() => {
    const recs = [];
    const seen = new Set();
    document.querySelectorAll("a").forEach((a) => {
      const t = a.textContent.trim();
      const h = a.href;
      if (t.match(/\(\d{4}\)/) && h.match(/mydramalist\.com\/\d+/) && !seen.has(h)) {
        seen.add(h);
        recs.push({ title: t, url: h });
      }
    });
    return recs;
  });
}

async function scrapeDrama(page, url, withRecs = false) {
  const cleanUrl = url.split("?")[0].split("#")[0];
  console.log(`\n  [Drama] ${cleanUrl}`);

  console.log(`    Details...`);
  await page.goto(cleanUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
  await sleep(300);
  const details = await extractDetails(page);

  await sleep(DELAY);
  const reviews = await extractReviews(page, cleanUrl);

  let recommendations = [];
  if (withRecs) {
    await sleep(DELAY);
    recommendations = await extractRecommendations(page, cleanUrl);
  }

  return { ...details, reviews, recommendations };
}

const PARALLEL = 3;

function collectRecs(drama, scraped, db) {
  const urls = [];
  for (const rec of drama.recommendations || []) {
    const u = rec.url.split("?")[0].split("#")[0];
    if (!scraped.has(u) && !db.some((d) => d.url === u)) urls.push(rec.url);
  }
  return urls;
}

async function scrapeRecursive(ctx, urls, depth, maxDepth, db, scraped) {
  if (depth > maxDepth || urls.length === 0) return;

  const indent = "  ".repeat(depth);
  const toScrape = [];
  const nextUrls = [];

  for (const url of urls) {
    const cleanUrl = url.split("?")[0].split("#")[0];
    if (scraped.has(cleanUrl)) continue;
    scraped.add(cleanUrl);

    const fetchRecs = depth < maxDepth;
    const existing = db.find((d) => d.url === cleanUrl);

    if (existing) {
      if (fetchRecs && existing.recommendations?.length) {
        console.log(`${indent}  ~ ${existing.title} (db, following ${existing.recommendations.length} recs)`);
        nextUrls.push(...collectRecs(existing, scraped, db));
      }
      continue;
    }

    toScrape.push({ url: cleanUrl, fetchRecs });
  }

  if (toScrape.length > 0) {
    console.log(`\n${indent}=== Depth ${depth}/${maxDepth} — scraping ${toScrape.length} new dramas (${PARALLEL} parallel) ===`);

    for (let i = 0; i < toScrape.length; i += PARALLEL) {
      const batch = toScrape.slice(i, i + PARALLEL);
      const results = await Promise.allSettled(
        batch.map(async ({ url, fetchRecs }) => {
          const page = await ctx.newPage();
          try {
            const drama = await scrapeDrama(page, url, fetchRecs);
            return { drama, fetchRecs };
          } finally {
            await page.close();
          }
        })
      );

      for (const result of results) {
        if (result.status === "fulfilled") {
          const { drama, fetchRecs } = result.value;
          saveToDb(drama, db);
          const rc = drama.recommendations?.length || 0;
          console.log(`${indent}  + ${drama.title} | ${drama.reviews.length} rev${fetchRecs ? ` | ${rc} recs` : ""} [db: ${db.length}]`);
          if (fetchRecs) nextUrls.push(...collectRecs(drama, scraped, db));
        } else {
          console.error(`${indent}  ✗ ${result.reason?.message || "unknown error"}`);
        }
      }
    }
  }

  if (nextUrls.length > 0) {
    await scrapeRecursive(ctx, nextUrls, depth + 1, maxDepth, db, scraped);
  }
}

async function main() {
  const startUrl = process.argv[2];
  const maxDepth = parseInt(process.argv[3] || "1", 10);

  if (!startUrl || !startUrl.includes("mydramalist.com")) {
    console.error("Usage: node scrape.mjs <mydramalist-url> [depth]");
    console.error("  depth: recommendation depth (default 1, 0 = root only)");
    process.exit(1);
  }

  if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });

  const db = loadDb();
  const scraped = new Set();

  console.log(`Launching browser... (max depth: ${maxDepth}, db has ${db.length} dramas, ${PARALLEL}x parallel)`);
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
  });

  await scrapeRecursive(ctx, [startUrl], 0, maxDepth, db, scraped);

  await browser.close();
  console.log(`\n=== Done! ${db.length} dramas total in ${DB_FILE} ===`);
}

main().catch(console.error);
