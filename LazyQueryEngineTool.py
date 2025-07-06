from llama_index.core.tools import BaseTool, ToolMetadata
from llama_index.core.agent.react.step import ToolOutput
from llama_index.core.base.response.schema import Response as LlamaResponse
from typing import Any, Callable

class LazyQueryEngineTool(BaseTool):
    def __init__(self, name: str, description: str, loader_fn: Callable[[], Any]):
        self.name = name
        self.description = description
        self._loader_fn = loader_fn
        self._engine_cache = None

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(name=self.name, description=self.description)

    def _load(self):
        if self._engine_cache is None:
            self._engine_cache = self._loader_fn()
        return self._engine_cache

    def __call__(self, *args, **kwargs):
        if kwargs:
            raw_input_dict = dict(kwargs)
        elif args and isinstance(args[0], dict):
            raw_input_dict = dict(args[0])
        elif args:
            raw_input_dict = {"input": args[0]}
        else:
            raise ValueError("No query argument provided to LazyQueryEngineTool")
        query_str = (
            raw_input_dict.get("input")
            or raw_input_dict.get("query")
            or next(iter(raw_input_dict.values()))
        )

        result: Any = self._load().query(query_str)

        if not isinstance(result, LlamaResponse):
            result = LlamaResponse(response=str(result))

        return ToolOutput(
            content=result.response,
            tool_name=self.name,
            raw_input=raw_input_dict,
            raw_output=result
        )