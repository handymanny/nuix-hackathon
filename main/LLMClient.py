import html
import requests


class LLMClient:

    def __init__(self, url):
        self.URI = url

    def generate_summary(self, context, user_input):
        history = {'internal': [], 'visible': []}
        request = {
            'user_input': context + "\n" + user_input,
            'max_new_tokens': 250,
            'auto_max_new_tokens': False,
            'max_tokens_second': 0,
            'history': history,
            'mode': 'chat-instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
            'character': 'AI',
            'instruction_template': 'Llama-v2',  # Will get autodetected if unset
            'your_name': 'You',
            'regenerate': False,
            '_continue': False,
            'chat_instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

            # Generation params. If 'preset' is set to different than 'None', the values
            # in presets/preset-name.yaml are used instead of the individual numbers.
            'preset': 'None',
            'do_sample': True,
            'temperature': 0.1,
            'top_p': 0.1,
            'typical_p': 1,
            'epsilon_cutoff': 0,  # In units of 1e-4
            'eta_cutoff': 0,  # In units of 1e-4
            'tfs': 1,
            'top_a': 0,
            'repetition_penalty': 1.18,
            'repetition_penalty_range': 0,
            'top_k': 40,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'mirostat_mode': 0,
            'mirostat_tau': 5,
            'mirostat_eta': 0.1,
            'grammar_string': '',
            'guidance_scale': 1,
            'negative_prompt': '',

            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'custom_token_bans': '',
            'skip_special_tokens': True,
            'stopping_strings': []
        }

        response = requests.post(self.URI, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['history']
            return html.unescape(result['visible'][-1][1])