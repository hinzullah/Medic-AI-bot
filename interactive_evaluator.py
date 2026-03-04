#!/usr/bin/env python3
"""
Interactive Pump.fun Tweet Evaluator CLI
"""

from pumpfun_tweet_evaluator import PumpFunEvaluator, format_analysis


def main():
    print("=" * 60)
    print("PUMP.FUN TOKEN LAUNCH TWEET EVALUATOR")
    print("=" * 60)
    print("\nAnalyzes tweets for viral token launch potential")
    print("Based on 7-dimension evaluation framework\n")
    
    evaluator = PumpFunEvaluator()
    
    while True:
        print("\n" + "-" * 60)
        print("Enter tweet text (or 'quit' to exit):")
        print("-" * 60)
        
        tweet_text = input("> ").strip()
        
        if tweet_text.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break
        
        if not tweet_text:
            print("⚠️  Please enter a tweet")
            continue
        
        # Optional: get replies
        print("\nInclude reply analysis? (y/n, default: n):")
        include_replies = input("> ").strip().lower() == 'y'
        
        replies = []
        if include_replies:
            print("\nEnter replies (one per line, empty line to finish):")
            while True:
                reply = input("  Reply: ").strip()
                if not reply:
                    break
                replies.append(reply)
        
        # Analyze
        print("\n⏳ Analyzing tweet...\n")
        
        analysis = evaluator.evaluate_tweet(
            tweet_text=tweet_text,
            replies=replies if replies else None
        )
        
        print(format_analysis(analysis))
        
        # Ask if user wants to continue
        print("\nAnalyze another tweet? (y/n):")
        continue_eval = input("> ").strip().lower()
        
        if continue_eval != 'y':
            print("\n👋 Goodbye!\n")
            break


if __name__ == "__main__":
    main()
