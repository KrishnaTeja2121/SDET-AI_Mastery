function isAnagram(s: string, t: string): boolean {
    if (s.length !== t.length) {
        return false;
    }

    const count: number[] = new Array(26).fill(0);
    for (let i = 0; i < s.length; i++) {
        count[s.charCodeAt(i) - 'a'.charCodeAt(0)]++;
        count[t.charCodeAt(i) - 'a'.charCodeAt(0)]--;
    }
    return count.every(freq => freq === 0);

}

/*
Interview Explanation

“Since anagrams must contain the same characters the same number of times,
I count character frequencies from one string and subtract frequencies from the other.
If all counts end at zero, the strings are anagrams.”
* */