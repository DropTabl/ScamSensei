import dspy
from backend.utils.helper import init_llm
from backend.utils.helper import retry

init_llm()

class Scam_Signature(dspy.Signature):
    """
    You are a highly intelligent scam detection system. Your task is to analyze the given text and determine if it contains any indicators of a scam.
    """

    text_input: str = dspy.InputField(desc="The text that needs to be analyzed for scam indicators.")

    scam_indicators: list[str] = dspy.OutputField(desc="A list of scam indicators found in the text, if any. If no indicators are found, return an empty list. "
                                                       "Please explain each indicator in detail. If none then Just one element with value 'Nothing' in the list. Structure: ['Indicator 1:detailed explanation', 'ndicator 1:detailed explanation', ...]."
                                                       "Answer in the defined language.")
    score: int = dspy.OutputField(desc="A score indicating the likelihood of the text being a scam. The higher the score, the more likely it is a scam. The score should be between 0 and 10.")




@retry(max_attempts=5, delay_seconds=5)
class ScamChecker(dspy.Module):
    def __init__(self):
        self.scam_signature = dspy.Predict(Scam_Signature)




    def forward(self, text_input):
        return  self.scam_signature(text_input=text_input)


async def detect_scam(text: str, language: str = "en"):
    """
    Detects if the given text contains any indicators of a scam.
    :param text: The text to analyze.
    :return: A dictionary containing the scam indicators and score.
    """
    scam_checker = ScamChecker()
    text = f"{text} \n\n ---------- Answer in : {language} ----------"
    result = scam_checker(text_input=text)
    return result.scam_indicators, result.score


