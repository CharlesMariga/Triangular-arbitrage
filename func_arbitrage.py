import requests
import json


# Make a get request
def get_coin_tickers(url):
    req = requests.get(url)
    return json.loads(req.text)


# Loop through each object and find the tradable pairs
def collect_tradables(coin_json):
    coin_list = []
    for coin in coin_json:
        is_frozen = coin_json[coin]["isFrozen"]
        post_only = coin_json[coin]["postOnly"]

        if is_frozen == "0" and post_only == "0":
            coin_list.append(coin)
    return coin_list


# Structure arbitrage Pairs
def structure_triangular_pairs(coin_list):
    triangular_pairs_list = []
    remove_duplicates_list = []
    pairs_list = coin_list[0:]

    # Get pair A
    for pair_a in pairs_list:
        pair_a_split = pair_a.split("_")
        a_base = pair_a_split[0]
        a_quote = pair_a_split[1]

        # Assign A to a box
        a_pair_box = [a_base, a_quote]

        # Get pair B
        for pair_b in pairs_list:
            pair_b_split = pair_b.split("_")
            b_base = pair_b_split[0]
            b_quote = pair_b_split[1]

            if pair_a != pair_b:
                if b_base in a_pair_box or b_quote in a_pair_box:

                    # Get pair C
                    for pair_c in pairs_list:
                        pair_c_split = pair_c.split("_")
                        c_base = pair_c_split[0]
                        c_quote = pair_c_split[1]

                        # Count the number of matching C items
                        if pair_c != pair_a and pair_c != pair_b:
                            combine_all = [pair_a, pair_b, pair_c]
                            pair_box = [a_base, a_quote, b_base,
                                        b_quote, c_base, c_quote]

                            count_c_base = 0
                            for i in pair_box:
                                if i == c_base:
                                    count_c_base += 1

                            count_c_quote = 0
                            for i in pair_box:
                                if i == c_quote:
                                    count_c_quote += 1

                            # Determining triangular match
                            if count_c_base == 2 and count_c_quote == 2 and c_base != c_quote:
                                combined = pair_a + "," + pair_b + "," + pair_c
                                unique_item = "".join(sorted(combine_all))

                                if unique_item not in remove_duplicates_list:
                                    match_dict = {
                                        "a_base": a_base,
                                        "b_base": b_base,
                                        "c_base": c_base,
                                        "a_quote": a_quote,
                                        "b_quote": b_quote,
                                        "c_quote": c_quote,
                                        "pair_a": pair_a,
                                        "pair_b": pair_b,
                                        "pair_c": pair_c,
                                        "combined": combined
                                    }
                                    triangular_pairs_list.append(match_dict)
                                    remove_duplicates_list.append(unique_item)

    print(len(triangular_pairs_list))
    for item in triangular_pairs_list[:20]:
        print(item)
