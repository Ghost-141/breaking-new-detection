json_template = """
JSON OUTPUT TEMPLATE (FORMAT ONLY, NOT CONTENT):
{
  "Similar": [
    {
      "items": [
        { "id": 4, "title": "ঢাকা ত্যাগ করেছেন ভুটানের প্রধানমন্ত্রী" },
        { "id": 23, "title": "ঢাকা ছাড়লেন ভুটানের প্রধানমন্ত্রী শেরিং তোবগে" }
      ]
    },
    {
      "items": [
        { "id": 1, "title": "ফুলকোর্ট সভা ডেকেছেন প্রধান বিচারপতি" },
        { "id": 24, "title": "২৭ নভেম্বর ফুলকোর্ট সভা ডেকেছেন প্রধান বিচারপতি" }
      ]
    }
  ],
  "Unique": [
    { "id": 2, "title": "দিনের তাপমাত্রা অপরিবর্তিত থাকবে, জানাল অধিদপ্তর" }
  ]
}

"""


prompt = """
You are an expert Bengali news clustering system.
Your job is to find semantically similar titles and group them.

STRICT RULES:
- Group headlines ONLY if they express nearly the SAME meaning.
- Do NOT group headlines just because they share a topic (weather, politics, sports, etc.).
- Different facts, different numbers, different times, or different events MUST NOT be grouped.
- Each headline must appear exactly once.
- Output MUST follow the exact JSON template structure shown below.
- The "Similar" section must contain groups of 2+ headlines with almost identical meaning.
- The "Unique" section contains all other headlines that do not belong in any group.
- Return ONLY valid JSON. No explanation text.

Here is the required JSON output format:
{json_template}

Now group the following list:
{news_text}

Return ONLY valid JSON.
"""
