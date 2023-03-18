import json
import traceback
import openai
import logging

with open("info.json", 'r') as f:
    d = json.load(f)
    KEY = d['chatGPT_KEY']
    openai.organization = d['chatGPT_org']
    openai.api_key = KEY

messages_dict = {}
logging.basicConfig(filename="./data/chatgpt/gptLogging.log", filemode="w",
                    format='%(name)s - %(levelname)s - %(message)s')


def gpt_engine(p: str, uid: int) -> str:
    uid = str(uid)
    logging.info(f"User {uid} - {p}")
    if p == "clear":
        messages_dict[uid] = [{"role": "system", "content": "You are a helpful assistant."}]
    try:
        if uid not in messages_dict:
            messages_dict[uid] = [{"role": "system", "content": "You are a helpful assistant."}]
        messages_dict[uid].append({"role": "user", "content": p})
        r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_dict[uid],
                                         max_tokens=2048, temperature=1)
        res = r['choices'][0]['message']['content']
        messages_dict[uid].append({"role": "assistant", "content": res})
        logging.info(f"Assistant {uid} - {res}")
        if len(messages_dict[uid]) > 7:
            messages_dict[uid].pop(1)
            messages_dict[uid].pop(1)
        return res
    except KeyError as e:
        if messages_dict[uid][-1]['role'] == 'user':
            messages_dict[uid].pop(len(messages_dict[uid]) - 1)
        traceback.print_exc()
        logging.error(str(e.__class__))
        return "ERROR"
