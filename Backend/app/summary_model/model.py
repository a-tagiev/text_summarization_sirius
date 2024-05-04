from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = 'utrobinmv/t5_summary_en_ru_zh_base_2048'
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)


def summarize(text):
    # text big summary generate
    prefix = 'summary big: '
    src_text = prefix + text
    input_ids = tokenizer(src_text, return_tensors="pt")
    generated_tokens = model.generate(**input_ids)
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return result

