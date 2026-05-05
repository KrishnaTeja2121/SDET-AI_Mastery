# Day 2: Arrays & Hashing

This folder contains implementations for two classic Array and Hashing problems: **Contains Duplicate** and **Valid Anagram**.

---

## 1. Contains Duplicate

**Problem Statement:** 
Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

**Approach:** 
We use a **Hash Set** to keep track of the elements we've seen so far.
- Iterate through each number in the array.
- If the number is already in the Hash Set, we have found a duplicate (return `true`).
- If it's not in the Set, add it and continue.
- If the loop finishes without finding duplicates, return `false`.

**Complexity:**
- **Time Complexity:** $O(n)$ - We traverse the array exactly once, and Hash Set insertions/lookups take $O(1)$ on average.
- **Space Complexity:** $O(n)$ - In the worst case (all elements are unique), we store all $n$ elements in the Set.

**Files:**
- `ContainsDuplicate.java`: Java implementation using `java.util.HashSet`.
- `containsDuplicate.Ts`: TypeScript implementation using `Set<number>`.

---

## 2. Valid Anagram

**Problem Statement:** 
Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise. (An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once).

**Approach:** 
Since the problem typically involves lowercase English letters, we can use a **Frequency Array** of size 26 instead of a Hash Map for better performance.
- Check if the lengths of `s` and `t` are the same. If they differ, they can't be anagrams.
- Create an integer array `count` of size 26.
- Iterate through the characters of both strings simultaneously:
  - For each character in `s`, increment its corresponding index in the `count` array.
  - For each character in `t`, decrement its corresponding index in the `count` array.
- Finally, check the `count` array. If all frequencies are exactly zero, the strings are anagrams.

**Complexity:**
- **Time Complexity:** $O(n)$ - Where $n$ is the length of the strings. We iterate over the strings and then do a fixed 26-element loop.
- **Space Complexity:** $O(1)$ - The size of the frequency array is fixed to 26 characters, which does not grow with the input size.

**Files:**
- `ValidAnagram.java`: Java implementation.
- `isAnagram.TS`: TypeScript implementation.
