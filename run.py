from simio_di import DependencyInjector, DependenciesContainer

from bin.cli import CliInterface
from bin.config import get_config


def main():
    config = get_config()

    injector = DependencyInjector(config, deps_container=DependenciesContainer())
    cli = injector.inject(CliInterface)()  # внедрили зависимости и инициализировали класс

    cli.start()


if __name__ == "__main__":
    main()
