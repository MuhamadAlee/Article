from transformers import GPT2Tokenizer,GPT2LMHeadModel
import warnings
warnings.filterwarnings("ignore")
class Summery:

    def __init__(self):
        self.tokenizer=GPT2Tokenizer.from_pretrained('gpt2')
        self.model=GPT2LMHeadModel.from_pretrained('gpt2')

    def summerize(self,original_text,length):
        inputs=self.tokenizer.batch_encode_plus([original_text],return_tensors='pt',max_length=length)
        summary_ids=self.model.generate(inputs['input_ids'],early_stopping=True)
        GPT_summary=self.tokenizer.decode(summary_ids[0],skip_special_tokens=True)
        return original_text



