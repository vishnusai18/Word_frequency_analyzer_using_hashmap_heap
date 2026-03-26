import os
import re
import json
from datasets import load_dataset, concatenate_datasets
from hashmap import HashMap
from heap_utils import least_k_word_counts, top_k_word_counts, to_dict_list

# did not use ai or other tools

DATASET_NAME = "NabeelShar/ai_and_human_text"
TOP_K = 20
OUTPUT_DIR = "outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "results.json")


def preprocess_text(text):
    if text is None:
        return []

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)*", text)


def combine_splits(ds_dict):
    split_names = list(ds_dict.keys())
    datasets_list = [ds_dict[name] for name in split_names]
    if len(datasets_list) == 1:
        return datasets_list[0]
    return concatenate_datasets(datasets_list)


def normalize_label(raw_label, label_names=None):
    """
    Converts dataset label into 'ai' or 'human'.
    Handles both string labels and integer labels.
    """

    if label_names is not None and isinstance(raw_label, int):
        if 0 <= raw_label < len(label_names):
            label_text = label_names[raw_label].lower()
        else:
            label_text = str(raw_label).lower()
    else:
        label_text = str(raw_label).lower()

    if "ai" in label_text:
        return "ai"
    if "human" in label_text:
        return "human"

    # fallback assumption if labels are numeric
    # this may need one small adjustment after checking the dataset
    if str(raw_label) == "1":
        return "ai"
    return "human"


def count_words(dataset):
    overall_map = HashMap()
    ai_map = HashMap()
    human_map = HashMap()

    total_rows = 0
    total_tokens = 0
    ai_tokens = 0
    human_tokens = 0

    for row in dataset:
        text = row.get("text", "")
        raw_label = row.get("generated", 0)
        label = normalize_label(raw_label)

        tokens = preprocess_text(text)
        total_rows += 1
        total_tokens += len(tokens)

        for token in tokens:
            overall_map.increment(token)

            if label == "ai":
                ai_map.increment(token)
                ai_tokens += 1
            else:
                human_map.increment(token)
                human_tokens += 1

    return {
        "overall": overall_map,
        "ai": ai_map,
        "human": human_map,
        "stats": {
            "total_rows": total_rows,
            "total_tokens": total_tokens,
            "ai_tokens": ai_tokens,
            "human_tokens": human_tokens,
            "unique_words_overall": len(overall_map),
            "unique_words_ai": len(ai_map),
            "unique_words_human": len(human_map),
        }
    }


def top_k_words(freq_map, k=20):
    return top_k_word_counts(freq_map.items(), k)


def least_k_words(freq_map, k=20):
    return least_k_word_counts(freq_map.items(), k)


def main():
    print("Loading dataset...")
    ds_dict = load_dataset(DATASET_NAME, cache_dir="./hf_cache")
    dataset = combine_splits(ds_dict)

    print("Running analysis...")
    results = count_words(dataset)

    overall_map = results["overall"]
    ai_map = results["ai"]
    human_map = results["human"]
    word_frequencies = {
        "overall": to_dict_list(overall_map.items()),
        "ai": to_dict_list(ai_map.items()),
        "human": to_dict_list(human_map.items()),
    }

    output = {
        "stats": results["stats"],
        "default_top_k": TOP_K,
        "word_frequencies": word_frequencies,
        "top_k_overall": to_dict_list(top_k_words(overall_map, TOP_K)),
        "least_k_overall": to_dict_list(least_k_words(overall_map, TOP_K)),
        "top_k_ai": to_dict_list(top_k_words(ai_map, TOP_K)),
        "top_k_human": to_dict_list(top_k_words(human_map, TOP_K)),
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("\nAnalysis complete.")
    print(f"Results saved to: {OUTPUT_FILE}")
    print("\nSummary:")
    for key, value in output["stats"].items():
        print(f"{key}: {value}")

    print("\nTop 10 overall words:")
    for item in output["top_k_overall"][:10]:
        print(f"{item['word']}: {item['count']}")


if __name__ == "__main__":
    main()
