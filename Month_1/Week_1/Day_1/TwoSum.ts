function twoSum(nums: number[], target: number): number[] {
    const map = new Map<number, number>();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (map.has(complement)) {
            return [map.get(complement)!, i]
        }
        map.set(nums[i], i);
    }
    return [];
}

//Why the ! after map.get(complement)?

/*
TypeScript treats Map.get() as possibly returning undefined.
Since we already checked map.has(complement), the ! tells TypeScript:
“Trust me — this value exists.”
*/

export {};