import { parseLogFile } from "./parser";
import { generateStats } from "./stats";

async function main() {
    const filepath = process.argv[2];
    if (!filepath) {
        console.log("Usage:npm start <log-files>");
        process.exit(1);
    }

    try {
        const statusCodes = await parseLogFile(filepath);

        const stats = generateStats(statusCodes);
        console.log("\n=== Category Summary ===");

        for (const [category, count] of Object.entries(stats.categoryCounts)) {
            console.log(`${category}: ${count}`);
        }

        console.log("\n=== Status Code Counts ===");

        for (const [code, count] of Object.entries(stats.codeCounts)) {
            console.log(`${code}: ${count}`);
        }


    }
    catch (error) {
        console.error("Error parsing log file:", error);

    }
}

main();