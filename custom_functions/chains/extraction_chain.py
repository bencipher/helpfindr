from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel


class ExtractionChain:

    def __init__(self, llm, model: BaseModel):
        self.llm = llm
        self.model = model

    def run(self, text):
        return self._extract_tool(text)

    def _extract_tool(self, text: str):
        output_format = PydanticOutputParser(pydantic_object=self.model)
        template = """Extract the following information from the provided text according to the specified schema 
                    and return it in the specified format. Do not add any additional text or format instruction. 
                    Only return information that logically fits the field and is found verbatim in the text.
                     Do not assume, guess, or hallucinate. Leave the field empty if the information is not found.
    
                    ### Schema/Format Instruction:
                    {format_instructions}
                    
                    ### Text:
                    {text}
                    
                    Instructions:
                    {format_instructions}
                    
                    """

        prompt = PromptTemplate(
            template=template,
            input_variables=["text", "format_instructions"],
        )
        format_instruction = output_format.get_format_instructions()
        chain = prompt | self.llm
        res = chain.invoke({"text": text, "format_instructions": format_instruction})
        output = output_format.parse(res.content)
        return output
