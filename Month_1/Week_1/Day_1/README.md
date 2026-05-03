# Day 1: Two Sum

This folder contains implementations of the classic **Two Sum** problem in three different languages.

## Problem Statement
Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.
You may assume that each input would have exactly one solution, and you may not use the same element twice.

## Approach
All implementations use an optimized **One-Pass Hash Map** approach:
- We iterate through the array once.
- For each element, we calculate its `complement` (i.e., `target - current_element`).
- We check if the `complement` already exists in our Hash Map.
  - If it does, we have found our two numbers and return their indices.
  - If it doesn't, we add the current element and its index to the Hash Map and continue.
- **Time Complexity:** $O(n)$ - Since we traverse the list containing $n$ elements exactly once, and hash map lookups take $O(1)$ time on average.
- **Space Complexity:** $O(n)$ - The extra space required depends on the number of items stored in the hash map, which stores at most $n$ elements.

## Files
1. **`TwoSum.java`**: Java implementation using `java.util.HashMap`.
2. **`TwoSum.ts`**: TypeScript implementation using `Map<number, number>`. (Includes an `export {}` statement to ensure it is treated as an isolated module, avoiding global scope conflicts).
3. **`TwoSum.js`**: JavaScript implementation (likely the compiled output or a parallel implementation) using the standard JS `Map` object.
