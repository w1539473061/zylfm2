#!/usr/bin/env node
// Direct local archive access through a compatible pakEngineWorker.js.
const fs = require("node:fs");
const path = require("node:path");
const { Worker } = require("node:worker_threads");

function parseArgs(args) {
  const [command, ...rest] = args;
  const options = {};
  for (const value of rest) {
    if (!value.startsWith("--") || !value.includes("=")) {
      throw new Error(`无效参数: ${value}`);
    }
    const separator = value.indexOf("=");
    options[value.slice(2, separator)] = value.slice(separator + 1);
  }
  if (!["info", "list", "export"].includes(command) || !options.file || !options.worker) {
    throw new Error(
      "用法: material_preview.js info|list|export --worker=pakEngineWorker.js --file=资源路径 " +
      "[--password-file=Pak.txt] [--password=密码] [--index=图片序号 --out=输出.png]",
    );
  }
  return { command, options };
}

function passwordFromFile(file, archive) {
  if (!file) return "";
  const text = new TextDecoder("gb18030").decode(fs.readFileSync(file));
  const archiveName = path.basename(archive).toLowerCase();
  const archivePath = path.resolve(archive).replaceAll("\\", "/").toLowerCase();
  let matched = "";
  let longest = -1;
  for (const line of text.split(/\r?\n/)) {
    const entry = line.trim();
    if (!entry || entry.startsWith(";") || entry.startsWith("#")) continue;
    const separator = entry.indexOf("|");
    if (separator < 0) continue;
    const name = entry.slice(0, separator).trim().replaceAll("\\", "/").toLowerCase();
    const exact = name === archivePath;
    if (exact || (path.posix.basename(name) === archiveName && longest < 0)) {
      matched = entry.slice(separator + 1).trim();
      longest = exact ? name.length : 0;
    }
  }
  return matched;
}

async function main() {
  const { command, options } = parseArgs(process.argv.slice(2));
  const file = path.resolve(options.file);
  const workerPath = path.resolve(options.worker);
  if (!fs.statSync(file).isFile() || !fs.statSync(workerPath).isFile()) {
    throw new Error("资源文件或解析器不存在");
  }
  const password = options.password ?? passwordFromFile(options["password-file"], file);
  const worker = new Worker(workerPath);
  const pending = new Map();
  let nextId = 0;
  worker.on("message", (message) => {
    const item = pending.get(String(message.id));
    if (!item) return;
    pending.delete(String(message.id));
    if (message.error) item.reject(new Error(String(message.error)));
    else item.resolve(message.result);
  });
  worker.on("error", (error) => {
    for (const item of pending.values()) item.reject(error);
    pending.clear();
  });
  worker.on("exit", (code) => {
    for (const item of pending.values()) item.reject(new Error(`解析器退出: ${code}`));
    pending.clear();
  });
  const request = (method, params = {}) => new Promise((resolve, reject) => {
    const id = String(++nextId);
    pending.set(id, { resolve, reject });
    worker.postMessage({ id, method, params });
  });

  let archive;
  try {
    await request("engine.initialize");
    archive = await request("archive.open", { path: file, password });
    if (command === "info") {
      const { archiveId, ...publicInfo } = archive;
      console.log(JSON.stringify({ file, ...publicInfo }, null, 2));
    } else if (command === "list") {
      const offset = Number(options.offset ?? 0);
      const limit = Number(options.limit ?? 100);
      if (!Number.isSafeInteger(offset) || offset < 0 ||
          !Number.isSafeInteger(limit) || limit < 1 || limit > 1000) {
        throw new Error("offset 必须为非负整数，limit 必须为 1-1000");
      }
      const entries = await request("archive.list", {
        archiveId: archive.archiveId, offset, limit, kind: "image",
      });
      console.log(JSON.stringify(entries, null, 2));
    } else {
      const index = Number(options.index);
      if (!Number.isSafeInteger(index) || index < 0 || !options.out) {
        throw new Error("export 需要非负整数 --index 和 --out");
      }
      const result = await request("entry.renderImagesEncoded", {
        archiveId: archive.archiveId, logicalIndices: [index],
      });
      const image = result.images?.[0];
      if (!image?.bytes) throw new Error(`图片不存在或无法解析: ${index}`);
      const output = path.resolve(options.out);
      fs.mkdirSync(path.dirname(output), { recursive: true });
      fs.writeFileSync(output, Buffer.from(image.bytes));
      console.log(JSON.stringify({
        file, output, logicalIndex: image.logicalIndex,
        width: image.width, height: image.height,
      }, null, 2));
    }
  } finally {
    if (archive) await request("archive.close", { archiveId: archive.archiveId }).catch(() => {});
    await request("engine.shutdown").catch(() => {});
    await worker.terminate();
  }
}

main().catch((error) => {
  console.error(error.message || String(error));
  process.exitCode = 1;
});
