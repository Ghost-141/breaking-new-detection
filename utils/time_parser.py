from datetime import datetime

bn_to_en = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

month_map_atn = {
    "জানুয়ারী": "January",
    "ফেব্রুয়ারী": "February",
    "মার্চ": "March",
    "এপ্রিল": "April",
    "মে": "May",
    "জুন": "June",
    "জুলাই": "July",
    "আগস্ট": "August",
    "সেপ্টেম্বর": "September",
    "অক্টোবর": "October",
    "নভেম্বর": "November",
    "ডিসেম্বর": "December",
}

month_map_boisakhi = {
    "জানুয়ারি": "01",
    "জানুয়ারী": "01",
    "ফেব্রুয়ারী": "02",
    "ফেব্রুয়ারি": "02",
    "মার্চ": "03",
    "এপ্রিল": "04",
    "মে": "05",
    "জুন": "06",
    "জুলাই": "07",
    "আগস্ট": "08",
    "সেপ্টেম্বর": "09",
    "অক্টোবর": "10",
    "নভেম্বর": "11",
    "ডিসেম্বর": "12",
}

MERIDIEM_MAP = {"এএম": "AM", "পিএম": "PM"}


def atn_datetime(text: str):
    text = text.replace("আপডেটঃ", "").strip()
    text = text.translate(bn_to_en)
    for bn, en in month_map_atn.items():
        text = text.replace(bn, en)
    return datetime.strptime(text, "%B %d, %Y %H:%M")


def boisakhi_datetime(text: str):
    text = (
        text.replace("প্রকাশ : ", "")
        .replace("প্রকাশ ", "")
        .replace("আপডেট : ", "")
        .strip()
    )
    text = text.translate(bn_to_en)
    for bn, en in month_map_boisakhi.items():
        text = text.replace(bn, en)
    for bn, en in MERIDIEM_MAP.items():
        text = text.replace(bn, en)
    return datetime.strptime(text, "%d %m %Y, %I:%M %p")
