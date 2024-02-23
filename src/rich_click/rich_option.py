import copy
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Sequence, Union

import click
from click.types import Choice, ParamType, convert_type
from rich import print
from rich.console import Console
from rich.prompt import Confirm, InvalidResponse
from rich.prompt import Prompt as _RichPrompt
from rich.text import Text

from rich_click import Context


def _confirm(
    text: str,
    default: Optional[bool] = False,
) -> Any:
    return Confirm.ask(text, default=default)


class _Prompt(_RichPrompt):

    def __init__(
        self,
        prompt: Union[str, Text] = "",
        *,
        console: Optional[Console] = None,
        password: bool = False,
        choices: Optional[List[str]] = None,
        show_default: bool = True,
        show_choices: bool = True,
        value_proc: Optional[Callable[[str], Any]] = None,
    ) -> None:
        self.value_proc = value_proc
        super().__init__(
            prompt,
            console=console,
            password=password,
            choices=choices,
            show_default=show_default,
            show_choices=show_choices,
        )

    def make_prompt(self, default: Any) -> Text:
        prompt = self.prompt.copy()
        prompt.end = ""

        if self.show_choices and self.choices:
            _choices = "/".join(self.choices)
            choices = f"[{_choices}]"
            prompt.append(" ")
            prompt.append(choices, "prompt.choices")

        if default != ... and self.show_default:
            prompt.append(" ")
            _default = self.render_default(default)
            prompt.append(_default)

        prompt.append(self.prompt_suffix)

        return prompt

    def process_response(self, value: str) -> Any:
        value = value.strip()
        try:
            return_value = self.value_proc(value) if self.value_proc else value
        except ValueError:
            raise InvalidResponse(self.validate_error_message)

        if self.choices is not None and not self.check_choice(value):
            raise InvalidResponse(self.illegal_choice_message)

        return return_value


def _prompt(
    text: str,
    default: Optional[Any] = None,
    hide_input: bool = False,
    confirmation_prompt: Union[bool, str] = False,
    type: Optional[Union[ParamType, Any]] = None,
    value_proc: Optional[Callable[[str], Any]] = None,
    prompt_suffix: str = ": ",
    show_default: bool = True,
    err: bool = False,
    show_choices: bool = True,
    default_is_missing: bool = True,
) -> Any:
    if value_proc is None:
        value_proc = convert_type(type, default)

    prompt_kwargs: Dict[str, Any] = {
        "prompt": text,
        "password": hide_input,
        "show_default": show_default,
        "show_choices": show_choices,
        "value_proc": value_proc,
    }

    if type is not None and show_choices and isinstance(type, Choice):
        prompt_kwargs["choices"] = type.choices

    if confirmation_prompt:
        if confirmation_prompt is True:
            confirmation_prompt = "Repeat for confirmation"

        prompt2_kwargs = copy.copy(prompt_kwargs)
        prompt2_kwargs["prompt"] = confirmation_prompt

    prompt = _Prompt(**prompt_kwargs)
    prompt.prompt_suffix = prompt_suffix
    prompt.value_proc = value_proc

    while True:
        value = prompt(default=default if not default_is_missing else ...)

        if not confirmation_prompt:
            return value

        prompt2 = _Prompt(**prompt2_kwargs)
        prompt2.prompt_suffix = prompt_suffix

        while True:
            value2 = prompt2(
                default=default if not default_is_missing else ...,
            )
            is_empty = not value and not value2
            if value2 or is_empty:
                break

        if value == value2:
            return value

        print("Error: The two entered values do not match.")


class RichOption(click.Option):
    """
    Option with support for Rich prompts.

    Inherits click.Option and overrides prompt_for_value
    to print richly formatted prompts.

    """

    @wraps(click.Option.__init__)
    def __init__(
        self,
        param_decls: Optional[Sequence[str]] = None,
        show_default: Optional[Union[bool, str]] = None,
        prompt: Union[bool, str] = False,
        confirmation_prompt: Union[bool, str] = False,
        prompt_required: bool = True,
        hide_input: bool = False,
        is_flag: Optional[bool] = None,
        flag_value: Optional[Any] = None,
        multiple: bool = False,
        count: bool = False,
        allow_from_autoenv: bool = True,
        type: Optional[Union[ParamType, Any]] = None,
        help: Optional[str] = None,
        hidden: bool = False,
        show_choices: bool = True,
        show_envvar: bool = False,
        **attrs: Any,
    ) -> None:
        """Option with rich prompts."""
        self.default_is_missing = "default" not in attrs
        super().__init__(
            param_decls,
            show_default,
            prompt,
            confirmation_prompt,
            prompt_required,
            hide_input,
            is_flag,
            flag_value,
            multiple,
            count,
            allow_from_autoenv,
            type,
            help,
            hidden,
            show_choices,
            show_envvar,
            **attrs,
        )

    def prompt_for_value(self, ctx: Context) -> Any:
        assert self.prompt is not None
        default = self.get_default(ctx)
        if self.is_bool_flag:
            return _confirm(self.prompt, default)

        return _prompt(
            self.prompt,
            default=default,
            type=self.type,
            hide_input=self.hide_input,
            show_choices=self.show_choices,
            confirmation_prompt=self.confirmation_prompt,
            value_proc=lambda x: self.process_value(ctx, x),
            default_is_missing=self.default_is_missing,
        )
