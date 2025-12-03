"""
Quiz Helpers for Money Talks

Provides interactive quiz functionality for Jupyter notebooks and Google Colab.
"""

from typing import Optional
import random


class Question:
    """Base class for quiz questions."""

    def __init__(
        self,
        question: str,
        correct_answer: str,
        explanation: str = "",
    ):
        self.question = question
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.user_answer: Optional[str] = None

    def check(self, answer: str) -> bool:
        """Check if the answer is correct."""
        self.user_answer = answer
        return answer.strip().lower() == self.correct_answer.strip().lower()

    def display(self) -> str:
        """Return question text for display."""
        return self.question


class MultipleChoiceQuestion(Question):
    """Multiple choice question with options."""

    def __init__(
        self,
        question: str,
        options: list[str],
        correct_index: int,
        explanation: str = "",
        shuffle: bool = False,
    ):
        self.options = options.copy()
        self._original_correct = options[correct_index]

        if shuffle:
            random.shuffle(self.options)

        self.correct_index = self.options.index(self._original_correct)
        super().__init__(
            question,
            self.options[self.correct_index],
            explanation,
        )

    def display(self) -> str:
        """Return formatted question with options."""
        lines = [self.question, ""]
        for i, option in enumerate(self.options):
            lines.append(f"  {chr(65 + i)}) {option}")
        return "\n".join(lines)

    def check(self, answer: str) -> bool:
        """Check answer by letter (A, B, C, D) or full text."""
        self.user_answer = answer
        answer = answer.strip().upper()

        # Accept letter answers
        if len(answer) == 1 and answer in "ABCD":
            index = ord(answer) - ord("A")
            if index < len(self.options):
                return index == self.correct_index

        # Accept full text answers
        return answer.lower() == self.correct_answer.lower()


def multiple_choice(
    question: str,
    options: list[str],
    correct_index: int,
    explanation: str = "",
    shuffle: bool = False,
) -> MultipleChoiceQuestion:
    """
    Create a multiple choice question.

    Args:
        question: The question text
        options: List of answer options
        correct_index: Index of the correct answer (0-based)
        explanation: Explanation shown after answering
        shuffle: Whether to shuffle the options

    Returns:
        MultipleChoiceQuestion object

    Example:
        >>> q = multiple_choice(
        ...     "What does NYSE stand for?",
        ...     ["New York Stock Exchange", "National Yield Securities Exchange",
        ...      "New York Securities Exchange", "National York Stock Exchange"],
        ...     0,
        ...     explanation="NYSE is the New York Stock Exchange, founded in 1792."
        ... )
        >>> print(q.display())
        >>> result = q.check("A")
    """
    return MultipleChoiceQuestion(question, options, correct_index, explanation, shuffle)


def true_false(
    question: str,
    correct_answer: bool,
    explanation: str = "",
) -> MultipleChoiceQuestion:
    """
    Create a true/false question.

    Args:
        question: The question text
        correct_answer: True or False
        explanation: Explanation shown after answering

    Returns:
        MultipleChoiceQuestion object (with True/False options)

    Example:
        >>> q = true_false(
        ...     "The stock market is open on weekends.",
        ...     False,
        ...     "US stock markets are closed on Saturdays and Sundays."
        ... )
    """
    return MultipleChoiceQuestion(
        question,
        ["True", "False"],
        0 if correct_answer else 1,
        explanation,
        shuffle=False,
    )


class Quiz:
    """
    Interactive quiz for Jupyter notebooks.

    Provides a simple interface for running quizzes in notebooks,
    with score tracking and feedback.
    """

    def __init__(self, title: str = "Quiz"):
        self.title = title
        self.questions: list[Question] = []
        self.current_index = 0
        self.score = 0
        self.completed = False

    def add(self, question: Question) -> "Quiz":
        """Add a question to the quiz."""
        self.questions.append(question)
        return self

    def add_multiple_choice(
        self,
        question: str,
        options: list[str],
        correct_index: int,
        explanation: str = "",
    ) -> "Quiz":
        """Add a multiple choice question."""
        self.questions.append(
            multiple_choice(question, options, correct_index, explanation)
        )
        return self

    def add_true_false(
        self,
        question: str,
        correct_answer: bool,
        explanation: str = "",
    ) -> "Quiz":
        """Add a true/false question."""
        self.questions.append(true_false(question, correct_answer, explanation))
        return self

    def run(self) -> None:
        """
        Run the quiz interactively.

        Works in standard Python, Jupyter, and Colab environments.
        """
        print(f"\n{'=' * 50}")
        print(f"  {self.title}")
        print(f"  {len(self.questions)} questions")
        print(f"{'=' * 50}\n")

        self.score = 0
        self.current_index = 0

        for i, q in enumerate(self.questions, 1):
            print(f"\nQuestion {i}/{len(self.questions)}:")
            print("-" * 40)
            print(q.display())
            print()

            answer = input("Your answer: ").strip()

            if q.check(answer):
                self.score += 1
                print("\n  Correct!")
            else:
                print(f"\n  Incorrect. The correct answer was: {q.correct_answer}")

            if q.explanation:
                print(f"\n  Explanation: {q.explanation}")

            self.current_index = i

        self._show_results()
        self.completed = True

    def _show_results(self) -> None:
        """Display final quiz results."""
        percentage = (self.score / len(self.questions)) * 100

        print(f"\n{'=' * 50}")
        print(f"  Quiz Complete!")
        print(f"{'=' * 50}")
        print(f"\n  Score: {self.score}/{len(self.questions)} ({percentage:.0f}%)")

        if percentage >= 90:
            print("\n  Excellent work!")
        elif percentage >= 70:
            print("\n  Good job! Keep studying to improve.")
        elif percentage >= 50:
            print("\n  You're making progress. Review the material and try again.")
        else:
            print("\n  Keep practicing! Review the lesson material.")

    def get_score(self) -> tuple[int, int]:
        """Return (correct, total) score."""
        return self.score, len(self.questions)

    def reset(self) -> None:
        """Reset quiz for retaking."""
        self.current_index = 0
        self.score = 0
        self.completed = False
        for q in self.questions:
            q.user_answer = None


# Convenience function for quick quizzes
def quick_quiz(questions_data: list[dict]) -> Quiz:
    """
    Create a quiz from a list of question dictionaries.

    Args:
        questions_data: List of dicts with keys:
            - question: str
            - options: list[str]
            - correct: int (index of correct answer)
            - explanation: str (optional)

    Returns:
        Quiz object ready to run

    Example:
        >>> quiz = quick_quiz([
        ...     {
        ...         "question": "What is the largest US stock exchange?",
        ...         "options": ["NYSE", "NASDAQ", "AMEX", "CBOE"],
        ...         "correct": 0,
        ...         "explanation": "NYSE is the largest by market cap."
        ...     },
        ...     {
        ...         "question": "NASDAQ is an auction market.",
        ...         "options": ["True", "False"],
        ...         "correct": 1,
        ...         "explanation": "NASDAQ is a dealer market."
        ...     }
        ... ])
        >>> quiz.run()
    """
    quiz = Quiz()
    for q in questions_data:
        quiz.add_multiple_choice(
            question=q["question"],
            options=q["options"],
            correct_index=q["correct"],
            explanation=q.get("explanation", ""),
        )
    return quiz
