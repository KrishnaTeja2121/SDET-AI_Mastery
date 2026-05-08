export function categorizeStatus(code: number): string {
    if (code >= 100 && code < 200) return "1xx- Informational";
    if (code >= 200 && code < 300) return "2xx- Success";
    if (code >= 300 && code < 400) return "3xx- Redirection";
    if (code >= 400 && code < 500) return "4xx- Client Error";
    if (code >= 500 && code < 600) return "5xx- Server Error";
    return "Unknown";
}