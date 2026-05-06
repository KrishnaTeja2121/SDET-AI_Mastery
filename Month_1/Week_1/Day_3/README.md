# Day 3: Arrays & Hashing

This folder contains implementations for the **Replace Elements with Greatest Element on Right Side** problem.

---

## 1. Replace Elements with Greatest Element on Right Side

**Problem Statement:** 
Given an array `arr`, replace every element in that array with the greatest element among the elements to its right, and replace the last element with `-1`.

After doing so, return the array.

**Approach:** 
We can solve this efficiently by traversing the array backwards (from right to left). 
- We keep track of the maximum value we've seen so far to our right, calling it `maxRight`. 
- We initialize `maxRight` as `-1` (since the problem states the last element should be replaced by `-1`).
- For each element as we move leftwards:
  1. We store the current element's value temporarily in `current`.
  2. We replace the current element with the `maxRight` we've tracked.
  3. We update `maxRight` to be the maximum of `maxRight` and `current`.
- This way, we don't have to repeatedly scan the right side of the array for every element, saving a lot of time!

**Complexity:**
- **Time Complexity:** $O(n)$ - We traverse the array exactly once from right to left.
- **Space Complexity:** $O(1)$ - We only use a couple of variables to keep track of state, so the space required does not scale with the size of the array. We modify the array in-place.

**Files:**
- `ReplaceElements.java`: Java implementation.
- `replaceElements.TS`: TypeScript implementation.
