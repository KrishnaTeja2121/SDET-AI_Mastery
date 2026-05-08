import fs from "fs";
import readline from "readline";

export async function parseLogFile(filepath: string): Promise<number[]> {

    const statusCodes: number[] = [];
    const fileStream = fs.createReadStream(filepath);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    for await (const line of rl) {
        const match = line.match(/\s(\d{3})$/);
        if (match) {
            statusCodes.push(Number(match[1]))
        }
    }

    return statusCodes;

}       