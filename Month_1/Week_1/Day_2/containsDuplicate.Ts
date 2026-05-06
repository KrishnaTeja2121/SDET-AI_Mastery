function containsDuplicate(nums: number[]): boolean {
    const seen = new Set<number>();
    for (const num of nums) {
        if (seen.has(num)) {
            return true;
        }
        seen.add(num);
    }
    return false;
}

export { };


/**
 * Alternative One-Liner (TypeScript)
 * const containsDuplicate = (nums: number[]): boolean =>
    new Set(nums).size !== nums.length;
 */