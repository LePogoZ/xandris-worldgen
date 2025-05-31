"""AWS Lambda handler for Xandris world generation."""

import json
import os
from seed_resolution import process_seed, process_60_digit_seed

def lambda_handler(event, context):
    """
    Lambda event structure:
    {
        "seed": <string or int>  # seed value; length <= 20 for a single world, > 20 for multiple sub-worlds
    }
    """
    seed = event.get("seed")
    if seed is None:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing 'seed' in event"})}

    seed_str = str(seed)
    try:
        if len(seed_str) <= 20:
            world_type, successes = process_seed(int(seed_str))
            body = {"world_type": world_type, "successes": successes}
        else:
            results = process_60_digit_seed(int(seed_str))
            worlds = []
            for wt, succ in results:
                worlds.append({"world_type": wt, "successes": succ})
            body = {"worlds": worlds}
        return {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}