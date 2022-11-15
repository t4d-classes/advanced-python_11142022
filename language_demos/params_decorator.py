from typing import Any, Callable

class App:
    """ app class """

    __routes = {}

    def route(self, url_path: str):
        """ route fn """

        def wrapper(func: Callable[..., Any]):
            """ wrapper fn """

            self.__routes[url_path] = func
            
            def inner(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
                """ inner """
                return func(*args, **kwargs)

            return inner

        return wrapper

app = App()


# @app.route("/")
def hello_world() -> str:
    """ hello world """
    return "<b>Hello, World!</b>"

hello_world = app.route("/")(hello_world)
