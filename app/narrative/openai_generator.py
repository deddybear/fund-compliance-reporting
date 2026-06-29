from __future__ import annotations
from openai import OpenAI
from app.computation.models import ComputationResult
from app.narrative.firewall import NarrativeFirewall
from app.narrative.generator import NarrativeGenerator
from app.narrative.models import (
    NarrativeContext,
    NarrativeResult,
)
from app.narrative.prompt import PromptBuilder


class OpenAINarrativeGenerator(
    NarrativeGenerator,
):

    def __init__(
        self,
        api_key: str,
        model: str,
        prompt_builder: PromptBuilder,
        firewall: NarrativeFirewall,
    ) -> None:

        self._client = OpenAI(
            api_key=api_key,
        )

        self._model = model

        self._prompt_builder = prompt_builder

        self._firewall = firewall

    def generate(
        self,
        *,
        context: NarrativeContext,
        computation: ComputationResult,
    ) -> NarrativeResult:

        system_prompt, user_prompt = (
            self._prompt_builder.build(
                context,
            )
        )

        response = (
            self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0.2,
            )
        )

        content = (
            response.choices[0].message.content
            or ""
        )

        firewall_result = (
            self._firewall.validate(
                computation=computation,
                narrative=content,
            )
        )

        if not firewall_result.passed:

            messages = []

            for issue in firewall_result.issues:

                messages.append(
                    f"[{issue.rule}] {issue.message}"
                )

            raise ValueError(
                "Narrative Firewall validation failed.\n"
                + "\n".join(messages)
            )

        usage = response.usage

        return NarrativeResult(
            content=content,
            model=self._model,
            prompt_tokens=(
                usage.prompt_tokens
                if usage
                else None
            ),
            completion_tokens=(
                usage.completion_tokens
                if usage
                else None
            ),
            total_tokens=(
                usage.total_tokens
                if usage
                else None
            ),
        )
