import together
from typing import Any, Dict
from pydantic import Extra, root_validator
from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env
from langchain import PromptTemplate, LLMChain
import json, os

with open("keys.json", "r") as file:
    os.environ["TOGETHER_API_KEY"] = json.load(file)["TOGETHER_API_KEY"]
    together.api_key = os.environ["TOGETHER_API_KEY"]


class TogetherLLM(LLM):
    """Together large language models."""

    model: str = "togethercomputer/llama-2-70b-chat"
    """model endpoint to use"""

    together_api_key: str = os.environ["TOGETHER_API_KEY"]
    """Together API key"""

    temperature: float = 0.7
    """What sampling temperature to use."""

    max_tokens: int = 512
    """The maximum number of tokens to generate in the completion."""

    class Config:
        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        api_key = get_from_dict_or_env(
            values, "together_api_key", "TOGETHER_API_KEY"
        )
        values["together_api_key"] = api_key
        return values

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    def _call(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """Call to Together endpoint."""
        together.api_key = self.together_api_key
        output = together.Complete.create(prompt,
                                          model=self.model,
                                          max_tokens=self.max_tokens,
                                          temperature=self.temperature,
                                          )
        text = output['output']['choices'][0]['text']
        return text


class llmRequester:
    def __init__(self):
        self.llama = None
        self.prompt = None
        self.llama = self.configure_llama()
        self.llm_chain = None
    
    def set_prompt(self, prompt):
        self.prompt = prompt

    def configure_llama(self):
        if self.llama == None:
            try:
                self.llama = TogetherLLM(
                    model= "togethercomputer/llama-2-70b-chat",
                    temperature=0.1,
                    max_tokens=512
                )
            except:
                print("No keys.json file found. Please create one with your Together API key.")
                self.llama = None
        return self.llama
    
    def run_llama(self, prompt, text):
        llama = self.configure_llama()
        
        self.prompt = PromptTemplate(template=prompt, input_variables=["text"])    
        self.llm_chain = LLMChain(prompt=self.prompt, llm=llama)
        answer = self.llm_chain.run(text)
        
        return answer
