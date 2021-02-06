from simio_di import DependencyInjector, DependenciesContainer

from config import get_config

from cli import CliInterface


def main():
    config = get_config()

    injector = DependencyInjector(config, deps_container=DependenciesContainer())
    cli = injector.inject(CliInterface)()  # внедрили зависимости и инициализировали класс

    cli.start()


if __name__ == "__main__":
    main()
