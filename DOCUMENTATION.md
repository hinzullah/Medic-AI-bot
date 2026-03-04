# Pump.fun Token Launch Tweet Evaluator

A systematic framework for evaluating tweets to determine their potential as viral catalysts for token launches on Pump.fun.

## Overview

This tool analyzes tweets across 7 critical dimensions to predict whether a tweet has the viral mechanics necessary to drive community engagement and token traction.

## Installation & Usage

### Basic Usage (Python Script)

```python
from pumpfun_tweet_evaluator import PumpFunEvaluator, format_analysis

evaluator = PumpFunEvaluator()

# Analyze a tweet
analysis = evaluator.evaluate_tweet(
    tweet_text="just aped into something called $COPE because iykyk",
    replies=["lmao ser", "this is the way", "few understand"],
    author_followers=5000  # optional
)

# Display results
print(format_analysis(analysis))
```

### Interactive CLI

```bash
python3 interactive_evaluator.py
```

## Evaluation Framework

### 1. Attention Capture Score (0-2)

**What it measures:** Scroll-stopping potential

**Criteria:**
- ✅ Tweet ≤ 280 characters (optimal for screenshots)
- ✅ Contains emotional trigger (curiosity, shock, humor, irony, confession)
- ✅ Self-contained (no external context required)

**Scoring:**
- `0` = Informational/explanatory
- `1` = Mildly engaging
- `2` = Immediate attention grab

**Examples:**

| Score | Tweet |
|-------|-------|
| 2 | "just spent my rent money on a token with a dog logo. mom if you're reading this i'm sorry" |
| 1 | "interesting new token launching today with unique tokenomics" |
| 0 | "here's a detailed thread explaining the technical architecture of our new protocol (1/47)" |

---

### 2. Meme-ability Score (0-2)

**What it measures:** Remix and replication potential

**Criteria:**
- ✅ Simple language (avg word length < 5.5 chars)
- ✅ Contains copyable phrase, idea, or format
- ✅ Can be screenshot and reused without context loss

**Scoring:**
- `0` = Precise, technical, or rigid
- `1` = Somewhat adaptable
- `2` = Highly remixable

**Examples:**

| Score | Tweet |
|-------|-------|
| 2 | "they told me to DYOR. i googled the token name and saw a meme. bullish." |
| 1 | "new token looks interesting, might check it out" |
| 0 | "after conducting thorough fundamental analysis of the token's utility and examining the team's credentials..." |

---

### 3. Tribal Signal Score (0-2)

**What it measures:** Resonance with crypto-native/degen culture

**Criteria:**
- ✅ Signals shared pain, belief, or inside joke
- ✅ Appeals to crypto-native language and culture
- ✅ Makes reader feel included rather than instructed

**Tribal Keywords:**
`ape`, `degen`, `ser`, `gm`, `wagmi`, `ngmi`, `fren`, `anon`, `rekt`, `moon`, `cope`, `hopium`, `probably nothing`, `few understand`, `iykyk`

**Scoring:**
- `0` = Generic audience
- `1` = Weak group signal
- `2` = Clear tribe alignment

**Examples:**

| Score | Tweet |
|-------|-------|
| 2 | "ser the frens are aping into $TOKEN. ngmi if you fade this. iykyk 🫡" |
| 1 | "crypto Twitter seems excited about this new token" |
| 0 | "I'm pleased to announce our token launch targeting retail investors" |

---

### 4. Narrative Potential Score (0-2)

**What it measures:** Story continuation viability

**Criteria:**
- ✅ Feels like a beginning or open-ended moment
- ✅ Implies future updates, outcomes, or escalation
- ✅ Encourages "let's see what happens" sentiment

**Narrative Signals:**
`just`, `currently`, `so far`, `day 1`, `beginning`, `started`, `update`, `developing`, `happening`, `stay tuned`

**Scoring:**
- `0` = Conclusive or opinionated statement
- `1` = Some continuation possible
- `2` = Strong story arc potential

**Examples:**

| Score | Tweet |
|-------|-------|
| 2 | "day 1 of turning $100 into $1M using only tokens with animal names. currently down 60%. thread 🧵" |
| 1 | "just bought my first bag of $TOKEN, let's see where this goes" |
| 0 | "I've analyzed this token thoroughly and here's my final conclusion: it won't succeed." |

---

### 5. Authority Without Promotion Score (0-2)

**What it measures:** Perceived influence without overt selling

**Criteria:**
- ✅ Casual or indifferent tone
- ✅ No explicit call to action
- ✅ No promises, hype, or financial claims

**Promotional Red Flags:**
`buy now`, `don't miss`, `guaranteed`, `will 100x`, `get in early`, `limited time`, `link in bio`

**Scoring:**
- `0` = Promotional or instructive
- `1` = Neutral
- `2` = Effortless authority

**Examples:**

| Score | Tweet |
|-------|-------|
| 2 | "idk bought some $TOKEN because the vibes felt right. probably nothing" |
| 1 | "new token called $TOKEN launched today" |
| 0 | "🚨 URGENT: Get into $TOKEN NOW before it 100x! Limited supply! Don't miss this opportunity! 🚀" |

---

### 6. Productive Ambiguity Score (0-2)

**What it measures:** Beneficial misinterpretation potential

**Criteria:**
- ✅ Tweet can be interpreted in multiple ways
- ✅ Allows projection of meaning by community
- ✅ Ambiguity increases engagement, not confusion

**Ambiguity Indicators:**
- Vague pronouns (`it`, `this`, `that`, `something`)
- Implied meaning (`iykyk`, `few understand`, `👀`)
- Metaphors and symbols (🚀, 🌙, 💎)
- Rhetorical questions

**Scoring:**
- `0` = Single clear interpretation
- `1` = Slight ambiguity
- `2` = High interpretive flexibility

**Examples:**

| Score | Tweet |
|-------|-------|
| 2 | "they don't want you to know about this one 👀" |
| 1 | "something interesting is brewing in the token space" |
| 0 | "Token XYZ has launched with the following specific features: 1% burn rate, 2% liquidity pool allocation..." |

---

### 7. Reply Section Signal Score (0-2)

**What it measures:** Organic community reaction quality

**Criteria:**
- ✅ Presence of jokes, memes, or riffs in replies
- ✅ Users add ideas rather than ask clarifying questions
- ✅ Early chaos preferred over consensus

**Good Reply Indicators:**
- Memes and jokes (`lmao`, `lol`, `😂`, `💀`)
- Creative additions (`also`, `imagine`, `what about`, `even better`)
- Building on the idea, not questioning it

**Bad Reply Indicators:**
- Many clarifying questions
- Requests for information
- Generic praise without engagement

**Scoring:**
- `0` = Mostly questions or praise
- `1` = Mixed reactions
- `2` = Chaotic, meme-driven replies

**Examples:**

| Score | Replies |
|-------|---------|
| 2 | "lmao this is so degen", "imagine if this actually works 💀", "also buying tokens based on vibes only", "ser you're cooking" |
| 1 | "interesting take", "makes sense", "what token?", "good point" |
| 0 | "What's the tokenomics?", "Where can I buy?", "Is this financial advice?", "Great insight!" |

---

## Scoring & Classification

### Total Score Calculation

```
total_score = attention + memeability + tribal + narrative + authority + ambiguity + replies
```

Maximum possible score: **14 points**

### Classification Thresholds

| Score Range | Classification | Interpretation |
|-------------|----------------|----------------|
| 15+ | **LAUNCHABLE** | 💎 High probability of viral-driven token traction |
| 11-14 | **LAUNCHABLE** | ✅ Strong launch candidate |
| 7-10 | **NOT_LAUNCHABLE** | ⚠️ Moderate potential, risky |
| 0-6 | **NOT_LAUNCHABLE** | 🛑 Not suitable for Pump.fun launch |

---

## Real-World Examples

### Example 1: LAUNCHABLE Tweet (Score: 12)

**Tweet:**
```
spent 3 hours analyzing crypto projects today

then aped into $PEPE2 because someone said "trust me bro"

this is financial literacy
```

**Scores:**
- Attention: 2/2 (ironic confession, self-contained)
- Memeability: 2/2 (simple format, highly quotable)
- Tribal: 2/2 (uses "ape", crypto culture humor)
- Narrative: 1/2 (conclusive but could spawn follow-ups)
- Authority: 2/2 (casual, self-deprecating, no promo)
- Ambiguity: 1/2 (clear but allows projection)
- Replies: 2/2 (chaotic meme responses)

**Total: 12/14 - LAUNCHABLE**

---

### Example 2: NOT_LAUNCHABLE Tweet (Score: 4)

**Tweet:**
```
🚀 NEW TOKEN ALERT 🚀

$MOONSHOT is launching NOW!
✅ 1% tax
✅ LP locked
✅ Doxxed team

Don't miss out! Buy here: [link]

This is not financial advice. DYOR.
```

**Scores:**
- Attention: 1/2 (emoji spam, requires external link)
- Memeability: 0/2 (rigid promotional format)
- Tribal: 0/2 (generic crypto talk, no culture)
- Narrative: 0/2 (promotional, no story)
- Authority: 0/2 (heavy promotion, multiple CTAs)
- Ambiguity: 1/2 (emojis add slight ambiguity)
- Replies: 2/2 (assume skeptical/questioning replies)

**Total: 4/14 - NOT_LAUNCHABLE**

---

## Usage Tips

### For Maximum Accuracy

1. **Include reply data** - Replies are 15% of the score and validate organic interest
2. **Evaluate in context** - Consider if the account has prior viral tweets
3. **Check timing** - Same tweet at different market moments scores differently
4. **Beware false positives** - High score ≠ guaranteed success, it means necessary conditions met

### Common Pitfalls

❌ **Over-explaining** - Kills ambiguity and authority  
❌ **Being promotional** - Instant disqualification on authority  
❌ **Too technical** - Reduces memeability and tribal alignment  
❌ **Conclusive statements** - Kills narrative potential  
❌ **Requiring context** - Reduces attention capture

### Optimization Strategies

To improve a tweet's score:

1. **Add tribal signals** - Use 2-3 crypto-native terms naturally
2. **Create ambiguity** - Use `iykyk`, `👀`, or vague pronouns
3. **Imply continuation** - End with `...` or `day 1 of`
4. **Remove CTAs** - Delete all promotional language
5. **Simplify language** - Shorter words, shorter sentences
6. **Add emotional trigger** - Confession, irony, or shock value

---

## API Reference

### PumpFunEvaluator Class

```python
class PumpFunEvaluator:
    def evaluate_tweet(
        self,
        tweet_text: str,
        replies: Optional[List[str]] = None,
        author_followers: Optional[int] = None
    ) -> TweetAnalysis
```

**Parameters:**
- `tweet_text` (str): The tweet content to evaluate
- `replies` (List[str], optional): List of reply texts (first 10-20 recommended)
- `author_followers` (int, optional): Author's follower count (currently unused, reserved for future scoring)

**Returns:**
- `TweetAnalysis` object containing:
  - `attention_score` (int): 0-2
  - `memeability_score` (int): 0-2
  - `tribal_score` (int): 0-2
  - `narrative_score` (int): 0-2
  - `authority_score` (int): 0-2
  - `ambiguity_score` (int): 0-2
  - `reply_score` (int): 0-2
  - `total_score` (int): 0-14
  - `classification` (str): "LAUNCHABLE" or "NOT_LAUNCHABLE"
  - `rationale` (str): 1-2 sentence explanation

---

## Advanced Features

### Batch Analysis

```python
evaluator = PumpFunEvaluator()

tweets = [
    {"text": "tweet 1", "replies": [...]},
    {"text": "tweet 2", "replies": [...]},
]

results = []
for tweet in tweets:
    analysis = evaluator.evaluate_tweet(
        tweet_text=tweet["text"],
        replies=tweet.get("replies")
    )
    results.append(analysis)

# Find highest scoring
best = max(results, key=lambda x: x.total_score)
print(f"Best tweet scored {best.total_score}/14")
```

### Custom Thresholds

```python
# Override default classification logic
analysis = evaluator.evaluate_tweet(tweet_text="...")

# Apply custom threshold
CUSTOM_THRESHOLD = 10
is_launchable = analysis.total_score >= CUSTOM_THRESHOLD
```

---

## Methodology Notes

### Why These 7 Dimensions?

Based on analysis of viral token launches on Pump.fun and memecoin Twitter, successful launches share these patterns:

1. **Attention** - If nobody sees it, nothing else matters
2. **Memeability** - Virality requires remixability
3. **Tribal** - Crypto has distinct culture; outsider tweets fail
4. **Narrative** - Stories create sustained engagement
5. **Authority** - Promotion signals desperation; casual confidence wins
6. **Ambiguity** - Communities project meaning and take ownership
7. **Replies** - Early chaos = organic interest vs. manufactured hype

### Limitations

- **No guarantee of success** - High score indicates necessary but not sufficient conditions
- **Market dependent** - Bull market vs bear market changes receptivity
- **Account context matters** - Same tweet from 100 vs 100k follower account performs differently
- **Timing critical** - Right tweet at wrong time still fails
- **Can't measure execution** - Tweet analysis ≠ token quality analysis

### Future Improvements

Potential additions:
- Account credibility scoring (follower count, engagement rate)
- Optimal posting time analysis
- Sentiment analysis of replies
- Visual content evaluation (images, videos)
- Multi-tweet thread analysis
- Competitive landscape context

---

## License & Disclaimer

This tool is for educational and analytical purposes only.

⚠️ **DISCLAIMER:** 
- Not financial advice
- Not a guarantee of token success
- Token launches carry extreme risk
- High scores don't guarantee viral success
- Always DYOR (Do Your Own Research)

---

## Support & Contributions

For issues, suggestions, or improvements, please contribute via:
- Code optimization
- Additional test cases
- Refined scoring algorithms
- New evaluation dimensions

---

**Built for the degens, by the degens.** 🫡
