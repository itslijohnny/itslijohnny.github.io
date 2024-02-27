---
title: Solve the Problem in a April Fool's Joke
tags: 
    - Python
    - Coding Challenge
    - Fun
    - Algorithms

categories:
  - Blog
  - Coding Challenge
keywords: [Python,Algorithms,Coding Challenge]
date: 2019-04-06 14:35:05
image: 5cc38cc539c01.jpg
math: true
---

On April 1st, one of the post on [v2ex](https://www.v2ex.com/t/550870) (An online community of developers and designers in China[^1]) become viral. The [post](https://www.v2ex.com/t/550870) title is "Seeking Dates" and it is posted on April 1st, so most reactions of this post are pointing out that this is the "new trap" of the recruiters.
<!-- more -->
<img src="https://i.loli.net/2019/04/27/5cc38cc160d0f.jpg" alt="It's a trap" width="400"/>
</br>

Here is the translation:
>I am born and raised in Hangzhou. I am a science student at Zhejiang University ... I hope to find a man can pass the following test. **My Wechat ID is my Family name Lin followed with two prime number. The smaller prime number is in the front. The product of these two prime numbers 7140229933.** If you can find my Wechat ID, I will sincerely date you. Bula bula bula ...


Disregard if it is a joke, I think the question is interesting. So let's solve it.

The idea is using Exhaustive Method (Brute Force Method) to find two prime factors. However, 7,140,229,933 is a relatively large number. To find all prime number could take a long time. Since 7,140,229,933 is the product of two prime, one of the numbers must smaller than the **Square Root** of it. Therefore the order of magnitude of range could reduce from $10^9$ to $10^4$.
Here is my solution.

```python
import time
start = time.time()

# The input number
input = 7140229933

for x in range (2,int(input**(0.5))):
  if input%x ==0:
    print(x)
    break

print(int(input / 83777))

end = time.time()
print('Total Time: {}s.'.format(end - start))
```
Output:
```python
83777
85229
Total Time: 0.01737499237060547s.
```

So the two prime number are 83777 and 85229.








[^1]: [https://zh.wikipedia.org/wiki/V2EX](https://zh.wikipedia.org/wiki/V2EX)

[^2]: Photo by [Kevin Wolf](https://unsplash.com/photos/t8VzS-PSNeI?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on Unsplash
