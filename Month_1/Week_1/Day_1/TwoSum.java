package Month_1.Week_1.Day_1;

import java.util.HashMap;
import java.util.Map;

public class TwoSum {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int comeplement = target - nums[i];
            if (map.containsKey(comeplement)) {
                return new int[] { map.get(comeplement), i };
            }
            map.put(nums[i], i);
        }
        return new int[] {};
    }
}
