function isPalindrome(s: string): boolean {
    let left = 0;
    let right = s.length - 1;
    while (left < right) {
        if (isAlphaNumeric(s[left])) {
            left++;
        } else if (isAlphaNumeric(s[right])) {
            right--;
        } else {
            if (s[left].toLowerCase() !== s[right].toLowerCase()) {
                return false;
            }
            left++;
            right--;
        }
    }
    return true;
}

function isAlphaNumeric(char: string): boolean {
    return /^[a-z0-9]+$/i.test(char);
}