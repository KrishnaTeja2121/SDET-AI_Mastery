import { categorizeStatus } from "./categorizer";

export function generateStats(statusCodes: number[]) {
    const categoryCounts: Record<string, number> = {};
    const codeCounts: Record<number, number> = {};

    for (const code of statusCodes) {
        const category = categorizeStatus(code);
        categoryCounts[category] = (categoryCounts[category] || 0) + 1;
        codeCounts[code] = (codeCounts[code] || 0) + 1;

    }

    return {
        categoryCounts,
        codeCounts,

    };
}