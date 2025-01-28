import dspy


class FollowUpQuestion(dspy.Signature):
  """Follow up on answer with additional questsions."""
  init_question: str = dspy.InputField(desc="initial question to human")
  human_answer: str = dspy.InputField(desc="human response to question")
  follow_up_question: list[str] = dspy.OutputField(desc="two additional questions to human to gather more information based on response")

generate_follow_up_questions = dspy.ChainOfThought(FollowUpQuestion)
